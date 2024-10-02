import json

from django.core.files.base import ContentFile
from django.db import migrations


def load_cafe(apps, schema_editor):
    cafe_model = apps.get_model('cafe', 'Cafe')
    json_data = open('cafe/migrations/data/cafe.json')
    cafes = json.load(json_data)

    cafe_list = []
    for cafe in cafes:
        cafe_list.append(
            cafe_model(name=cafe.get("name"), description=cafe.get("description"),
                       location=cafe.get("location"), logo=cafe.get("logo")))
    saved_cafes = cafe_model.objects.bulk_create(cafe_list)

    for cafe in saved_cafes:
        cafe_json_obj = next(c for c in cafes if c.get("name") == cafe.name)
        filename = cafe_json_obj.get('logo')
        if filename:
            with open(filename, 'rb') as f:
                data = f.read()
                cafe.logo.save(filename.rsplit('/', 1)[-1], ContentFile(data))


class Migration(migrations.Migration):
    dependencies = [
        ('cafe', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_cafe),
    ]
