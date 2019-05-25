import os 

def adr_config():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    #bin_dir=("adr_bin_dir=\'" + dir_path + "\'")
    #template_dir=("adr_template_dir=\"" + dir_path + "\"")
    config = {"bin_dir"     : dir_path ,
              "template_dir": dir_path 
    }
    return(config)

if __name__ == "__main__":
    import sys
    config = adr_config()
    for key,val in config.items():
        print(key,"=\"",val,"\"", sep='')