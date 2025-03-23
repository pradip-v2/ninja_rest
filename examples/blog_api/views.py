from django.db.models import Count
from ninja import Query, Field
from ninja_rest import ModelViewSet
from ninja_rest.permissions import IsAuthenticated
from ninja_rest.pagination import PageNumberPagination
from .models import Category, Post, Comment
from .schemas import (
    CategorySchema, PostListSchema, PostDetailSchema, 
    PostCreateSchema, CommentSchema, CommentCreateSchema
)
from .permissions import IsPublishedPost
from .api import api

@api.tags(['categories'])
class CategoryViewSet(ModelViewSet):
    """ViewSet for managing blog categories"""
    schema = CategorySchema
    queryset = Category.objects.all()
    pagination_class = PageNumberPagination

class PostFilters(Query):
    category: int = Field(None, description="Filter posts by category ID")
    tag: str = Field(None, description="Filter posts by tag")
    my_posts: bool = Field(False, description="Show only the current user's posts")

@api.tags(['posts'])
class PostViewSet(ModelViewSet):
    """ViewSet for managing blog posts with filtering and pagination"""
    queryset = Post.objects.select_related('author', 'category').prefetch_related('comments')
    permission_classes = [IsAuthenticated, IsPublishedPost]
    pagination_class = PageNumberPagination

    def get_schema(self):
        """Return different schemas for different operations"""
        if self.operation in ['create', 'update']:
            return PostCreateSchema
        elif self.operation == 'list':
            return PostListSchema
        return PostDetailSchema

    def get_queryset(self):
        """Filter queryset based on query parameters"""
        queryset = super().get_queryset()
        
        # Add comment count for list view
        if self.operation == 'list':
            queryset = queryset.annotate(comment_count=Count('comments'))

        # Get filters from request
        filters = PostFilters.from_request(self.request)

        # Apply filters
        if filters.category:
            queryset = queryset.filter(category_id=filters.category)
        if filters.tag:
            queryset = queryset.filter(tags__icontains=filters.tag)
        if filters.my_posts:
            queryset = queryset.filter(author=self.request.user)
        elif self.operation == 'list':
            queryset = queryset.filter(is_published=True)

        return queryset

    def perform_create(self, schema_instance):
        """Set the author to the current user when creating a post"""
        instance = super().perform_create(schema_instance)
        instance.author = self.request.user
        instance.save()
        return instance

class CommentFilters(Query):
    post: int = Field(None, description="Filter comments by post ID")

@api.tags(['comments'])
class CommentViewSet(ModelViewSet):
    """ViewSet for managing post comments with filtering and pagination"""
    queryset = Comment.objects.select_related('author', 'post')
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_schema(self):
        """Return different schemas for different operations"""
        if self.operation == 'create':
            return CommentCreateSchema
        return CommentSchema

    def get_queryset(self):
        """Filter queryset based on query parameters"""
        queryset = super().get_queryset()

        # Get filters from request
        filters = CommentFilters.from_request(self.request)

        # Apply filters
        if filters.post:
            queryset = queryset.filter(post_id=filters.post)

        return queryset.filter(is_approved=True)

    def perform_create(self, schema_instance):
        """Set the author to the current user when creating a comment"""
        instance = super().perform_create(schema_instance)
        instance.author = self.request.user
        instance.save()
        return instance
