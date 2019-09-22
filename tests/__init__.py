# __init__ file
import unittest


def get_tests():

    from .test_mppinverter import test_mppinverter
    from .test_mpputils import test_mpputils

    mppinverter = unittest.TestLoader().loadTestsFromTestCase(test_mppinverter)
    mpputils = unittest.TestLoader().loadTestsFromTestCase(test_mpputils)

    return unittest.TestSuite([mppinverter, mpputils])
