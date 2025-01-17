from requests import get, post, put, packages
import requests
from re import findall
from os.path import exists
import json
import os
import sys,re
import random,time
import base64
import hashlib
import urllib.parse
import uuid

packages.urllib3.disable_warnings()
from urllib.parse import unquote
"""
new Env('wskey本地转换');
9 9 9 9 * jd_wsck.py
by:lonesomexz
"""
hadsend=True
UserAgent=""

def printf(text):
    print(text)
    sys.stdout.flush()

def randomuserAgent():
    global struuid,addressid,iosVer,iosV,clientVersion,iPhone,area,ADID,lng,lat
    global UserAgent
    struuid=''.join(random.sample(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','a','b','c','z'], 40))
    addressid = ''.join(random.sample('1234567898647', 10))
    iosVer = ''.join(random.sample(["15.1.1","14.5.1", "14.4", "14.3", "14.2", "14.1", "14.0.1"], 1))
    iosV = iosVer.replace('.', '_')
    clientVersion=''.join(random.sample(["10.3.0", "10.2.7", "10.2.4"], 1))
    iPhone = ''.join(random.sample(["8", "9", "10", "11", "12", "13"], 1))
    area=''.join(random.sample('0123456789', 2)) + '_' + ''.join(random.sample('0123456789', 4)) + '_' + ''.join(random.sample('0123456789', 5)) + '_' + ''.join(random.sample('0123456789', 5))
    ADID = ''.join(random.sample('0987654321ABCDEF', 8)) + '-' + ''.join(random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(random.sample('0987654321ABCDEF', 12))
    lng='119.31991256596'+str(random.randint(100,999))
    lat='26.1187118976'+str(random.randint(100,999))
    UserAgent=f'jdapp;iPhone;10.0.4;{iosVer};{uuid};network/wifi;ADID/{ADID};model/iPhone{iPhone},1;addressid/{addressid};appBuild/167707;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS {iosV} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/null;supportJDSHWK/1'


def get_proxy_api(proxy_url, max_retries=5, timeout=60, retry_delay=1):
    for retry in range(max_retries):
        res = get(url=proxy_url)
        printf(f"本次获取到的代理：{res.text}")
        proxy_ip_port = res.text.strip()
        proxy_address = f"http://{proxy_ip_port}"

        try:
            response = get("https://jd.com", proxies={"http": proxy_address, "https": proxy_address}, timeout=timeout)
            if response.status_code == 200:
                return proxy_address
        except Exception as e:
            print(f"代理检测失败，错误信息：{e}")

        print("代理检测失败，重新获取...")
        time.sleep(retry_delay)
    
    print("无法获取可用的代理IP，尝试次数已达上限。")
    return None



def load_send():
    global send
    global hadsend
    cur_path = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(cur_path)
    if os.path.exists(cur_path + "/sendNotify.py"):
        try:
            from sendNotify import send
            hadsend=True
        except:
            printf("加载sendNotify.py的通知服务失败，请检查~")
            hadsend=False
    else:
        printf("加载通知服务失败,缺少sendNotify.py文件")
        hadsend=False
load_send()

def send_notification(title, content,summary):
    # Add your own WxPusher API key here
    api_key = os.environ["WP_APP_TOKEN_ONE"]
    uids= os.environ["WP_APP_MAIN_UID"]
    desp = '''<section style="width: 24rem; max-width: 100%;border:none;border-style:none;margin:2.5rem auto;" id="shifu_imi_57"
    donone="shifuMouseDownPayStyle(&#39;shifu_imi_57&#39;)">
    <section
        style="margin: 0px auto;text-align: left;border: 2px solid #212122;padding: 10px 0px;box-sizing:border-box; width: 100%; display:inline-block;"
        class="ipaiban-bc">
        <section style="margin-top: 1rem; float: left; margin-left: 1rem; margin-left: 1rem; font-size: 1.3rem; font-weight: bold;">
            <p style="margin: 0; color: black">
                texttext
            </p>
        </section>
        <section style="display: block;width: 0;height: 0;clear: both;"></section>
        <section
            style="margin-top:20px; display: inline-block; border-bottom: 1px solid #212122; padding: 4px 20px; box-sizing:border-box;"
            class="ipaiban-bbc">
            <section
                style="width:25px; height:25px; border-radius:50%; background-color:#212122;display:inline-block;line-height: 25px"
                class="ipaiban-bg">
                <p style="text-align:center;font-weight:1000;margin:0">
                    <span style="color: #ffffff;font-size:20px;">📢</span>
                </p>
            </section>
            <section style="display:inline-block;padding-left:10px;vertical-align: top;box-sizing:border-box;">
            </section>
        </section>
        <section style="margin-top:0rem;padding: 0.8rem;box-sizing:border-box;">
            <p style=" line-height: 1.6rem; font-size: 1.1rem; ">
                despdesp
			</p>            
        </section>
    </section>
</section>'''
    desp=desp.replace("texttext",title)
    desp=desp.replace("despdesp" ,content.replace("\n", '<br>'))


    payload = {"appToken": api_key,
                "content": desp,
                "summary": title+"\n"+summary,
                "contentType": 2,
                "uids": [uids]
                }
                    
    # Send the request
    res = requests.post('http://wxpusher.zjiecode.com/api/send/message', json=payload, timeout=15).json()
    if res["code"]==1000:
        printf("WxPusher 发送通知消息成功!")
    else:
        printf(res.text)


def randomstr(num):
    randomstr = ''.join(str(uuid.uuid4()).split('-'))[num:]
    return randomstr

def randomstr1(num):
    randomstr = ""
    for i in range(num):
        randomstr = randomstr + random.choice("abcdefghijklmnopqrstuvwxyz0123456789")
    return randomstr

def sign_core(inarg):
    key = b'80306f4370b39fd5630ad0529f77adb6'
    mask = [0x37, 0x92, 0x44, 0x68, 0xA5, 0x3D, 0xCC, 0x7F, 0xBB, 0xF, 0xD9, 0x88, 0xEE, 0x9A, 0xE9, 0x5A]
    array = [0 for _ in range(len(inarg))]
    for i in range(len(inarg)):
        r0 = int(inarg[i])
        r2 = mask[i & 0xf]
        r4 = int(key[i & 7])
        r0 = r2 ^ r0
        r0 = r0 ^ r4
        r0 = r0 + r2
        r2 = r2 ^ r0
        r1 = int(key[i & 7])
        r2 = r2 ^ r1
        array[i] = r2 & 0xff
    return bytes(array)

def base64Encode(string):
    return base64.b64encode(string.encode("utf-8")).decode('utf-8').translate(str.maketrans("KLMNOPQRSTABCDEFGHIJUVWXYZabcdopqrstuvwxefghijklmnyz0123456789+/", "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"))

def base64Decode(string):
    return base64.b64decode(string.translate(str.maketrans("KLMNOPQRSTABCDEFGHIJUVWXYZabcdopqrstuvwxefghijklmnyz0123456789+/", "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"))).decode('utf-8')

def randomeid():
    return 'eidAaf8081218as20a2GM%s7FnfQYOecyDYLcd0rfzm3Fy2ePY4UJJOeV0Ub840kG8C7lmIqt3DTlc11fB/s4qsAP8gtPTSoxu' % randomstr1(20)

def get_ep(jduuid : str=''):
    if not jduuid:
        jduuid = randomstr(16)
    ts = str(int(time.time() * 1000))
    bsjduuid = base64Encode(jduuid)
    area = base64Encode('%s_%s_%s_%s' % (
        random.randint(1, 10000), random.randint(1, 10000), random.randint(1, 10000), random.randint(1, 10000)))
    d_model = random.choice(['Mi11Ultra', 'Mi11', 'Mi10'])
    d_model = base64Encode(d_model)
    return '{"hdid":"JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw=","ts":%s,"ridx":-1,"cipher":{"area":"%s","d_model":"%s","wifiBssid":"dW5hbw93bq==","osVersion":"CJS=","d_brand":"WQvrb21f","screen":"CtS1DIenCNqm","uuid":"%s","aid":"%s","openudid":"%s"},"ciphertype":5,"version":"1.2.0","appname":"com.jingdong.app.mall"}' % (
        int(ts) - random.randint(100, 1000), area, d_model, bsjduuid, bsjduuid, bsjduuid), jduuid, ts

def get_sign(functionId, body, client : str="android", clientVersion : str='11.2.8',jduuid : str='') -> dict:
    if isinstance(body,dict):
        d=body
        body=json.dumps(body)
    else:
        d=json.loads(body)

    if "eid" in d:
        eid=d["eid"]
    else:
        eid=randomeid()

    ep, suid, st = get_ep(jduuid)
    sv = random.choice(["102", "111", "120"])
    all_arg = "functionId=%s&body=%s&uuid=%s&client=%s&clientVersion=%s&st=%s&sv=%s" % (functionId, body, suid, client, clientVersion, st, sv)
    back_bytes = sign_core(str.encode(all_arg))
    sign = hashlib.md5(base64.b64encode(back_bytes)).hexdigest()
    convertUrl='functionId=%s&body=%s&clientVersion=%s&client=%s&sdkVersion=31&lang=zh_CN&harmonyOs=0&networkType=wifi&oaid=%s&eid=%s&ef=1&ep=%s&st=%s&sign=%s&sv=%s' % (functionId,body, clientVersion, client, suid, eid, urllib.parse.quote(ep), st, sign, sv)
    return convertUrl
    
def getcookie_wskey(key):
    proxys = proxy_url
    if os.environ.get("WSKEY_PROXY_URL") is not None:
        proxys = get_proxy_api(proxy_url)

    body = "body=%7B%22to%22%3A%22https%3A//plogin.m.jd.com/jd-mlogin/static/html/appjmp_blank.html%22%7D"
    pin = findall("pin=([^;]*);", key)[0]

            
    for num in range(0,5):
        sign = get_sign("genToken",{"url": "https://plogin.m.jd.com/jd-mlogin/static/html/appjmp_blank.html"},"android","11.2.8")       
        url = f"https://api.m.jd.com/client.action?functionId=genToken&{sign}"
        headers = {
            "cookie": key,
            'user-agent': UserAgent,
            'accept-language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
            'content-type': 'application/x-www-form-urlencoded;'
        }
        try:
            token = post(url=url, headers=headers, data=body, verify=False, proxies={"http": proxys, "https": proxys}).json()
            token=token['tokenKey']
        except Exception as error:
            print(f"【警告】{unquote(pin)}在获取token时失败，等待5秒后重试")
            time.sleep(5)
            if num == 4:
                print(f"【错误】{unquote(pin)}在获取token时：\n{error}")
                return pin, "False"
            randomuserAgent()
            if os.environ.get("WSKEY_PROXY_URL") is not None:
                proxys = get_proxy_api(proxy_url)
            continue

        if token!="xxx":
            break
        else:
            printf(f"【警告】{unquote(pin)}在获取token时失败，等待5秒后重试")
            time.sleep(5)
            randomuserAgent()
            if os.environ.get("WSKEY_PROXY_URL") is not None:
                proxys = get_proxy_api(proxy_url)
            
    if token=="xxx":
        printf(f"【错误】{unquote(pin)}在获取token时失败，跳过")
        return "Error"

    for num in range(0, 5):
        url = 'https://un.m.jd.com/cgi-bin/app/appjmp'
        params = {
            'tokenKey': token,
            'to': 'https://plogin.m.jd.com/cgi-bin/m/thirdapp_auth_page',
            'client_type': 'android',
            'appid': 879,
            'appup_type': 1,
        }
        try:
            res = get(url=url, params=params, verify=False,
                      allow_redirects=False, proxies={"http": proxys, "https": proxys}).cookies.get_dict()        
        except Exception as error:
            print(f"【警告】{unquote(pin)}在获取cookie时失败，等待5秒后重试")
            time.sleep(5)
            if num == 4:
                # 最后一次重试时输出错误消息并返回 "Error"
                print(f"【错误】{unquote(pin)}在获取cookie时：\n{error}")
                return "Error"
            randomuserAgent()
            if os.environ.get("WSKEY_PROXY_URL") is not None:
                proxys = get_proxy_api(proxy_url)
            continue
        
    try:
        if "app_open" in res['pt_key']:
            cookie = f"pt_key={res['pt_key']};pt_pin={res['pt_pin']};"
            return cookie
        else:        
            return ("Error:"+str(res))
    except Exception as error:
        printf(f"【错误】{unquote(pin)}在获取cookie时：\n{str(res)}")
        return "Error"

def arcadia_getwskey():
    possible_paths = ['/arcadia/config/account.json', '/jd/config/account.json']

    for wskey_file in possible_paths:
        if os.path.isfile(wskey_file):
            with open(wskey_file, 'r') as f:
                data = json.load(f)

            json_data = []
            for item in data:
                # 跳过空的 pt_pin 或 ws_key
                if not item['pt_pin'] or not item['ws_key']:
                    continue
                pt_pin = item['pt_pin']
                ws_key = item['ws_key']
                remarks = item['remarks'][0] if item['remarks'] else ''
                json_item = f"pin={pt_pin};wskey={ws_key};"
                json_data.append((json_item, remarks))
            return json_data
    return []

def arcadia_subcookie(cookie, token):
    url = 'http://127.0.0.1:5678/openApi/updateCookie'
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ', 'api-token': f'{token}'} 
    data = {
        "cookie": cookie
    }    
    res = post(url, data=json.dumps(data), headers=headers).json()
    return res

# 登录青龙 返回值 token
def get_qltoken(username, password, twoFactorSecret):  # 方法 用于获取青龙 Token
    printf("Token失效, 新登陆\n")  # 日志输出
    remot_ql_url='http://172.17.0.2:5600/'
    if twoFactorSecret:
        try:
            twoCode = ttotp(twoFactorSecret)
        except Exception as err:
            printf(str(err))  # Debug日志输出
            printf("TOTP异常")
            sys.exit(1)
        url = remot_ql_url + "api/user/login"  # 设置青龙地址 使用 format格式化自定义端口
        payload = json.dumps({
            'username': username,
            'password': password
        })  # HTTP请求载荷
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }  # HTTP请求头 设置为 Json格式
        try:  # 异常捕捉
            res = requests.post(url=url, headers=headers, data=payload)  # 使用 requests模块进行 HTTP POST请求
            if res.status_code == 200 and res.json()["code"] == 420:
                url = remot_ql_url + 'api/user/two-factor/login'
                data = json.dumps({
                    "username": username,
                    "password": password,
                    "code": twoCode
                })
                res = requests.put(url=url, headers=headers, data=data)
                if res.status_code == 200 and res.json()["code"] == 200:
                    token = res.json()["data"]['token']  # 从 res.text 返回值中 取出 Token值
                    return token
                else:
                    printf("两步校验失败\n")  # 日志输出
                    sys.exit(1)
            elif res.status_code == 200 and res.json()["code"] == 200:
                token = res.json()["data"]['token']  # 从 res.text 返回值中 取出 Token值
                return token
        except Exception as err:
            logger.debug(str(err))  # Debug日志输出
            sys.exit(1)
    else:
        url = remot_ql_url + 'api/user/login'
        payload = {
            'username': username,
            'password': password
        }  # HTTP请求载荷
        payload = json.dumps(payload)  # json格式化载荷
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }  # HTTP请求头 设置为 Json格式
        try:  # 异常捕捉
            res = requests.post(url=url, headers=headers, data=payload)  # 使用 requests模块进行 HTTP POST请求
            if res.status_code == 200 and res.json()["code"] == 200:
                token = res.json()["data"]['token']  # 从 res.text 返回值中 取出 Token值
                return token
            else:
                ql_send("青龙登录失败!")
                sys.exit(1)  # 脚本退出
        except Exception as err:
            printf(str(err))  # Debug日志输出
            printf("使用旧版青龙登录接口")
            url = remot_ql_url + 'api/login'  # 设置青龙地址 使用 format格式化自定义端口
            payload = {
                'username': username,
                'password': password
            }  # HTTP请求载荷
            payload = json.dumps(payload)  # json格式化载荷
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }  # HTTP请求头 设置为 Json格式
            try:  # 异常捕捉
                res = requests.post(url=url, headers=headers, data=payload)  # 使用 requests模块进行 HTTP POST请求
                token = json.loads(res.text)["data"]['token']  # 从 res.text 返回值中 取出 Token值
            except Exception as err:  # 异常捕捉
                printf(str(err))  # Debug日志输出
                printf("青龙登录失败, 请检查面板状态!")  # 标准日志输出
                ql_send('青龙登陆失败, 请检查面板状态.')
                sys.exit(1)  # 脚本退出
            else:  # 无异常执行分支
                return token  # 返回 token值
        # else:  # 无异常执行分支
        #     return token  # 返回 token值


# 返回值 Token
def ql_login():  # 方法 青龙登录(获取Token 功能同上)
    remot_ql_url='http://172.17.0.2:5600/'
    path = '/ql/config/auth1.json'  # 设置青龙 auth文件地址
    if not os.path.isfile(path):
        path = '/ql/data/config/auth1.json'  # 尝试设置青龙 auth 新版文件地址
    if os.path.isfile(path):  # 进行文件真值判断
        with open(path, "r") as file:  # 上下文管理
            auth = file.read()  # 读取文件
            file.close()  # 关闭文件
        auth = json.loads(auth)  # 使用 json模块读取
        username = auth["username"]  # 提取 username
        password = auth["password"]  # 提取 password
        token = auth["token"]  # 提取 authkey
        try:
            twoFactorSecret = auth["twoFactorSecret"]
        except Exception as err:
            printf(str(err))  # Debug日志输出
            twoFactorSecret = ''
        if token == '':  # 判断 Token是否为空
            return get_qltoken(username, password, twoFactorSecret)  # 调用方法 get_qltoken 传递 username & password
        else:  # 判断分支
            url = remot_ql_url + 'api/user'  # 设置URL请求地址 使用 Format格式化端口
            headers = {
                'Authorization': 'Bearer {0}'.format(token),
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38'
            }  # 设置用于 HTTP头
            res = requests.get(url=url, headers=headers)  # 调用 request模块发送 get请求
            if res.status_code == 200:  # 判断 HTTP返回状态码
                return token  # 有效 返回 token
            else:  # 判断分支
                return get_qltoken(username, password, twoFactorSecret)  # 调用方法 get_qltoken 传递 username & password
    else:  # 判断分支
        printf("没有发现auth文件, 你这是青龙吗???")  # 输出标准日志
        sys.exit(0)  # 脚本退出


def subcookie(pt_pin, cookie, token):
    if True:
        reamrk=""
        if token!="":
            strptpin=pt_pin
            if re.search('%', strptpin):
                strptpin = unquote(strptpin, 'utf-8')
            url = 'http://172.17.0.2:5600/api/envs'
            headers = {'Authorization': f'Bearer {token}'}
            body = {
                'searchValue': pt_pin,
                'Authorization': f'Bearer {token}'
            }
            datas = get(url, params=body, headers=headers).json()['data']            
            old = False
            isline=True
            for data in datas:
                if "pt_key" in data['value']:
                    try:
                        body = {"name": "JD_COOKIE", "value": cookie, "_id": data['_id']}
                    except:    
                        body = {"name": "JD_COOKIE", "value": cookie, "id": data['id']}
                        isline=False
                    old = True
                    try:
                        reamrk=data['remarks']
                    except:
                        reamrk=""

                    if reamrk!="" and not reamrk is None:
                        strptpin=strptpin+"("+reamrk.split("@@")[0]+")"
                        
            if old:
                put(url, json=body, headers=headers)
                url = 'http://172.17.0.2:5600/api/envs/enable'
                if isline:
                    body = [body['_id']]
                else:
                    body = [body['id']]
                put(url, json=body, headers=headers)
                printf(f"更新成功：{strptpin}")
            else:
                body = [{"value": cookie, "name": "JD_COOKIE"}]
                post(url, json=body, headers=headers)
                printf(f"新增成功：{strptpin}")

def getRemark(pt_pin,token):    
    reamrk=""
    if re.search('%', pt_pin):
        strreturn=unquote(pt_pin, 'utf-8')
    else:
        strreturn=pt_pin

    if token!="":
        url = 'http://127.0.0.1:5600/api/envs'
        headers = {'Authorization': f'Bearer {token}'}
        body = {
            'searchValue': pt_pin,
            'Authorization': f'Bearer {token}'
        }
        datas = get(url, params=body, headers=headers).json()['data']
        for data in datas:
            if "pt_key" in data['value']:
                try:
                    reamrk=data['remarks']
                    break
                except:
                    pass
        if not reamrk is None and reamrk!="":
            strreturn=strreturn+"("+reamrk.split("@@")[0]+")"

    return strreturn

def main():
    printf("版本: 20230602")
    printf("说明: 如果用Wxpusher通知需配置WP_APP_TOKEN_ONE和WP_APP_MAIN_UID，其中WP_APP_MAIN_UID是你的Wxpusher UID")
    printf("隧道型代理池接口:export WSKEY_PROXY_TUNNRL='http://127.0.0.1:123456'")
    printf("拉取型代理API接口(数据格式:txt;提取数量:每次一个):export WSKEY_PROXY_URL='http://xxx.com/apiUrl'")
    printf("没有代理可以自行注册，比如携趣，巨量，每日免费1000IP，完全够用")
    printf("====================================")
    config=""
    envtype=""
    global proxy_url
    proxy_url=os.environ.get("WSKEY_PROXY_URL") or os.environ.get("WSKEY_PROXY_TUNNRL") or None
    iswxpusher=False
    counttime=0

    if os.path.exists("/ql/config/auth.json"):
        config="/ql/config/auth.json"
        envtype="ql"
    
    if os.path.exists("/ql/data/config/auth.json"):
        config="/ql/data/config/auth.json"
        envtype="ql"

    if os.path.exists("/jd/config/auth.json"):
        config="/jd/config/auth.json"
        envtype="arcadia"


    if os.path.exists("/arcadia/config/auth.json"):
        config="/arcadia/config/auth.json"
        envtype="arcadia"
        
    if config=="":
        printf(f"无法判断使用环境，退出脚本!")
        return  
    try:
        if os.environ.get("WP_APP_TOKEN_ONE")==None or os.environ.get("WP_APP_MAIN_UID")==None:
            printf('没有配置Wxpusher相关变量,将调用sendNotify.py发送通知')
        else:
            if os.environ.get("WP_APP_TOKEN_ONE")=="" or os.environ.get("WP_APP_MAIN_UID")=="":
                printf('没有配置Wxpusher相关变量,将调用sendNotify.py发送通知')
            else:
                printf('检测到已配置Wxpusher相关变量,将使用Wxpusher发送通知')
                iswxpusher=True
    except:
        iswxpusher=False
                
    if proxy_url is None:
        print("没有配置代理，无法使用代理!\n请配置环境变量WSKEY_PROXY_TUNNRL或WSKEY_PROXY_URL\n")
        print("====================================")
    else:
        print(f"已配置代理: {proxy_url}\n")

    resurt=""
    resurt1=""
    resurt2=""
    summary=""

    if envtype == "ql":
        with open(config, "r", encoding="utf-8") as f1:
            token = json.load(f1)['token']
        url = 'http://127.0.0.1:5600/api/envs'
        headers = {'Authorization': f'Bearer {token}'}
        body = {
            'searchValue': 'DDDD',
            'Authorization': f'Bearer {token}'
        }
        datas = get(url, params=body, headers=headers).json()['data']
    elif envtype == "arcadia":
        with open(config, "r", encoding="utf-8") as f1:
            #token = json.load(f1)['token']
            data = json.load(f1)
            token = data.get('openApiToken', '')
        url = 'http://127.0.0.1:5678/openApi/count'
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ', 'api-token': f'{token}'} 
        datas = get(url, headers=headers).json()["data"]["accountCount"]
    
    # printf(f"token：{token}")
    # printf(f"datas：{datas}")
        

    if datas > 0 if isinstance(datas, int) else len(datas) > 0:
        printf("\n===============开始转换JD_WSCK==============")
    else:
        printf("\n错误:没有需要转换的JD_WSCK，退出脚本!")
        return

    if envtype == "ql":
        remotToken=ql_login()
        for data in datas:
            randomuserAgent()
            if data['status']!=0:
                continue
            key = data['value']
            pin = re.findall(r'(pin=([^; ]+)(?=;?))',key)[0][1]        
            cookie = getcookie_wskey(key)
            if "app_open" in cookie:
                #printf("转换成功:"cookie)     
                orgpin = cookie.split(";")[1].split("=")[1]            
                subcookie(orgpin, cookie, remotToken)
                newpin=getRemark(orgpin,token)
                resurt1=resurt1+f"转换成功：{newpin}\n"
            else:
                newpin=getRemark(pin,token)
                if "fake_" in cookie:
                    message = f"pin为{newpin}的wskey过期了！"
                    printf(message)
                    url = 'http://127.0.0.1:5600/api/envs/disable'
                    try:
                        body = [data['_id']]
                    except:   
                        body = [data['id']]
                    put(url, json=body, headers=headers)                
                    printf(f"禁用成功:{newpin}")
                    resurt2=resurt2+f"wskey已禁用:{newpin}\n"
                else:
                    message = f"转换失败:{newpin}"
                    resurt2=resurt2+f"转换失败:{newpin}\n"

    elif envtype == "arcadia":
        wslist = arcadia_getwskey()
        #printf(f"wslist:\n{wslist}")
        for ws,remark in wslist:
            randomuserAgent()
            pin = re.findall(r'(pin=([^; ]+)(?=;?))',ws)[0][1]
            printf(f"当前转换的pin:\n{pin}")
            cookie = getcookie_wskey(ws)
            printf(f"转换后的cookie:\n{cookie}\n")

            if "app_open" in cookie:
                #printf("转换成功:"cookie)     
                res = arcadia_subcookie(cookie, token)
                resurt1=resurt1+f"转换成功：{remark}@{pin}"
                if res["code"] == 1:
                    resurt1=resurt1+f"，面板同步成功！ ✅\n"
                else:
                    resurt1=resurt1+f"，面板同步失败，token错误或者请求失败。 ❌\n"
            else:
                if "fake_" in cookie:
                    message = f"{remark}@{pin}，wskeyk可能过期了！ ❌\n"
                    printf(message)
                    resurt2=resurt2+f"{remark}@{pin}，wskeyk可能过期了！ ❌\n"
                else:
                    message = f"{remark}@{pin}，转换失败！ ❌"
                    printf(message)
                    resurt2=resurt2+f"{remark}@{pin}，转换失败！ ❌\n"

               
    if resurt2!="": 
        resurt="👇👇👇👇👇转换异常👇👇👇👇👇\n"+resurt2+"\n"
        summary="部分CK转换异常"
        
        if resurt1!="": 
            resurt=resurt+"👇👇👇👇👇转换成功👇👇👇👇👇\n"+resurt1
            if summary=="":
                summary="全部转换成功"
                
        if iswxpusher:
            send_notification("JD_WSCK转换结果",resurt,summary)
        else:
            if hadsend:
                send("JD_WSCK转换结果",resurt)
            else:
                printf("没有启用通知!")
    else:
        if resurt1!="": 
            resurt=resurt+"👇👇👇👇👇转换成功👇👇👇👇👇\n"+resurt1

        if iswxpusher:
            send_notification("JD_WSCK转换结果",resurt,summary)
        else:
            if hadsend:
                send("JD_WSCK转换结果",resurt)
            else:
                printf("没有启用通知!")   

    printf("\n\n===============转换结果==============\n")
    printf(resurt)

if __name__ == '__main__':    
    main()
