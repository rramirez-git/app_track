from zend_django.views import GenericAppRootView


class NotasView(GenericAppRootView):
    html_template = "zend_django/idx_empty.html"
    titulo = "Notas"
    titulo_descripcion = ""
    toolbar = None
    app = 'nota'
