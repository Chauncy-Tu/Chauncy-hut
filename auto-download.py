import requests
import json
import os
import sys
from string import digits
from six.moves import urllib

def getAccessToken():
    '''
    获取接口调用凭据access_token，在之后的http api中都要用到这个发送post请求
    :return: 接口调用凭据 access_token str
    '''
    appid = "wx36c2130b391f6a75"                  #appid和secret为小程序内部数据，勿传
    secret = "2af608a70df21048483bd939bc15e4b2"
    url1="https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid="+appid+"&secret="+secret
    requests1 = requests.get(url=url1)
    c = requests1.json()                    #把json格式的response对象改为python中字典对象
    return c['access_token']

def databasequery(access_token):
    '''
    小程序数据库查询，获取filepath文件夹中的文件ID
    :param access_token: 接口调用凭据access_token
    :return: 文件ID file_id list
    '''
    url1 = "https://api.weixin.qq.com/tcb/databasequery?access_token=" + access_token
    postdatas1 = {
        "env": "audiocollect-ruiud",
        "query": "db.collection('filepath').get()"
    }
    requests1 = requests.post(url=url1, json=postdatas1)
    c = requests1.json()
    num = (len(c["data"]))
    file_id = []
    for i in range(num):
        file_id.append(c["data"][i].split(",")[1][10:-1])   #取出data字典中的file_id
    return file_id

def batchdownloadfile(access_token, file_id):
    '''
    获取文件下载地址url
    :param access_token: 接口调用凭据access_token
    :param file_id: 文件ID file_id
    :return:
    '''
    url1 = "https://api.weixin.qq.com/tcb/batchdownloadfile?access_token=" + access_token
    download_url = []
    for i in range(num):
        postdatas = {
            "env": "audiocollect-ruiud",
            "file_list": [
                {
                    "fileid": file_id[i],
                    "max_age": 7200
                }
            ]
        }
        requests1 = requests.post(url=url1, json=postdatas)
        c = requests1.json()
        download_url.append(c["file_list"][0]["download_url"])
    return download_url

def auto_download(filepath, base_dir):
    """根据给定的URL地址下载文件

    Parameter:
        filepath: list 文件的URL路径地址
        base_dir: str  基础保存路径
    Return:
        None
    """
    for url, index in zip(filepath, range(len(filepath))):
        filename = url.split('/')[-1]
        remove_digits = str.maketrans('', '', digits)     #除去文件名中的数字（获取文件夹名）
        res = filename.translate(remove_digits)           #！！！要求words中不含数字
        save_dir=base_dir+"/"+res[0:-4]                         #文件保存路径
        if not (os.path.isdir(save_dir)):                 #如果目标文件夹不存在，创建一个文件夹
            os.mkdir(save_dir)
        save_path = os.path.join(save_dir, filename)
        urllib.request.urlretrieve(url, save_path)
        sys.stdout.write('\r>> Downloading %.1f%%' % (float(index + 1) / float(len(filepath)) * 100.0))  #显示下载进度
        sys.stdout.flush()
    print('\nSuccessfully downloaded')


if __name__ == '__main__':
    base_dir = 'E:/test'        # 基础下载地址取为'E:/test'
    access_token = getAccessToken()
    file_id = databasequery(access_token)
    num = len(file_id)
    download_url = batchdownloadfile(access_token, file_id)
    filepath = download_url
    auto_download(filepath, base_dir)
