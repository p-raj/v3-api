import json
import logging

from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

logger = logging.getLogger(__name__)


@receiver(post_save)
def fire_web_hooks(sender, **kwargs):
    from apps.terminals.models import Terminal, TerminalLog

    if sender not in [Terminal, TerminalLog]:
        return

    # follow the convention and check whether
    # the event has been registered
    event_name = '{model}:{action}'.format(**{
        'model': sender._meta.model_name,
        'action': 'create' if kwargs.get('created') else 'update'
    })

    # find the event that has just happened
    # and fire all web hooks registered
    from apps.terminals.models import Event
    try:
        event = Event.objects.get(name=event_name)
    except Event.DoesNotExist as e:
        logger.warn(e)
        return

    # get the payload according to the the event type
    # TODO
    # different serializations or some kind of adapter
    # or may be different signals all together :/

    # currently let's only handle terminal log event
    payload = None
    if isinstance(sender, TerminalLog):
        payload = json.loads(kwargs.get('instance').data)

    if payload is not None:
        return

    for web_hook in event.webhook_set.filter(is_active=True):
        web_hook.fire(payload=payload)
