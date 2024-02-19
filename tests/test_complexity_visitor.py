from graphql import parse, visit

from src.estimators import SimpleEstimator
from src.visitor import ComplexityVisitor


def _evaluate_complexity(query: str, estimator=None):
    ast = parse(query)
    estimator = estimator or SimpleEstimator(1, 1)
    visitor = ComplexityVisitor(estimator=estimator)
    visit(ast, visitor)

    return visitor.evaluate()


def test_one_field_simple_complexity_calculation():
    query = """
        query Something {
            a1ComplexityField
        }   
    """

    complexity = _evaluate_complexity(query)

    assert complexity == 1


def test_two_fields_simple_complexity_calculation():
    query = """
        query Something {
            a1ComplexityField
            alias: a1ComplexityField
        }   
    """

    complexity = _evaluate_complexity(query)

    assert complexity == 2


def test_complexity_visitor_respects_graphql_result_data():
    query = """
        query Something {
            a1ComplexityField
            a2ComplexityField
            anObj {
                aStr
                anInt
            }
            anObjList {
                aStr
                anInt
            }
        }   
    """

    complexity = _evaluate_complexity(query)

    assert complexity == 8


def test_complexity_with_a_complex_query():
    query = """
        query Something {
            a1ComplexityField
            a2ComplexityField
            anObj {
                aStr
                anInt
            }
            anObjList {
                aStr
                anInt
            }
        }   
    """

    complexity = _evaluate_complexity(query, SimpleEstimator(0, 0))

    assert complexity == 0


def test_complexity_works_with_multiple_operation_definitions():
    query = """
        query Something {
            a1ComplexityField
            alias: a1ComplexityField
        }
        query SomethingElse {
            a1ComplexityField
            alias: a1ComplexityField
        }   
    """

    complexity = _evaluate_complexity(query)

    assert complexity == 4


def test_complexity_handles_fragments():
    query = """
        fragment fields on Obj {
            aStr
            anInt
        }
        query Something {
            anObj {
                ... fields
            }
        }
    """

    complexity = _evaluate_complexity(query)

    assert complexity == 3


def test_complexity_handles_fragments_used_more_than_once():
    query = """
        fragment fields on Obj {
            aStr
            anInt
        }
        query Something {
            anObj {
                ... fields
            }
            another_one: anObj {
                ... fields
            }
        }
    """

    complexity = _evaluate_complexity(query)

    assert complexity == 6


def test_complexity_handles_fragments_definition_after_operation_definition():
    query = """
        query Something {
            anObj {
                ... fields
            }
            another_one: anObj {
                ... fields
            }
        }
        fragment fields on Obj {
            aStr
            anInt
        }

    """

    complexity = _evaluate_complexity(query)

    assert complexity == 6


def test_7():
    query = """
        query Something {
            aFieldWithArgs (anArg: "input")
        }   
    """

    complexity = _evaluate_complexity(query)

    assert complexity == 1


def test_8():
    query = """
        query Something {
            anNComplexityField
        }   
    """

    complexity = _evaluate_complexity(query)

    assert complexity == 1
