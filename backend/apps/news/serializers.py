# apps/news/serializers.py

from rest_framework import serializers
from .models import NewsArticle, Source, Category, Language, Country


class BaseChoiceSerializer(serializers.ModelSerializer):
    """Base serializer for models with choice fields"""
    name = serializers.SerializerMethodField()
    
    def get_name(self, obj):
        """Generic method to get display name from choices"""
        # Works for both get_name_display() and get_code_display()
        if hasattr(obj, 'get_name_display'):
            return obj.get_name_display()
        elif hasattr(obj, 'get_code_display'):
            return obj.get_code_display()
        return str(obj)


class CategorySerializer(BaseChoiceSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'name']


class LanguageSerializer(BaseChoiceSerializer):
    class Meta:
        model = Language
        fields = ['id', 'code', 'name']


class CountrySerializer(BaseChoiceSerializer):
    class Meta:
        model = Country
        fields = ['id', 'code', 'name']


class SourceMinimalSerializer(serializers.ModelSerializer):
    """Minimal serializer for nested use"""
    class Meta:
        model = Source
        fields = ['id', 'source_id', 'name']


class SourceSerializer(serializers.ModelSerializer):
    """Full source serializer with nested relationships"""
    category = CategorySerializer(read_only=True)
    language = LanguageSerializer(read_only=True)
    country = CountrySerializer(read_only=True)
    
    class Meta:
        model = Source
        fields = [
            'id', 'source_id', 'name', 'description', 
            'url', 'category', 'language', 'country'
        ]


class NewsArticleListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views"""
    source = SourceMinimalSerializer(read_only=True)
    category_name = serializers.CharField(source='category.get_name_display', read_only=True)
    country_name = serializers.CharField(source='country.get_code_display', read_only=True)
    language_name = serializers.CharField(source='language.get_code_display', read_only=True)
    
    class Meta:
        model = NewsArticle
        fields = [
            'id', 'title', 'description', 'url', 'image_url',
            'published_at', 'source', 'category_name', 
            'country_name', 'language_name', 'created_at'
        ]



class NewsArticleDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single article"""
    source = SourceSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    language = LanguageSerializer(read_only=True)
    country = CountrySerializer(read_only=True)
    
    class Meta:
        model = NewsArticle
        fields = [
            'id', 'title', 'description', 'url', 'image_url',
            'published_at', 'source', 'category', 'language',
            'country', 'created_at'
        ]
