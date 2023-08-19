from .views import GenericAppRootView


class ConfiguracionView(GenericAppRootView):
    html_template = "zend_django/idx_empty.html"
    titulo = "Configuración"
    app = 'configuracion'


class AdministracionView(GenericAppRootView):
    html_template = "zend_django/idx_empty.html"
    titulo = "Administración"
    app = 'administrar'
