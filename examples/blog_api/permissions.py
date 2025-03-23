from ninja_rest.permissions import BasePermission
from .models import Post, Comment

class IsPostAuthor(BasePermission):
    def has_object_permission(self, request, obj: Post) -> bool:
        """Check if user is the author of the post"""
        return obj.author == request.user

class IsCommentAuthor(BasePermission):
    def has_object_permission(self, request, obj: Comment) -> bool:
        """Check if user is the author of the comment"""
        return obj.author == request.user

class IsPublishedPost(BasePermission):
    def has_object_permission(self, request, obj: Post) -> bool:
        """Allow access only if post is published or user is the author"""
        return obj.is_published or obj.author == request.user
