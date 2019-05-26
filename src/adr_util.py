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


# adr-new
def adr_new():
    return(0)