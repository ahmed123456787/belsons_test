from django.contrib import admin
from .models import (
    Category,
    Language,
    Country,
    Source,
    NewsArticle,
)

class ReadOnlyAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Category)
class CategoryAdmin(ReadOnlyAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Language) 
class LanguageAdmin(ReadOnlyAdmin):
    list_display = ("code",)
    search_fields = ("code",)


@admin.register(Country)
class CountryAdmin(ReadOnlyAdmin):
    list_display = ("code",)
    search_fields = ("code",)


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "source_id",
        "category",
        "language",
        "country",
    )
    list_filter = ("category", "language", "country")
    search_fields = ("name", "source_id")
    ordering = ("name",)


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "source",
        "category",
        "language",
        "country",
        "published_at",
    )
    list_filter = ("category", "language", "country", "published_at")
    search_fields = ("title", "description")
    date_hierarchy = "published_at"
    ordering = ("-published_at",)
    readonly_fields = ("created_at",)