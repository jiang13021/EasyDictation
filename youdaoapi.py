import urllib.request
import json
#有道词典api接口
URL= 'http://fanyi.youdao.com/openapi.do?keyfrom=youdaoci&key=694691143&type=data&doctype=json&version=1.1'
#从互联网获取请求信息
def response(words):
    query =  urllib.request.urlopen(URL + '&q=' + words, timeout=10)
#返回xml页面
    return query

#将HTTPResponse 变为 dict (根据http://fanyi.youdao.com/openapi?path=data-mode 中的说明，我们得到的是一个json)
def res2dict(resu):
    return json.loads(s = resu.read(), encoding='utf-8')

def main():
    words = 'a'
    resu = response(words)
    if not resu:
        return
    print(resu.read())
    dic = res2dict(resu)
    print(dic)
if __name__=='__main__':
    main()