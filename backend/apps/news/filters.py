import django_filters
from .models import NewsArticle, Country, Language


class NewsArticleFilter(django_filters.FilterSet):
    """
    Custom filter for NewsArticle model.
    """
    category = django_filters.CharFilter(
        field_name='category__name',
        label='Category',
        method='filter_category'
    )
    country = django_filters.CharFilter(
        field_name='country',
        label='Country',
        method='filter_country'
    )
    language = django_filters.CharFilter(
        field_name='language',
        label='Language',
        method='filter_language'
    )
    source = django_filters.CharFilter(
        field_name='source__name',
        label='Source',
        method='filter_source'
    )

    class Meta:
        model = NewsArticle
        fields = ['category', 'country', 'language', 'source']

    def filter_category(self, queryset, name, value):
        """Filter by category name (case-insensitive)"""
        if value:
            return queryset.filter(category__name__iexact=value)
        return queryset

    def filter_country(self, queryset, name, value):
        """Filter by country code or name (case-insensitive)"""
        if value:
            return queryset.filter(
                country__code__iexact=value
            ) | queryset.filter(
                country__code__in=[
                    code for code, display_name in Country.COUNTRY_CHOICES
                    if display_name.lower() == value.lower()
                ]
            )
        return queryset

    def filter_language(self, queryset, name, value):
        """Filter by language code or name (case-insensitive)"""
        if value:
            return queryset.filter(
                language__code__iexact=value
            ) | queryset.filter(
                language__code__in=[
                    code for code, display_name in Language.LANGUAGE_CHOICES
                    if display_name.lower() == value.lower()
                ]
            )
        return queryset

    def filter_source(self, queryset, name, value):
        """Filter by source name (case-insensitive)"""
        if value:
            return queryset.filter(source__name__iexact=value)
        return queryset


