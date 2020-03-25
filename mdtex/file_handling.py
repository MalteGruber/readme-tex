import os.path
def get_text_of_file(file_path):
    file = open(file_path, 'r')
    text = file.read()
    file.close()
    return text

def save_text_to_file(file_path,text):
    text_file = open(file_path, "w")
    text_file.write(text)
    text_file.close()
    
def file_append_to_path(path,filename):
    if(path[-1]=="/"):
        path+=filename
    else:
        path+="/"+filename
    return path

def test_path_validity(path):
    if not os.path.exists(path):
        print("ERROR: Could not find the location <{}>".format(path))
        exit(-1)
def path_exists(path):
    return os.path.exists(path)
        
             
def path_has_file(path,filename):
    path=file_append_to_path(path,filename)
    return os.path.isfile(path)

        
def test_if_path_has_file(path,filename):
    path=file_append_to_path(path,filename)
    if not os.path.isfile(path):
        print("ERROR: Could not find the file",path)
        exit(-1)
def get_mdtex_folder():
    return os.path.dirname(os.path.abspath(__file__))
