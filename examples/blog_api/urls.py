from django.urls import path
from .views import CategoryViewSet, PostViewSet, CommentViewSet
from .api import api

# Register viewsets with their respective URL prefixes
CategoryViewSet.register(api, 'categories')
PostViewSet.register(api, 'posts')
CommentViewSet.register(api, 'comments')

urlpatterns = [
    path('api/', api.urls),  # This includes the API endpoints and Swagger UI
]
