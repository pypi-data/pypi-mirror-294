from django.db import (
    migrations,
)


# SQL-запросы для удаления индекса и ограничения
sql_drop_constraints_and_index = """
    -- Удаление первичного ключа, связанного с внешним id
    ALTER TABLE academic_year DROP CONSTRAINT IF EXISTS academic_year_external_id_15371dc8_pk;

    -- Удаление индекса
    DROP INDEX IF EXISTS academic_year_external_id_15371dc8_like;
"""

# SQL-запросы для восстановления индекса и ограничения
sql_create_constraints_and_index = """
    -- Восстановление первичного ключа, связанного с внешним id
    ALTER TABLE academic_year ADD CONSTRAINT academic_year_external_id_15371dc8_pk PRIMARY KEY (external_id);

    -- Восстановление индекса
    CREATE INDEX academic_year_external_id_15371dc8_like ON academic_year (external_id);
"""


class Migration(migrations.Migration):
    dependencies = [
        ('academic_years', '0003_remove_academicyear_id_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql=sql_drop_constraints_and_index,
            reverse_sql=sql_create_constraints_and_index,
        )
    ]
