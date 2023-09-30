import requests
import logging

#获取token

def get_token():
    token_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=" + "wxe9f2ec40a63636e0" + "&secret=" + "b3cc4849e29f37f227a6f337e1b58735"
    try:
        token = requests.get(token_url)
        token = token.json()
        return token["access_token"]
    except Exception as e:
        logging.error(e)
        print("token wront!")

if __name__ =='__main__':
    get_token()
