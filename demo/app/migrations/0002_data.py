# Generated by Django 4.2 on 2023-05-03 09:50

from django.db import migrations


def forwards_func(apps, schema_editor):
    Ausgabe = apps.get_model("app", "Ausgabe")
    data = [
        {"name": f"2022-{n}", "jahr": "2022", "num": f"{n}", "lnum": f"{n+100}"}
        for n in range(1, 50)
    ]
    data.insert(10, {"name": f"VERY LONG NAME THAT IS PROBABLY GOING TO CAUSE SOME PROBLEMS 2022", "jahr": "", "num": "", "lnum": "5000000"})
    for d in data:
        Ausgabe.objects.create(**d)


def reverse_func(apps, schema_editor):
    Ausgabe = apps.get_model("app", "Ausgabe")
    Ausgabe.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func)
    ]
