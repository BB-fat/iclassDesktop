from PyQt5.QtWidgets import QWidget,QMessageBox

from utils.iclass import *
from ui_py import login,list,confirm,coursewarelist
from threading import Thread

class myAPP(QWidget,login.Ui_Form):
    def __init__(self):
        super(QWidget,self).__init__()
        self.setupUi(self)
        # 连接登陆确认函数
        self.buttonBox.accepted.connect(self.login)

    def login(self):
        courseList=getCourseList(self.LineEdit.text())
        if courseList==None:
            QMessageBox.warning(self,"错误","学号有误，请重新输入",QMessageBox.Ok)
            self.show()
            self.LineEdit.clear()
        else:
            self.close()
            self.listPage=listPage(courseList)
            self.listPage.show()


class listPage(QWidget,list.Ui_Form):
    def __init__(self,courseList):
        super(QWidget,self).__init__()
        self.courseList=courseList
        self.setupUi(self)
        self.listWidget.itemDoubleClicked['QListWidgetItem*'].connect(self.clickCourse)

    def clickCourse(self,item):
        for course in self.courseList:
            if course['course_name']==item.text():
                self.coursewareList = getCoursewareList(course['course_code'])
                break
        if self.coursewareList == None:
            self.confirmBox = confirm.confirmBox('亲', '抱歉，暂无课件！')
            self.confirmBox.show()
        else:
            print(self.coursewareList)
            self.hide()
            self.downloadPage=downloadPage(self.coursewareList,self)
            self.downloadPage.show()


class downloadPage(QWidget,coursewarelist.Ui_Form):
    def __init__(self,coursewareList,father):
        self.father=father
        self.coursewareList=coursewareList
        super(QWidget,self).__init__()
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.showFather)

    def showFather(self):
        self.close()
        self.father.show()