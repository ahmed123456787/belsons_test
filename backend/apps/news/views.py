from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from .models import NewsArticle, Source, Category, Language, Country
from .serializers import (
    NewsArticleListSerializer,
    NewsArticleDetailSerializer,
    NewsArticleCreateSerializer,
    SourceSerializer,
    CategorySerializer,
    LanguageSerializer,
    CountrySerializer
)

# from .filters import NewsArticleFilter
# from .pagination import NewsArticlePagination

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




class NewsArticleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for NewsArticle model
    
    Provides CRUD operations and custom filtering endpoints
    
    List endpoint supports filtering by:
    - category: Filter by category name (e.g., 'technology')
    - country: Filter by country code (e.g., 'us')
    - language: Filter by language code (e.g., 'en')
    - source: Filter by source ID (e.g., 'bbc-news')
    - title: Search in title (case-insensitive)
    - published_from: Articles published after this date
    - published_to: Articles published before this date
    - ordering: Sort by field (e.g., '-published_at')
    
    Custom endpoints:
    - /articles/by_category/?category=technology
    - /articles/by_country/?country=us
    - /articles/by_source/?source=bbc-news
    - /articles/recent/?days=7
    - /articles/stats/
    """
    
    queryset = NewsArticle.objects.select_related(
        'source', 'category', 'language', 'country'
    ).all()
    
    
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter
    ]
    
    
    ordering_fields = ['published_at', 'created_at', 'title']
    ordering = ['-published_at']  # Default ordering
    
    search_fields = ['title', 'description']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'retrieve':
            return NewsArticleDetailSerializer
        elif self.action == 'create':
            return NewsArticleCreateSerializer
        return NewsArticleListSerializer
    
    @method_decorator(cache_page(60 * 5))  # Cache for 5 minutes
    def list(self, request, *args, **kwargs):
        """
        List all articles with filtering and pagination
        
        Example URLs:
        - /api/v1/articles/
        - /api/v1/articles/?category=technology
        - /api/v1/articles/?country=us&category=business
        - /api/v1/articles/?source=bbc-news
        - /api/v1/articles/?published_from=2024-01-01
        - /api/v1/articles/?ordering=-published_at
        - /api/v1/articles/?search=artificial intelligence
        """
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error listing articles: {str(e)}", exc_info=True)
            return Response(
                {'error': 'An error occurred while fetching articles.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve single article by ID
        
        Example: /api/v1/articles/123/
        """
        try:
            return super().retrieve(request, *args, **kwargs)
        except NewsArticle.DoesNotExist:
            return Response(
                {'error': 'Article not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error retrieving article: {str(e)}", exc_info=True)
            return Response(
                {'error': 'An error occurred while fetching the article.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )    
   
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """
        Get articles filtered by category
        
        Query params:
        - category: Category name (required) - e.g., 'technology', 'business'
        
        Example: /api/v1/articles/by_category/?category=technology
        """
        category_name = request.query_params.get('category')
        
        if not category_name:
            return Response(
                {'error': 'category parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            articles = self.queryset.filter(category__name=category_name)
            
            if not articles.exists():
                return Response(
                    {'message': f'No articles found for category: {category_name}', 'results': []},
                    status=status.HTTP_200_OK
                )
            
            page = self.paginate_queryset(articles)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(articles, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Error filtering by category: {str(e)}", exc_info=True)
            return Response(
                {'error': 'An error occurred while filtering articles.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def by_country(self, request):
        """
        Get articles filtered by country
        
        Query params:
        - country: Country code (required) - e.g., 'us', 'fr'
        
        Example: /api/v1/articles/by_country/?country=us
        """
        country_code = request.query_params.get('country')
        
        if not country_code:
            return Response(
                {'error': 'country parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            articles = self.queryset.filter(country__code=country_code)
            
            if not articles.exists():
                return Response(
                    {'message': f'No articles found for country: {country_code}', 'results': []},
                    status=status.HTTP_200_OK
                )
            
            page = self.paginate_queryset(articles)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(articles, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Error filtering by country: {str(e)}", exc_info=True)
            return Response(
                {'error': 'An error occurred while filtering articles.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def by_source(self, request):
        """
        Get articles filtered by source
        
        Query params:
        - source: Source ID (required) - e.g., 'bbc-news'
        
        Example: /api/v1/articles/by_source/?source=bbc-news
        """
        source_id = request.query_params.get('source')
        
        if not source_id:
            return Response(
                {'error': 'source parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            articles = self.queryset.filter(source__source_id=source_id)
            
            if not articles.exists():
                return Response(
                    {'message': f'No articles found for source: {source_id}', 'results': []},
                    status=status.HTTP_200_OK
                )
            
            page = self.paginate_queryset(articles)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(articles, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Error filtering by source: {str(e)}", exc_info=True)
            return Response(
                {'error': 'An error occurred while filtering articles.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        Get recent articles
        
        Query params:
        - days: Number of days to look back (default: 7)
        
        Example: /api/v1/articles/recent/?days=7
        """
        try:
            days = int(request.query_params.get('days', 7))
            
            if days < 1:
                return Response(
                    {'error': 'days must be a positive integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            cutoff_date = timezone.now() - timedelta(days=days)
            articles = self.queryset.filter(published_at__gte=cutoff_date)
            
            page = self.paginate_queryset(articles)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(articles, many=True)
            return Response(serializer.data)
            
        except ValueError:
            return Response(
                {'error': 'days must be a valid integer'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error fetching recent articles: {str(e)}", exc_info=True)
            return Response(
                {'error': 'An error occurred while fetching recent articles.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
  

class SourceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Source model (Read-only)
    
    List all sources with optional filtering by category, language, country
    """
    queryset = Source.objects.select_related(
        'category', 'language', 'country'
    ).all()
    
    serializer_class = SourceSerializer
    
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category__name', 'language__code', 'country__code']
    ordering_fields = ['name', 'source_id']
    ordering = ['name']
    
    @method_decorator(cache_page(60 * 30))  # Cache for 30 minutes
    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error listing sources: {str(e)}", exc_info=True)
            return Response(
                {'error': 'An error occurred while fetching sources.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Source.DoesNotExist:
            return Response(
                {'error': 'Source not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error retrieving source: {str(e)}", exc_info=True)
            return Response(
                {'error': 'An error occurred while fetching the source.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


