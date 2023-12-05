from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('cat/', CategoriesListViews.as_view()),
    path('cat/create/', CategoryCreateView.as_view()),
    path('cat/<int:pk>/', CategoryDetailView.as_view()),
    path('cat/<int:pk>/delete/', CategoryDeleteView.as_view()),
    path('cat/<int:pk>/update/', CategoryUpdateView.as_view()),
    path('ads/', AsdListViews.as_view()),
    path('ads/create/', AdsCreateView.as_view()),
    path('ads/<int:pk>/', AdsDetailView.as_view()),
    path('ads/<int:pk>/delete/', AdsDeleteView.as_view()),
    path('ads/<int:pk>/update/', AdsUpdateView.as_view()),
    path('ads/<int:pk>/upload_image/', AdsImageView.as_view()),
    path('user/', UsersListViews.as_view()),
    path('user/create/', UserCreateView.as_view()),
    path('user/<int:pk>/', UserDetailView.as_view()),
    path('user/<int:pk>/delete/', UserDeleteView.as_view()),
    path('user/<int:pk>/update/', UserUpdateView.as_view()),
]
