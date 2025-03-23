# Blog API Example

This example demonstrates how to build a full-featured blog API using the ninja_rest package. It showcases various features including:

- Model relationships (One-to-Many, Many-to-One)
- Custom permissions
- Dynamic schema selection
- Query parameter filtering
- Nested serialization
- Automatic pagination

## Models

The API includes three main models:
- `Category`: For organizing posts
- `Post`: The main blog post model
- `Comment`: User comments on posts

## API Endpoints

### Categories

```
GET /api/categories/ - List all categories
POST /api/categories/ - Create a new category
GET /api/categories/{id}/ - Get category details
PUT /api/categories/{id}/ - Update a category
DELETE /api/categories/{id}/ - Delete a category
```

### Posts

```
GET /api/posts/ - List all published posts
POST /api/posts/ - Create a new post
GET /api/posts/{id}/ - Get post details with comments
PUT /api/posts/{id}/ - Update a post
DELETE /api/posts/{id}/ - Delete a post

Query Parameters:
- category: Filter by category ID
- tag: Filter by tag
- my_posts: Show only the current user's posts
```

### Comments

```
GET /api/comments/ - List all approved comments
POST /api/comments/ - Create a new comment
GET /api/comments/{id}/ - Get comment details
PUT /api/comments/{id}/ - Update a comment
DELETE /api/comments/{id}/ - Delete a comment

Query Parameters:
- post: Filter by post ID
```

## Features Demonstrated

### 1. Dynamic Schema Selection
```python
def get_schema(self, request, operation):
    if operation == 'list':
        return PostListSchema
    elif operation == 'create':
        return PostCreateSchema
    return PostDetailSchema
```

### 2. Custom Permissions
```python
class IsPostAuthor(BasePermission):
    def has_object_permission(self, request, obj: Post) -> bool:
        return obj.author == request.user
```

### 3. Automatic Author Assignment
```python
def perform_create(self, schema_instance):
    instance = super().perform_create(schema_instance)
    instance.author = self.request.user
    instance.save()
    return instance
```

### 4. Query Parameter Filtering
```python
def get_queryset(self):
    queryset = self.queryset
    category_id = self.request.query_params.get('category')
    if category_id:
        queryset = queryset.filter(category_id=category_id)
    return queryset
```

### 5. Nested Serialization
```python
class PostDetailSchema(NinjaModelSchema):
    author: UserSchema
    category: CategorySchema
    comments: List[CommentSchema]
```

## Usage Example

```python
# Create a new post
response = client.post(
    "/api/posts/",
    json={
        "title": "My First Post",
        "content": "Hello, World!",
        "category_id": 1,
        "is_published": True,
        "tags": "python,django,api"
    },
    headers={"Authorization": "Bearer your-token"}
)

# Get posts by category
posts = client.get("/api/posts/?category=1")

# Get user's own posts
my_posts = client.get("/api/posts/?my_posts=true")

# Add a comment
comment = client.post(
    "/api/comments/",
    json={
        "post_id": 1,
        "content": "Great post!"
    }
)
```

## Security Features

- Posts are only visible if published (unless you're the author)
- Comments must be approved to be visible
- Only authenticated users can create posts and comments
- Only authors can modify their own posts and comments
- Automatic author assignment prevents impersonation

This example demonstrates best practices for building APIs with ninja_rest, including proper resource organization, security, and efficient database queries.
