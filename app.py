from flask import Flask,request
import random
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Koyeb'


def proxy():
    valid = []
    if not types:
        types = 'socks5'
    proxylist = requests.get('https://api.proxyscrape.com/?request=displayproxies&proxytype='+types+'&timeout=10000&country=all&ssl=all&anonymity=all').text.split('\r\n')
    with ThreadPoolExecutor(max_workers=int(len(proxylist))+2) as pool:
        for proxy in proxylist:
            pool.submit(filterProxy,types+'://'+proxy,valid)
    return {'author':'Muhammad Idris','result':valid}


def filterProxy(proxy,valid):
    try:
        proxies = {
            'http': proxy,
            'https': proxy
                    }
        response = requests.request(
                    'GET',
                    'https://ipinfo.io/json',
                    proxies=proxies,timeout=3
                    )
        if not "ID" in response.json()['country']:
            valid.append(proxies)
    except Exception as e:pass

@app.route("/api/uptime")
def uptime():
    target = request.args.get("target")
    if not target:
        target = "https://nfd2st-33517.csb.app"
    upprox = proxy()["result"]
    while True:
        proxyp = random.choice(upprox)
        if len(upprox)<2:break
        try:
            return requests.get(target,proxies=proxyp,timeout=3).text
            break
        except Exception as e:
            upprox.remove(proxyp)
    return {"error":upprox}


if __name__ == "__main__":
    app.run()
