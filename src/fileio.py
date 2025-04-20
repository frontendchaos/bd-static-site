import os
import shutil

def get_root_path():
    return os.path.abspath(os.getcwd())

def delete_dir(dir):
    if os.path.exists(dir) == False:
        raise Exception(f"{dir} does not exist")
    for filename in os.listdir(dir):
        file_path = os.path.join(dir,filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
            else:                
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason %s" % (file_path, e))
    pass

def copy_to_dir(from_dir, to_dir):
    print("copy from " + from_dir + " -> " + to_dir)
    #if from_dir does not exist, exception
    if os.path.exists(from_dir) == False:
        raise Exception(f"{from_dir} does not exist")
    if os.path.exists(to_dir):
        #print(f"{to_dir} exists")
        pass
    else:
        #if to_dir does not exist, create it
        print(f"{to_dir} does not exist, creating it")
        os.mkdir(to_dir)
    #if to_dir has contents, nuke it all
    try:
        delete_dir(to_dir)
    except Exception as e:
        print(e)
    #for all contents
    for filename in os.listdir(from_dir):
        #build dest path
        file_path = os.path.join(from_dir,filename)
        dst = os.path.join(to_dir, filename)
        try:
            #if file, copy it to dest
            if os.path.isfile(file_path) or os.path.islink(file_path):
                shutil.copy(file_path, dst)
            else:                
                #if dir, copy_to_dir(my path to dest path + dir name)
                copy_to_dir(file_path, to_dir + filename)
        except Exception as e:
            print("Failed to copy %s. Reason %s" % (file_path, e))
        pass
    pass
