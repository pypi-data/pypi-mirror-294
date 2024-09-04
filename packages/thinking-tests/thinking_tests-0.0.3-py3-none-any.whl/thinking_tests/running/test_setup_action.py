from os.path import abspath, join, dirname

from coverage import Coverage
from thinking_modules.main_module import main_module
from thinking_runtime.model import BootstrapAction, ConfigurationRequirement

from thinking_tests.running.test_config import test_config


def _is_abs_path(x: str) -> bool:
    return abspath(x) == x

def _repo_root_dir() -> str:
    root_pkg = main_module.root_package_name.module_descriptor
    root_init_file = root_pkg.file_path
    root_pkg_dir = dirname((root_init_file))
    repo = join(root_pkg_dir, "..")
    return abspath(repo)

def _against_repo_root(p: str) -> str:
    if not _is_abs_path(p):
        return abspath(join(_repo_root_dir(), p))
    return p

COVERAGE = None

class SetupTests(BootstrapAction):
    def requirements(self) -> list[ConfigurationRequirement]:
        return [ ConfigurationRequirement(["__test__", "__tests__", "__testing__"]) ]

    def perform(self) -> None:
        global COVERAGE
        if test_config.unittest.xml_report_enabled:
            test_config.unittest.xml_report_path = _against_repo_root(test_config.unittest.xml_report_path)
        else:
            assert not test_config.unittest.xml_report_enabled

        if test_config.unittest.html_report_enabled:
            test_config.unittest.html_report_path = _against_repo_root(test_config.unittest.html_report_path)

        if test_config.coverage.binary_report_enabled:
            test_config.coverage.binary_report_path = _against_repo_root(test_config.coverage.binary_report_path)
            COVERAGE = Coverage(
                test_config.coverage.binary_report_path,
                check_preimported=True,
                include=test_config.coverage.include,
                omit=test_config.coverage.omit,
                branch=test_config.coverage.branch
            )
            COVERAGE.start()
        else:
            assert test_config.coverage.branch is None
            assert test_config.coverage.omit is None
            assert test_config.coverage.include is None
            assert not test_config.coverage.xml_report_enabled
            assert not test_config.coverage.html_report_enabled

        if test_config.coverage.xml_report_enabled:
            test_config.coverage.xml_report_path = _against_repo_root(test_config.coverage.xml_report_path)
        if test_config.coverage.html_report_enabled:
            test_config.coverage.html_report_dir = _against_repo_root(test_config.coverage.html_report_dir)