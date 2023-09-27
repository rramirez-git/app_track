from zend_django.views import GenericAppRootView


class AlertasView(GenericAppRootView):
    html_template = "zend_django/idx_empty.html"
    titulo = "Alertas"
    titulo_descripcion = ""
    toolbar = None
    app = 'alerta'
