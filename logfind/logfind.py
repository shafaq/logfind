
import sys
import os 
import re
import argparse


DEBUG = True

def usage():
    pass

def debug_log(log_list):
    if not DEBUG:
        return

    print("\n ---debug infomation---")

    for message, obj in log_list:
        print("To be printed :", message)
        print(obj)

    print("---debug infomation---\n")


def read_lines(filename):
    
    with open(filename) as f:
        for line in f:
            yield line



def match_terms(filename, search_terms, logic):
    ''' Returns true if a file has all or any (according to logic) of the search terms'''

    logic_array = [False for x in search_terms]
    for line in read_lines(filename):
        for index,term in enumerate(search_terms):
            if re.search(term ,line): # refactor to use match_regex
                logic_array[index] =  True
                if logic(logic_array):
                    return True                   
    else:
        return False
        
    

        
def load_file_regexes(regex_file):
    ''' Reads the types of files to be searched from ~/.logfind. The file specifies the criteria using regular expressions. 
    If the file does not exists or is empty then by default searches for .log files '''
    
    type_regs = []
    
    default_reg = r'.*\.log$'

    try:

        for line in read_lines(regex_file):
            line = line.strip(' \t\n\r')
            if line != '':
                type_regs.append(line) 
        
    except OSError:
        msg = '***Error: .logfind file does not exist.'  
        exit_application(msg)              
    
    if len(type_regs) == 0:
        type_regs.append(default_reg) 
    
    debug_log([("regular expressions", type_regs)])
    regexes = [re.compile(p) for p in type_regs if is_valid_regex(p)]
    
    if len(regexes) == 0:
        exit_application('No valid regex found in file.')

    return regexes 

def is_valid_regex(regexp):

    try:
        re.compile(regexp)
        return True
    except re.error:
        print('***Warning, not a valid regex %s' %regexp)
        return False
            

def exit_application(message):
    print(message)
    usage()
    sys.exit()              
    
      
def matches_regex(file_name, regexes):
    '''use any built in '''
    ''' returns true if file_name matches any of the regex provided'''
    for r in regexes:
        if r.match(file_name):
            return True
    return False        
 

def process_args(argv):
    
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-o', dest="logic", action="store_const", const=any, default= all, 
                        help="option of or-ing the search terms instead of default anding")
    parser.add_argument('terms', nargs='+', metavar='TERM',  
                           help='search terms to search the files text for')
     
    args = parser.parse_args(argv)
        
    return(args.logic, args.terms)



def main(argv):
    
    search_logic, search_terms = process_args(argv)     
    
    HOME = os.path.expanduser("~")
    REGEX_FILE_PATH = os.path.join(HOME, '.logfind')

    regexes = load_file_regexes(REGEX_FILE_PATH) 
    output_files = []
    
    for root, dirs, files in os.walk(HOME):
        scan_list = [os.path.join(root,f) for f in files if matches_regex(f, regexes)]
        for f in scan_list:
            if match_terms(f, search_terms, search_logic):
                output_files.append(f) 

    
    for i in output_files: 
        print(i)
    
    
if __name__ == "__main__":
   
   main(sys.argv[1:])
