from django_chuck.template.base import BaseEngine
from django_chuck.utils import write_to_file
from django_chuck.exceptions import TemplateError
import os
import re

class TemplateEngine(BaseEngine):
    input_file = ""
    base_file = ""
    extension_file = ""
    line_count = ""
    input = ""
    output = ""

    keyword_patterns = {
        "extends": re.compile(r"#!chuck_extends [\'\"]?(.+)[\'\"]?", re.IGNORECASE),
        "extends_if_exists": re.compile(r"#!chuck_extends_if_exists [\'\"]?(.+)[\'\"]?", re.IGNORECASE),
        "renders": re.compile(r"#!chuck_renders ([\w\d\_\-]+)", re.IGNORECASE),
        "appends": re.compile(r"#!chuck_appends ([\w\d\_\-]+)", re.IGNORECASE),
        "prepends": re.compile(r"#!chuck_prepends ([\w\d\_\-]+)", re.IGNORECASE),
    }


    def get_block_content(self, content, block_name="", keyword="renders"):
        """
        Get the content of a chuck block (chuck_renders, chuck_append, chuck_prepend)
        """
        block_content = ""

        match = re.search(r"#!chuck_" + keyword +" " + re.escape(block_name) + "([\r\n\s]+.*?)#!end",
                          content,
                          re.MULTILINE|re.DOTALL)

        if match:
            block_content = match.group(1)

        return block_content


    def update_block_content(self, block_name, keyword="renders"):
        """
        Update output depending on keyword (append, prepend, renders) from template with block named block_name
        """
        old_block_content = self.get_block_content(self.output, block_name)

        if old_block_content:
            new_block_content = self.get_block_content(self.input, block_name, keyword)

            if new_block_content:
                if keyword == "appends":
                    update_content = old_block_content + new_block_content
                elif keyword == "prepends":
                    update_content = new_block_content + old_block_content
                else:
                    update_content = new_block_content

                self.output = re.sub(r"#!chuck_renders " + block_name + re.escape(old_block_content) + "#!end",
                                     r"#!chuck_renders " + block_name + update_content + "#!end",
                                     self.output,
                                     re.IGNORECASE|re.DOTALL|re.MULTILINE)

            else:
                raise TemplateError("Content of block " + block_name + " cannot be found in file " + self.input_file + " line " + str(self.line_count))
        else:
            raise TemplateError("Block " + block_name + " cannot be found in file " + self.base_file)


    @staticmethod
    def found_keyword_in_line(line):
        """
        Parse keyword in line
        """
        keyword = None
        match = re.search(r"#!chuck_(\w+)", line)

        if match:
            keyword = match.group(1)

        return keyword


    def write_file(self, filename):
        """
        Replace placeholder and write file
        """
        for (var, value) in self.placeholder.items():
            self.output = self.output.replace("$" + var, value)

        write_to_file(filename, self.output)


    def get_real_basefile_path(self):
        """
        Return the real basefile path. Resolve project to dir name.
        """
        base_file = os.path.join(self.site_dir, self.extension_file).rstrip("\"").rstrip("\'").lstrip()

        if self.extension_file.startswith("project"):
            # remove first dir (project) from path
            (tmp_path, tmp_file) = os.path.split(self.extension_file)
            tmp_path = tmp_path.lstrip()
            tmp_dirs = tmp_path.split(os.sep)

            # project dir is not the only dir
            if len(tmp_dirs) > 1:
                tmp_path = os.sep.join(tmp_dirs[1:])
            else:
                tmp_path = ""

            # and add the real project dir
            base_file = os.path.join(self.project_dir, tmp_path, tmp_file)

        return base_file


    def extend_file(self):
        """
        command extends
        """
        # Write old base file
        if self.base_file:
            self.write_file(self.base_file)

        # Remove old extension block
        tmp = self.input.splitlines()
        self.input = "\n".join(tmp[self.line_count:])

        # Load base template
        self.base_file = self.get_real_basefile_path()

        try:
            fh = open(self.base_file, "r")
            self.output = fh.read()
            fh.close()
        except IOError:
            raise TemplateError("Cannot find extension file " + self.base_file + " in file " + self.input_file + " line " + str(self.line_count))


    def handle(self, input_file, output_file, placeholder):
        """
        Render template
        """
        self.base_file = None
        self.input = None
        self.line_count = 0
        self.input_file = input_file
        self.base_file = ""
        self.extension_file = None
        self.output = ""
        self.placeholder = placeholder

        with open(self.input_file, "r") as f:
            self.input = f.read()

        lines = self.input.splitlines()
        self.output = self.input

        for line in lines:
            self.line_count += 1

            # Something to do for chuck?
            keyword = self.found_keyword_in_line(line)

            if keyword:
                if self.keyword_patterns.get(keyword):
                    match = self.keyword_patterns[keyword].match(line)

                    # EXTENDS
                    if match and keyword == "extends":
                        self.extension_file = match.group(1).rstrip("\"").rstrip("\'")
                        self.extend_file()

                    # EXTENDS_IF_EXISTS
                    elif match and keyword == "extends_if_exists":
                        self.extension_file = match.group(1).rstrip("\"").rstrip("\'")

                        if os.path.exists(self.get_real_basefile_path()):
                            self.extend_file()
                        else:
                            self.base_file = None

                    # RENDERS
                    elif match and match.group(1) and keyword == "renders" and self.base_file:
                        self.update_block_content(match.group(1), keyword)

                    # PREPENDS, APPENDS
                    elif match and match.group(1) and (keyword == "prepends" or keyword == "appends") and self.base_file:
                        self.update_block_content(match.group(1), keyword)
                else:
                    raise TemplateError("Unknown keyword " + keyword + " found in file " + self.input_file + " line " + str(self.line_count))

        if self.base_file:
            self.write_file(self.base_file)
        else:
            self.write_file(output_file)



    def remove_keywords(self, input_file):
        """
        Remove chuck keywords from file
        """
        output = []

        with open(input_file, "r") as f:
            for line in f.xreadlines():
                keyword = self.found_keyword_in_line(line)

                if keyword:
                    match = self.keyword_patterns[keyword].search(line)

                    if match:
                        line = re.sub(r"#!chuck_" + keyword + " " + re.escape(match.group(1)) + "\s?\r?\n?", "", line, re.IGNORECASE)

                line = re.sub(r"#!end\s*\r?\n?", "", line, re.IGNORECASE)
                output.append(line)

        with open(input_file, "w") as f:
            f.write("".join(output))
