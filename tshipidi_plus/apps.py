from django.apps import AppConfig
from django.db.models.signals import post_migrate


def edc_configure_callback(sender, **kwargs):
    from .edc_app_configuration import EdcAppConfiguration
    edc_app_configuration = EdcAppConfiguration()
    edc_app_configuration.prepare()


class TshipidiPlusAppConfig(AppConfig):
    name = 'tshipidi_plus'
    verbose_name = 'Tshipidi Plus'

    def ready(self):
        post_migrate.connect(edc_configure_callback, sender=self)
