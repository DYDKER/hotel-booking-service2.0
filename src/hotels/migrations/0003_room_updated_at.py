from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hotels", "0002_booking_updated_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="room",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
