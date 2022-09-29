import os
import sys
from ftplib import FTP


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload2ftp(localfile):
    encode = ['UTF-8','gbk','GB2312','GB18030','Big5','HZ']
    try:
        ftp = FTP()
        ftp.connect(os.getenv("FTPIP"), int(os.getenv("FTPPort")))
        ftp.encoding = "UTF-8"
        ftp.login(os.getenv("FTPUser"), os.getenv("FTPPassword"))
        ftp.retrlines('LIST')
        f = open(localfile, 'rb')
        ftp.storbinary('STOR %s' % os.path.basename(localfile), f)

        end_upload_file_list = []
        ftp.retrlines('NLST', end_upload_file_list.append)
        print(f"{end_upload_file_list}")

        ftp.quit()
        print("FTP 檔案上傳完成")
    except OSError as e:
        print(f"FTP 服務連接失敗 : {e}")

def getlist4ftp():
    encode = ['UTF-8','gbk','GB2312','GB18030','Big5','HZ']
    try:
        ftp = FTP()
        ftp.connect(os.getenv("FTPIP"), int(os.getenv("FTPPort")))
        ftp.encoding = "UTF-8"
        ftp.login(os.getenv("FTPUser"), os.getenv("FTPPassword"))
        ftp_file_list = []
        ftp.retrlines('NLST', ftp_file_list.append)
        print(f"{ftp_file_list}")
        ftp.quit()
        return ftp_file_list
    except OSError as e:
        print(f"FTP 服務連接失敗 : {e}")
        return None