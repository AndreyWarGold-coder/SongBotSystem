import io
import dropbox
from dropbox.exceptions import AuthError
from dropbox import DropboxOAuth2FlowNoRedirect

APP_KEY = "7mjganz2gtvy3qt"
APP_SECRET = "am79k47alsu8bo6"

token = "sl.BYA0G-PuWjg_AR-nehIq9HJTlBAAIwuKQIYSAoqZcI6PfGJOZf4WutLMWZMt_UHqf4_Tf-u4GFeaRgrDJw3-vfR8opNtVGDQYFic9_FfyktDQ0t52t-zZIW942dXWOaHXuAXE06J_Rew"
dbx: dropbox.Dropbox = None
def dropbox_connect():
    global dbx
    """Create a connection to Dropbox."""
    try:
        dbx = dropbox.Dropbox(token)
        auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)

        authorize_url = auth_flow.start()
        print("1. Go to: " + authorize_url)
        print("2. Click \"Allow\" (you might have to log in first).")
        print("3. Copy the authorization code.")
        auth_code = input("Enter the authorization code here: ").strip()

        try:
            oauth_result = auth_flow.finish(auth_code)
        except Exception as e:
            print('Error: %s' % (e,))
            exit(1)
        dbx = dropbox.Dropbox(oauth2_access_token=oauth_result.access_token)
    except AuthError as e:
        print('Error connecting to Dropbox with access token: ' + str(e))
    return dbx

def dropbox_delete_file(path):
    dbx.files_delete_v2("/" + path)
    print("Delete " + path + " done!")

def dropbox_list_files(path):
    try:
        add = ""
        if(path == ""):
            add = ""
        else:
            add = "/"
        files = dbx.files_list_folder(add+path+add).entries
        files_list = []
        for file in files:
            if isinstance(file, dropbox.files.FileMetadata):
                files_list.append(file.name)
        return files_list
    except Exception as e:
        print('Error getting list of files from Dropbox: ' + str(e))


def dropbox_download_file(dropbox_file_path:str = "", content = False):
    """Download a file from Dropbox to the local machine."""
    print("Start download with DropBox ", dropbox_file_path)
    metadata, result = dbx.files_download(path="/"+dropbox_file_path)
    print("End download with DropBox ", dropbox_file_path)
    if(content == False):
        res = io.BytesIO(result.content)
        print(dropbox_file_path, res.getbuffer().nbytes)
        return res
    else:
        return result.content

def dropbox_upload_file(fileIO, file, dropbox_file_path = "/"):
    try:
        meta = dbx.files_upload(fileIO, "/"+dropbox_file_path+"/"+file, mode=dropbox.files.WriteMode("overwrite"))
        return meta
    except Exception as e:
        print('Error uploading file to Dropbox: ' + str(e))

#dropbox_upload_file(file="test.mp3")
#dropbox_download_file("/test.mp3", "nice.mp3")
dropbox_connect()