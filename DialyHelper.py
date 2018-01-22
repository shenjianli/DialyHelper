#coding=utf8
import itchat
import time
import xlrd
import datetime
import threading
import Config

# 自动回复
# 封装好的装饰器，当接收到的消息是Text，即文字消息
import RemindDB


@itchat.msg_register('Text')
def text_reply(msg):
    # 当消息不是由自己发出的时候
    if not msg['FromUserName'] == myUserName:
        # 发送一条提示给文件助手
        itchat.send_msg(u"[%s]收到好友@%s 的信息：%s\n" %
                        (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['CreateTime'])),
                         msg['User']['NickName'],
                         msg['Text']), 'filehelper')
        send_msg_to_admin(msg=msg['Text'])
        # 回复给好友
        return u'【笨鸟助手】您好，您的的信息：%s  我会转达给我的主人，谢谢使用\n' % (msg['Text'])


# 起床
def notify_getup():
    print("一天之际在于晨，起床啦")
    getup_list = RemindDB.query_sleep_remind()
    notify_wechat(Config.we_chat_hint + '一天之际在于晨，起床啦', getup_list)
    notifyMyself('骚年，上班啦，记得签到啊！')


# 签到
def notify_sign():
    print("骚年，上班啦，记得签到啊！")
    signin_list = RemindDB.query_signin_remind()
    notify_wechat(Config.we_chat_hint + "不敬业要失业！不爱岗要下岗！骚年，上班啦 ----- 签到,打卡",signin_list)
    notifyMyself('骚年，上班啦，记得签到啊！')

# 午饭
def notify_lunch():
    print("人是铁饭是钢，午饭，走起！")
    lunch_list = RemindDB.query_lunch_remind()
    notify_wechat(Config.we_chat_hint + "人是铁饭是钢 ----- 午饭", lunch_list)
    notifyMyself('人是铁饭是钢，午饭，走起！')


# 一起下班
def notify_offwork():
    print("一天最美的事，莫过于下班，下班，走起！")
    offwork_list = RemindDB.query_offwork_remind()
    notify_wechat(Config.we_chat_hint + "一天最美的事，莫过 ----- 打卡，签退，下班", offwork_list)
    notifyMyself('一天最美的事，莫过于下班，打卡，签退，走起！')


# 签退
def notify_signout():
    print("枯藤老树昏鸦，上班下班回家")
    signout_list = RemindDB.query_signout_remind()
    notify_wechat(Config.we_chat_hint + "一天最美的事，莫过 ----- 打卡，签退，下班", signout_list)
    notifyMyself('一天最美的事，莫过于下班，打卡，签退，走起！')

# 加班
def notify_extrawork():
    print("加班写代码中")
    overtime_list = RemindDB.query_overtime_remind()
    notify_wechat(Config.we_chat_hint + "加班真是炫，好处看得见 ----- 打卡，签退", overtime_list)
    notifyMyself('一天最美的事，莫过于下班，打卡，签退，走起！')


# 睡觉
def notify_sleep():
    print("垂死病中惊坐起，今日到底星期几。抬望眼，卧槽，周一。低头，完了，十点。")
    sleep_list = RemindDB.query_sleep_remind()
    notify_wechat('早睡早起，身体好，为了明天，睡觉啦！', sleep_list)


# 向微信发送消息
def notify_wechat(msg,person):
    print(msg,person)
    for p in person:
        if p == "":
            print("名字为空不进行发送")
        else:
            # 想给谁发信息，先查找到这个朋友
            users = itchat.search_friends(name= p)
            # 找到UserName
            userName = users[0]['UserName']
            # 然后给他发消息
            itchat.send(msg, toUserName=userName)


def notifyMyself(msg):
    # 向自己文件传输助手发消息
    itchat.send(msg, 'filehelper')


def notify_admin():
    notify_wechat(Config.we_chat_hint + "系统运行正常，请主人放心", Config.admin)


def send_msg_to_admin(msg):
    notify_wechat(msg, Config.admin)


class dialy_remind_thread (threading.Thread):

    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        notify_admin()
        while True:

            localtime = time.localtime(time.time())
            # 格式化成2016-03-20 11:45:39形式
            print(time.strftime("%Y-%m-%d %H:%M:%S", localtime))

            dayOfWeek = datetime.datetime.now().weekday()
            print("今天是星期", dayOfWeek + 1)

            s_hour = localtime.tm_hour
            s_min = localtime.tm_min

            print("现在时间：", s_hour, ":", s_min)

            s_hour = int(input("请输入小时："))
            s_min = int(input("请输入分钟："))

            # 每半小时通知一次
            # if (s_min == 30 or s_min == 0):
            #     notify_admin()

            if dayOfWeek == 5 or dayOfWeek == 6:
                print("今天是周末")
                time.sleep(60 * 20)

            # 进行提示
            elif Config.getup_hour == s_hour and Config.getup_min == s_min:
                notify_getup()
            elif Config.sign_hour == s_hour and Config.sign_min == s_min:
                notify_sign()
            elif Config.lunch_hour == s_hour and Config.lunch_min == s_min:
                notify_lunch()
            elif Config.offwork_hour == s_hour and Config.offwork_min == s_min:
                notify_offwork()
            elif Config.sign_out_hour == s_hour and Config.sign_out_min == s_min:
                notify_signout()
            elif Config.extra_hour == s_hour and Config.extra_min == s_min:
                notify_extrawork()
            elif Config.sleep_hour == s_hour and Config.sleep_min == s_min:
                notify_sleep()
            if s_hour < (Config.getup_hour - 1) or s_hour > (Config.sleep_hour + 1):
                time.sleep(60 * 20)
            else:
                time.sleep(20)


if __name__ == '__main__':


    ''''
    
    itchat.auto_login()

    # 获取自己的UserName
    myUserName = itchat.get_friends(update=True)[0]["UserName"]
    # 向自己文件传输助手发消息
    itchat.send(u"开始", 'filehelper')


    # 想给谁发信息，先查找到这个朋友
    users = itchat.search_friends(name=u'吴佳健')
    # 找到UserName
    userName = users[0]['UserName']
    # 然后给他发消息
    itchat.send('hello', toUserName=userName)

    #user = itchat.search_friends(name=u'吴佳健')[0]
    #user.send(u'机器人say hello')

    # 想给谁发信息，先查找到这个朋友
    users = itchat.search_friends()
    # 找到UserName
    userName = users[0]['UserName']
    # 然后给他发消息
    itchat.send('hello', toUserName=userName)

    itchat.run()'''


    itchat.auto_login()

    # 获取自己的UserName
    myUserName = itchat.get_friends(update=True)[0]["UserName"]
    # 向自己文件传输助手发消息
    itchat.send(u"系统开始运行", 'filehelper')
    print("系统开始运行")

    # 创建线程
    try:
        dialy_remind_thread = dialy_remind_thread(1988, "dialy_remind_thread")
        dialy_remind_thread.start()
    except:
        print("Error: 无法启动线程")

    itchat.run()
