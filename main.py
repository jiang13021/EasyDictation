from word_class import Baseword
from youdaoapi import response, res2dict
import json
import time
#获取列表文件的信息
filename = "word_list.txt"
try:
    with open('test', 'r', encoding='utf-8') as f0:
        wordlist = [Baseword(1, js = i) for i in f0.readlines()]
except:
    wordlist = []

def PrintHelp():
    print("使用说明：")
    print("添加词汇到词库中，请输入：0")
    print("开始听写，请输入：1")
    print("保存背诵记录并退出，请输入：2")
    print("列出词库中的所有单词，请输入：3")
    print("删除某个单词，请输入：4")
    print("清空全部单词，请输入：5")
    print("查看使用说明，请输入：6")
    print("当出现\"请输入指令继续\"时，代表一次操作完成，可以继续操作")
if __name__ == "__main__":
    PrintHelp()
    while True:
        try:
            op = int(input())
            assert op >= 0 and op < 7
        except:
            print("指令无法识别")
            continue
        ########################## 0、添加词汇到词库中 ##############################
        if op == 0:
            print("请输入要添加的单词：")
            tempword = input()
            err = 0
            try:
                res = response(tempword)
                res_dic = res2dict(res)
            except:
                print("网络错误，可能接口炸了，也可能您网络不好")
                err = 1
            print(res.read())
            if res_dic['errorCode'] != 0 and err == 0:
                print("未能查到该单词")
                err = 1
            #网络查询失败 判断是否需要手动输入
            if err == 1:
                print("是否使用手动输入？如果手动输入，请输入：y, 否则按任意键继续")
                char = input()
                if char[0] == 'y' and len(char) == 1:
                    print("请输入单词及释义并用空格隔开, 例如：good 好的,良好的")
                    s = input().split()
                    try:
                        print("您要输入的单词为：" + s[0]+ '\n' + "其释义为："+str(s[1:]))
                        print("确定将该单词加入词库 请输入：y, 否则按任意键继续")
                        char = input()
                        if char == 'y':
                            wordlist.append(Baseword(2, word = s[0], explains = s[1:]))
                            print("添加成功")
                        else:
                            print("您拒绝了手动输入")
                    except:
                        print("无法识别输入")
                        pass
            #网络查询成功，将其写入wordlist
            else:
                wordlist.append(Baseword(0, resu= res_dic))
                print('添加成功')
        ########################## 1、开始听写 ######################################
        elif op == 1:
            print("您的词库中一共%d个单词"%len(wordlist))
            print("请输入您要听写的单词数量")
            try:
                num = int(input())
                assert num > 0 and num <= len(wordlist)
            except:
                print("数字输入失败，已退出听写")
                print("\n请输入指令继续")
                continue
            wordlist.sort(reverse=True)
            print("听写开始，输入#退出")
            cor, allword = 0, 0
            for i in range(1, num+1):
                print("第%d个单词:"%i)
                print(wordlist[i].explains)
                my_ans = input()
                if my_ans == wordlist[i].word:
                    print("正确！")
                    cor += 1
                    wordlist[i].stage += 1
                else:
                    if my_ans == '#':
                        print("已退出听写")
                        break
                    print("错误！给点提示")
                    print(wordlist[i].phonetic)
                    my_ans = input()
                    if my_ans == wordlist[i].word:
                        print("正确！")
                    else:
                        if my_ans == '#':
                            print("已退出听写")
                            break
                        print("错误！")
                        print("正确的单词为: "+wordlist[i].word)
                    wordlist[i].errors += 1
                wordlist[i].lasttime = time.time()
                allword += 1
            print("听写已完成，准确率"+str(cor/allword))
                
        ########################## 2、保存背诵记录并退出 ############################
        elif op == 2:
            print("您确定要保存并退出吗？如果是，请输入：y 否则按任意键取消该操作")
            char = input()
            if char == 'y':
                with open(filename, 'w', encoding='utf-8') as f1:
                    f1.writelines([json.dumps(elem.TOdict())+'\n' for elem in wordlist])
                print("已保存到 "+filename+ " 中")
                break
            else:
                print("您取消了保存并退出")
        ########################## 3、列出词库中的所有单词 ##########################
        elif op == 3:
            if len(wordlist) > 0:
                for elem in wordlist:
                    print(elem.word)
                    print(elem.explains)
            else:
                print("您的词库空空如也")
        ########################## 4、删除某个单词 #################################
        elif op == 4:
            print("请输入您要删除的单词")
            tempword = input()
            emptyflag = True
            for w in wordlist:
                if tempword == w.word:
                    emptyflag = False
                    print("您确定要删除 "+tempword+" 吗？如果是，请输入：y 否则按任意键取消该操作")
                    char = input()
                    if char == 'y':
                        wordlist.pop(wordlist.index(w))
                        print("单词 " + tempword + " 已从词库中删除")
                    else:
                        print("单词 " + tempword + " 未被删除")
                    break
            if emptyflag:
                print("单词 " + tempword + " 不在词库中")
        ########################## 5、清空全部单词 #################################
        elif op == 5:
            print("您确定要清空词库中的全部单词吗？如果是，请输入：y 否则按任意键取消该操作")
            char = input()
            if char == 'y':
                wordlist = []
                print("您的词库已经清空，如果您不保存直接退出，还有挽回的余地哦")
            else:
                print("您拒绝了清空词库")
        ########################## 6、查看使用说明 #################################
        elif op == 6:
            PrintHelp()
        print("\n请输入指令继续")
        