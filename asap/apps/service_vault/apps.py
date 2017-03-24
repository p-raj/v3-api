from django.apps import AppConfig


class ServiceVaultConfig(AppConfig):
    name = 'asap.apps.service_vault'

    def ready(self):
        import asap.apps.service_vault.signals
