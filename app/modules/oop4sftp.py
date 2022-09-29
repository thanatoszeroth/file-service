import os 
import sys
import time
import pysftp

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def getlist4sftp():
    cnopts = pysftp.CnOpts(knownhosts = 'known_hosts')
    cnopts.hostkeys = None
    try:
        with pysftp.Connection(
            os.getenv("SFTPIP"), 
            port = int(os.getenv("SFTPPort")),
            username = os.getenv("SFTPUser"), 
            password = os.getenv("SFTPPassword"),
            cnopts = cnopts) as sftp:
        
            sftp.cwd('./upload/')
            directory = sftp.listdir_attr()
            for attr in directory:
                print (attr.filename, attr)
            return directory
    except OSError as e:
        print(f"SFTP 服務連接失敗 : {e}")
        return None

def upload2sftp(localfile):
    cnopts = pysftp.CnOpts(knownhosts = 'known_hosts')
    cnopts.hostkeys = None
    try:
        with pysftp.Connection(
            os.getenv("SFTPIP"), 
            port = int(os.getenv("SFTPPort")),
            username = os.getenv("SFTPUser"), 
            password = os.getenv("SFTPPassword"),
            cnopts = cnopts) as sftp:

            sftp.cwd('./upload/')
            sftp.put(localfile)
            print("SFTP 檔案上傳完成")
    except OSError as e:
        print(f"SFTP 服務連接失敗 : {e}")
        return None