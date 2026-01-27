from django.db import migrations

def seed_reference_data(apps, schema_editor):
    Category = apps.get_model("news", "Category")
    Language = apps.get_model("news", "Language")
    Country = apps.get_model("news", "Country")

    categories = [
        "business",
        "entertainment",
        "general",
        "health",
        "science",
        "sports",
        "technology",
    ]

    for name in categories:
        Category.objects.get_or_create(name=name)

    for code in ["en", "fr", "ar"]:
        Language.objects.get_or_create(code=code)

    for code in ["us", "fr", "eg", "ca"]:
        Country.objects.get_or_create(code=code)

class Migration(migrations.Migration):

    dependencies = [
        ("news", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_reference_data),
    ]