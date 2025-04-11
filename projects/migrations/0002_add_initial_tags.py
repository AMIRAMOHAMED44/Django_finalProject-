from django.db import migrations

def add_initial_tags(apps, schema_editor):
    Tag = apps.get_model('projects', 'Tag')
    initial_tags = [
        'Technology',
        'Education',
        'Healthcare',
        'Environment',
        'Community'
    ]
    
    for tag_name in initial_tags:
        Tag.objects.get_or_create(name=tag_name)

def remove_initial_tags(apps, schema_editor):
    Tag = apps.get_model('projects', 'Tag')
    Tag.objects.filter(name__in=[
        'Technology',
        'Education',
        'Healthcare',
        'Environment',
        'Community'
    ]).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_initial_tags, remove_initial_tags),
    ] 