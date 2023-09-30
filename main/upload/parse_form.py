from get_token import get_token
from get_upload_url import get_upload_url



def parse_form(res):

    form = {}
    print(res["url"])
    env_id_index = res["url"].find("vajmmm-4g27p1907cb91d34")#找到地址中云环境id的位置
    slash_index = res["url"].find("/", env_id_index )#找到云环境id后第一个/
    cropped_part = res["url"][slash_index:]#将云环境id后的部分裁剪出来，即取目标云存储地址
    print(cropped_part)
    form["key"] = cropped_part 
    
    form["Signature"] = res["authorization"]
    form["x-cos-security-token"] = res["token"]
    form["x-cos-meta-fileid"] = res["cos_file_id"]
    return (form, res["url"])

if __name__=='__main__':
    print(parse_form(get_upload_url(get_token(),'vajmmm-4g27p1907cb91d34','./clfan/curveleg/')))
    