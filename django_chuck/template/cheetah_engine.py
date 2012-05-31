from django_chuck.template.base import BaseEngine
from django_chuck.utils import write_to_file
from Cheetah.Template import Template

class TemplateEngine(BaseEngine):
    def handle(self, input_file, output_file, placeholder):
        with open(input_file, "rb") as f:
            write_to_file(output_file, f.read())

        template = str(Template(output_file, searchList=[placeholder]))

        with open(input_file, "w") as f:
            f.write(template)



