from django_chuck.template.base import BaseEngine
from django_chuck.utils import write_to_file
from django_chuck.exceptions import TemplateError

from mako.template import Template
from mako.lookup import TemplateLookup
from mako.exceptions import SyntaxException, TemplateLookupException


class TemplateEngine(BaseEngine):
    def handle(self, input_file, output_file, placeholder):
        lookup = TemplateLookup(directories=[self.module_basedir])

        try:
            template = Template(filename=input_file, lookup=lookup).render(**placeholder)
        except TemplateLookupException, e:
            raise TemplateError("Lookup error: " + str(e))
        except SyntaxException, e:
            raise TemplateError("Syntax error: " + str(e))

        write_to_file(output_file, template)
