import unittest
from argparse import ArgumentError
from logfind import logfind 
import re
import tempfile

class TestProcessArguments(unittest.TestCase):
    
    def setUp(self):
        pass
        #self.a

    def tearDown(self):
        pass
    

    '''
    Deferring need monkey patching
    def test_process_arg_without_any_option(self):
        
        self.assertRaises(logfind.process_args([]), ArgumentError)

    def test_process_args_with_file_option_no_file(self):

        self.assertRaises(logfind.process_args(['-o']), ArgumentError)
    ''' 

    def test_process_args_without_or(self):
        logic, terms = logfind.process_args(['term1', 'term2'])
        self.assertEqual(logic, all)

    def test_process_args_with_or(self):
        logic, terms = logfind.process_args(['term1', 'term2', '-o'])
        self.assertEqual(logic, any)

    def test_process_args_terms(self):
        logic, terms = logfind.process_args(['term1', 'term2' , '*', 'a*b'])
        self.assertEqual(terms, ['term1', 'term2', '*', 'a*b'])

    def test_process_args_terms_or(self):
        
        self.assertEqual(logfind.process_args(['term1', 'term2' , '*', 'a*b', '-o']), (any, ['term1', 'term2', '*', 'a*b']))


class TestLoadRegex(unittest.TestCase):
    
    def setUp(self):
        
        self.empty_file = tempfile.NamedTemporaryFile('r+b')
        self.valid_file = tempfile.NamedTemporaryFile('r+b')
        self.valid_file.write(b'.*\.py\n')
        self.valid_file.write(b'.*\.(txt|csv)\n.*\.test')
        
        self.valid_file.seek(0)

    def tearDown(self):
        pass

    #def test_load_regex_non_existent_file(self):
     #   self.assertRaises(logfind.load_file_regexes('testfile'), SystemExit)

    def test_load_regex_empty_file(self):
            
        self.assertEqual(logfind.load_file_regexes(self.empty_file.name), [re.compile(r'.*\.log$')])        

    def test_load_regex_valid_file(self):
            
        self.assertEqual(logfind.load_file_regexes(self.valid_file.name), [re.compile(r'.*\.py'), re.compile(r'.*\.(txt|csv)'), re.compile(r'.*\.test')])


class TestMatchRegex(unittest.TestCase):

    def setUp(self):
        file_name_regexes = [r'.*\.test', r'.*\.(txt|csv)']
        self.regexes = [re.compile(r) for r in file_name_regexes]


    def tearDown(self):
        pass
    
    def test_match_regex_true(self):
        self.assertTrue(logfind.matches_regex('abc.txt', self.regexes))  
    
    def test_match_regex_false(self):
        self.assertFalse(logfind.matches_regex('txt.py', self.regexes))    


class TestMatchTerms(unittest.TestCase):
    def setUp(self):
        #self.file1 = open('/home/shafaq/test.txt','r+t')
        #self.file1.write('file write\n')
        #self.file1.write('file a string \n')
        #self.file1.write('file a food \n')
        #self.file1.write('file like \n')
        #self.file1.seek(0)
        pass

    def tearDown(self):
        pass
    def test_match_terms_and_true(self):
        self.assertTrue(logfind.match_terms('/home/shafaq/test.txt', [r'\b.*ood\b', r'like'] ,all))
    def test_match_terms_and_false(self):
        self.assertFalse(logfind.match_terms('/home/shafaq/test.txt', [r'\b.*ood\b', r'like', r'rude'] ,all))        

if __name__ == '__main__' :

    unittest.main()

    #print(dir())
    #print(sys.path)



