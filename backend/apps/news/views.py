from rest_framework import  status, filters
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import timedelta

from .models import NewsArticle, Source, Category, Language, Country
from .serializers import (
    NewsArticleListSerializer,
    NewsArticleDetailSerializer,
    SourceSerializer,
    CategorySerializer,
    LanguageSerializer,
    CountrySerializer
)
from .pagination import NewsArticlePagination

import logging
logger = logging.getLogger(__name__)



class CategoryListView(ListAPIView):
    """ViewSet for Category model (Read-only)"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class LanguageListView(ListAPIView):
    """ViewSet for Language model (Read-only)"""
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class CountryListView(ListAPIView):
    """ViewSet for Country model (Read-only)"""
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class SourceListAPIView(ListAPIView):
    """
    List all sources with optional filtering by category, language, country
    """
    queryset = Source.objects.select_related('category', 'language', 'country').all()
    serializer_class = SourceSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    pagination_class = NewsArticlePagination
   


class NewsArticleListView(ListAPIView):
    """
    List all news articles with filtering, search, and ordering.
    Supports query params:
    - category: Filter by category name
    - country: Filter by country code
    - language: Filter by language code
    - source: Filter by source ID
    - title: Search in title
    - published_from: Filter articles published after date (YYYY-MM-DD)
    - published_to: Filter articles published before date (YYYY-MM-DD)
    - days: Filter recent articles from last N days
    - ordering: Sort by field (e.g., -published_at)
    """
    queryset = NewsArticle.objects.select_related(
        'source', 'category', 'language', 'country'
    ).all()
    serializer_class = NewsArticleListSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category__name', 'country__code', 'language__code', 'source__source_id']
    search_fields = ['title', 'description']
    ordering_fields = ['published_at', 'created_at', 'title']
    ordering = ['-published_at']


    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()

            # Filter by published_from / published_to
            published_from = request.query_params.get('published_from')
            published_to = request.query_params.get('published_to')
            days = request.query_params.get('days')

            if published_from:
                queryset = queryset.filter(published_at__gte=published_from)
            if published_to:
                queryset = queryset.filter(published_at__lte=published_to)
            if days:
                try:
                    days = int(days)
                    if days > 0:
                        cutoff = timezone.now() - timedelta(days=days)
                        queryset = queryset.filter(published_at__gte=cutoff)
                except ValueError:
                    return Response({'error': 'days must be a positive integer'}, status=status.HTTP_400_BAD_REQUEST)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        except Exception as e:
            logger.error(f"Error listing articles: {str(e)}", exc_info=True)
            return Response({'error': 'An error occurred while fetching articles.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NewsArticleRetrieveView(RetrieveAPIView):
    """
    Retrieve single article by ID
    """
    queryset = NewsArticle.objects.select_related(
        'source', 'category', 'language', 'country'
    ).all()
    serializer_class = NewsArticleDetailSerializer