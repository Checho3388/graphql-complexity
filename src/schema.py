import typing
import extensions

from src.complexity import QueryComplexity

from extensions import build_complexity_extension


@strawberry.type
class Book:
    title: str
    author: str


@strawberry.type
class Query:
    books: typing.List[Book]


def get_books() -> typing.Iterable[Book]:
    return [
        Book(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
        ),
    ]


@strawberry.type
class Query:
    books: typing.List[Book] = strawberry.field(resolver=get_books)


extension = build_complexity_extension()
schema = strawberry.Schema(query=Query, extensions=[QueryComplexity])
