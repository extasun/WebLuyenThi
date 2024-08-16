from django.apps import AppConfig

class DanhGiaTuDuyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'DanhGiaTuDuy'

    def ready(self):
        import DanhGiaTuDuy.templatetags.custom_filters
