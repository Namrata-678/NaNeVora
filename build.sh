#!/usr/bin/env bash

set -o errexit

python -m pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py shell <<'PY'
from django.db.migrations.recorder import MigrationRecorder

rows = MigrationRecorder.Migration.objects.filter(
    app__in=["sites", "socialaccount"]
).order_by("app", "name")

for row in rows:
    print("MIGRATION:", row.app, row.name)
PY

python manage.py migrate