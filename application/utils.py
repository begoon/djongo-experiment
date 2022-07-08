from distutils.log import debug
from typing import List

import kwlog
from django.apps import apps
from django.contrib import auth
from django.db.migrations.recorder import MigrationRecorder
from django.db.models import Model

from application import settings

logger = kwlog.logger(__name__)


def mask_database_url_password(url: str) -> str:
    parts = url.split(":")
    assert len(parts) == 4
    parts = parts[2].split('@')
    assert len(parts) == 2
    password = parts[0]
    updated_url = url.replace(password, "***")
    assert url != updated_url
    return updated_url


def application_models(application: str) -> List[Model]:
    return apps.get_app_config(application).get_models()


def check_database_connectivity():
    logger.info(
        'database',
        name=settings.MONGODB_NAME,
        url=settings.MONGODB_URI,
    )

    last_migration = MigrationRecorder.Migration.objects.order_by(
        'applied'
    ).last()

    logger.info(
        'latest migration',
        app=last_migration.app,
        name=last_migration.name,
        when=str(last_migration.applied),
    )

    model = auth.models.User
    users = [
        f'{user.username}:{user.is_superuser}'
        for user in model.objects.filter()
    ]
    logger.info('django', users=users)

    for model in application_models('cms'):
        name = model._meta.model_name
        logger.info(f'{name}s', count=model.objects.all().count())
