# __init__ file
import unittest


def get_tests():

    from .test_mppcommands import test_mppcommands
    from .test_mpputils import test_mpputils

    mppcommands = unittest.TestLoader().loadTestsFromTestCase(test_mppcommands)
    mpputils = unittest.TestLoader().loadTestsFromTestCase(test_mpputils)

    return unittest.TestSuite([mppcommands, mpputils])
