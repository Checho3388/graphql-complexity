from typing import Type

from graphql import GraphQLError
from strawberry.extensions import SchemaExtension

from graphql_complexity import get_complexity
from graphql_complexity.estimators import ComplexityEstimator


def build_complexity_extension(
    estimator: ComplexityEstimator,
    max_complexity: int | None = None,
) -> Type[SchemaExtension]:
    class ComplexityExtension(SchemaExtension):
        estimated_complexity: int | None = None

        def on_validate(
            self,
        ):
            self.estimated_complexity = get_complexity(
                query=self.execution_context.query,
                schema=self.execution_context.schema._schema,
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
