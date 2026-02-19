from typing import List, Optional

import strawberry

from graphql_complexity.estimators import SimpleEstimator
from graphql_complexity.estimators.arguments import ArgumentsEstimator
from graphql_complexity.estimators.directive import DirectivesEstimator
from graphql_complexity.extensions.strawberry_graphql import build_complexity_extension


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

@strawberry.type
class Tag:
    id: strawberry.ID
    name: str


@strawberry.type
class Comment:
    id: strawberry.ID
    body: str
    author: str


@strawberry.type
class Post:
    id: strawberry.ID
    title: str
    body: str
    tags: List[Tag]
    comments: List[Comment]


@strawberry.type
class User:
    id: strawberry.ID
    name: str
    email: str
    posts: List[Post]


def _make_tag(n: int) -> Tag:
    return Tag(id=strawberry.ID(str(n)), name=f"tag-{n}")


def _make_comment(n: int) -> Comment:
    return Comment(id=strawberry.ID(str(n)), body=f"comment-{n}", author=f"author-{n}")


def _make_post(n: int) -> Post:
    return Post(
        id=strawberry.ID(str(n)),
        title=f"post-{n}",
        body=f"body-{n}",
        tags=[_make_tag(i) for i in range(2)],
        comments=[_make_comment(i) for i in range(3)],
    )


def _make_user(n: int) -> User:
    return User(
        id=strawberry.ID(str(n)),
        name=f"user-{n}",
        email=f"user-{n}@example.com",
        posts=[_make_post(i) for i in range(2)],
    )


@strawberry.type
class Query:
    @strawberry.field()
    def user(self) -> User:
        return _make_user(1)

    @strawberry.field()
    def users(self, limit: Optional[int] = 10) -> List[User]:
        return [_make_user(i) for i in range(min(limit, 3))]

    @strawberry.field()
    def post(self) -> Post:
        return _make_post(1)

    @strawberry.field()
    def posts(self, limit: Optional[int] = 10) -> List[Post]:
        return [_make_post(i) for i in range(min(limit, 3))]


# ---------------------------------------------------------------------------
# SDL for DirectivesEstimator
# Field names must match Strawberry's camelCase output; all names here are
# already lowercase so no conversion is needed.
# ---------------------------------------------------------------------------

SCHEMA_SDL = """
    directive @complexity(value: Int!) on FIELD_DEFINITION

    type Tag {
        id: ID
        name: String
    }

    type Comment {
        id: ID
        body: String @complexity(value: 1)
        author: String
    }

    type Post {
        id: ID
        title: String
        body: String @complexity(value: 2)
        tags: [Tag] @complexity(value: 1)
        comments: [Comment] @complexity(value: 3)
    }

    type User {
        id: ID
        name: String
        email: String @complexity(value: 1)
        posts: [Post] @complexity(value: 5)
    }

    type Query {
        user: User @complexity(value: 1)
        users(limit: Int): [User] @complexity(value: 10)
        post: Post @complexity(value: 1)
        posts(limit: Int): [Post] @complexity(value: 5)
    }
"""

# ---------------------------------------------------------------------------
# Queries
# ---------------------------------------------------------------------------

SIMPLE_QUERY = """
    query {
        user {
            id
            name
        }
    }
"""

# Multiple root selections, aliases, no fragments
COMPLEX_QUERY = """
    query {
        user {
            id
            name
            email
            posts {
                id
                title
            }
        }
        post {
            id
            title
            body
            tags {
                id
                name
            }
            comments {
                id
                body
                author
            }
        }
        secondPost: post {
            id
            title
            body
        }
    }
"""

# Deep nesting + fragments + list arguments — exercises the visitor fully
DEEP_QUERY = """
    fragment TagFields on Tag {
        id
        name
    }

    fragment CommentFields on Comment {
        id
        body
        author
    }

    fragment PostFields on Post {
        id
        title
        body
        tags {
            ...TagFields
        }
        comments {
            ...CommentFields
        }
    }

    query DeepQuery {
        user {
            id
            name
            email
            posts {
                ...PostFields
            }
        }
        users(limit: 5) {
            id
            name
            email
            posts {
                ...PostFields
            }
        }
        posts(limit: 10) {
            ...PostFields
        }
        singlePost: post {
            ...PostFields
        }
    }
"""

# ---------------------------------------------------------------------------
# Schemas (one per estimator + one baseline without extension)
# ---------------------------------------------------------------------------

schema_without_extension = strawberry.Schema(query=Query)

schema_simple = strawberry.Schema(
    query=Query,
    extensions=[build_complexity_extension(estimator=SimpleEstimator())],
)

schema_directives = strawberry.Schema(
    query=Query,
    extensions=[build_complexity_extension(estimator=DirectivesEstimator(SCHEMA_SDL))],
)

schema_arguments = strawberry.Schema(
    query=Query,
    extensions=[build_complexity_extension(
        estimator=ArgumentsEstimator(multipliers=["limit"], default_complexity=1)
    )],
)

# ---------------------------------------------------------------------------
# Benchmarks
# ---------------------------------------------------------------------------

def test_without_extension_simple_query(benchmark):
    benchmark(schema_without_extension.execute_sync, SIMPLE_QUERY)


def test_without_extension_complex_query(benchmark):
    benchmark(schema_without_extension.execute_sync, COMPLEX_QUERY)


def test_without_extension_deep_query(benchmark):
    benchmark(schema_without_extension.execute_sync, DEEP_QUERY)


def test_simple_estimator_simple_query(benchmark):
    benchmark(schema_simple.execute_sync, SIMPLE_QUERY)


def test_simple_estimator_complex_query(benchmark):
    benchmark(schema_simple.execute_sync, COMPLEX_QUERY)


def test_simple_estimator_deep_query(benchmark):
    benchmark(schema_simple.execute_sync, DEEP_QUERY)


def test_directives_estimator_simple_query(benchmark):
    benchmark(schema_directives.execute_sync, SIMPLE_QUERY)


def test_directives_estimator_complex_query(benchmark):
    benchmark(schema_directives.execute_sync, COMPLEX_QUERY)


def test_directives_estimator_deep_query(benchmark):
    benchmark(schema_directives.execute_sync, DEEP_QUERY)


def test_arguments_estimator_simple_query(benchmark):
    benchmark(schema_arguments.execute_sync, SIMPLE_QUERY)


def test_arguments_estimator_complex_query(benchmark):
    benchmark(schema_arguments.execute_sync, COMPLEX_QUERY)


def test_arguments_estimator_deep_query(benchmark):
    benchmark(schema_arguments.execute_sync, DEEP_QUERY)