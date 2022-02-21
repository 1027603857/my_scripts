'''
健康填报
====================================
[task_local]
#健康填报
0 10 * * * health_report.py, tag=健康填报, enabled=true
new Env("健康填报");
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

def prints(text):
    global Text
    print(text)
    Text += text

# 返回值 list[healthck]
def get_healthck():
    if "healthck" in os.environ:
        wskey_list = os.environ['healthck'].split('&')
        if len(wskey_list) > 0:
            return wskey_list
        else:
            logger.info("healthck变量未启用")
            sys.exit(1)
    else:
        logger.info("未添加healthck变量")
        sys.exit(0)

# 签到 bool
def sign(ck):
    url = "http://xgsys.swjtu.edu.cn/SPCPTest3/Web/Report/Index"
    headers = {
        'Host': 'xgsys.swjtu.edu.cn',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'http://xgsys.swjtu.edu.cn',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; M2006J10C Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3185 MMWEBSDK/20220105 Mobile Safari/537.36 MMWEBID/9716 MicroMessenger/8.0.19.2080(0x28001337) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/wxpic,image/tpg,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'X-Requested-With': 'com.tencent.mm',
        'Referer': 'http://xgsys.swjtu.edu.cn/SPCPTest3/Web/Report/Index',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': ck
    }
    res = requests.get(url=url, headers=headers)
    if res.text.find("ReSubmiteFlag") == -1:
        if res.text.find("已登记") == -1:
            prints("未知错误，可能是cookie过期，请检查日志！\n\n")
            return False
        prints("今日已填报\n\n")
        return False
    ReSubmiteFlag = getmidstring(res.text, "<input name=\"ReSubmiteFlag\" type=\"hidden\" value=\"", "\"")
    print("获取日期代码：" + ReSubmiteFlag)
    data = "StudentId=2018110682&Name=%E5%BC%A0%E7%BA%AA%E9%BE%99&Sex=%E7%94%B7&SpeType=B&CollegeNo=01&SpeGrade=2018&SpecialtyName=%E5%9C%9F%E6%9C%A8%E5%B7%A5%E7%A8%8B&ClassName=%E5%9C%9F%E6%9C%A82018-06%E7%8F%AD&MoveTel=17623217713&Province=510000&City=510100&County=510115&ComeWhere=%E5%85%AC%E5%B9%B3%E8%A1%97%E9%81%93%E9%94%A6%E6%B1%87%E5%9F%8EA%E5%8C%BA&FaProvince=500000&FaCity=500100&FaCounty=500112&FaComeWhere=%E9%BE%99%E5%B1%B1%E8%A1%97%E9%81%93%E6%9D%BE%E7%89%8C%E8%B7%AF81%E5%8F%B7&radio_1=99243c67-bc34-435f-9d5a-d7fad7f3d39a&radio_2=a03d84a1-c24f-438d-8be6-ff4e8c14cb59&radio_3=24ee3594-2612-4ef4-94ad-5c9f7d5deaed&radio_4=28c7ee37-8d47-47ac-aed6-d65f7467c90d&Other=&GetAreaUrl=%2FSPCPTest3%2FWeb%2FReport%2FGetArea&IdCard=500102200007137097&ProvinceName=%E5%9B%9B%E5%B7%9D%E7%9C%81&CityName=%E6%88%90%E9%83%BD%E5%B8%82&CountyName=%E6%B8%A9%E6%B1%9F%E5%8C%BA&FaProvinceName=%E9%87%8D%E5%BA%86&FaCityName=%E9%87%8D%E5%BA%86%E5%B8%82&FaCountyName=%E6%B8%9D%E5%8C%97%E5%8C%BA&radioCount=4&checkboxCount=0&blackCount=0&PZData=%5B%7B%22OptionName%22%3A%22%E5%90%A6%EF%BC%8C%E6%9C%AA%E6%84%9F%E6%9F%93%22%2C%22SelectId%22%3A%2299243c67-bc34-435f-9d5a-d7fad7f3d39a%22%2C%22TitleId%22%3A%2212b4a828-2ed3-4559-99f3-d84e8cab2810%22%2C%22OptionType%22%3A%220%22%7D%2C%7B%22OptionName%22%3A%22%E5%90%A6%EF%BC%8C%E6%B2%A1%E6%9C%89%E8%BA%AB%E5%A4%84%E9%AB%98%E4%B8%AD%E9%A3%8E%E9%99%A9%E5%9C%B0%E5%8C%BA%22%2C%22SelectId%22%3A%22a03d84a1-c24f-438d-8be6-ff4e8c14cb59%22%2C%22TitleId%22%3A%2215e1bb64-bd72-4ea3-a8f9-e79c226a3ec3%22%2C%22OptionType%22%3A%220%22%7D%2C%7B%22OptionName%22%3A%22%E5%90%A6%EF%BC%8C%E6%97%A0%E6%8E%A5%E8%A7%A6%22%2C%22SelectId%22%3A%2224ee3594-2612-4ef4-94ad-5c9f7d5deaed%22%2C%22TitleId%22%3A%22c3cf045f-c257-4bce-8dd6-136d2d9f9694%22%2C%22OptionType%22%3A%220%22%7D%2C%7B%22OptionName%22%3A%22%E6%97%A0%E4%BB%A5%E4%B8%8A%E7%8A%B6%E5%86%B5%22%2C%22SelectId%22%3A%2228c7ee37-8d47-47ac-aed6-d65f7467c90d%22%2C%22TitleId%22%3A%229cb1a236-0a22-4744-9d1d-841dc0679771%22%2C%22OptionType%22%3A%220%22%7D%5D&CurAreaName=%E5%9B%9B%E5%B7%9D%E7%9C%81%E6%88%90%E9%83%BD%E5%B8%82%E6%AD%A6%E4%BE%AF%E5%8C%BA&CurAreaCode=510107&ReSubmiteFlag=" + ReSubmiteFlag
    res = requests.post(url=url, headers=headers ,data=data)
    print(res.text)
    if res.status_code == 200:
        prints(getmidstring(res.text, "content: '", "'") + "\n\n")
        return True
    else:
        prints("填报失败，可能是网络错误或Cookie过期\n\n")
        return False

def getmidstring(html, start_str, end):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()

if __name__ == '__main__':
    cklist = get_healthck()
    prints("开始执行\n每日自动健康填报 by zjl\n--------------------\n")
    prints("查询到共有%d"%len(cklist) + "个账号\n--------------------\n")
    i = 1
    for ck in cklist:
        prints("第%d"%i + "个账号开始健康填报\n\n")
        logger.info(ck + "\n")
        if sign(ck):
            prints("第%d"%i + "个账号签到成功\n--------------------\n")
        else:
            prints("第%d"%i + "个账号签到失败\n--------------------\n")
        i += 1
    prints("执行完成\n")
    send("健康填报",Text)
    sys.exit(0)
