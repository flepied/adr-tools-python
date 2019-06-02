import os
import fileinput
# To copy files
from shutil import copyfile
from datetime import date

#by default, do not print.
# Most hints on using variables came from this page: https://stackoverflow.com/questions/1977362/how-to-create-module-wide-variables-in-python 
# variable is a list, because lists are mutable.
__adr_verbose = [False]

def get_adr_verbosity():
    return __adr_verbose[0]

def set_adr_verbosity(verbosity):
    adr_print('verbosity set to ' + str(verbosity) )
    if verbosity == True:
        print('Verbose printing is enabled')
        __adr_verbose[0] = True
    else:
        #print('silent...')
        __adr_verbose[0] = False

# adr-config:
# Original bash implementation generates strings with paths to
# bin and template dir (both the same).

# In this python implementation I've changed this to a 
# dictionary. I think this is more future proof and way
# more 'pythonic' and less error prone.

def adr_print(text):
    if(get_adr_verbosity() == True):
        print(text)

def adr_config():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config = {"adr_bin_dir"     : dir_path ,
              "adr_template_dir": dir_path 
    }
    return(config)

# adr-init

# file IO:
# https://docs.python.org/3/tutorial/inputoutput.html

def adr_init(config, localpath, dirname):
    if (str(dirname) != 'doc/adr/'):
        with open('.adr-dir','w') as f:
            f.write(dirname)
# create subdirectories
# https://stackabuse.com/creating-and-deleting-directories-with-python/        
    try:  
        os.makedirs(dirname)
    except OSError:  
        print ("Creation of the directory %s failed" % dirname)
    else:  
        print ("Successfully created the directory %s" % dirname)
        adr_new(config, localpath, 'record-architecture-decisions')
    return(0)

# This function is used to read the .adr-dir file (written in adr_init), to determine the relative path for the 
# adrs. default is /doc/adr/ . 
# In order to find this file in another directory, an optional directory can be passed.
def find_alternate_dir(dir = 'doc/adr/'):
    directory = dir
    try:
        # open local file
        fh = open(os.path.join(dir,'.adr-dir'), 'r')
        # add slash to remain compatible with 'default' /doc/adr/
        directory = fh.read()+'/'
    except FileNotFoundError:
        None
    return directory

def adr_find_index(adr_dir):
    # find all files in a directory
    # https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
    from os import listdir
    from os.path import isfile, join
    
    adr_index = dict()
    # start with index is zero, will be incremented after search
    adr_index['n'] = 0
    adr_index['text'] = '0000'
    adr_index['adr_list'] = list()
    adr_print('adr_find_index; adr directory is '+ adr_dir)
    onlyfiles = [f for f in listdir(adr_dir) if isfile(join(adr_dir, f))]
    # search for highest adr number
    for file in onlyfiles:
        try:
            adr_index['adr_list'].append(file)
            #print(type(file))
            # get number by reading first 4 characters
            number = int(file[:4])
            #print(number)
            # increase index if higher number is found
            if (number > adr_index['n']):
                adr_index['n'] = number
        except: 
            adr_print (file + " is not a valid ADR filename")
            None
    adr_index['n'] += 1

    # Format number to string with 4 characters
    # https://stackoverflow.com/questions/11714859/how-to-display-the-first-few-characters-of-a-string-in-python

    adr_index['text'] = '{0:04d}'.format(adr_index['n'])
    #print(onlyfiles)
    print(adr_index['adr_list'])
    adr_print("new adr_index is " + adr_index['text'])
    return adr_index

# adr-new
def adr_new(config, localpath, title):
    # start with no error; if it changes along the way, we have an error
    _adr_dir()
    result = 'no error'

    # directory for the template
    src= config["adr_template_dir"]+'/template.md'
    
    #check input argument for the ADR title
    try:
        # check if title can be converted to string, and 
        # replace spaces with dashes on the go
        adr_print(title)
        
        if type(title) == list:
            title_checked = "-".join(title).replace(' ','-')
        elif type(title) == str:
            title_checked = (title).replace(' ','-')
    except ValueError:
        result = 'Title was no string'
        print ("adr-new had no valid input for the title")
    
    if (result == 'no error' ):
        # location of adrs
        adr_dir = _adr_dir()
        # find highest index
        adr_index  = adr_find_index(adr_dir)
        # combine data to make destination path
        dst =  os.path.join(adr_dir , adr_index['text'] + '-' + title_checked + '.md')
        adr_print('adr-new; ' + src + ' ' + dst)
        # copy template to destination directory, with correct title
        copyfile(src, dst)
        adr_write_number_and_header(dst, adr_index, title_checked)
        #adr_write_header_title(dst, title_checked)
        #adr_write_date(dst, date)
        #adr_write_status(dst,status)
    return(result)

# Write ADR number in filename and header
def adr_write_number_and_header(dst,adr_index,adr_title=None):
    test=''
    # open file for appending and reading and replacing
    # https://kaijento.github.io/2017/05/28/python-replacing-lines-in-file/
    for line in fileinput.input(dst, inplace=True):
        if fileinput.filelineno() == 1:
            test = line
            # first replace number
            line = '# '+str(adr_index['n'])+'. ' + test.split('.',1)[1]
            # now add title if needed
            if (adr_title != None):
                line = line.split('.',1)[0] + '. ' + adr_title.replace('-',' ').title()
            print(line,end='\n')
        elif fileinput.filelineno() == 3:
            # https://www.programiz.com/python-programming/datetime/current-datetime
            today = date.today()
            print('Date: ' + today.strftime("%Y-%m-%d") )
        else:
        #keep existing content 
            print(line, end='')
    fileinput.close()
    print(test)
            

def _adr_dir():
    newdir = dir = os.getcwd()

# confuscated do-while
# https://www.javatpoint.com/python-do-while-loop
    while True:
        adr_print('_adr_dir: ' + dir)
        dir_docadr = os.path.join(dir , 'doc/adr')
        path_adrdir = os.path.join(dir , '.adr-dir')
        if (os.path.isdir(dir_docadr)):
            adr_print('_adr_dir, found /doc/adr in ' + dir_docadr )
            newdir = dir_docadr
            break
        elif (os.path.isfile(path_adrdir)):
            adrdir_directory=os.path.join(dir,find_alternate_dir(dir))
            adr_print('_adr_dir, found .adr_dir, referring to ' + adrdir_directory)
            newdir = adrdir_directory
            break
        # https://stackoverflow.com/questions/9856683/using-pythons-os-path-how-do-i-go-up-one-directory
        # Go up one directory
        newdir = os.path.dirname(dir)
        # If you can't go up further, you've reached the root.
        if newdir ==  dir:
            #default value is 'doc/adr/'
            newdir = 'doc/adr/'
            break
        
        dir = newdir
    return(newdir)

def adr_list(dir):
    from os import listdir
    from os.path import isfile, join

    adr_dir = _adr_dir()
    adr_print('adr_list: dir = '+ adr_dir)
    
    adr_index = dict()
    # start with index is zero, will be incremented after search
    adr_index['n'] = 0
    adr_index['text'] = '0000'
    adr_index['adr_list'] = list()
    adr_print('adr_find_index; adr directory is '+ adr_dir)
    onlyfiles = [f for f in listdir(adr_dir) if isfile(join(adr_dir, f))]
    # search for highest adr number
    for file in onlyfiles:
        try:
            #print(type(file))
            # get number by reading first 4 characters
            # if this fails, the 'except' will be executed, and actions past this line will be skipped 
            number = int(file[:4])
            #print(number)
            # increase index if higher number is found
            if (number > adr_index['n']):
                adr_index['n'] = number
            adr_index['adr_list'].append(file)
        except: 
            adr_print (file + " is not a valid ADR filename")
            None
    adr_index['n'] += 1
    return sorted(adr_index['adr_list'])
