from flask import current_app
from urllib import request
import re


# 通过sohu公共ip库获取本机公网ip
def get_ip():
    sohu_ip_url = 'http://txt.go.sohu.com/ip/soip'
    r = request.urlopen(sohu_ip_url)
    text = r.read().decode()
    result = re.findall(r'\d+.\d+.\d+.\d+', text)
    if result:
        return result[0]
    else:
        return None


def admin_url():
    ip = get_ip()
    ip = ip if ip else "localhost"
    if current_app.config['DEBUG']:
        ip = "0.0.0.0"
    url = "http://{ip}:{port}/admin".format(ip=ip, port=5000)
    return url
