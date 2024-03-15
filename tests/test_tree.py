import pytest
from graphql import build_schema

from graphql_complexity import SimpleEstimator
from graphql_complexity.evaluator.complexity import build_complexity_tree
from graphql_complexity.evaluator.nodes import ComplexityNode
from tests import ut_utils


def _build_complexity_tree(query: str, estimator=None):
    estimator = estimator or SimpleEstimator(1)
    schema = build_schema(ut_utils.schema)
    return build_complexity_tree(query, schema, estimator)


def test_tree_describes_simple_query():
    query = """
        query {
            version
        }
    """

    tree = _build_complexity_tree(query)

    assert tree.describe() == """root (RootNode) = 1
\tversion (Field) = 1"""


def test_tree_describes_skipped_fields():
    query = """query Foo ($shouldSkip: Boolean = false) {
        version @include(if: $shouldSkip)
    }"""

    tree = _build_complexity_tree(query)

    assert tree.describe() == """root (RootNode) = 0
\tversion (SkippedField) = 0"""


def test_tree_describes_lists():
    query = """query {
        droid {
            friends {
                name
            }
        }
    }"""

    tree = _build_complexity_tree(query)

    assert tree.describe() == """root (RootNode) = 3
\tdroid (Field) = 3
\t\tfriends (ListField) = 2
\t\t\tname (Field) = 1"""


def test_describes_fragment_spread():
    query = """query {
        ...fragmentName
    }
    fragment fragmentName on Droid {
        id
    }"""

    tree = _build_complexity_tree(query)

    assert tree.describe() == """root (RootNode) = 1
\tfragmentName (FragmentSpreadNode) = 1"""


def test_describes_complex_query():
    query = """query {
        droid {
            friends {
                name
            }
            appearsIn
        }
    }"""

    tree = _build_complexity_tree(query)

    assert tree.describe() == """root (RootNode) = 4
\tdroid (Field) = 4
\t\tfriends (ListField) = 2
\t\t\tname (Field) = 1
\t\tappearsIn (ListField) = 1"""


def test_typename_is_built_as_meta():
    query = """query {
        droid {
            __typename
            id
        }
    }"""

    tree = _build_complexity_tree(query)

    assert tree.describe() == """root (RootNode) = 2
\tdroid (Field) = 2
\t\t__typename (MetaField) = 0
\t\tid (Field) = 1"""


def test_complexity_node_can_not_be_evaluated():
    node = ComplexityNode(
        name="root"
    )

    with pytest.raises(NotImplementedError):
        node.evaluate()


def test_complexity_node_have_no_parent_until_they_are_linked():
    node_parent = ComplexityNode(name="parent")
    node_child = ComplexityNode(name="child")

    assert node_parent.parent is None
    assert node_child.parent is None
    assert node_parent.children == []
    assert node_child.children == []

    node_parent.add_child(node_child)

    assert node_parent.parent is None
    assert node_child.parent is node_parent
    assert node_parent.children == [node_child]
    assert node_child.children == []


def test_children_should_be_complexity_nodes():
    node = ComplexityNode(name="root")

    with pytest.raises(TypeError, match="^Children must be ComplexityNode instances, got <class 'str'>$"):
        node.add_child("not a node")
