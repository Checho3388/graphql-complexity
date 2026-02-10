[![GraphQL Complexity Logo](https://github.com/Checho3388/graphql-complexity/raw/main/.github/logo.png)](https://github.com/Checho3388/graphql-complexity/raw/main/.github/logo.png)

# GraphQL Complexity

Welcome to GraphQL-Complexity! This Python library provides functionality to compute the complexity of a GraphQL operation, contributing to better understanding and optimization of your GraphQL APIs. This library is designed to be stable, robust, and highly useful for developers working with GraphQL.

[![Build](https://github.com/Checho3388/graphql-complexity/actions/workflows/python-build.yml/badge.svg)](https://github.com/Checho3388/graphql-complexity/actions/workflows/python-build.yml/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/graphql-complexity?label=pypi%20package)](https://pypi.org/project/graphql-complexity/)
[![codecov](https://codecov.io/gh/Checho3388/graphql-complexity/graph/badge.svg?token=4LH7AVN119)](https://codecov.io/gh/Checho3388/graphql-complexity)
[![Downloads](https://static.pepy.tech/badge/graphql-complexity)](https://pepy.tech/project/graphql-complexity)

## Features

* Compute complexity of GraphQL queries
* Multiple built-in estimators for complexity computation
* Customizable estimators for specific use cases
* Support for Strawberry GraphQL library

## Table of Contents

* [Installation](#installation-quick-start)
* [Getting Started](#getting-started)
* [Estimators](#estimators)
  * [SimpleEstimator](#simpleestimator)
  * [DirectivesEstimator](#directivesestimator)
  * [Custom Estimator](#custom-estimator)
* [Advanced Examples](#advanced-examples)
  * [Handling Fragments](#handling-fragments)
  * [Complex Nested Queries](#complex-nested-queries)
  * [Working with Arguments](#working-with-arguments)
  * [Combining Multiple Estimators](#combining-multiple-estimators)
* [Framework Integration](#framework-integration)
  * [Strawberry GraphQL](#strawberry-graphql)
  * [Django Integration](#django-integration)
  * [FastAPI Integration](#fastapi-integration)
  * [Flask Integration](#flask-integration)
* [Real-World Use Cases](#real-world-use-cases)
* [Credits](#credits)

## Installation (Quick Start)

You can install the library via pip:

```bash
pip install graphql-complexity
```

For Strawberry GraphQL integration, use the following command:

```bash
pip install graphql-complexity[strawberry-graphql]
```

## Getting Started

Create a file named `complexity.py` with the following content:

```python
from graphql_complexity import get_complexity, SimpleEstimator
from graphql import build_schema


schema = build_schema("""
    type User {
        id: ID!
        name: String!
    }
    type Query {
        user: User
    }
""")

query = """
    query SomeQuery {
        user {
            id
            name
        }
    }
"""

complexity = get_complexity(
    query=query, 
    schema=schema,
    estimator=SimpleEstimator(complexity=10)
)
if complexity > 10:
    raise Exception("Query is too complex")
```

The library exposes the method `get_complexity` with the algorithm to compute the complexity of a GraphQL operation.
The algorithm visits each node of the query and computes the complexity of each field using an **estimator**.

## Estimators

GraphQL-Complexity provides various built-in estimators for computing query complexity:

### SimpleEstimator

Estimate fields complexity based on constants for complexity and multiplier. This assigns a constant
complexity value to each field and multiplies it by another constant, which is propagated along the depth of the query.

```python
from graphql_complexity import SimpleEstimator


estimator = SimpleEstimator(complexity=2)
```

### DirectivesEstimator

Define fields complexity using schema directives. This assigns a complexity value to each field and multiplies it
by the depth of the query. It also supports the @complexity directive to assign a custom complexity value to a field.

```python
from graphql_complexity import DirectivesEstimator


schema = """
directive @complexity(
  value: Int!
) on FIELD_DEFINITION

type Query {
  oneField: String @complexity(value: 5)
  otherField: String @complexity(value: 1)
  withoutDirective: String
}
"""

estimator = DirectivesEstimator(schema)
```

### Custom estimator

Custom estimators can be defined to compute the complexity of a field using the `ComplexityEstimator` interface.

```python
from graphql_complexity import ComplexityEstimator


class CustomEstimator(ComplexityEstimator):
    def get_field_complexity(self, node, type_info, path) -> int:
        if node.name.value == "specificField":
            return 100
        return 1
```

## Advanced Examples

### Handling Fragments

GraphQL fragments allow you to reuse query parts. Here's how complexity is calculated for queries with fragments:

```python
from graphql_complexity import get_complexity, SimpleEstimator
from graphql import build_schema

schema = build_schema("""
    type User {
        id: ID!
        name: String!
        email: String!
        posts: [Post!]!
    }
    
    type Post {
        id: ID!
        title: String!
        content: String!
        author: User!
    }
    
    type Query {
        user(id: ID!): User
        users: [User!]!
    }
""")

# Query with named fragment
query = """
    query GetUsers {
        users {
            ...UserFields
            posts {
                ...PostFields
            }
        }
    }
    
    fragment UserFields on User {
        id
        name
        email
    }
    
    fragment PostFields on Post {
        id
        title
        content
    }
"""

complexity = get_complexity(
    query=query,
    schema=schema,
    estimator=SimpleEstimator(complexity=1)
)
print(f"Query complexity: {complexity}")
```

### Complex Nested Queries

When dealing with nested relationships, complexity can grow exponentially. Here's how to handle it:

```python
from graphql_complexity import get_complexity, DirectivesEstimator
from graphql import build_schema

schema = build_schema("""
    directive @complexity(
        value: Int!
    ) on FIELD_DEFINITION
    
    type Organization {
        id: ID!
        name: String!
        teams: [Team!]! @complexity(value: 5)
    }
    
    type Team {
        id: ID!
        name: String!
        members: [User!]! @complexity(value: 3)
    }
    
    type User {
        id: ID!
        name: String!
        email: String!
        tasks: [Task!]! @complexity(value: 2)
    }
    
    type Task {
        id: ID!
        title: String!
        description: String!
    }
    
    type Query {
        organization(id: ID!): Organization
    }
""")

# Deeply nested query
query = """
    query GetOrgStructure {
        organization(id: "1") {
            id
            name
            teams {
                id
                name
                members {
                    id
                    name
                    email
                    tasks {
                        id
                        title
                        description
                    }
                }
            }
        }
    }
"""

estimator = DirectivesEstimator(schema)
complexity = get_complexity(query=query, schema=schema, estimator=estimator)

# Set a reasonable limit
MAX_COMPLEXITY = 100
if complexity > MAX_COMPLEXITY:
    raise Exception(f"Query too complex: {complexity} > {MAX_COMPLEXITY}")
```

### Working with Arguments

Field arguments can significantly impact query complexity, especially with pagination:

```python
from graphql_complexity import ComplexityEstimator, get_complexity
from graphql import build_schema, FieldNode
from graphql.language import ast

schema = build_schema("""
    type Product {
        id: ID!
        name: String!
        price: Float!
    }
    
    type Query {
        products(first: Int, offset: Int): [Product!]!
        product(id: ID!): Product
    }
""")

class ArgumentAwareEstimator(ComplexityEstimator):
    """Custom estimator that considers pagination arguments"""
    
    def get_field_complexity(self, node: FieldNode, type_info, path) -> int:
        field_name = node.name.value
        
        # Base complexity
        base_complexity = 1
        
        # Check for list/pagination arguments
        if node.arguments:
            for arg in node.arguments:
                if arg.name.value == "first":
                    # Extract the limit value
                    if isinstance(arg.value, ast.IntValue):
                        limit = int(arg.value.value)
                        # Multiply complexity by the number of items requested
                        base_complexity *= min(limit, 100)  # Cap at 100
        
        # Apply higher base cost for lists
        if field_name == "products":
            base_complexity *= 5
        
        return base_complexity

query = """
    query GetProducts {
        products(first: 50) {
            id
            name
            price
        }
    }
"""

complexity = get_complexity(
    query=query,
    schema=schema,
    estimator=ArgumentAwareEstimator()
)
print(f"Query complexity with pagination: {complexity}")
```

### Combining Multiple Estimators

You can create sophisticated complexity analysis by combining estimators:

```python
from graphql_complexity import (
    ComplexityEstimator,
    SimpleEstimator,
    DirectivesEstimator,
    get_complexity
)
from graphql import build_schema

schema = build_schema("""
    directive @complexity(value: Int!) on FIELD_DEFINITION
    
    type User {
        id: ID!
        name: String!
        expensiveComputation: String! @complexity(value: 50)
        posts: [Post!]!
    }
    
    type Post {
        id: ID!
        title: String!
    }
    
    type Query {
        user(id: ID!): User
        users: [User!]!
    }
""")

class CompositeEstimator(ComplexityEstimator):
    """Combines multiple estimation strategies"""
    
    def __init__(self):
        self.directive_estimator = DirectivesEstimator(schema)
        self.simple_estimator = SimpleEstimator(complexity=1)
    
    def get_field_complexity(self, node, type_info, path) -> int:
        # First, try directive-based estimation
        directive_complexity = self.directive_estimator.get_field_complexity(
            node, type_info, path
        )
        
        # If directive provides a value, use it
        if directive_complexity > 1:
            return directive_complexity
        
        # Otherwise, fall back to simple estimation
        return self.simple_estimator.get_field_complexity(node, type_info, path)

query = """
    query GetUserData {
        user(id: "1") {
            id
            name
            expensiveComputation
            posts {
                id
                title
            }
        }
    }
"""

complexity = get_complexity(
    query=query,
    schema=schema,
    estimator=CompositeEstimator()
)
print(f"Combined estimator complexity: {complexity}")
```

## Framework Integration

### Strawberry GraphQL

The library is compatible with [strawberry-graphql](https://pypi.org/project/strawberry-graphql/).
Use the following command to install the library with Strawberry support:

```bash
poetry install --extras strawberry-graphql
```

To use the library with Strawberry GraphQL, use the `build_complexity_extension` method to build the complexity
extension and add it to the schema. This method receives an estimator and returns a complexity extension that can be added to the schema.

```python
import strawberry
from graphql_complexity import SimpleEstimator
from graphql_complexity.extensions.strawberry_graphql import build_complexity_extension


@strawberry.type
class Query:
    @strawberry.field()
    def hello_world(self) -> str:
        return "Hello world!"

extension = build_complexity_extension(estimator=SimpleEstimator())
schema = strawberry.Schema(query=Query, extensions=[extension])

schema.execute_sync("query { helloWorld }")
```

The `build_complexity_extension` method accepts an estimator as optional argument giving the possibility to use one
of the built-in estimators or a custom estimator.

### Django Integration

Integrate complexity analysis with Django and Graphene:

```python
# myapp/complexity.py
from graphql_complexity import get_complexity, SimpleEstimator
from graphql import GraphQLError


class ComplexityMiddleware:
    def __init__(self, max_complexity=1000):
        self.max_complexity = max_complexity
        self.estimator = SimpleEstimator(complexity=1)
    
    def resolve(self, next, root, info, **args):
        # Calculate complexity on first field resolution
        if not hasattr(info.context, '_complexity_checked'):
            try:
                complexity = get_complexity(
                    query=info.operation.loc.source.body,
                    schema=info.schema,
                    estimator=self.estimator
                )
                
                if complexity > self.max_complexity:
                    raise GraphQLError(
                        f"Query is too complex: {complexity}. "
                        f"Maximum allowed complexity: {self.max_complexity}"
                    )
                
                info.context._complexity_checked = True
                info.context._query_complexity = complexity
                
            except Exception as e:
                raise GraphQLError(f"Complexity analysis failed: {str(e)}")
        
        return next(root, info, **args)


# settings.py
GRAPHENE = {
    'MIDDLEWARE': [
        'myapp.complexity.ComplexityMiddleware',
    ],
}
```

### FastAPI Integration

Use complexity analysis with FastAPI and Strawberry:

```python
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import strawberry
from graphql_complexity import SimpleEstimator
from graphql_complexity.extensions.strawberry_graphql import build_complexity_extension


@strawberry.type
class User:
    id: strawberry.ID
    name: str
    email: str


@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: strawberry.ID) -> User:
        return User(id=id, name="John Doe", email="john@example.com")
    
    @strawberry.field
    def users(self) -> list[User]:
        return [
            User(id="1", name="John Doe", email="john@example.com"),
            User(id="2", name="Jane Smith", email="jane@example.com"),
        ]


# Configure complexity limit
MAX_COMPLEXITY = 1000
extension = build_complexity_extension(
    estimator=SimpleEstimator(complexity=1),
    max_complexity=MAX_COMPLEXITY
)

schema = strawberry.Schema(query=Query, extensions=[extension])
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
```

### Flask Integration

Integrate with Flask-GraphQL:

```python
from flask import Flask, request, jsonify
from flask_graphql import GraphQLView
from graphql import build_schema, GraphQLError
from graphql_complexity import get_complexity, SimpleEstimator


app = Flask(__name__)

schema = build_schema("""
    type User {
        id: ID!
        name: String!
        email: String!
    }
    
    type Query {
        user(id: ID!): User
        users: [User!]!
    }
""")

MAX_COMPLEXITY = 1000
estimator = SimpleEstimator(complexity=1)


def validate_complexity(query_string):
    """Validate query complexity before execution"""
    try:
        complexity = get_complexity(
            query=query_string,
            schema=schema,
            estimator=estimator
        )
        
        if complexity > MAX_COMPLEXITY:
            raise GraphQLError(
                f"Query exceeds complexity limit. "
                f"Query complexity: {complexity}, Max allowed: {MAX_COMPLEXITY}"
            )
        
        return complexity
    except Exception as e:
        raise GraphQLError(f"Complexity validation error: {str(e)}")


class ComplexityGraphQLView(GraphQLView):
    def dispatch_request(self):
        # Get the query from request
        data = request.get_json()
        query = data.get('query', '')
        
        # Validate complexity
        try:
            complexity = validate_complexity(query)
            # Store complexity in request context for logging
            request.query_complexity = complexity
        except GraphQLError as e:
            return jsonify({'errors': [{'message': str(e)}]}), 400
        
        # Proceed with normal GraphQL execution
        return super().dispatch_request()


app.add_url_rule(
    '/graphql',
    view_func=ComplexityGraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)


if __name__ == '__main__':
    app.run(debug=True)
```

## Real-World Use Cases

### E-commerce Platform

Protect your e-commerce API from expensive queries:

```python
from graphql_complexity import ComplexityEstimator, get_complexity
from graphql import build_schema

schema = build_schema("""
    directive @complexity(value: Int!) on FIELD_DEFINITION
    
    type Product {
        id: ID!
        name: String!
        description: String!
        price: Float!
        reviews: [Review!]! @complexity(value: 10)
        relatedProducts: [Product!]! @complexity(value: 15)
    }
    
    type Review {
        id: ID!
        rating: Int!
        comment: String!
        author: User!
    }
    
    type User {
        id: ID!
        name: String!
        orders: [Order!]! @complexity(value: 20)
    }
    
    type Order {
        id: ID!
        items: [Product!]!
        total: Float!
    }
    
    type Query {
        product(id: ID!): Product
        products(limit: Int, offset: Int): [Product!]!
    }
""")

# This query would be too expensive
expensive_query = """
    query ExpensiveQuery {
        products(limit: 100) {
            id
            name
            reviews {
                author {
                    orders {
                        items {
                            relatedProducts {
                                reviews {
                                    comment
                                }
                            }
                        }
                    }
                }
            }
        }
    }
"""

# Reasonable query
reasonable_query = """
    query ReasonableQuery {
        product(id: "123") {
            id
            name
            price
            description
        }
    }
"""
```

### Social Media API

Rate limit complex social graph queries:

```python
from graphql_complexity import ComplexityEstimator, get_complexity
from graphql import build_schema

schema = build_schema("""
    directive @complexity(value: Int!) on FIELD_DEFINITION
    
    type User {
        id: ID!
        username: String!
        followers: [User!]! @complexity(value: 10)
        following: [User!]! @complexity(value: 10)
        posts: [Post!]! @complexity(value: 5)
    }
    
    type Post {
        id: ID!
        content: String!
        author: User!
        likes: [User!]! @complexity(value: 5)
        comments: [Comment!]! @complexity(value: 3)
    }
    
    type Comment {
        id: ID!
        text: String!
        author: User!
    }
    
    type Query {
        user(id: ID!): User
        feed(limit: Int): [Post!]!
    }
""")


class SocialMediaEstimator(ComplexityEstimator):
    """Custom estimator for social media queries"""
    
    def get_field_complexity(self, node, type_info, path) -> int:
        field_name = node.name.value
        
        # Heavy penalty for deeply nested social graphs
        depth = len(path)
        depth_penalty = 2 ** depth if depth > 3 else 1
        
        # Base costs
        costs = {
            'followers': 10,
            'following': 10,
            'posts': 5,
            'likes': 5,
            'comments': 3,
            'feed': 8,
        }
        
        base_cost = costs.get(field_name, 1)
        return base_cost * depth_penalty


# Example: Preventing graph explosion
problematic_query = """
    query DeepSocialGraph {
        user(id: "1") {
            followers {
                following {
                    posts {
                        likes {
                            followers {
                                # This gets exponentially expensive!
                                username
                            }
                        }
                    }
                }
            }
        }
    }
"""
```

### Analytics Dashboard

Manage complexity for data-heavy analytics queries:

```python
from graphql_complexity import ComplexityEstimator, get_complexity
from graphql import build_schema
from datetime import datetime

schema = build_schema("""
    directive @complexity(value: Int!) on FIELD_DEFINITION
    
    type Analytics {
        pageViews: Int! @complexity(value: 5)
        uniqueVisitors: Int! @complexity(value: 5)
        averageSessionDuration: Float! @complexity(value: 10)
        conversionRate: Float! @complexity(value: 15)
        revenueByDay: [DailyRevenue!]! @complexity(value: 20)
    }
    
    type DailyRevenue {
        date: String!
        amount: Float!
        transactions: Int!
    }
    
    type Query {
        analytics(
            startDate: String!
            endDate: String!
            granularity: String
        ): Analytics @complexity(value: 10)
    }
""")


def calculate_analytics_complexity(query: str, date_range_days: int) -> int:
    """Calculate complexity based on date range"""
    base_complexity = get_complexity(
        query=query,
        schema=schema,
        estimator=SimpleEstimator(complexity=1)
    )
    
    # Multiply by date range (more days = more expensive)
    range_multiplier = max(1, date_range_days / 7)  # Weekly baseline
    
    return int(base_complexity * range_multiplier)
```

## Credits

Estimators idea was heavily inspired by [graphql-query-complexity](https://github.com/slicknode/graphql-query-complexity).

## About

Python library to compute the complexity of a GraphQL operation

### Topics

[python](https://github.com/topics/python)
[graphql](https://github.com/topics/graphql)
[strawberry](https://github.com/topics/strawberry)
[graphql-core](https://github.com/topics/graphql-core)

### License

[MIT license](LICENSE)
