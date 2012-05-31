import os
import re
import shutil
import unittest
import utils
import django_chuck.template.base
from django_chuck.exceptions import TemplateError


class UtilsTest(unittest.TestCase):
    def setUp(self):
        self.test_file = os.path.join("test", "project_dir", "test_file")

        if os.path.isfile(self.test_file):
            os.unlink(self.test_file)

    def test_get_files(self):
        files = utils.get_files(os.curdir)
        self.assertTrue(len(files) > 0)

        for file in files:
            self.assertTrue(os.path.isfile(file))


    def test_write_to_file(self):
        test_data = "some wicked cool stuff"
        utils.write_to_file(self.test_file, test_data)

        with open(self.test_file, "r") as f:
            self.assertEqual(f.read(), test_data)


    def test_append_to_file(self):
        test_data = "some wicked cool stuff"
        test_data2 = "even more test data"

        utils.write_to_file(self.test_file, test_data)
        utils.append_to_file(self.test_file, test_data2)

        with open(self.test_file, "r") as f:
            self.assertEqual(f.read(), test_data + test_data2)


    def test_find_chuck_module_path(self):
        self.assertTrue(os.path.exists(utils.find_chuck_module_path()))


    def test_find_chuck_command_path(self):
        self.assertTrue(os.path.exists(utils.find_chuck_command_path()))


    def test_find_commands(self):
        self.assertTrue(len(utils.find_commands()) > 0)


    def test_autoload_commands(self):
        import argparse
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()
        cfg = {}
        cmds = utils.find_commands()

        self.assertTrue(utils.autoload_commands(subparsers, cfg, cmds))


    def test_get_template_engine(self):
        obj = utils.get_template_engine("test", "test/project_dir")
        self.assertTrue(issubclass(obj.__class__, django_chuck.template.base.BaseEngine))


    def test_compile_template_with_extension(self):
        shutil.copy("test/templates/base.html", "test/project_dir/base.html")
        placeholder = {"WHO": "Balle"}

        result = utils.compile_template("test/templates/site.html", "test/project_dir/site.html", placeholder, "test", "test/project_dir")
        self.assertTrue(result)
        self.assertFalse(os.path.isfile("test/project_dir/site.html"))

        with open("test/project_dir/base.html", "r") as f:
            content = f.read()
            self.assertIn("<html>", content)
            self.assertIn("Hello Balle", content)


    def test_compile_template_without_extension(self):
        placeholder = {"WHO": "Balle"}

        result = utils.compile_template("test/templates/placeholder.html", "test/project_dir/placeholder.html", placeholder, "test", "test/project_dir")
        self.assertTrue(os.path.isfile("test/project_dir/placeholder.html"))

        with open("test/project_dir/placeholder.html", "r") as f:
            content = f.read()
            self.assertIn("Hello Balle", content)


if __name__ == '__main__':
    unittest.main()
