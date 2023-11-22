from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('cat/', CategoriesViews.as_view()),
    path('ads/', AsdViews.as_view()),
    path('ads/<int:pk>/', AdsDetailView.as_view()),
    path('cat/<int:pk>/', CategoryDetailView.as_view())

]
