from dataclasses import dataclass
from typing import Optional, Iterable

from lazy import lazy


@dataclass
class UnittestConfig:
    #todo log level for capturing handler
    xml_report_path: Optional[str] = "./test_report.xml"
    html_report_path: Optional[str] = "./test_report.html"

    @property
    def enabled(self) -> bool:
        return self.xml_report_path is not None

    @enabled.setter
    def enabled(self, val: bool):
        assert not val, "Only config.enabled = False is allowed! Otherwise use config.(xml|html)_report_path"
        self.xml_report_path = None
        self.html_report_path = None

    @property
    def xml_report_enabled(self) -> bool:
        return self.xml_report_path is not None

    @xml_report_enabled.setter
    def xml_report_enabled(self, val: bool):
        assert not val, "Only config.xml_report_enabled = False is allowed! Otherwise use config.xml_report_path"
        self.xml_report_path = None


    @property
    def html_report_enabled(self) -> bool:
        return self.html_report_path is not None


    @html_report_enabled.setter
    def html_report_enabled(self, val: bool):
        assert not val, "Only config.html_report_enabled = False is allowed! Otherwise use config.html_report_path"
        self.html_report_path = None



@dataclass
class CoverageConfig:
    binary_report_path: Optional[str] = "./.coverage"
    xml_report_path: Optional[str] = "./coverage.xml"
    html_report_dir: Optional[str] = "./coverage"
    #todo print report to stdout/err/...
    branch: Optional[bool] = None
    omit: Optional[str | Iterable[str]] = None
    include: Optional[str | Iterable[str]] = None
    #todo omit/include per report?
    #todo source/source_pkgs args to Coverage?

    @property
    def enabled(self) -> bool:
        return self.binary_report_path is not None

    @enabled.setter
    def enabled(self, val):
        assert not val, "Only config.enabled = False is allowed! Otherwise use config.(binary|xml|html)_report_(path|dir)"
        self.binary_report_path = None
        self.xml_report_path = None
        self.html_report_dir = None

    @property
    def binary_report_enabled(self) -> bool:
        return self.xml_report_path is not None

    @binary_report_enabled.setter
    def binary_report_enabled(self, val):
        assert not val, "Only config.binary_report_enabled = False is allowed! Otherwise use config.binary_report_path"
        self.binary_report_path = None

    @property
    def xml_report_enabled(self) -> bool:
        return self.xml_report_path is not None

    @xml_report_enabled.setter
    def xml_report_enabled(self, val):
        assert not val, "Only config.xml_report_enabled = False is allowed! Otherwise use config.xml_report_path"
        self.binary_report_path = None

    @property
    def html_report_enabled(self) -> bool:
        return self.html_report_dir is not None

    @html_report_enabled.setter
    def html_report_enabled(self, val):
        assert not val, "Only config.html_report_enabled = False is allowed! Otherwise use config.html_report_dir"
        self.html_report_dir = None


@dataclass
class TestConfig:
    @lazy
    def coverage(self) -> CoverageConfig:
        return CoverageConfig()

    @lazy
    def unittest(self) -> UnittestConfig:
        return UnittestConfig()

test_config = TestConfig()