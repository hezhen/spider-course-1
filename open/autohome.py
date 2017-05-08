import urllib2
import json
from bs4 import BeautifulSoup

url_format = 'http://www.autohome.com.cn/grade/carhtml/%s.html';

request_headers = {
    'host': "www.autohome.com.cn",
    'connection': "keep-alive",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'accept-language': "zh-CN,en-US;q=0.8,en;q=0.6",
    'cookie': "sessionid=7782F0A9-9F9E-1F85-F5BC-FD98407FC9C8%7C%7C2015-04-01+12%3A12%3A40.586%7C%7C0; sessionuid=7782F0A9-9F9E-1F85-F5BC-FD98407FC9C8||2015-04-01+12%3A12%3A40.586||0; _ga=GA1.3.2074740228.1427861558; ag_fid=GDdl821Vp27BEY3F; fvlid=14683980655168PgJdugt; pcpopclub=3AA2AE347FB1A2CB0766B72995E2D46D0A2ABFB0F77C010259D645328E4F1E817F4BD1AACFFA0886D5B6E1D3ED22B1206A7332C8614C83CA1D69090A38E7DA89C04C37A012AF25E1658379C75A2BDB0049BE94002C54A7A1BD15A6227700DA3E28E6E4E194B0FF9F4100D3209D0BF885D49D2373115BD115C3B470BEB20491BAF581C4321D14A4EA8A056EE1583DB818BD2AF6C28781C7FA4B8C66F05368845DE2A9CC3147B43E7DB92BC31C254B5C229848B4BECEE956EF401E4C21FA8946C06D3BBBFCE0B64F69F75BBEE8F5E69E0EC1DFF298608A0D8AB362A55BD2F7C4FC84388E695F91F24FB2834D6AEC44D30B9682A447B7A784EC9C4702DE44A94202A4DD9DAF1712946CE0A2D985A6A836ED87474745D346E9340CF40BBDDEA99F8DE61F5930787B41286DF4151474AEDEDE93D3646F; clubUserShow=30027334|177|2|omasay|0|0|0||2016-08-23 20:53:54|0; autouserid=30027334; mallsfvi=1474647193411vUtFIQuD%7Cwww.autohome.com.cn%7C2018302; historybbsName4=c-3615%7C%E9%94%90%E7%95%8C%7C%2Cc-3420%7CXC%20Classic%2FXC90%7C%2F2015%2F07%2F12%2F13%2F41531570-2636-16c4-k2cf-n202ambfee6n_s.jpg%2Cc-3059%7C%E6%AF%94%E4%BA%9A%E8%BF%AAS7%7C; sessionfid=210792421; cookieCityId=110100; sessionip=139.214.116.101; ASP.NET_SessionId=kwph4l1az525j25qmsrhajzt; sessionuserid=30027334; sessionlogin=ea00df44ebef4eecbe971fca2dd6136101ca2e46; ahpvno=9; __utma=1.2074740228.1427861558.1483296371.1483325383.21; __utmc=1; __utmz=1.1483296371.20.8.utmcsr=newsmth.net|utmccn=(referral)|utmcmd=referral|utmcct=/nForum/; ref=www.newsmth.net%7C0%7C0%7Cwww.baidu.com%7C2017-01-02+10%3A52%3A12.555%7C2016-10-13+14%3A10%3A37.202; area=220199; ahrlid=1483325538111GZZsRMht-1483325542122",
    'if-modified-since': "Mon, 02 Jan 2017 02:30:35 GMT",
    'cache-control': "no-cache",
    'postman-token': "6faa9a97-f82d-4ac6-07ed-6b3a807fde72"
    }

try:
    fo = open('autohome1.html', 'r')
except IOError:
    html_doc = ''
    start_char = 'A'

    for i in range(ord('A'), ord('Z')):
        req = urllib2.Request(url_format % (chr(i)),headers=request_headers)
        response = urllib2.urlopen(req)
        page = response.read()
        html_doc += page;
    fo = open('autohome1.html', 'wb+')
    fo.write('<!DOCTYPE html>\
        <html>\
        <head>\
        <meta http-equiv=Content-Type content="text/html;charset=gb2312">\
        <meta http-equiv=X-UA-Compatible content="IE=edge,chrome=1">\
        <meta content=always name=referrer>\
        <script type="text/javascript" src="jquery-3.1.1.min.js"></script>\
        <script type="text/javascript" src="autohome.js"></script>\
        <title>Autohome</title>\
        </head>\
        <body>\
        ')
    fo.write(html_doc);
    fo.write('</body>')

soup = BeautifulSoup(fo, "html.parser")

models_file = open("models.txt", "wb")

for model in soup.find_all("h4"):
    try:
        if model.string is not None:
            models_file.write("%s\r\n" % (model.string.encode('utf-8')))
    except ValueError:
        continue

fo.close()
models_file.close()