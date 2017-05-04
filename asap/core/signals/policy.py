import logging
import requests

from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

logger = logging.getLogger(__name__)

# FIXME
AM_SERVER_URL = 'http://172.20.0.1:8080'
AM_SERVER_HEADER = {
    'Host': 'am.veris.in'
}


@receiver(post_save)
def create_policy(sender, **kwargs):
    if not hasattr(sender, 'author'):
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
            'server': AM_SERVER_URL
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
        headers=AM_SERVER_HEADER
    )

    logger.info(response.status_code)
    logger.info(response.json())
