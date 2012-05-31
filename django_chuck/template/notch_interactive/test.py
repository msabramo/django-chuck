import os
import re
import shutil
import unittest
from engine import TemplateEngine
from django_chuck.exceptions import TemplateError


class TemplateEngineTest(unittest.TestCase):
    def setUp(self):
        self.engine = TemplateEngine(os.getcwd() + "/test", os.getcwd() + "/test/project_dir")


    def test_get_block_content(self):
        with open("test/templates/common.py", "r") as f:
            content = f.read()
            block_content = self.engine.get_block_content(content, "MIDDLEWARE_CLASSES")
            self.assertNotIn("#!chuck", block_content)

            block_content = self.engine.get_block_content(content, "SETTINGS")
            self.assertEqual(block_content, " ")

    #
    # TEST BASIC KEYWORDS
    #

    def test_renders(self):
        shutil.copy("test/templates/base.html", "test/project_dir/base.html")
        self.engine.handle("test/templates/replace.html", "test/project_dir/replace.html", {})

        with open("test/project_dir/base.html") as f:
            content = f.read()
            self.assertIn("<html>", content)
            self.assertIn("#!chuck_renders content", content)


    def test_render_multiple_blocks(self):
        shutil.copy("test/templates/base.html", "test/project_dir/base.html")
        self.engine.handle("test/templates/replace_three_blocks.html", "test/project_dir/replace_three_blocks.html", {})

        with open("test/project_dir/base.html") as f:
            content = f.read()
            self.assertIn("<html>", content)
            self.assertIn("#!chuck_renders content", content)
            self.assertIn("lets start", content)
            self.assertIn("MOOOOOH", content)
            self.assertIn("go home", content)


    def test_appends(self):
        shutil.copy("test/templates/base.html", "test/project_dir/base.html")
        self.engine.handle("test/templates/append.html", "test/project_dir/append.html", {})

        with open("test/project_dir/base.html") as f:
            content = f.read()
            self.assertTrue(re.search(r"One must have chaos in oneself to give birth to a dancing star.+The big MOOOOOH has pwned you", content, re.MULTILINE|re.DOTALL), content)


    def test_prepends(self):
        shutil.copy("test/templates/base.html", "test/project_dir/base.html")
        self.engine.handle("test/templates/prepend.html", "test/project_dir/prepend.html", {})

        with open("test/project_dir/base.html") as f:
            content = f.read()
            self.assertTrue(re.search(r"The big MOOOOOH has pwned you.+One must have chaos in oneself to give birth to a dancing star", content, re.MULTILINE|re.DOTALL), content)


    def test_extends_if_exists(self):
        shutil.copy("test/templates/base.html", "test/project_dir/base.html")
        self.engine.handle("test/templates/extends_if_exists.html", "test/project_dir/extends_if_exists.html", {})

        with open("test/project_dir/base.html") as f:
            content = f.read()
            self.assertTrue(re.search(r"One must have chaos in oneself to give birth to a dancing star.+The big MOOOOOH has pwned you", content, re.MULTILINE|re.DOTALL), content)


    def test_placeholder(self):
        shutil.copy("test/templates/base.html", "test/project_dir/base.html")
        self.engine.handle("test/templates/placeholder.html", "test/project_dir/placeholder.html", {"SOMETHING": "cool things"})

        with open("test/project_dir/base.html") as f:
            content = f.read()
            self.assertIn("cool things", content)


    def test_placeholder_without_extend(self):
        shutil.copy("test/templates/placeholder_without_extend.html", "test/project_dir/placeholder_without_extend.html")
        self.engine.handle("test/templates/placeholder_without_extend.html", "test/project_dir/placeholder_without_extend.html", {"SOMETHING": "cool things"})

        with open("test/project_dir/placeholder_without_extend.html") as f:
            content = f.read()
            self.assertIn("cool things", content)


    def test_remove_keywords(self):
        shutil.copy("test/templates/remove_keywords.html", "test/project_dir/remove_keywords.html")
        self.engine.handle("test/project_dir/remove_keywords.html", "test/project_dir/remove_keywords.html", {})
        self.engine.remove_keywords("test/project_dir/remove_keywords.html")

        with open("test/project_dir/remove_keywords.html") as f:
            content = f.read()
            self.assertFalse("#!chuck" in content, content)
            self.assertTrue("chaos" in content, content)



    def test_complex_example(self):
        shutil.copy("test/templates/common.py", "test/project_dir/common.py")

        self.engine.handle("test/templates/extends_common.py", "test/project_dir/extends_common.py", {"PROJECT_NAME": "test"})
        self.engine.remove_keywords("test/project_dir/common.py")

        with open("test/project_dir/common.py") as f:
            content = f.read()
            self.assertIn("# -*- coding", content.splitlines()[0])  # right order
            self.assertIn("CMS_TEMPLATES", content)                 # appends
            self.assertIn("ROOT_URLCONF = 'test.urls'", content)    # placeholder
            self.assertFalse("#!chuck" in content, content)         # removed keywords


    #
    # ADVANCED FEATURES
    #

    def test_extends_two_files(self):
        shutil.copy("test/templates/base.html", "test/project_dir/base.html")
        shutil.copy("test/templates/base2.html", "test/project_dir/base2.html")

        self.engine.handle("test/templates/extend_two_files.html", "test/project_dir/extend_two_files.html", {})

        with open("test/project_dir/base.html") as f:
            content = f.read()
            self.assertIn("big MOOOOOH", content)
            self.assertIn("#!chuck_renders content", content)

        with open("test/project_dir/base2.html") as f:
            content = f.read()
            self.assertIn("Balle was here", content)
            self.assertIn("#!chuck_renders content", content)



    #
    # ERRORS
    #
    def test_keyword_not_found(self):
        with self.assertRaises(TemplateError):
            self.engine.handle("test/templates/broken_keyword.html", "test/project_dir/broken_keyword.html", {})


    def test_syntax_error(self):
        with self.assertRaises(TemplateError):
            self.engine.handle("test/templates/broken_syntax.html", "test/project_dir/broken_syntax.html", {})


    def test_non_existent_block_name(self):
        with self.assertRaises(TemplateError):
            self.engine.handle("test/templates/broken_block_name.html", "test/project_dir/brocken_block_name.html", {})


    def test_non_existent_base_file(self):
        with self.assertRaises(TemplateError):
            self.engine.handle("test/templates/broken_base_file.html", "test/project_dir/broken_base_file.html", {})

    def test_non_existent_base_file_with_if_exists(self):
        self.engine.handle("test/templates/broken_base_file_with_if_exists.html", "test/project_dir/broken_base_file_with_if_exists.html", {})


if __name__ == '__main__':
    unittest.main()
