from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="historicaluser",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical User Account",
                "verbose_name_plural": "historical User Accounts",
            },
        ),
        migrations.AlterModelOptions(
            name="user",
            options={
                "ordering": ("-id",),
                "verbose_name": "User Account",
                "verbose_name_plural": "User Accounts",
            },
        ),
    ]
