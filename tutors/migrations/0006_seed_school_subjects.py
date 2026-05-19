from django.db import migrations
from django.utils.text import slugify


SCHOOL_SUBJECTS = [
    'Математика',
    'Алгебра',
    'Геометрия',
    'Русский язык',
    'Литература',
    'Английский язык',
    'Немецкий язык',
    'Французский язык',
    'Испанский язык',
    'Китайский язык',
    'Информатика',
    'Физика',
    'Химия',
    'Биология',
    'География',
    'История',
    'Обществознание',
    'Экономика',
    'Право',
    'Астрономия',
    'Черчение',
    'Музыка',
    'ИЗО',
    'Подготовка к школе',
    'Начальная школа',
]


def add_school_subjects(apps, schema_editor):
    Subject = apps.get_model('tutors', 'Subject')
    for name in SCHOOL_SUBJECTS:
        existing = Subject.objects.filter(name__iexact=name).first()
        if existing:
            continue

        base_slug = slugify(name) or 'subject'
        slug = base_slug
        idx = 2
        while Subject.objects.filter(slug=slug).exists():
            slug = f'{base_slug}-{idx}'
            idx += 1

        Subject.objects.create(name=name, slug=slug)


class Migration(migrations.Migration):

    dependencies = [
        ('tutors', '0005_studentgroup_tutorstudentlink'),
    ]

    operations = [
        migrations.RunPython(add_school_subjects, migrations.RunPython.noop),
    ]
