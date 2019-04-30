import sys
sys.path.insert( 0, ".." )

import unittest
import rest_api



class TestStringMethods( unittest.TestCase ):

    # Baseline test
    def test_upper( self ):
        self.assertEqual( "foo".upper(), "FOO" )


class TestGeneratorFunctions( unittest.TestCase ):

    # Request test
    def test_request( self ):
        self.assertEqual( "test", "test" )


if( __name__ == "__main__" ):
    unittest.main()
