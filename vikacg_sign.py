'''
维咔签到
====================================
[task_local]
#维咔签到
5 0 * * * vikacg_sign.py, tag=维咔签到, enabled=true
new Env("维咔签到");
'''

import os
import requests
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
try:
    import requests
except Exception as e:
    logger.info(str(e) + "\n\n缺少requests模块, 请执行命令：pip3 install requests\n\n")
    sys.exit(1)
os.environ['no_proxy'] = '*'
requests.packages.urllib3.disable_warnings()
try:
    from notify import send
except:
    logger.info("无推送文件")

Text = ""

# 返回值 list[wskey]
def get_vikck():
    if "vikck" in os.environ:
        wskey_list = os.environ['vikck'].split('&')
        if len(wskey_list) > 0:
            return wskey_list
        else:
            logger.info("vikck变量未启用")
            sys.exit(1)
    else:
        logger.info("未添加vikck变量")
        sys.exit(0)

# 签到 bool
def sign(ck):
        global Text
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
            print(res.text)
            if res.text.find("credit") == -1:
                Text += "今日已签到，获得" + getmidstring(res.text, "\"", "\"") + "枚金币\n\n"
            else:
                Text += "本次签到获得" + getmidstring(res.text, "\"credit\":", ",") + "枚金币\n\n"
            return True
        else:
            Text += "签到失败，可能是网络错误或Cookie过期\n\n"
            return False

def getmidstring(html, start_str, end):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()

if __name__ == '__main__':
    cklist = get_vikck()
    Text += "开始执行\n--------------------\n"
    Text += "查询到共有%d"%len(cklist) + "个账号\n\n"
    i = 1
    for ck in cklist:
        Text += "第%d"%i + "个账号开始签到\n\n"
        logger.info(ck + "\n")
        if sign(ck):
            Text += "第%d"%i + "个账号签到成功\n--------------------\n"
        else:
            Text += "第%d"%i + "个账号签到失败\n--------------------\n"
        i += 1
    Text += "执行完成\n" 
    send("维咔签到",Text)
    sys.exit(0)
