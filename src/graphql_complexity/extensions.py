from typing import Type

from graphql import visit

from strawberry.extensions import SchemaExtension
from graphql_complexity.estimators import ComplexityEstimator, SimpleEstimator
from graphql_complexity.visitor import ComplexityVisitor


def build_complexity_extension(
    estimator: ComplexityEstimator | None = None,
) -> Type[SchemaExtension]:
    estimator = estimator or SimpleEstimator(1, 1)

    class ComplexityExtension(SchemaExtension):
        visitor = None

        def on_parse(self):
            yield
            self.visitor = ComplexityVisitor(estimator=estimator)
            visit(self.execution_context.graphql_document, self.visitor)

        def get_results(self):
            return {"complexity": {"value": self.visitor.evaluate()}}

    return ComplexityExtension
