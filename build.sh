#!/usr/bin/env bash

set -o errexit

python -m pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate

python manage.py shell <<'PY'
import os
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

client_id = os.environ.get("GOOGLE_CLIENT_ID")
client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")

if client_id and client_secret:
    site, _ = Site.objects.get_or_create(
        id=1,
        defaults={
            "domain": "nanevora.onrender.com",
            "name": "NaNeVora",
        },
    )

    app, created = SocialApp.objects.get_or_create(
        provider="google",
        defaults={
            "name": "NaNeVora Google",
            "client_id": client_id,
            "secret": client_secret,
        },
    )

    if not created:
        app.name = "NaNeVora Google"
        app.client_id = client_id
        app.secret = client_secret
        app.save()

    app.sites.add(site)
PY