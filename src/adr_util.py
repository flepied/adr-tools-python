import os
# To copy files
from shutil import copyfile

# adr-config:
# Original bash implementation generates strings with paths to
# bin and template dir (both the same).

# In this python implementation I've changed this to a 
# dictionary. I think this is more future proof and way
# more 'pythonic' and less error prone.

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
        adr_new(config, localpath, dirname, 'record-architecture-decisions')
    return(0)

# This function is used to read the .adr-dir file (written in adr_init), to determine the relative path for the 
# adrs. default is /doc/adr/ . 
def find_alternate_dir():
    directory = 'doc/adr/'
    try:
        fh = open('.adr-dir', 'r')
        directory = fh.read()
    except FileNotFoundError:
        None
    return directory

# adr-new
def adr_new(config, localpath, dirname, title):
    src= config["adr_template_dir"]+'/template.md'
    dst = localpath+'/'+dirname + 'template.md'
    print(src + ' ' + dst)
    copyfile(src, dst)
    return(0)