"""Demo server for the complexity directive extension using the strawberry library."""

import strawberry

from .directive import ComplexityDirective
from .extension import build_complexity_extension_using_directive_estimator

MAX_COMPLEXITY = 100


@strawberry.type
class AnObject:
    name: str = strawberry.field(
        description="A name field of the object",
        directives=[ComplexityDirective(value=1)],
    )
    description: str = strawberry.field(
        description="A value field of the object",
        directives=[ComplexityDirective(value=10)],
    )


@strawberry.type
class Query:
    @strawberry.field(
        description="Example fixed field with a complexity of 1",
        directives=[ComplexityDirective(value=1)],
    )
    def complexity_1(self) -> str:
        return "Hello, I have 1 complexity!"

    @strawberry.field(
        description="Example fixed field with a complexity of 2",
        directives=[ComplexityDirective(value=2)],
    )
    def complexity_2(self) -> str:
        return "Hello, I have 2 complexity!"

    @strawberry.field(
        description="Example fixed object with a complexity of 3 and inner fields also annotated",
        directives=[ComplexityDirective(value=3)],
    )
    def complex_object(self) -> AnObject:
        return AnObject(
            name="Complex object",
            description="I'm a 3 complexity object!, but also inner fields such as "
            "name have complexity 1 and description has complexity 10",
        )

    @strawberry.field(
        description=f"Example fixed field with a complexity above the limit of the demo ({MAX_COMPLEXITY})",
        directives=[ComplexityDirective(value=1000000)],
    )
    def too_complex(self) -> str:
        return "I'm too complex, you shouldn't see me with the example configuration!"


extension = build_complexity_extension_using_directive_estimator(
    max_complexity=MAX_COMPLEXITY
)
schema = strawberry.Schema(
    query=Query,
    schema_directives=[ComplexityDirective],
    extensions=[extension],
)
