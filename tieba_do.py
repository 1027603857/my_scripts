// author: 疯疯
/*
幸运大转盘
活动地址：https://pro.m.jd.com/mall/active/3ryu78eKuLyY5YipWWVSeRQEpLQP/index.html
脚本兼容: Quantumult X, Surge, Loon, JSBox, Node.js
==============Quantumult X==============
[task_local]
#幸运大转盘
4 10 * * * https://github.com/1027603857/my_scripts/edit/main/tieba_do.py, tag=幸运大转盘, enabled=true
==============Loon==============
[Script]
cron "4 10 * * *" https://github.com/1027603857/my_scripts/edit/main/tieba_do.py,tag=幸运大转盘
================Surge===============
幸运大转盘 = type=cron,cronexp="4 10 * * *",wake-system=1,timeout=3600,https://github.com/1027603857/my_scripts/edit/main/tieba_do.py
===============小火箭==========
幸运大转盘 = type=cron,script-path=https://github.com/1027603857/my_scripts/edit/main/tieba_do.py, cronexpr="4 10 * * *", timeout=3600, enable=true
*/

import requests
url = "http://zlong.asia/TiebaSign/do.php"

# 最简单的get请求
r = requests.get(url)
print(r.status_code)
print(r.text)
