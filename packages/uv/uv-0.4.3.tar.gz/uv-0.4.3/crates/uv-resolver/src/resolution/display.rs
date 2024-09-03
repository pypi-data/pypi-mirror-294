use std::collections::BTreeSet;

use owo_colors::OwoColorize;
use petgraph::visit::EdgeRef;
use petgraph::Direction;
use rustc_hash::{FxBuildHasher, FxHashMap};

use distribution_types::{DistributionMetadata, Name, SourceAnnotation, SourceAnnotations};
use pep508_rs::MarkerTree;
use uv_normalize::PackageName;

use crate::graph_ops::{propagate_markers, Markers};
use crate::resolution::{RequirementsTxtDist, ResolutionGraphNode};
use crate::{ResolutionGraph, ResolverMarkers};

static UNIVERSAL_MARKERS: ResolverMarkers = ResolverMarkers::Universal {
    fork_preferences: vec![],
};

/// A [`std::fmt::Display`] implementation for the resolution graph.
#[derive(Debug)]
#[allow(clippy::struct_excessive_bools)]
pub struct DisplayResolutionGraph<'a> {
    /// The underlying graph.
    resolution: &'a ResolutionGraph,
    /// The marker environment, used to determine the markers that apply to each package.
    marker_env: &'a ResolverMarkers,
    /// The packages to exclude from the output.
    no_emit_packages: &'a [PackageName],
    /// Whether to include hashes in the output.
    show_hashes: bool,
    /// Whether to include extras in the output (e.g., `black[colorama]`).
    include_extras: bool,
    /// Whether to include environment markers in the output (e.g., `black ; sys_platform == "win32"`).
    include_markers: bool,
    /// Whether to include annotations in the output, to indicate which dependency or dependencies
    /// requested each package.
    include_annotations: bool,
    /// Whether to include indexes in the output, to indicate which index was used for each package.
    include_index_annotation: bool,
    /// The style of annotation comments, used to indicate the dependencies that requested each
    /// package.
    annotation_style: AnnotationStyle,
}

#[derive(Debug)]
enum DisplayResolutionGraphNode {
    Root,
    Dist(RequirementsTxtDist),
}

impl Markers for DisplayResolutionGraphNode {
    fn set_markers(&mut self, markers: MarkerTree) {
        if let DisplayResolutionGraphNode::Dist(node) = self {
            node.markers = markers;
        }
    }
}

impl<'a> From<&'a ResolutionGraph> for DisplayResolutionGraph<'a> {
    fn from(resolution: &'a ResolutionGraph) -> Self {
        Self::new(
            resolution,
            &UNIVERSAL_MARKERS,
            &[],
            false,
            false,
            false,
            true,
            false,
            AnnotationStyle::default(),
        )
    }
}

impl<'a> DisplayResolutionGraph<'a> {
    /// Create a new [`DisplayResolutionGraph`] for the given graph.
    #[allow(clippy::fn_params_excessive_bools)]
    pub fn new(
        underlying: &'a ResolutionGraph,
        marker_env: &'a ResolverMarkers,
        no_emit_packages: &'a [PackageName],
        show_hashes: bool,
        include_extras: bool,
        include_markers: bool,
        include_annotations: bool,
        include_index_annotation: bool,
        annotation_style: AnnotationStyle,
    ) -> DisplayResolutionGraph<'a> {
        Self {
            resolution: underlying,
            marker_env,
            no_emit_packages,
            show_hashes,
            include_extras,
            include_markers,
            include_annotations,
            include_index_annotation,
            annotation_style,
        }
    }
}

/// Write the graph in the `{name}=={version}` format of requirements.txt that pip uses.
impl std::fmt::Display for DisplayResolutionGraph<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        // Determine the annotation sources for each package.
        let sources = if self.include_annotations {
            let mut sources = SourceAnnotations::default();

            for requirement in self.resolution.requirements.iter().filter(|requirement| {
                requirement.evaluate_markers(self.marker_env.marker_environment(), &[])
            }) {
                if let Some(origin) = &requirement.origin {
                    sources.add(
                        &requirement.name,
                        SourceAnnotation::Requirement(origin.clone()),
                    );
                }
            }

            for requirement in self
                .resolution
                .constraints
                .requirements()
                .filter(|requirement| {
                    requirement.evaluate_markers(self.marker_env.marker_environment(), &[])
                })
            {
                if let Some(origin) = &requirement.origin {
                    sources.add(
                        &requirement.name,
                        SourceAnnotation::Constraint(origin.clone()),
                    );
                }
            }

            for requirement in self
                .resolution
                .overrides
                .requirements()
                .filter(|requirement| {
                    requirement.evaluate_markers(self.marker_env.marker_environment(), &[])
                })
            {
                if let Some(origin) = &requirement.origin {
                    sources.add(
                        &requirement.name,
                        SourceAnnotation::Override(origin.clone()),
                    );
                }
            }

            sources
        } else {
            SourceAnnotations::default()
        };

        // Convert from `AnnotatedDist` to `RequirementsTxtDist`.
        let petgraph = to_requirements_txt_graph(&self.resolution.petgraph);

        // Propagate markers across the graph.
        let petgraph = propagate_markers(petgraph);

        // Reduce the graph, such that all nodes for a single package are combined, regardless of
        // the extras.
        let petgraph = combine_extras(&petgraph);

        // Collect all packages.
        let mut nodes = petgraph
            .node_indices()
            .filter_map(|index| {
                let dist = &petgraph[index];
                let name = dist.name();
                if self.no_emit_packages.contains(name) {
                    return None;
                }

                Some((index, dist))
            })
            .collect::<Vec<_>>();

        // Sort the nodes by name, but with editable packages first.
        nodes.sort_unstable_by_key(|(index, node)| (node.to_comparator(), *index));

        // Print out the dependency graph.
        for (index, node) in nodes {
            // Display the node itself.
            let mut line = node
                .to_requirements_txt(self.include_extras, self.include_markers)
                .to_string();

            // Display the distribution hashes, if any.
            let mut has_hashes = false;
            if self.show_hashes {
                for hash in &node.hashes {
                    has_hashes = true;
                    line.push_str(" \\\n");
                    line.push_str("    --hash=");
                    line.push_str(&hash.to_string());
                }
            }

            // Determine the annotation comment and separator (between comment and requirement).
            let mut annotation = None;

            // If enabled, include annotations to indicate the dependencies that requested each
            // package (e.g., `# via mypy`).
            if self.include_annotations {
                // Display all dependents (i.e., all packages that depend on the current package).
                let dependents = {
                    let mut dependents = petgraph
                        .edges_directed(index, Direction::Incoming)
                        .map(|edge| &petgraph[edge.source()])
                        .map(distribution_types::Name::name)
                        .collect::<Vec<_>>();
                    dependents.sort_unstable();
                    dependents.dedup();
                    dependents
                };

                // Include all external sources (e.g., requirements files).
                let default = BTreeSet::default();
                let source = sources.get(node.name()).unwrap_or(&default);

                match self.annotation_style {
                    AnnotationStyle::Line => match dependents.as_slice() {
                        [] if source.is_empty() => {}
                        [] if source.len() == 1 => {
                            let separator = if has_hashes { "\n    " } else { "  " };
                            let comment = format!("# via {}", source.iter().next().unwrap())
                                .green()
                                .to_string();
                            annotation = Some((separator, comment));
                        }
                        dependents => {
                            let separator = if has_hashes { "\n    " } else { "  " };
                            let dependents = dependents
                                .iter()
                                .map(ToString::to_string)
                                .chain(source.iter().map(ToString::to_string))
                                .collect::<Vec<_>>()
                                .join(", ");
                            let comment = format!("# via {dependents}").green().to_string();
                            annotation = Some((separator, comment));
                        }
                    },
                    AnnotationStyle::Split => match dependents.as_slice() {
                        [] if source.is_empty() => {}
                        [] if source.len() == 1 => {
                            let separator = "\n";
                            let comment = format!("    # via {}", source.iter().next().unwrap())
                                .green()
                                .to_string();
                            annotation = Some((separator, comment));
                        }
                        [dependent] if source.is_empty() => {
                            let separator = "\n";
                            let comment = format!("    # via {dependent}").green().to_string();
                            annotation = Some((separator, comment));
                        }
                        dependents => {
                            let separator = "\n";
                            let dependent = source
                                .iter()
                                .map(ToString::to_string)
                                .chain(dependents.iter().map(ToString::to_string))
                                .map(|name| format!("    #   {name}"))
                                .collect::<Vec<_>>()
                                .join("\n");
                            let comment = format!("    # via\n{dependent}").green().to_string();
                            annotation = Some((separator, comment));
                        }
                    },
                }
            }

            if let Some((separator, comment)) = annotation {
                // Assemble the line with the annotations and remove trailing whitespaces.
                for line in format!("{line:24}{separator}{comment}").lines() {
                    let line = line.trim_end();
                    writeln!(f, "{line}")?;
                }
            } else {
                // Write the line as is.
                writeln!(f, "{line}")?;
            }

            // If enabled, include indexes to indicate which index was used for each package (e.g.,
            // `# from https://pypi.org/simple`).
            if self.include_index_annotation {
                if let Some(index) = node.dist.index() {
                    let url = index.redacted();
                    writeln!(f, "{}", format!("    # from {url}").green())?;
                }
            }
        }

        Ok(())
    }
}

/// Indicate the style of annotation comments, used to indicate the dependencies that requested each
/// package.
#[derive(Debug, Default, Copy, Clone, PartialEq, serde::Deserialize)]
#[serde(deny_unknown_fields, rename_all = "kebab-case")]
#[cfg_attr(feature = "clap", derive(clap::ValueEnum))]
#[cfg_attr(feature = "schemars", derive(schemars::JsonSchema))]
pub enum AnnotationStyle {
    /// Render the annotations on a single, comma-separated line.
    Line,
    /// Render each annotation on its own line.
    #[default]
    Split,
}

type ResolutionPetGraph =
    petgraph::graph::Graph<ResolutionGraphNode, MarkerTree, petgraph::Directed>;

type IntermediatePetGraph =
    petgraph::graph::Graph<DisplayResolutionGraphNode, MarkerTree, petgraph::Directed>;

type RequirementsTxtGraph =
    petgraph::graph::Graph<RequirementsTxtDist, MarkerTree, petgraph::Directed>;

/// Convert a [`petgraph::graph::Graph`] based on [`ResolutionGraphNode`] to a graph based on
/// [`DisplayResolutionGraphNode`].
///
/// In other words: converts from [`AnnotatedDist`] to [`RequirementsTxtDist`].
fn to_requirements_txt_graph(graph: &ResolutionPetGraph) -> IntermediatePetGraph {
    let mut next = IntermediatePetGraph::with_capacity(graph.node_count(), graph.edge_count());
    let mut inverse = FxHashMap::with_capacity_and_hasher(graph.node_count(), FxBuildHasher);

    // Re-add the nodes to the reduced graph.
    for index in graph.node_indices() {
        match &graph[index] {
            ResolutionGraphNode::Root => {
                inverse.insert(index, next.add_node(DisplayResolutionGraphNode::Root));
            }
            ResolutionGraphNode::Dist(dist) => {
                let dist = RequirementsTxtDist::from(dist);
                inverse.insert(index, next.add_node(DisplayResolutionGraphNode::Dist(dist)));
            }
        }
    }

    // Re-add the edges to the reduced graph.
    for edge in graph.edge_indices() {
        let (source, target) = graph.edge_endpoints(edge).unwrap();
        let weight = graph[edge].clone();
        let source = inverse[&source];
        let target = inverse[&target];
        next.update_edge(source, target, weight);
    }

    next
}

/// Reduce the graph, such that all nodes for a single package are combined, regardless of
/// the extras.
///
/// For example, `flask` and `flask[dotenv]` should be reduced into a single `flask[dotenv]`
/// node.
///
/// We also remove the root node, to simplify the graph structure.
fn combine_extras(graph: &IntermediatePetGraph) -> RequirementsTxtGraph {
    let mut next = RequirementsTxtGraph::with_capacity(graph.node_count(), graph.edge_count());
    let mut inverse = FxHashMap::with_capacity_and_hasher(graph.node_count(), FxBuildHasher);

    // Re-add the nodes to the reduced graph.
    for index in graph.node_indices() {
        let DisplayResolutionGraphNode::Dist(dist) = &graph[index] else {
            continue;
        };

        if let Some(index) = inverse.get(&dist.version_id()) {
            let node: &mut RequirementsTxtDist = &mut next[*index];
            node.extras.extend(dist.extras.iter().cloned());
            node.extras.sort_unstable();
            node.extras.dedup();
        } else {
            let index = next.add_node(dist.clone());
            inverse.insert(dist.version_id(), index);
        }
    }

    // Re-add the edges to the reduced graph.
    for edge in graph.edge_indices() {
        let (source, target) = graph.edge_endpoints(edge).unwrap();
        let DisplayResolutionGraphNode::Dist(source_node) = &graph[source] else {
            continue;
        };
        let DisplayResolutionGraphNode::Dist(target_node) = &graph[target] else {
            continue;
        };
        let weight = graph[edge].clone();
        let source = inverse[&source_node.version_id()];
        let target = inverse[&target_node.version_id()];

        // If either the existing marker or new marker is `true`, then the dependency is
        // included unconditionally, and so the combined marker should be `true`.
        if let Some(edge) = next
            .find_edge(source, target)
            .and_then(|edge| next.edge_weight_mut(edge))
        {
            if edge.is_true() || weight.is_true() {
                *edge = MarkerTree::TRUE;
            } else {
                edge.and(weight.clone());
            }
        } else {
            next.update_edge(source, target, weight);
        }
    }

    next
}
