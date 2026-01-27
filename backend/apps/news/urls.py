from django.urls import path
from .views import (SourceListAPIView, CountryListView, CategoryListView, 
                    LanguageListView, NewsArticleListView, NewsArticleRetrieveView

)
  

urlpatterns = [
    path('sources/', SourceListAPIView.as_view(), name='source-list'),
    path('countries/', CountryListView.as_view(), name='country-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('languages/', LanguageListView.as_view(), name='language-list'),
    path('articles/', NewsArticleListView.as_view(), name='newsarticle-list'),
    path('articles/<int:pk>/', NewsArticleRetrieveView.as_view(), name='newsarticle-detail'),
]