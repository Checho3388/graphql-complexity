from graphql import parse, visit

from src.estimators import SimpleEstimator
from src.visitor import ComplexityVisitor


def _evaluate_complexity_with_simple_estimator(
    query: str, field_complexity=1, multiplier=1
):
    ast = parse(query)
    estimator = SimpleEstimator(field_complexity, multiplier)
    visitor = ComplexityVisitor(estimator=estimator)
    visit(ast, visitor)

    return visitor.evaluate()


def test_root_fields_do_not_multiply():
    query = """
        query Something {
            a_field
        }   
    """

    complexity = _evaluate_complexity_with_simple_estimator(query, 3, 10)

    assert complexity == 3


def test_root_fields_complexity_is_added():
    query = """
        query Something {
            a_field
            another_field
        }   
    """

    complexity = _evaluate_complexity_with_simple_estimator(query, 5, 1)

    assert complexity == 10


def test_complexity_multiplies_with_objects():
    query = """
        query Something {
            anObj {
                a_field
                another_field
            }
        }   
    """

    complexity = _evaluate_complexity_with_simple_estimator(query, 1, 10)

    assert complexity == 21


def test_complexity_multiplies_two_levels():
    query = """
        query Something {
            anObj {
                anotherObj {
                    a_field
                }
            }
        }   
    """

    complexity = _evaluate_complexity_with_simple_estimator(query, 1, 10)

    assert complexity == 111


def test_complexity_multiplies_with_depth():
    query = """
        query Something {
            anObj {
                anotherObj {
                    a_field
                }
                another_field
            }
        }   
    """

    complexity = _evaluate_complexity_with_simple_estimator(query, 1, 10)

    assert complexity == 121
