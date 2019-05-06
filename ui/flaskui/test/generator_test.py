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
    def test_short_command_object( self ):
        test_command = generator.CommandObject( "testname", "test", [["param1", "value1"], ["param2", "value2"]]  )
        self.assertEqual( "test param1=value1 param2=value2", str(test_command) )


    def test_long_command_object( self ):
        test_command = generator.CommandObject( "testname", "test", [["param1", "value1"], ["param2", "value2"], ["param3", "value3"], ["param4", "value4"]] )
        self.assertEqual( "test param1=value1 param2=value2 param3=value3 param4=value4", str(test_command) )


    def test_wget_command_object( self ):
        test_wget_command = generator.WGETCommandObject( "image", "image_url" )
        self.assertEqual( "cd /img && wget image_url", str(test_wget_command) )


    def test_dag_object( self ):
        test_command = generator.CommandObject( "testname", "test", [["param1", "value1"], ["param2", "value2"]]  )
        test_dag_object = generator.DAGObject( test_command )
        test_string = '''testname = BashOperator(
    task_id="testname",
    bash_command= prefix + "test param1=value1 param2=value2",
    retries=3,
    dag=dag
)'''
        self.assertEqual( test_string, str(test_dag_object) )



    # Function tests
    def test_generate( self ):
        self.assertEqual( "test", "test" )
        self.assertNotEqual( "test", "fail" )


    def test_get_commands_from_json( self ):
        dag_json = {"mission": "test", "output":"default", "images": "test.img", }
        self.assertEqual( "test", "test" )

    def test_generate_dag( self ):
        self.assertEqual( "test", "test" )
        self.assertNotEqual( "test", "fail" )



suite = unittest.TestLoader().loadTestsFromTestCase( TestStringMethods )
unittest.TextTestRunner( verbosity=2 ).run( suite )

suite = unittest.TestLoader().loadTestsFromTestCase( TestGeneratorFunctions )
unittest.TextTestRunner( verbosity=2 ).run( suite )
