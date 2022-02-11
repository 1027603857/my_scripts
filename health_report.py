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

# 签到 bool
def sign():
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
        'Cookie': 'WXOpenid=oV6nVs3gpcdteELGPHTI-80ileas; CenterSoftSPCPSwjtuWeb=C8AF1B05CA64374A62DA0C2A0C13E4EF9C34B2CAE2655F30311457D6DAB87BA143B68E31F070F98B8E9E3ADC0E867E6C9CCC19936AB41A9D4FC42C3EB51E121484DE16F2419A07F3804327DDF7F6822EBA0553E30873B9FF5F2B3B1EB35E3005667442B7B7CE5D721544CE4B3EDC0A17BB57210028AF7627150071CC006914363FEDD0BC59A3AEEE720F1625D8C2B6827030D24302BBBB19D19D9311DAD345096143165B57B79F7A0D9BAE9B94E464339A46186C7866B5578B4DED146441892A2DAFB5EA49FE4C7491835D968B0DBBF0DEAACC4849F939F97F1DB938C8262BD6D2EC885DC6C84387AE52980360E8B45A5472093E5DD1B33BF9B72AE445E9FB1534B1390015C94E21CB7CF18D5F21B8E795B5CF9E45BBDBC28FF3B07E8E7B3035A8024670A230F631E6742A6E849184BA04BE059E58946815414C56D4C8ABA173ED591FBF5B026D177127C12A1779DEFB93E0472B821EFCF83E5CF05C5154CB4EE8504853F6E1043B024510C9CB613F4A'
    }
    res = requests.get(url=url, headers=headers)
    if res.text.find("ReSubmiteFlag") == -1:
        if res.text.find("已登记") == -1:
            sys.exit(1)
        prints("今日已填报\n\n")
        return False
    ReSubmiteFlag = getmidstring(res.text, "<input name=\"ReSubmiteFlag\" type=\"hidden\" value=\"", "\"")
    print("获取日期代码：" + ReSubmiteFlag)
    data = "StudentId=2018110682&Name=%E5%BC%A0%E7%BA%AA%E9%BE%99&Sex=%E7%94%B7&SpeType=B&CollegeNo=01&SpeGrade=2018&SpecialtyName=%E5%9C%9F%E6%9C%A8%E5%B7%A5%E7%A8%8B&ClassName=%E5%9C%9F%E6%9C%A82018-06%E7%8F%AD&MoveTel=17623217713&Province=500000&City=500100&County=500112&ComeWhere=%E9%BE%99%E5%B1%B1%E8%A1%97%E9%81%93%E6%9D%BE%E7%89%8C%E8%B7%AF81%E5%8F%B7&FaProvince=500000&FaCity=500100&FaCounty=500112&FaComeWhere=%E9%BE%99%E5%B1%B1%E8%A1%97%E9%81%93%E6%9D%BE%E7%89%8C%E8%B7%AF81%E5%8F%B7&radio_1=99243c67-bc34-435f-9d5a-d7fad7f3d39a&radio_2=a03d84a1-c24f-438d-8be6-ff4e8c14cb59&radio_3=24ee3594-2612-4ef4-94ad-5c9f7d5deaed&radio_4=28c7ee37-8d47-47ac-aed6-d65f7467c90d&Other=&GetAreaUrl=%2FSPCPTest3%2FWeb%2FReport%2FGetArea&IdCard=500102200007137097&ProvinceName=%E9%87%8D%E5%BA%86&CityName=%E9%87%8D%E5%BA%86%E5%B8%82&CountyName=%E6%B8%9D%E5%8C%97%E5%8C%BA&FaProvinceName=%E9%87%8D%E5%BA%86&FaCityName=%E9%87%8D%E5%BA%86%E5%B8%82&FaCountyName=%E6%B8%9D%E5%8C%97%E5%8C%BA&radioCount=4&checkboxCount=0&blackCount=0&PZData=%5B%7B%22OptionName%22%3A%22%E5%90%A6%EF%BC%8C%E6%9C%AA%E6%84%9F%E6%9F%93%22%2C%22SelectId%22%3A%2299243c67-bc34-435f-9d5a-d7fad7f3d39a%22%2C%22TitleId%22%3A%2212b4a828-2ed3-4559-99f3-d84e8cab2810%22%2C%22OptionType%22%3A%220%22%7D%2C%7B%22OptionName%22%3A%22%E5%90%A6%EF%BC%8C%E6%B2%A1%E6%9C%89%E8%BA%AB%E5%A4%84%E9%AB%98%E4%B8%AD%E9%A3%8E%E9%99%A9%E5%9C%B0%E5%8C%BA%22%2C%22SelectId%22%3A%22a03d84a1-c24f-438d-8be6-ff4e8c14cb59%22%2C%22TitleId%22%3A%2215e1bb64-bd72-4ea3-a8f9-e79c226a3ec3%22%2C%22OptionType%22%3A%220%22%7D%2C%7B%22OptionName%22%3A%22%E5%90%A6%EF%BC%8C%E6%97%A0%E6%8E%A5%E8%A7%A6%22%2C%22SelectId%22%3A%2224ee3594-2612-4ef4-94ad-5c9f7d5deaed%22%2C%22TitleId%22%3A%22c3cf045f-c257-4bce-8dd6-136d2d9f9694%22%2C%22OptionType%22%3A%220%22%7D%2C%7B%22OptionName%22%3A%22%E6%97%A0%E4%BB%A5%E4%B8%8A%E7%8A%B6%E5%86%B5%22%2C%22SelectId%22%3A%2228c7ee37-8d47-47ac-aed6-d65f7467c90d%22%2C%22TitleId%22%3A%229cb1a236-0a22-4744-9d1d-841dc0679771%22%2C%22OptionType%22%3A%220%22%7D%5D&CurAreaName=%E9%87%8D%E5%BA%86%E5%B8%82%E9%87%8D%E5%BA%86%E5%B8%82%E6%B8%9D%E4%B8%AD%E5%8C%BA&CurAreaCode=500103&ReSubmiteFlag=" + ReSubmiteFlag
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
    sign()
    prints("执行完成\n")
    send("健康填报",Text)
    sys.exit(0)
