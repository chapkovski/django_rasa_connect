
from django.views.generic import TemplateView as OldTemplateView


class TemplateMixin(OldTemplateView):
    def get_template_names(self):
        if self.template_name: return super().get_template_names()
        return [f'med/{self.__class__.__name__}.html']





