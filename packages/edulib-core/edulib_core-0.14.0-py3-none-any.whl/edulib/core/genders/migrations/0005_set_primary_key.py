from django.db import (
    migrations,
)


# SQL-запросы для удаления индекса и ограничения
sql_drop_constraints_and_index = """
    -- Удаление существующего первичного ключа, если он есть
    ALTER TABLE gender DROP CONSTRAINT IF EXISTS gender_pkey;

    -- Удаление возможных индексов, которые могут конфликтовать
    DROP INDEX IF EXISTS gender_id_key;
"""

# SQL-запросы для установки нового PK и индекса
sql_create_constraints_and_index = """
    -- Установка поля id как primary key
    ALTER TABLE gender ADD CONSTRAINT gender_pkey PRIMARY KEY (id);
"""

class Migration(migrations.Migration):

    dependencies = [
        ('genders', '0004_alter_gender_id'),
    ]

    operations = [
        migrations.RunSQL(
            sql=sql_drop_constraints_and_index,
            reverse_sql=sql_create_constraints_and_index,
        ),
        migrations.RunSQL(
            sql=sql_create_constraints_and_index,
            reverse_sql=sql_drop_constraints_and_index,
        ),
    ]
