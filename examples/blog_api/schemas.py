from typing import List, Optional
from ninja_rest import NinjaModelSchema
from django.contrib.auth.models import User
from .models import Category, Post, Comment

class UserSchema(NinjaModelSchema):
    class Config:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class CategorySchema(NinjaModelSchema):
    class Config:
        model = Category
        fields = ['id', 'name', 'description', 'created_at']

class CommentSchema(NinjaModelSchema):
    author: UserSchema

    class Config:
        model = Comment
        fields = ['id', 'content', 'created_at', 'is_approved', 'author']

class PostListSchema(NinjaModelSchema):
    author: UserSchema
    category: CategorySchema
    comment_count: int

    class Config:
        model = Post
        fields = ['id', 'title', 'category', 'author', 'created_at', 'is_published', 'tags']

class PostDetailSchema(NinjaModelSchema):
    author: UserSchema
    category: CategorySchema
    comments: List[CommentSchema]

    class Config:
        model = Post
        fields = ['id', 'title', 'content', 'category', 'author', 
                 'created_at', 'updated_at', 'is_published', 'tags', 'comments']

class PostCreateSchema(NinjaModelSchema):
    category_id: int
    tags: Optional[str] = None

    class Config:
        model = Post
        fields = ['title', 'content', 'category_id', 'is_published', 'tags']

class CommentCreateSchema(NinjaModelSchema):
    post_id: int

    class Config:
        model = Comment
        fields = ['content', 'post_id']
