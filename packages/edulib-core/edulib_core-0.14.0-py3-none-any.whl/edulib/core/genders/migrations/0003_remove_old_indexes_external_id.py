from django.db import (
    migrations,
)


# SQL-запросы для удаления индекса и ограничения
sql_drop_constraints_and_index = """
    -- Удаление первичного ключа, связанного с внешним id
    ALTER TABLE gender DROP CONSTRAINT IF EXISTS gender_external_id_776cb429_pk;

    -- Удаление индекса
    DROP INDEX IF EXISTS gender_external_id_776cb429_like;
"""

# SQL-запросы для восстановления индекса и ограничения
sql_create_constraints_and_index = """
    -- Восстановление первичного ключа, связанного с внешним id
    ALTER TABLE gender ADD CONSTRAINT gender_external_id_776cb429_pk PRIMARY KEY (external_id);

    -- Восстановление индекса
    CREATE INDEX gender_external_id_776cb429_like ON gender (external_id);
"""

class Migration(migrations.Migration):

    dependencies = [
        ('genders', '0002_remove_gender_id_alter_gender_external_id'),
    ]

    operations = [
        migrations.RunSQL(
            sql=sql_drop_constraints_and_index,
            reverse_sql=sql_create_constraints_and_index,
        )
    ]
