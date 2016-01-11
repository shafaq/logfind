""" The module is a minified grep command. It searches for search words
in files specified by extensions in ~/.logfind file.

Create a .logfind file in home directory to specify extension of file
in which to search for string. Default is .log files.
On command line run python logfind [-o] <searchword1> <searchword2>.
Regular expressions can be provided enclosed in "". With -o option
or-ing of search terms is done.
"""
#!/usr/bin/env python2
import sys
import os
import re
import argparse


def usage():
    """Return the usage of the script."""
    print "python logfind [-o] [-h] > <Term> <Term>"


def debug_log(log_list):
    """ For printing debugging information."""
    debug_flag = False
    if not debug_flag:
        return
    print "\n ---debug infomation---"
    for message, obj in log_list:
        print "To be printed :", message
        print obj
    print "---debug infomation---\n"


def read_lines(filename):
    """ Read line from the file name provided. Return line one by one.

    filename -- name of the file to read from
    """
    with open(filename) as file_handle:
        for line in file_handle:
            yield line


def match_regex(to_match, regexes):
    """ Return which regexes have been matched """
    logic_array = [False] * len(regexes)
    for index, rex in enumerate(regexes):
        #print(to_match)
        if rex.search(to_match):
            logic_array[index] = True
    #print(logic_array)
    return logic_array


def is_valid_regex(regexp):
    """Check if the provided regular expression is valid."""
    try:
        re.compile(regexp)
        return True
    except re.error:
        print '***Warning, not a valid regex %s' %regexp
        return False


def match_terms(filename, search_terms, logic):
    """ Return true if a file has all or any (according to logic) of
    the search terms.
    """
    search_regexes = [re.compile(p) for p in search_terms if is_valid_regex(p)]
    all_found = [False for x in search_regexes]

    for line in read_lines(filename):
        #print(line)
        current_line_found = match_regex(line, search_regexes)
        #print(temp)
        all_found = [x or y for x, y in list(zip(all_found,
                                                  current_line_found))]
        if logic(all_found):
            return True

    return False


def load_file_regexes(regex_file):
    """ Reads the types of files to be searched from ~/.logfind.

    The file specifies the criteria using regular expressions. If the
    file does not exists or is empty then by default searches for .log
    files.
    """
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


def exit_application(message):
    """Exit application with the message."""
    print message
    usage()
    sys.exit(1)


def process_args(argv):
    """Process command line arguments and return the logic and args."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', dest="logic", action="store_const", const=any,
                        default=all, help="option of or-ing the search terms\
                        instead of default anding")
    parser.add_argument('terms', nargs='+', metavar='TERM',
                         help='search terms to search the files text for')
    args = parser.parse_args(argv)
    return(args.logic, args.terms)


def main(argv):
    """Main driver of the script."""
    search_logic, search_words = process_args(argv)
    home_path = os.path.expanduser("~")
    regex_file_path = os.path.join(home_path, '.logfind')
    regexes = load_file_regexes(regex_file_path)
    output_files = []
    for root, dummy1, files in os.walk(home_path):
        #if f matches any of regexes
        scan_list = [os.path.join(root, filename) for filename in files if
                     any(match_regex(filename, regexes))]
        for file_ in scan_list:
            if match_terms(file_, search_words, search_logic):
                output_files.append(file_)
    return output_files


if __name__ == "__main__":
    FILES = main(sys.argv[1:])
    for result in FILES:
        print result
