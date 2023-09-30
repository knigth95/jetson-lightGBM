import json
import os
import requests
import logging
from get_token import get_token
from get_upload_url import get_upload_url
from parse_form import parse_form


access_token=get_token()
upload=get_upload_url(access_token,'vajmmm-4g27p1907cb91d34','./clfan/curveleg/')
res=parse_form(upload)
form=res[0]
upload_url=res[1]

with open("D:\\临时\\mjx.jpg", "rb") as f:
        file_path = "D:\\临时\\mjx.jpg"
        file_name = os.path.basename(file_path)
        form["key"]=form["key"]+file_name
        print(form["key"])
        form["file"] = f.read()
        
try:
  success = requests.post(upload_url, files=form)
  print(success)
except Exception as e:
  logging.error(e)

