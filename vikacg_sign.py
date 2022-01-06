import os
import requests
import sys

# 返回值 list[wskey]
def get_vikck():
    if "vikck" in os.environ:
        wskey_list = os.environ['vikck'].split('&')
        if len(wskey_list) > 0:
            return wskey_list
        else:
            print("vikck变量未启用")
            sys.exit(1)
    else:
        print("未添加vikck变量")
        sys.exit(0)

# 签到 bool
def sign(ck):
        url = 'https://www.vikacg.com/wp-json/b2/v1/userMission'
        headers = {
            'Authorization': ck,
            'Host': 'www.vikacg.com',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'Origin': 'https://www.vikacg.com',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.vikacg.com/mission/today',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }
        res = requests.post(url=url, headers=headers)
        if res.status_code == 200:
            print("本次签到获得" + res.text + "枚金币\n")
            return True
        else:
            print("接口错误码: " + str(res.status_code) + "\n")
            return False

if __name__ == '__main__':
    cklist = get_vikck()
    print("查询到共有%d"%len(cklist) + "个账号\n")
    i = 1
    for ck in cklist:
        print("第%d"%i + "个账号开始签到")
        print(ck + "\n")
        if sign(ck):
            print("第%d"%i + "个账号签到成功\n")
        else:
            print("第%d"%i + "个账号签到失败\n")
        i = i + 1
    print("执行完成\n--------------------")
    sys.exit(0)
