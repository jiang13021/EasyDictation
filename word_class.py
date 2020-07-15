from youdaoapi import res2dict, response
import time
import json


class Baseword:
    forgettingCurve = [ #一共8个背诵阶段 单位：秒
            0,
            5*60,            # 5分钟 
            30*60,            # 30分钟 
            12*60*60,        # 12小时 
            1*24*60*60,    # 1天
            2*24*60*60,    # 2天 
            4*24*60*60,    # 4天 
            7*24*60*60,    # 7天 
            15*24*60*60    # 15天 
    ]
    def __init__(self, inittype = 0 ,resu = None, js = None, word = None, explains = None): 
        if inittype == 0: #从HTTPResponse转换成的dict中读取信息
            self.word = resu['query'] #单词
            try:
                self.explains = resu['basic']['explains'] #释义
            except:
                self.explains = resu['translation']
            self.stage = 0 #背诵阶段
            self.lasttime = time.time() #加入时间
            self.errors = 0 #错误次数
            try:
                self.phonetic = resu['basic']['phonetic'] #音标
            except:
                self.phonetic = ''

        elif inittype == 1: #从json中读取信息
            dic = json.loads(s = js, encoding='utf-8')
            self.word = dic['word'] #单词
            self.explains = dic['explains'] #释义
            self.stage = dic['stage'] #背诵阶段
            self.lasttime = dic['lasttime'] #加入时间
            self.errors = dic['errors']
            self.phonetic = dic['phonetic'] #音标

        elif inittype == 2: #手动构造
            self.word = word #单词
            self.explains = [explains] #释义
            self.phonetic = ''
            self.stage = 0 #背诵阶段
            self.lasttime = time.time() #加入时间
            self.errors = 0
        else:
            print("Init fail")
            assert False

    def Deltstage(self):
        currentTime = time.time()
        timeDiff = currentTime - self.lasttime #单位:秒
        if self.stage < 9: #stage >= 9 时视为已经背会
            if (timeDiff > self.forgettingCurve[self.stage]): #如果超过了已知阶段的对应时长，则安排背诵
                for i in range(9):
                    if self.forgettingCurve[i] >= timeDiff:
                        return i - self.stage
        return 0

    def calImportance(self):
        alpha, beta = 0.1, 1.0
        if self.stage < 9:
            return alpha * self.errors + beta * self.Deltstage()
        else:
            return 0

    def TOdict(self): #将Baseword变为dict用于储存
        dic = {}
        dic['word'] = self.word
        dic['explains'] = self.explains
        dic['phonetic'] = self.phonetic
        dic['stage'] = self.stage
        dic['lasttime'] = self.lasttime #加入时间
        dic['errors'] = self.errors
        return dic
    def __lt__(self, other):
        return self.calImportance() < other.calImportance()


if __name__ == "__main__":
    with open('test', 'r', encoding='utf-8') as f0:
        wordlist = [Baseword(1, js = i) for i in f0.readlines()]
    print(wordlist[0].word)
