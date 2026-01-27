from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class NewsArticlePagination(PageNumberPagination):
    """
    Custom pagination for news
    Default: 50 articles per page
    """
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        """Custom pagination response format"""
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'page_size': self.get_page_size(self.request),
            'results': data
        })