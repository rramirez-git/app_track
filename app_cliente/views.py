from zend_django.views import GenericAppRootView


class ClientesView(GenericAppRootView):
    html_template = "zend_django/idx_empty.html"
    titulo = "Clientes"
    titulo_descripcion = ""
    toolbar = None
    app = 'cliente'
