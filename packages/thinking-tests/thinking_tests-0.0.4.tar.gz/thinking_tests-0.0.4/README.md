# thinking-tests

[![CI](https://github.com/FilipMalczak/thinking-tests/actions/workflows/ci.yml/badge.svg)](https://github.com/FilipMalczak/thinking-tests/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/thinking-tests.svg)](https://badge.fury.io/py/thinking-tests)

> Part of [thinking](https://github.com/search?q=owner%3AFilipMalczak+thinking&type=repositories) family.

Declarative API over unittest with customizable auto-discovery and test lifecycle.

> Requires python 3.12. Is mostly typed.

What started as fluent, decorator-based API over `unittest`, grew into a facade that uses `unittest` as testing
backend, while providing bunch of report and integrating coverage too.

Is heavily based on `thinking` framework pieces, so you better get acquainted with [`thinking-runtime`](https://github.com/FilipMalczak/thinking-runtime).

## Usage

### Declaring tests

Put your tests into package lying in repository root. This assumption is important for discovery, but also a good practice.

For this part you need [`decorators` module](./thinking_tests/decorators.py):

```python
from thinking_tests.decorators import case, setup, teardown
```

You declare test cases with decorator:

```python
@case
def my_case():
    assert 1 + 1 == 2 
```

You can tweak setup and teardown with context managers:

```python
def my_setup():
    ...

def my_teardown():
    ...

with setup(my_setup), teardown(my_teardown):
    @case
    def my_case():
        ...
```

## Running tests

Use the `__name__ == "__main__"` idiom and `run_(all|current_(module|package))()` functions (from 
[`thinking_tests.running.start` module](./thinking_tests/running/start.py)).

 - `run_all()` will scan the current root package for test cases and run them all
   - if you call that function from `pkg.subpkg.module`, it will scan every module (at any depth) in `pkg` package
 - `run_current_package()` will do similar thing, but will run all the tests in the same package (and lower) as from
  where you call it
   - e.g. if you have tests in `pkg.sub.sub1.mod` and `pkg.sub.sub2.mod` and call it from `pkg.sub.run`, it will pick up
     both these modules, but not cases defined in `pkg.another.mod`
 - `run_current_module()` will only run cases defined in the module where it is called

See [`test_fixture`](./test_fixture) for an example usage - `x` and `y` modules will use `if __name__=="__main__": run_current_module()`,
while `run_all` will have `if __name__=="__main__": run_all()`. That way you can have `x` and `y` suites, while being
able to run all available tests with `python -m test_fixture.run_all`.

## Reporting

`thinking-tests` come with JUnit XML and HTML reports, Coverage data files, XML reports and HTML reports out of the box.

By default all of them are enabled. Tha way you're set up for CI (which may consume unittest XML report and Coverage 
binary/XML report) as well as local development (where you probably wanna see report in nice, webbrowser-based UI).

> Great kudos to [vjunit](https://github.com/ahsayde/vjunit) and [junit_xml](https://github.com/kyrus/python-junit-xml)
> authors, from which I stole the code before tweaking it for smoother experience.

### Configuration

As mentioned, configuration is based on [`thinking-runtime`](https://github.com/FilipMalczak/thinking-runtime) bootstrapping
mechanism. You can define your own `__test__`/`__tests__`/`__testing__` config file, where you interact with
[`thinking_tests.running.test_config.test_config`](./thinking_tests/running/test_config.py) object.

It has 2 properties:

 - `unittest`
   - exposes 2 `str` properties:
     - `xml_report_path`
     - `html_report_path`
   - both of them are resolved against repository root, if they are not `None` and are not absolute paths
   - if they are `None`, appropriate report is turned off
   - if XML report is disabled, HTML report must be disabled, or it will be an error
   - there are also `(xml|html)_report_enabled` and simply `enabled` properties
     - they have getters
     - they also have setters, but if you pass `True`, it will be an error - use them only to quickly turn off appropriate
        report
     - `(...).enabled = False` will set `None` to both paths
 - `coverage`
   - exposes 3 `str` properties:
     - `binary_report_path` - being the Coverage SQLite data file path
     - `xml_report_path`
     - `html_report_dir` - notice that it points to a directory, not a single file
   - they are also resolved against repo root, same as with `unittest`, and they are interpreted in the same fashion 
     when they are `None`
   - binary report must be enabled for other reports to be enabled, or you'll get an error
   - you'll also find `(binary|xml|html)_report_enabled` and just `enabled` properties that behave similarly as with `unittest`
   - there are also properties passed directly [to Coverage](https://coverage.readthedocs.io/en/7.6.1/api_coverage.html#coverage.Coverage)
     - they are:
       - `branch: Optional[bool]`
       - 'include: Optional[str | Iterable[str]]'
       - 'omit: Optional[str | Iterable[str]]'
     - they must be `None` (default) if binary report is disabled