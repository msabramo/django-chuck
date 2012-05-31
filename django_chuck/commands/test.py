import os
import unittest
from mock import Mock
from django_chuck.commands.base import BaseCommand


class ComandsTest(unittest.TestCase):
    def setUp(self):
        test_class = type("Test", (BaseCommand,), {})
        self.test_obj = test_class()
        self.test_obj.cfg = {}
        self.test_obj.arg = {}


    def test_arg_or_cfg(self):
        self.test_obj.arg = type("Argh", (object,), {"project_name": "unfug"})
        self.assertEqual(self.test_obj.arg_or_cfg("project_name"), "unfug")

        self.test_obj.arg = {}
        self.test_obj.cfg["project_name"] = "balle was here"
        self.assertEqual(self.test_obj.arg_or_cfg("project_name"), "balle was here")


    def test_insert_default_modules(self):
        self.test_obj.cfg["default_modules"] = ["tick", "trick", "track"]
        self.assertEqual(self.test_obj.insert_default_modules(["donald"]), ["core", "tick", "trick", "track", "donald"])


    def test_get_install_modules(self):
        self.test_obj.args = type("Argh", (object,), {"modules": "simpsons, futurama"})
        self.test_obj.cfg["default_modules"] = ["tick", "trick", "track"]
        self.test_obj.cfg["module_aliases"] = {"simpsons": ["homer", "marge", "bart", "lisa", "maggie"]}
        self.assertEqual(self.test_obj.get_install_modules(), ["core", "tick", "trick", "track", "homer", "marge", "bart", "lisa", "maggie", "futurama"])


    def test_inject_variables_and_functions(self):
        victim_class = type("Victim", (object,), {})

        self.test_obj.cfg["site_dir"] = "site_dir"
        self.test_obj.cfg["project_dir"] = "project_dir"
        self.test_obj.cfg["project_prefix"] = "project_prefix"
        self.test_obj.cfg["project_name"] = "project_name"
        self.test_obj.cfg["project_basedir"] = "project_basedir"

        victim_class = self.test_obj.inject_variables_and_functions(victim_class)

        self.assertEqual(victim_class.virtualenv_dir, "project_prefix-project_name")
        self.assertEqual(victim_class.site_dir, "project_basedir/project_prefix-project_name")
        self.assertEqual(victim_class.project_dir, "project_basedir/project_prefix-project_name/project_name")
        self.assertEqual(victim_class.project_name, "project_name")
        self.assertEqual(victim_class.site_name, "project_prefix-project_name")

        self.assertTrue(getattr(victim_class, "execute_in_project"))
        self.assertTrue(getattr(victim_class, "db_cleanup"))
        self.assertTrue(getattr(victim_class, "load_fixtures"))


if __name__ == '__main__':
    unittest.main()
