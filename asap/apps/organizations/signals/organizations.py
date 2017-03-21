from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from asap.apps.organizations.models.organizations import Organization
from asap.apps.process.models.process_locker import ProcessLocker
from asap.apps.vrt.models.runtime_locker import RuntimeLocker
from asap.apps.widgets.models.widget_locker import WidgetLocker


@receiver(post_save, sender=Organization)
def enable_default_services(sender, **kwargs):
    if not kwargs.get('created'):
        return

    instance = kwargs.get('instance')

    # TODO
    # remove hard bindings & hard coded strings
    # and direct access to different services
    # this is just to speed up dev cycle :(
    rl = RuntimeLocker.objects.create(author=instance.author)
    instance.service_set.create(author=instance.author,
                                name='runtime',
                                service_client_id=rl.uuid)

    wl = WidgetLocker.objects.create(author=instance.author)
    instance.service_set.create(author=instance.author,
                                name='widget',
                                service_client_id=wl.uuid)

    pl = ProcessLocker.objects.create(author=instance.author)
    instance.service_set.create(author=instance.author,
                                name='process',
                                service_client_id=pl.uuid)
