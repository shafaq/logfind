# logfind
LogFind is a miniature "grep" command. It searches for files with extensions provided in a config file that have the search words that have the search words that user provides it. 

LogFind is described in http://projectsthehardway.com/2015/06/16/project-1-logfind-2/

Create a config file .logfind in home direcory. In Linux it is ~/.logfind. Give the extensions of files that you want to search for the keywords. If you do not provide any then .log files are searched by default.

For running the program type python logfind.py <keyword>...
keyword can be a regular expression enclosed in quotes. ('' or "")

