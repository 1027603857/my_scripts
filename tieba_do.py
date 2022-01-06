/*
[task_local]
#贴吧签到
*/5 * * * * tieba_do.py, tag=贴吧签到, enabled=true
 */

import requests
url = "http://zlong.asia/TiebaSign/do.php"

# 最简单的get请求
r = requests.get(url)
print(r.status_code)
print(r.text)
