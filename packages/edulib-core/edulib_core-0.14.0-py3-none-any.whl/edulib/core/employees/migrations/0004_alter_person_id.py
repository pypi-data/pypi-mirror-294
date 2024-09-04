from django.db import (
    migrations,
)


sql = """\
DROP INDEX IF EXISTS "employee_person_id_id_23291c0b";
ALTER TABLE "employee" RENAME COLUMN "person_id" TO "person";
ALTER TABLE "employee" ALTER COLUMN "person" TYPE varchar(36) USING "person"::varchar(36);

ALTER TABLE "employee" RENAME COLUMN "person" TO "person_id";
CREATE INDEX "employee_person_id_0c86fe9c" ON "employee" ("person_id");
ALTER TABLE "employee" ADD CONSTRAINT "employee_person_id_0c86fe9c_fk_person_id" FOREIGN KEY ("person_id") REFERENCES "person" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "employee_person_id_0c86fe9c_like" ON "employee" ("person_id" varchar_pattern_ops);
"""


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0003_remove_employee_id_alter_employee_external_id'),
        ('persons', '0003_remove_person_id_alter_person_external_id'),
    ]

    operations = [
        migrations.RunSQL(sql)
    ]
