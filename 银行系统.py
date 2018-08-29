from sql import mySql
from admin import View
from atm import ATM
import pickle
import time
import os
def main():
    #界面对象
    view = View()
    #管理员开机
    view.printAdminView()
    #view.adminOption()
    view.login()
    app = mySql()
    # with open(os.path.join(os.getcwd(), 'pwd.txt'), 'rb')as f:
    #     allUser = pickle.load(f)
    #allUser = {}
    atm = ATM(app)
    # print(allUser)

    while True:
        view.printSysFunctionView()
        #等待用户操作
        option = input("请输入您的操作： ")
        if option == '1':
            atm.createUser()
        elif option == '2':
            atm.searchUserInfo()
        elif option == '3':
            atm.getMoney()
        elif option == '4':
            atm.saveMoney()
        elif option == '5':
            atm.transferMoney()
        elif option == '6':
            atm.changePwd()
        elif option == '7':
            atm.lockUser()
        elif option == '8':
            atm.unlockUser()
        elif option == '9':
            atm.newCard()
        elif option == '0':
            atm.killUser()
        elif option == 't':
            return -1

            # if not view.adminOption():
            #     with open(os.path.join(os.getcwd(), 'pwd.txt'), 'wb')as f1:
            #         pickle.dump(allUser, f1)
            #     return -1

        time.sleep(2)

if __name__ == "__main__":
    main()