# File Service


Package for Local File/FTP/SFTP
```sh
pip install pyftpdlib
pip install fabric
pip uninstall -y cryptography
pip install cryptography==36.0.2
pip install pysftp
```

Run on Service 
```sh
ServiceIP=0.0.0.0
ServicePort=19191
uvicorn main:app --host ${ServiceIP} --port ${ServicePort} --reload
```

Export openapi.json
```sh
curl -O ServiceIP:ServicePort/openapi.json
```