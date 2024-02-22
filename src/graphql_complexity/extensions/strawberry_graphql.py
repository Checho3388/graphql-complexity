from typing import Type

from graphql import GraphQLError, visit
from strawberry.extensions import SchemaExtension

from graphql_complexity import (
    ComplexityEstimator,
    ComplexityVisitor,
    SimpleEstimator
)


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
            self.visitor = ComplexityVisitor(estimator=estimator)
            visit(self.execution_context.graphql_document, self.visitor)

            self.estimated_complexity = self.visitor.evaluate()

            if max_complexity and self.estimated_complexity > max_complexity:
                error = GraphQLError(
                    f"Query is too complex. Max complexity is {max_complexity}, estimated "
                    f"complexity is {self.estimated_complexity}"
                )
                self.execution_context.errors = [error]

        def get_results(self):
            return {"complexity": {"value": self.estimated_complexity}}

    return ComplexityExtension
