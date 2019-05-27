import os 


# adr-config:
# Original bash implementation generates strings with paths to
# bin and template dir (both the same).

# In this python implementation I've changed this to a 
# dictionary. I think this is more future proof and way
# more 'pythonic' and less error prone.

def adr_config():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config = {"bin_dir"     : dir_path ,
              "template_dir": dir_path 
    }
    return(config)

# adr-init

# file IO:
# https://docs.python.org/3/tutorial/inputoutput.html

def adr_init(config, dirname):
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
    return(0)

# adr-new
def adr_new():
    return(0)