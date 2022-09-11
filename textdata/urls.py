from django.urls import path, include

from rest_framework.routers import DefaultRouter

from textdata.views import TagView, SnippetView


router = DefaultRouter()
router.register(r'tags', TagView, basename="tags")
router.register(r'snippet', SnippetView, basename="snippet")

urlpatterns = [
    path('', include(router.urls)),
]

