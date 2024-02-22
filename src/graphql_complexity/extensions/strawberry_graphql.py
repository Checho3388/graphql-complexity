from typing import Type

from graphql import GraphQLError
from strawberry.extensions import SchemaExtension

from graphql_complexity.estimators import ComplexityEstimator, SimpleEstimator
from graphql_complexity.evaluator.complexity import get_ast_complexity


def build_complexity_extension(
    estimator: ComplexityEstimator | None = None,
    max_complexity: int | None = None,
) -> Type[SchemaExtension]:
    estimator = estimator or SimpleEstimator(1, 1)

    class ComplexityExtension(SchemaExtension):
        visitor = None
        estimated_complexity: int = None

        def on_validate(
            self,
        ):
            self.estimated_complexity = get_ast_complexity(
                ast=self.execution_context.graphql_document,
                estimator=estimator
            )

            if max_complexity and self.estimated_complexity > max_complexity:
                error = GraphQLError(
                    f"Query is too complex. Max complexity is {max_complexity}, estimated "
                    f"complexity is {self.estimated_complexity}"
                )
                self.execution_context.errors = [error]

        def get_results(self):
            return {"complexity": {"value": self.estimated_complexity}}

    return ComplexityExtension
