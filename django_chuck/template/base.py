from django_chuck.utils import find_chuck_module_path

class BaseEngine(object):
    module_basedir = find_chuck_module_path()
    site_dir = ""
    project_dir = ""

    def __init__(self, site_dir, project_dir):
        self.site_dir = site_dir
        self.project_dir = project_dir


    def handle(self, input_file, output_file, placeholder):
        raise NotImplementedError()
