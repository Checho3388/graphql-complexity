from graphql import build_schema

from graphql_complexity import SimpleEstimator, get_complexity
from graphql_complexity.config import Config
from tests.ut_utils import schema


def _evaluate_complexity_with_simple_estimator(query: str, field_complexity=1):
    estimator = SimpleEstimator(field_complexity)
    return get_complexity(query, build_schema(schema), estimator)


def test_complexity_reads_count_from_query_args():
    query = """query {
        droid {
            friends(first: 10) {
                name
            }
        }
      }"""

    complexity = _evaluate_complexity_with_simple_estimator(query, 1)

    assert complexity == 12


def test_complexity_reads_count_from_query_args_with_different_name():
    query = """query {
        droid {
            friends(count: 10) {
                name
            }
        }
      }"""

    complexity = get_complexity(query, build_schema(schema), SimpleEstimator(), Config(count_arg_name="count"))

    assert complexity == 12


def test_complexity_config_allows_penalizing_missing_count_argument():
    query = """query {
        droid {
            friends {
                name
            }
        }
      }"""

    complexity = get_complexity(query, build_schema(schema), SimpleEstimator(), Config(count_missing_arg_value=100))

    assert complexity == 102
