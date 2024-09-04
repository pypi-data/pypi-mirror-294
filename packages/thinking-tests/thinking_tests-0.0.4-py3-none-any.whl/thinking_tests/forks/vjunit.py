"""
This is forked* from https://github.com/ahsayde/vjunit, specifically from commit 93f86cce5456a691e24c1558add48962342f8f3d.
I needed to tweak the template, as well as the code a bit to match what I wanted to achieve with thinking-tests.

Major changes are
- replacement of el.getchildren() with list(el)
- removal of container div, so that report fits the whole screen
- tweak of stdout/stderr/logs handling
- alignment of counting cases to account for subsuites

* not really forked - you won't find it in GIT history, because at the same time I needed to tweak junit_xml, which got
the same treatment.
"""

import os
import xml.etree.ElementTree as ET

import jinja2


class VJunit(object):
    def __init__(self, *args, **kwargs):
        self._envrionment = jinja2.Environment()
        self._load_template()

    def _load_file(self, path):
        with open(path, "r") as f:
            content = f.read()
        return content

    def _load_template(self):
        path = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(path, "template.html")
        self._template = self._load_file(template_path)

    def parse(self, path):
        return self.parse_content(self._load_file(path))

    def parse_content(self, content):
        result = list()
        tree = ET.fromstring(content)
        def handle_suite(testsuite):
            _testsuite = dict(summary={}, testcases=[])
            _testsuite["summary"] = testsuite.attrib
            for testcase in testsuite.iter(tag="testcase"):
                _testcase = testcase.attrib
                _testcase["status"] = "success"
                children = list(testcase)
                if children:
                    stdout = []
                    for child in children:
                        if child.tag == "system-out":
                            stdout.append(child.text)
                        elif child.tag == "system-err":
                            _testcase["stderr"] = child.text
                        elif child.tag == "properties":
                            for props_child in child:
                                assert props_child.tag == "property"
                                if props_child.attrib.get("name") == "log":
                                    _testcase["log"] = props_child.text
                        elif child.tag in ("error", "failure", "skipped"):
                            _testcase["status"] = child.tag
                            _testcase["text"] = child.text
                            _testcase["type"] = child.attrib.get("type")
                            _testcase["message"] = child.attrib.get("message")

                    else:
                        _testcase["stdout"] = "\n".join(stdout)
                    # _testcase["logs"] = child.attrib.get("logs")
                else:
                    _testcase["status"] = "success"

                _testsuite["testcases"].append(_testcase)

            tests = testsuite.attrib.get("tests", 0)
            errors = testsuite.attrib.get("errors", 0)
            failures = testsuite.attrib.get("failures", 0)
            skipped = testsuite.attrib.get("skip", 0) or testsuite.attrib.get(
                "skipped", 0
            )

            if int(errors):
                _testsuite["summary"]["status"] = "error"
            elif int(failures):
                _testsuite["summary"]["status"] = "failure"
            elif int(tests) == int(skipped):
                _testsuite["summary"]["status"] = "skipped"
            else:
                _testsuite["summary"]["status"] = "success"

            result.append(_testsuite)
        for testsuite in tree.iter(tag="testsuite"):
            handle_suite(testsuite)
        return result

    def generate_html(self, result, embed=False):
        template = self._envrionment.from_string(self._template)
        html = template.render(embed=embed, testsuites=result)
        return html

    def _export_html(self, html, path="."):
        with open(path, "w") as f:
            f.write(html)
        print("File saved to {}".format(path))

    def convert(self, path, dest):
        testsuites = self.parse(path)
        html = self.generate_html(testsuites)
        self._export_html(html, dest)