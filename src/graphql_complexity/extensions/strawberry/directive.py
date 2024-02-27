import strawberry
from strawberry.schema_directive import Location


@strawberry.schema_directive(
    name="complexity",
    print_definition=True,
    description="Cost of the field",
    locations=[Location.FIELD_DEFINITION],
)
class ComplexityDirective:
    value: int
