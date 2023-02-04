import pickle
import dropboxFN

def save_obj(obj, name , folder):
    with open(name+'.pickle', 'wb') as handle:
        pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)
    handle.close()
    dropboxFN.dropbox_upload_file(open(name+'.pickle', "rb").read(), name+'.pickle', folder)

def load_obj(name, folder ):
    return pickle.load(dropboxFN.dropbox_download_file(folder+"/"+name+'.pickle'))