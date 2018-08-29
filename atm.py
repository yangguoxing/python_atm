#属性：用户信息（字典）
#行为：开户、查询、取款、存款、转账、改密、锁定、解锁、补卡、销户
import random
# from card import Card
# from user import User
from sql import mySql
class ATM(object):
    app = mySql()

    def __init__(self,app):

        self.app = app
        #self.allUser = allUser #结果是一个user对象和一个card对象
    # def Card(self, cardId, cardPwd, cardMoney):
    #         self.cardId = cardId
    #         self.cardPwd = cardPwd
    #         self.cardMoney = cardMoney
    #         self.cardLock = False
    # def User(self, name, address, phone, card):
    #     self.name = name
    #     self.idCard = address
    #     self.phone = phone
    #     self.card = card
    def createUser(self):
        name = input("请输入姓名：")
        address = input("请输入身份证号：")
        phone = input("请输入电话： ")
        money = int(input("请输入预存金额： "))
        if money < 0:
            print("请输入的金额有误！！！！")
            return -1
        onePwd = input("设置密码： ")
        if not self.checkPwd(onePwd):
            print("密码输入有误！！开户失败")
            return -1
        cardStr = self.randomCardId()
        insert = "insert into user (card,pwd,name,money,address,phone) values ('%s','%s','%s',%d,'%s','%s')" % (cardStr,onePwd,name,money,address,phone)
        self.app.insertTable(insert)
        print("开户成功，卡号为: %s" %(cardStr))

    def searchUserInfo(self):
        cardNum = input("请输入卡号：")
        info = "select card,money from user where card='%s'" % (cardNum)
        user = self.app.fetchall(info)
        print(user)
        if  not user:
            print("卡号不存在！！失败")
            return -1
        # if user.card.cardLock:
        #     print("此卡已被锁定！请解锁。。。")
        #     return -1
        # if not self.checkPwd(user.card.cardPwd):
        #     print("此卡已被锁定！请解锁。。。")
        #     user.card.cardLock = True
        #     return -1
        print("卡号%s-金额%d" % (user[0][0],user[0][1]))

    def getMoney(self):
        cardNum = input("请输入卡号：")
        info = "select card,money from user where card='%s'" % (cardNum)
        user = self.app.fetchall(info)
        if  not user:
            print("卡号不存在！！取款失败。。。")
            return -1

        # if user.card.cardLock:
        #     print("此卡已被锁定！请解锁。。。")
        #     return -1
        #
        if not self.checkPwd(user[0][1]):
            print("密码有误，取款失败，卡已被锁定")
            # user.card.cardLock = True
            return -1
        money = int(input("请输入取款金额： "))
        if money < 0:
            print("输入金额有误。。。")
            return -1
        if money > user[0][1]:
            print("余额不足。。。")
            return -1
        minfo = "update user set money=money - %s where card=%s" % (money, cardNum)
        self.app.update(minfo)
        pmoney = self.app.fetchall(info)
        print("取款金额为%d, 余额为%d"  % (money, pmoney[0][1]))

    def saveMoney(self):
        cardNum = input("请输入卡号：")
        info = "select card,money from user where card='%s'" % (cardNum)
        user = self.app.fetchall(info)
        if not user:
            print("卡号不存在！！取款失败。。。")
            return -1

        # if user.card.cardLock:
        #     print("此卡已被锁定！请解锁。。。")
        #     return -1
        #
        if not self.checkPwd(user[0][1]):
            print("密码有误，存款失败，卡已被锁定")
            # user.card.cardLock = True
            return -1

        money = int(input("请输入存款金额： "))
        if money < 0:
            print("输入金额有误。。。")
            return -1
        minfo = "update user set money=money + %s where card=%s" % (money, cardNum)
        self.app.update(minfo)
        pmoney = self.app.fetchall(info)
        print("取款金额为%d, 余额为%d" % (money, pmoney[0][1]))

    def transferMoney(self):
        cardNum = input("请输入卡号：")
        info = "select card,name,money from user where card='%s'" % (cardNum)
        user = self.app.fetchall(info)
        if not user:
            print("卡号不存在！！取款失败。。。")
            return -1
        # if user.card.cardLock:
        #     print("此卡已被锁定！请解锁。。。")
        #     return -1
        transferNum = input("请输入对方卡号： ")
        toinfo = "select card,name,money from user where card='%s'" % (transferNum)
        touser = self.app.fetchall(toinfo)
        if not touser:
            print("卡号不存在！！存款失败。。。")
            return -1
        transferMoney = int(input("请输入转账金额： "))
        if transferMoney < 0:
            print("输入金额有误。。。")
            return -1
        if not self.checkPwd(user[0][1]):
            print("密码有误，存款失败，卡已被锁定")
            # user.card.cardLock = True
            return -1
        print('转账到%s，Y确认，N取消' % (touser[0][1]))
        ok = input("Y确认，N取消:  ")
        if ok == 'N':
            print("转账已取消")
            return -1
        minfo = "update user set money=money - %s where card=%s" % (transferMoney, cardNum)
        tinfo = "update user set money=money + %s where card=%s" % (transferMoney, transferNum)
        self.app.update(minfo)
        self.app.update(tinfo)
        pmoney = self.app.fetchall(info)
        tomoney = self.app.fetchall(toinfo)
        #print(pmoney,tomoney)
        print('转账到%s已完成, 余额为%d,对方余额为%d' % (transferMoney ,pmoney[0][2], tomoney[0][2]))
#改密码
    def changePwd(self):
        cardNum = input("请输入卡号：")
        info = "select card,pwd,name from user where card='%s'" % (cardNum)
        user = self.app.fetchall(info)
        if not user:
            print("卡号不存在！！")
        if not self.checkPwd(user[0][1]):
            print("原密码输入有误，改密失败！！！")
            return -1
        newpwd = input("请输入新密码：")
        twopwd = input("请确认新密码：")
        if  newpwd != twopwd:
            print("俩次密码输入不一致，改密失败")
            return -1
        newinfo = "update user set pwd=%s where card=%s" % (newpwd, cardNum)
        self.app.update(newinfo)
        print("改密成功")
    # def lockUser(self):
    #     cardNum = input("请输入卡号：")
    #     info = "select card,name,money from user where card='%s'" % (cardNum)
    #     user = self.app.fetchall(info)
    #     if not user:
    #         print("卡号不存在！！锁卡失败")
    #         return -1
    #     if user.card.cardLock:
    #         print("此卡已被锁定！请解锁。。。")
    #         return -1
    #     if not self.checkPwd(user.card.cardPwd):
    #         print("密码有误，锁卡失败！！！")
    #         return -1
    #
    #     tempId = input("请输入身份证号：")
    #     if tempId != user.idCard:
    #         print("身份证号输入有误，锁卡失败！！！")
    #         return -1
    #     user.card.cardLock = True
    #     print("锁卡成功！！")

#     def unlockUser(self):
#         cardNum = input("请输入卡号：")
#         user = self.allUser.get(cardNum)
#         if not user:
#             print("卡号不存在！！解卡失败")
#             return -1
#         if not user.card.cardLock:
#             print("此卡没有锁定！无需解锁。。。")
#             return -1
#         if not self.checkPwd(user.card.cardPwd):
#             print("密码有误，解卡失败！！！")
#             return -1
#
#         tempId = input("请输入身份证号：")
#         if tempId != user.idCard:
#             print("身份证号输入有误，解卡失败！！！")
#             return -1
#
#         user.card.cardLock = False
#         print("解锁成功")
#
    def newCard(self):
        address = input("请输入身份：")
        info = "select card,pwd,name,address from user where address='%s'" % (address)
        user = self.app.fetchall(info)
        if not user:
            print("身份不存在！！")
        self.createUser()
        killinfo = "delete from user where address=%s" % (address)
        self.app.delete(killinfo)

    def killUser(self):
        cardNum = input("请输入卡号：")
        info = "select card,pwd,name from user where card='%s'" % (cardNum)
        user = self.app.fetchall(info)
        if not user:
            print("卡号不存在！！")
        if not self.checkPwd(user[0][1]):
            print("原密码输入有误，改密失败！！！")
            return -1
        print('确认要销户%s-name: %s，Y确认，N取消' % (user[0][0], user[0][2]))
        ok = input("Y确认，N取消:  ")
        if ok == 'N':
            print("已取消")
            return -1
        killinfo = "delete from user where card=%s" % (cardNum)
        self.app.delete(killinfo)
        print("已销户%s" % (cardNum))

    def checkPwd(self, realPwd):
        for i in range(3):
            tempPwd = input("请输入密码：")
            if tempPwd == realPwd:
                return True
        return False

    def randomCardId(self):
        while True:
            str = ""
            for i in range(6):
                ch = chr(random.randrange(ord('0'), ord('9') + 1))
                str += ch
            return str
