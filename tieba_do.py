'''
贴吧签到
====================================
[task_local]
#贴吧签到
*/5 * * * * tieba_do.py, tag=贴吧签到, enabled=true
new Env("贴吧签到");
'''

import requests
import logging
import os

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

url = "http://zlong.asia/TiebaSign/do.php"

# 最简单的get请求
r = requests.get(url)
if (r.status_code == 200):
    logger.info("执行成功")
else:
    send("贴吧签到监控", "服务器访问错误，错误代码：%d"%r.status_code)
