import requests
url = "http://zlong.asia/TiebaSign/do.php"

# 最简单的get请求
r = requests.get(url)
print(r.status_code)
print(r.text)
