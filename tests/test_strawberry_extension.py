from typing import Iterable

import strawberry
from graphql import GraphQLError

from graphql_complexity.estimators import SimpleEstimator
from graphql_complexity.extensions.strawberry_graphql import (
    build_complexity_extension
)


@strawberry.type
class Obj:
    a_str: str
    an_int: int


def get_value() -> str:
    return "Strawberry"


def get_list() -> Iterable[str]:
    return ["Strawberry"]


def get_obj() -> Obj:
    return Obj(a_str="a_str", an_int=3)


def get_obj_list() -> Iterable[Obj]:
    return [Obj(a_str="a_str_in_list", an_int=3), Obj(a_str="another_str", an_int=3)]


@strawberry.input
class AnInput:
    sth: str


@strawberry.type
class Query:
    a_1_complexity_field: str = strawberry.field(resolver=get_value)
    a_2_complexity_field: str = strawberry.field(resolver=get_value)
    an_n_complexity_field: list[str] = strawberry.field(resolver=get_list)
    an_obj: Obj = strawberry.field(resolver=get_obj)
    an_obj_list: list[Obj] = strawberry.field(resolver=get_obj_list)

    @strawberry.field()
    def a_field_with_args(self, an_arg: str) -> str:
        return "Something"


def _execute_with_complexity(query: str, estimator=None):
    extension = build_complexity_extension(estimator=estimator)
    schema = strawberry.Schema(query=Query, extensions=[extension])

    return schema.execute_sync(query)


def _execute_limiting_complexity(query: str, max_complexity: int, estimator=None):
    extension = build_complexity_extension(
        estimator=estimator, max_complexity=max_complexity
    )
    schema = strawberry.Schema(query=Query, extensions=[extension])

    return schema.execute_sync(query)


def test_one_field_simple_complexity_calculation():
    query = """
        query Something {
            a1ComplexityField
        }
    """

    result = _execute_with_complexity(query)

    assert result.extensions["complexity"]["value"] == 1


def test_two_fields_simple_complexity_calculation():
    query = """
        query Something {
            a1ComplexityField
            alias: a1ComplexityField
        }
    """

    result = _execute_with_complexity(query)

    assert result.extensions["complexity"]["value"] == 2


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

    result = _execute_with_complexity(query)

    assert result.data == {
        "a1ComplexityField": "Strawberry",
        "a2ComplexityField": "Strawberry",
        "anObj": {"aStr": "a_str", "anInt": 3},
        "anObjList": [
            {"aStr": "a_str_in_list", "anInt": 3},
            {"aStr": "another_str", "anInt": 3},
        ],
    }

    assert result.extensions["complexity"]["value"] == 8


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

    result = _execute_with_complexity(query, SimpleEstimator(0, 1))

    assert result.extensions["complexity"]["value"] == 0


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

    result = _execute_with_complexity(query)

    assert result.extensions["complexity"]["value"] == 4


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

    result = _execute_with_complexity(query)

    assert result.extensions["complexity"]["value"] == 3


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

    result = _execute_with_complexity(query)

    assert result.extensions["complexity"]["value"] == 6


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

    result = _execute_with_complexity(query)

    assert result.extensions["complexity"]["value"] == 6


def test_extension_returns_error_when_complexity_is_bigger_than_the_limit():
    query = """
        query Something {
            a1ComplexityField
            alias: a1ComplexityField
        }
    """

    result = _execute_limiting_complexity(query, 1)

    assert result.errors == [
        GraphQLError(
            "Query is too complex. Max complexity is 1, estimated complexity is 2"
        )
    ]
    assert result.data is None


def test_extension_does_not_resolve_fields_when_limiting():
    resolver_calls = 0

    @strawberry.type()
    class Query:
        @strawberry.field()
        def resolver_calls_count(self) -> int:
            nonlocal resolver_calls
            resolver_calls += 1
            return resolver_calls

    query = """
        query {
            resolverCallsCount
        }
    """

    # Attempt to execute a query with a complexity of 10, but the max complexity is 1
    # The resolver should not be called
    extension = build_complexity_extension(
        estimator=SimpleEstimator(10, 1),
        max_complexity=1,
    )
    schema = strawberry.Schema(query=Query, extensions=[extension])
    schema.execute_sync(query)

    assert resolver_calls == 0

    # Confirm if the resolver is called when the complexity is within the limit
    # The resolver should be called
    extension = build_complexity_extension(
        estimator=SimpleEstimator(1, 1),
        max_complexity=1,
    )
    schema = strawberry.Schema(query=Query, extensions=[extension])
    schema.execute_sync(query)

    assert resolver_calls == 1
