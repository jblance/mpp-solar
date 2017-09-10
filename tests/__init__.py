import os
# import unittest

PATTERN = "test_*.py"


def load_tests(loader, tests, pattern):
    # Add core tests (from this package)
    core_tests_dir = os.path.dirname(os.path.abspath(__file__))
    tests.addTests(loader.discover(core_tests_dir, PATTERN))
    print tests

    return tests
