import os
import imp

class BaseModule(object):

    def __init__(self, module_name, module_dir):
        self.name = module_name
        self.dir = module_dir

        cfg_file = os.path.join(self.dir, "chuck_module.py")
        if os.access(cfg_file, os.R_OK):
            self.cfg = imp.load_source(self.name.replace("-", "_"), cfg_file)
        else:
            self.cfg = None

    def get_priority(self):
        if self.cfg and hasattr(self.cfg, 'priority'):
            return self.cfg.priority
        return 100000
    priority = property(get_priority)

    def get_dependencies(self):
        if self.cfg and hasattr(self.cfg, 'depends'):
            return self.cfg.depends
        return None
    dependencies = property(get_dependencies)

    def get_incompatibles(self):
        if self.cfg and hasattr(self.cfg, 'incompatible_with'):
            return self.cfg.incompatible_with
        return None
    incompatibles = property(get_incompatibles)

    def get_description(self):
        if self.cfg and hasattr(self.cfg, 'description'):
            return self.cfg.description
        return None
    description = property(get_description)

    def get_post_build(self):
        if self.cfg and hasattr(self.cfg, 'post_build'):
            return self.cfg.post_build
        return None
    post_build = property(get_post_build)

    def get_post_setup(self):
        if self.cfg and hasattr(self.cfg, 'post_setup'):
            return self.cfg.post_build
        return None
    post_setup = property(get_post_setup)

