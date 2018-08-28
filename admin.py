import time
from sql import mySql
class View(object):
    app = mySql()
    # admin = '1'
    # passwd = '1'


    def printAdminView(self):
        print("***************************************************************")
        print("*                                                             *")
        print("*                                                             *")
        print("*                          兴哥银行                            *")
        print("*                                                             *")
        print("*                                                             *")
        print("***************************************************************")
    def printSysFunctionView(self):
        print("***************************************************************")
        print("*            开户(1)                        查询(2)            *")
        print("*            取款(3)                        存款(4)            *")
        print("*            转账(5)                        改密(6)            *")
        print("*            锁定(7)                        解锁(8)            *")
        print("*            补卡(9)                        销户(0)            *")
        print("*                            退出(t)                              *")
        print("************************************************************** *")
    # def adminOption(self):
    #     inputAdmin = input("请输入账号： ")
    #     if self.admin != inputAdmin:
    #         print("账号输入有误！！")
    #         return -1
    #     inputPasswd = input("请输入密码： ")
    #     if self.passwd != inputPasswd:
    #         print("密码有误！")
    #         return -1
    #     print("操作成功！")
    #     time.sleep(2)
    #     return 0
    def login(self):
        k = 3
        while k:
            k = 3
            inputUser = input("请输入账号： ")
            userinfo = "select * from user where name='%s'" % (inputUser)
            conn = self.app.fetchone(userinfo)
            #print(conn)
            if conn == '':
                print("用户名不能为空")
            elif conn == None:
                k -= 1
                if k != 0:
                    print("用户名错误，请重新输入")
                else:
                    print("你已输错三次！")
                    return -1
            else:
                break
        k = 3
        while k:
            inputPasswd = input("请输入你的密码：")
            userinfoes = "SELECT * FROM user WHERE name='%s' and pwd='%s'" % (inputUser, inputPasswd)
            conn = self.app.fetchone(userinfoes)
            if conn == '':
                print("密码不能为空")
            elif conn == None:
                k -= 1
                if k != 0:
                    print("密码错误，请重新输入")
                else:
                    print("你已输错三次！")
                    exit()
            else:
                print('操作成功')
                time.sleep(1)
                return 0








