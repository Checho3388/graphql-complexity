"""
GraphQL Complexity Playground
==============================

A simple interactive playground to demonstrate graphql-complexity.

Deploy this to Replit, Railway, or run locally to showcase your library!

Usage:
  python playground.py

Then visit: http://localhost:8000/graphql
"""

import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from graphql_complexity import SimpleEstimator
from graphql_complexity.extensions.strawberry_graphql import build_complexity_extension


# Sample data
USERS = [
    {"id": "1", "name": "Alice", "email": "alice@example.com"},
    {"id": "2", "name": "Bob", "email": "bob@example.com"},
    {"id": "3", "name": "Charlie", "email": "charlie@example.com"},
]

POSTS = [
    {"id": "1", "title": "GraphQL is awesome", "content": "Learn GraphQL...", "author_id": "1"},
    {"id": "2", "title": "Python tips", "content": "Python tricks...", "author_id": "1"},
    {"id": "3", "title": "FastAPI tutorial", "content": "FastAPI guide...", "author_id": "2"},
]


# GraphQL Types
@strawberry.type
class User:
    id: strawberry.ID
    name: str
    email: str

    @strawberry.field
    def posts(self) -> list["Post"]:
        """Get all posts by this user"""
        return [
            Post(**post) for post in POSTS
            if post["author_id"] == self.id
        ]


@strawberry.type
class Post:
    id: strawberry.ID
    title: str
    content: str
    author_id: str

    @strawberry.field
    def author(self) -> User:
        """Get the author of this post"""
        user_data = next(u for u in USERS if u["id"] == self.author_id)
        return User(**user_data)


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        """Simple hello world query"""
        return "Hello from GraphQL Complexity Playground! 🚀"

    @strawberry.field
    def user(self, id: strawberry.ID) -> User:
        """Get a single user by ID"""
        user_data = next((u for u in USERS if u["id"] == id), None)
        if not user_data:
            raise Exception(f"User {id} not found")
        return User(**user_data)

    @strawberry.field
    def users(self) -> list[User]:
        """Get all users"""
        return [User(**u) for u in USERS]

    @strawberry.field
    def post(self, id: strawberry.ID) -> Post:
        """Get a single post by ID"""
        post_data = next((p for p in POSTS if p["id"] == id), None)
        if not post_data:
            raise Exception(f"Post {id} not found")
        return Post(**post_data)

    @strawberry.field
    def posts(self) -> list[Post]:
        """Get all posts"""
        return [Post(**p) for p in POSTS]


# Create schema with complexity extension
# TRY THESE LIMITS:
# - max_complexity=50  (allows most queries)
# - max_complexity=20  (blocks deeply nested queries)
# - max_complexity=5   (blocks almost everything - great for demo!)

extension = build_complexity_extension(
    estimator=SimpleEstimator(complexity=1),
    max_complexity=50  # <-- Change this to test!
)

schema = strawberry.Schema(
    query=Query,
    extensions=[extension]
)


# Create FastAPI app
app = FastAPI(
    title="GraphQL Complexity Playground",
    description="Interactive playground for graphql-complexity library"
)


# Add GraphQL endpoint
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")


# Add a nice landing page
@app.get("/", response_class=HTMLResponse)
def landing_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>GraphQL Complexity Playground</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 40px 20px;
                background: #f5f5f5;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            h1 {
                color: #e10098;
                margin-bottom: 10px;
            }
            .subtitle {
                color: #666;
                font-size: 18px;
                margin-bottom: 30px;
            }
            .btn {
                display: inline-block;
                background: #e10098;
                color: white;
                padding: 12px 24px;
                border-radius: 6px;
                text-decoration: none;
                font-weight: 600;
                margin-right: 10px;
                margin-bottom: 10px;
            }
            .btn:hover {
                background: #c1007a;
            }
            .example {
                background: #f8f8f8;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
                border-left: 4px solid #e10098;
            }
            .example h3 {
                margin-top: 0;
                color: #333;
            }
            pre {
                background: #2d2d2d;
                color: #f8f8f8;
                padding: 15px;
                border-radius: 6px;
                overflow-x: auto;
            }
            code {
                font-family: 'Monaco', 'Menlo', monospace;
                font-size: 14px;
            }
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }
            .stat {
                background: #f8f8f8;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
            }
            .stat-value {
                font-size: 32px;
                font-weight: bold;
                color: #e10098;
            }
            .stat-label {
                color: #666;
                margin-top: 5px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 GraphQL Complexity Playground</h1>
            <p class="subtitle">Interactive demo of the graphql-complexity Python library</p>
            
            <div style="margin: 30px 0;">
                <a href="/graphql" class="btn">Open GraphiQL IDE →</a>
                <a href="https://github.com/Checho3388/graphql-complexity" class="btn" style="background: #333;">View on GitHub</a>
            </div>

            <div class="stats">
                <div class="stat">
                    <div class="stat-value">50</div>
                    <div class="stat-label">Max Complexity</div>
                </div>
                <div class="stat">
                    <div class="stat-value">5.5k+</div>
                    <div class="stat-label">Downloads</div>
                </div>
                <div class="stat">
                    <div class="stat-value">100%</div>
                    <div class="stat-label">Python</div>
                </div>
            </div>

            <h2>Try These Queries</h2>

            <div class="example">
                <h3>✅ Simple Query (Low Complexity)</h3>
                <p>This query should pass complexity validation:</p>
                <pre><code>query SimpleQuery {
  hello
  users {
    id
    name
  }
}</code></pre>
            </div>

            <div class="example">
                <h3>⚠️ Nested Query (Medium Complexity)</h3>
                <p>This query has moderate complexity:</p>
                <pre><code>query NestedQuery {
  users {
    id
    name
    posts {
      id
      title
    }
  }
}</code></pre>
            </div>

            <div class="example">
                <h3>❌ Deeply Nested (High Complexity)</h3>
                <p>This query will likely exceed the limit:</p>
                <pre><code>query DeepNesting {
  users {
    id
    name
    posts {
      id
      title
      author {
        id
        name
        posts {
          id
          title
          author {
            name
          }
        }
      }
    }
  }
}</code></pre>
                <p><em>Try lowering max_complexity to 20 in the code to block this!</em></p>
            </div>

            <h2>How It Works</h2>
            <p>The <code>graphql-complexity</code> library analyzes each GraphQL query and calculates a complexity score. Queries that exceed the configured limit are rejected before execution, preventing expensive operations from overloading your API.</p>

            <h2>Installation</h2>
            <pre><code>pip install graphql-complexity

# For Strawberry integration
pip install graphql-complexity[strawberry-graphql]</code></pre>

            <h2>Features</h2>
            <ul>
                <li>🛡️ Protect against expensive queries and DoS attacks</li>
                <li>📊 Multiple complexity estimation strategies</li>
                <li>🔧 Customizable complexity limits</li>
                <li>🍓 Strawberry GraphQL integration</li>
                <li>⚡ Production-ready and battle-tested</li>
            </ul>
        </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🚀 GraphQL Complexity Playground")
    print("="*60)
    print("\n📍 Landing Page: http://localhost:8000")
    print("🎮 GraphiQL IDE:  http://localhost:8000/graphql")
    print("\n💡 Try changing max_complexity in the code to see different behaviors!")
    print("\nPress CTRL+C to stop\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)
