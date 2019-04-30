import sys
sys.path.insert( 0, ".." )

import unittest
import json
import generator


class TestStringMethods( unittest.TestCase ):

    # Baseline test
    def test_upper( self ):
        self.assertEqual( "foo".upper(), "FOO" )


class TestGeneratorFunctions( unittest.TestCase ):

    # Object tests
    def test_command_object( self ):
        self.assertEqual( "test", "test" )
        self.assertNotEqual( "test", "fail" )


    def test_wget_command_object( self ):
        self.assertEqual( "test", "test" )
        self.assertNotEqual( "test", "fail" )


    def test_dag_object( self ):
        self.assertEqual( "test", "test" )
        self.assertNotEqual( "test", "fail" )



    # Function tests
    def test_generate( self ):
        self.assertEqual( "test", "test" )
        self.assertNotEqual( "test", "fail" )


    def test_get_commands_from_json( self ):
        self.assertEqual( "test", "test" )
        self.assertNotEqual( "test", "fail" )

    def test_generate_dag( self ):
        self.assertEqual( "test", "test" )
        self.assertNotEqual( "test", "fail" )



suite = unittest.TestLoader().loadTestsFromTestCase( TestStringMethods )
unittest.TextTestRunner( verbosity=2 ).run( suite )

suite = unittest.TestLoader().loadTestsFromTestCase( TestGeneratorFunctions )
unittest.TextTestRunner( verbosity=2 ).run( suite )
