from django.urls import path
from .views import SourceListView, CountryListView, CategoryListView, LanguageListView


urlpatterns = [
    path('sources/', SourceListView.as_view(), name='source-list'),
    path('countries/', CountryListView.as_view(), name='country-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('languages/', LanguageListView.as_view(), name='language-list'),
]