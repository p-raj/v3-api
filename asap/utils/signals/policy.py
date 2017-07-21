import logging
import requests

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

logger = logging.getLogger(__name__)


@receiver(post_save)
def create_policy(sender, **kwargs):
    if not hasattr(sender, 'author') or not hasattr(sender, 'uuid'):
        # we are creating policies only
        # for our models :)
        return

    instance = kwargs.get('instance')
    author = instance.author

    resource_name = 'vrn:resource:{name}:{uuid}:'.format(**{
        'name': sender.__name__.lower(),
        'uuid': instance.uuid
    })

    # FIXME
    response = requests.post(
        url='{server}/micro-service/am/policy/'.format(**{
            'server': getattr(settings, 'V3__API_GATEWAY')
        }),
        json={
            'source': author.username,
            'source_permission_set': [{
                'target': resource_name,
                'create': True,
                'read': True,
                'update': True,
                'delete': True,
            }]
        },
        headers={
            'Host': getattr(settings, 'V3__HOST_AUTHORIZATION')
        }
    )

    logger.info(response.status_code)
    logger.info(response.json())
