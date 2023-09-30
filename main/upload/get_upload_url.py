import json
import requests
import logging
from get_token import get_token

def get_upload_url(token, env, path):

    post_url = "https://api.weixin.qq.com/tcb/uploadfile?access_token=" + token
    playload = json.dumps({"env":env, "path":path})

    try:
        upload = requests.post(post_url, data=playload)
        res=upload.json()
        return upload.json()
    except Exception as e:
        print("upload_url wrong!")
        logging.error(e)

if __name__=='__main__':
    get_upload_url(get_token(),'vajmmm-4g27p1907cb91d34','./')