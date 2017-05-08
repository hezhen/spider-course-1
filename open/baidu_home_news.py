import urllib
import urllib2
import json

url_format = 'https://www.baidu.com/home/pcweb/data/mancardwater?id=2&offset=%d&sessionId=14832978921842&p_params=31415927&newsNum=3&indextype=manht&_req_seqid=0xf7e28ac600008a71&asyn=1&t=1483297904932&sid=1445_21093_20691_21554_21592'

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
values = {'name': 'Michael Foord',
          'location': 'Northampton',
          'language': 'Python' }
request_headers = {
    'host': "www.baidu.com",
    'connection': "keep-alive",
    'accept': "text/plain, */*; q=0.01",
    'x-requested-with': "XMLHttpRequest",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
    'referer': "https://www.baidu.com/",
    'accept-language': "zh-CN,en-US;q=0.8,en;q=0.6",
    'cookie': "BDUSS=MxdFM3QnVka3Q4WTE0U3lEdXk1NUhDbXVjODk3M34wMVdFMWFYNEtzYUQxYzVXQVFBQUFBJCQAAAAAAAAAAAEAAAC4Qr0zzve5z7rNv9bB-gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAINIp1aDSKdWSW; BAIDUID=946010BB5C5DBC222BAA5CB3C4DE8ED3:FG=1; BIDUPSID=0726B003FD9B7521B1A86792D098373B; PSTM=1478141569; pgv_pvi=5789051904; pgv_si=s6251470848; MCITY=-131%3A; cflag=15%3A3; BD_HOME=1; BD_UPN=123253; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; BD_CK_SAM=1; PSINO=2; H_PS_PSSID=1445_21093_20691_21554_21592; BDSVRTM=0; __bsi=16647653956835173400_00_0_I_R_2_0303_C02F_N_I_I_0; BDUSS=MxdFM3QnVka3Q4WTE0U3lEdXk1NUhDbXVjODk3M34wMVdFMWFYNEtzYUQxYzVXQVFBQUFBJCQAAAAAAAAAAAEAAAC4Qr0zzve5z7rNv9bB-gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAINIp1aDSKdWSW; BAIDUID=946010BB5C5DBC222BAA5CB3C4DE8ED3:FG=1; BIDUPSID=0726B003FD9B7521B1A86792D098373B; PSTM=1478141569; pgv_pvi=5789051904; pgv_si=s6251470848; MCITY=-131%3A; cflag=15%3A3; H_PS_645EC=11e21%2FaLzaFQGzuvMqHuLOSzxG2LWWPuHEyS%2BIlpEDH6OEM70PneN9KsfhoNwJv1cAky; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; PSINO=2; BDUSS=MxdFM3QnVka3Q4WTE0U3lEdXk1NUhDbXVjODk3M34wMVdFMWFYNEtzYUQxYzVXQVFBQUFBJCQAAAAAAAAAAAEAAAC4Qr0zzve5z7rNv9bB-gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAINIp1aDSKdWSW; BAIDUID=946010BB5C5DBC222BAA5CB3C4DE8ED3:FG=1; BIDUPSID=0726B003FD9B7521B1A86792D098373B; PSTM=1478141569; pgv_pvi=5789051904; pgv_si=s6251470848; MCITY=-131%3A; cflag=15%3A3; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; BD_CK_SAM=1; PSINO=2; H_PS_PSSID=1445_21093_20691_21554_21592; __bsi=16647653956835173400_00_0_I_R_2_0303_C02F_N_I_I_0; BD_HOME=1; H_PS_PSSID=1445_21093_20691_21554_21592; BD_UPN=123253; __bsi=15922515846260939017_00_0_I_R_19_0303_C02F_N_I_I_0",
    'cache-control': "no-cache",
    'postman-token': "88519f9f-0032-60a2-c5bc-becb15610a7a"
    }

data = urllib.urlencode(values)
html_doc = ''
for i in range(1,6):
	req = urllib2.Request(url_format % (i),headers=request_headers)
	response = urllib2.urlopen(req)
	page = response.read()
	page = page.replace('\\x22','Xx22').replace('\\', '').replace('Xx22', '\\"')
	response_obj = json.loads(page)
	html_doc += response_obj['html'].replace('\\"', '"').encode('utf-8')

fo = open('baidu.html', 'wb')
fo.write('<!DOCTYPE html><html><head><meta http-equiv=Content-Type content="text/html;charset=utf-8"><meta http-equiv=X-UA-Compatible content="IE=edge,chrome=1"><meta content=always name=referrer><title></title></head><body>')
fo.write(html_doc);
fo.write('</body>')
fo.close()