from ninja import NinjaAPI
from ninja.security import HttpBearer
from typing import Optional
from django.contrib.auth.models import User

class BearerAuth(HttpBearer):
    def authenticate(self, request, token: str) -> Optional[User]:
        try:
            # This is a simple example. In production, use proper token validation
            return User.objects.get(auth_token__key=token)
        except User.DoesNotExist:
            return None

api = NinjaAPI(
    title="Blog API",
    version="1.0.0",
    description="""
    A full-featured blog API built with Django Ninja REST.
    
    This API provides endpoints for managing blog posts, categories, and comments.
    Features include:
    * Authentication using Bearer tokens
    * Post creation and management
    * Category organization
    * Comment system
    * Filtering and pagination
    """,
    auth=BearerAuth(),
    urls_namespace="blog_api",
    docs_url="/docs",
    openapi_url="/openapi.json",
    csrf=False,
)

# Tags for API documentation
api.add_tag({
    "name": "categories",
    "description": "Operations with blog categories"
})

api.add_tag({
    "name": "posts",
    "description": "Operations with blog posts"
})

api.add_tag({
    "name": "comments",
    "description": "Operations with post comments"
})
