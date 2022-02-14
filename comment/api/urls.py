from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from . import views
from appointment.api.urls import router

# router = DefaultRouter()
# router.register('comment', views.CommentViewSet, basename='comment')
# NestedDefaultRouter
comment_router = NestedDefaultRouter(router, "appointment", lookup="appointment")
comment_router.register("comment", views.CommentViewSet, basename="comment")

urlpatterns = [path("", include(comment_router.urls))]
