Write your own template engine
==============================

Like all other parts of Django Chuck even the template engine can be customized. For the first version we tried to use `Cheetah <http://cheetahtemplate.org/>`_ and `Mako <http://www.makotemplates.org>`_, but both didnt really fit our needs so we implemented our own template engine. Nevertheless both old engines still exist and you can use them to write your Chuck templates. Of course you will have to rewrite all modules if you switch the template engine. They cannot be mixed.

Using either Cheetah or Mako is as easy as setting a config value.

.. code-block:: bash

  template_engine="django_chuck.template.mako_engine"

You dont like all three and want to implement another one or even your own? No problem! Just create a module in ``django_chuck.template``, let it inherit from ``BaseEngine`` and implement the ``handle`` function that gets called with the name of each file in each module, it's output filename in the site directory and a placeholder dictionary containing all variables and their values.

All the handle function now has to do is read the ``input_file``, render the template stuff in it by using the ``placeholder`` dictionary and write it to the ``output_file``.

Here's the implementation of the Cheetah engine as an example:

.. code-block:: python

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
