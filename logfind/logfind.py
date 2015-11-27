import sys
import os 
import os.path
import glob
import re
import getopt
import os.path

DEBUG = False



def usage():
    ''' usage of this module'''
    pass

def debug_log(log_list):
    ''' logs debugging information to console or file'''
    if DEBUG:
        print("\n ---debug infomation---")
        for item in log_list:
            print("To be printed :", item[0])
            print(item[1])
        print("---debug infomation---\n")




def and_searching(file_in, search_terms):
    
    #print('In and_searching(), file :', file_in)
    debug_log([('search terms', search_terms),])
    fd = open(file_in)
    text = fd.read()
    #print(text)
    for w in search_terms:  
        #print('looking for search term', w)
        if re.search(w,text) is None:
                fd.close()
                return None
    else: 
        #print('All words found in ', file_in)
        fd.close()   
        return file_in

def or_searching(file_in, search_terms):
    #print('In or_searching()')
    fd = open(file_in)
    text = fd.read()

    for w in search_terms:  
        if re.search(w, text) is not None:
            fd.close()
            return file_in
    else: 
        fd.close()   
        return None

        
def load_file_regexes():
    ''' Reads the types of files to be searched from ~/.logfind.txt. The file specifies the criteria using regular expressions. 
    If the file is empty then by default searches for .log files '''
    type_regs = []
    default_reg = r'.*\.log$'

    file_name = os.path.join(os.path.expanduser("~") , '.logfind')

    with open(file_name) as fo:
        for line in fo:
            
            line = line.strip(' \t\n\r')
            if line != '':
                type_regs.append(line)

    if len(type_regs) == 0:
        type_regs.append(default_reg)

    #debug_log([("regular expressions", type_regs)])
    
    regexes = [re.compile(p) for p in type_regs]

    #print (regexes) 
    return regexes 
        

def main(argv):
    ''' Driver of this module when running as primary module'''


    #1 Read command line arguments
    AND_SEARCH = True
    OR_SEARCH = False
    search_terms = []
    output_files = []
    def process_args():
        nonlocal AND_SEARCH
        nonlocal OR_SEARCH   
        nonlocal search_terms
        #print(argv)
        try:
            opts, args = getopt.getopt(argv, 'o', ['or',])
            #print('opts =', opts)
            #print('args =', args)
        except getopt.GetoptError:
            usage() 
            sys.exit(2)
        
        if len(opts) == 0:
            #print('length of option is zero')
            AND_SEARCH = True
        else:    
            opt, arg = opts[0]
            if opt in ('-o', '--or'):
                AND_SEARCH = False
                OR_SEARCH = True
         
        search_terms =  args    
        
        #debug_log([("AND_SEARCH-inside process_args", [AND_SEARCH])])
        #debug_log([("OR_SEARCH-inside process args", [OR_SEARCH])])
    
    
    process_args()     
    
    #debug_log([("AND_SEARCH", [AND_SEARCH])])
    #debug_log([("OR_SEARCH", [OR_SEARCH])])
            
    #2 Load files and populate regexes
    
    regexes = load_file_regexes() 
    debug_log([('regex', regexes),])

    debug_log([('search terms', search_terms),])
    
    #3 Search in files
    

    for root, dirs, files in os.walk('/home/shafaq/python'):
        scan_list = []
        for f in files: 
            for r in regexes:
                if r.match(f):
                    scan_list.append(os.path.join(root, f))
                    break
        if AND_SEARCH:
            output_files.extend([and_searching(x, search_terms) for x in  scan_list if and_searching(x, search_terms)])

        else:
            output_files.extend([or_searching(x, search_terms) for x in  scan_list if or_searching(x, search_terms)])



    #4 List output files. 
    debug_log([('output files', output_files),])

    for i in output_files:
        print(i)
    #return output_files
    
if __name__ == "__main__":
   
   main(sys.argv[1:])

     
    
