import yaml
import time
from selenium import webdriver


def startBrowser(path):
    '''
    启动浏览器
    :param path: 浏览器驱动位置
    :return: webdriver对象
    '''
    print('正在启动浏览器')
    driver = webdriver.Chrome(path)  # 实例化一个webdriver对象，参数为浏览器驱动位置
    print('浏览器启动成功')
    driver.implicitly_wait(5)  # 设置最大等待时间，防止因要查找的数据为加载而报错
    return driver


def getYamlData(path):
    '''
    读取配置文件信息
    :param path: 配置文件的路径
    :return:  配置文件的内容
    '''
    file = open(path, 'r', encoding='utf-8')  # 以只读方式打开yaml文件

    fileData = file.read()  # 读取的yaml存放的数据（string）
    userInfo = yaml.load(fileData, Loader=yaml.FullLoader)  # 使用内部函数将string转化为dict

    file.close()
    return userInfo


def login(wd, url, user, pwd):
    '''
    模拟登录
    :param wd: webdriver对象
    :param url: 登录链接
    :param user: 用户名
    :param pwd: 密码
    '''
    print('【账号：{}】登录中'.format(user))
    wd.get(url)  # 打开登录链接
    time.sleep(0.5)
    wd.find_element_by_css_selector('input[name="account_name"]').send_keys(user)  # 填写用户名
    time.sleep(0.5)
    wd.find_element_by_css_selector('input[name="user_password"]').send_keys(pwd)  # 填写密码
    time.sleep(0.5)
    wd.find_element_by_css_selector('button#login-button-1').click()  # 点击登录
    print('账号登录完成')


def enterClass(wd, teacherName, subjectName):
    '''
    根据老师姓名、课程名称进入对应的课程活动页面
    :param wd: webdriver对象
    :param teacherName: 老师姓名
    :param subjectName: 课程名称
    '''
    print('正在进入【{}】老师的【{}】课程'.format(teacherName, subjectName))
    classItems = wd.find_elements_by_css_selector('ul[data-is-loaded="Y"]>li.class-item')  # 选择所有已加入的课程
    for classItem in classItems:  # 遍历所有课程，分别获取每个课程的老师姓名、课程名称
        tName = classItem.find_element_by_css_selector('.class-info-teacher').text  # 获取老师姓名
        sName = classItem.find_element_by_css_selector('.class-info-subject').text  # 获取课程名称
        # print(tName, sName)
        if tName == teacherName and sName == subjectName:  # 如果老师姓名、课程名称均与配置文件中的一致
            classItem.click()  # 点击进入
            print('成功进入该课程')
            break


def getEvaluation(wd):
    '''
    获取 "活动" 页面中要互评的作业信息
    :param wd: webdriver对象
    :return: list，存放需要互评的作业链接
    '''
    print('正在统计要互评的作业信息')
    evaluationList = wd.find_elements_by_css_selector('.interaction-status.evaluation')  # 选择作业状态为"评分中"的所有作业，包含已互评、未互评
    evaluationAllNum = len(evaluationList)  # 互评作业总数目
    evaluationNum = 0  # 需要互评作业总数目

    urlList = []  # 存放互评作业链接

    for evaluation in evaluationList:
        evaluationWb = evaluation.find_element_by_xpath('./../..//*[10]')  # 通过经验值颜色判断该作业是否需要互评
        if evaluationWb.get_attribute('style') == 'color: rgb(236, 105, 65);':  # 红色，需要互评
            url = evaluation.find_element_by_xpath('./../../..').get_attribute('data-url')  # 获取该作业的链接
            urlList.append(url)  # 将该链接加入urlList中
            evaluationNum += 1
    print('信息统计完成，互评作业总数：【{}】，未互评个数【{}】'.format(evaluationAllNum, evaluationNum))
    return urlList


def mark(wd, url, scoreSet):
    '''
    进入作业url，进行互评
    :param wd: webdriver对象
    :param url: 作业链接
    :param scoreSet: 评分值
    '''
    js = "window.open('{}');".format(url)
    wd.execute_script(js)  # 使用selenium执行js代码，打开新的标签页

    windows = wd.window_handles  # 获取所有标签页handle值
    wd.switch_to.window(windows[-1])  # 将窗口切换到最新打开的标签页

    print("正在获取活动信息")
    topscore = wd.find_element_by_xpath(r"//div[@class='score-hint color-99']/span").get_attribute(
        'textContent')  # 该作业所设置的最高分

    scoreMaxStr = topscore.split(' ')
    scoreMax = int(scoreMaxStr[0])  # int，最高分

    print("最高分数：【{}】，设定分数为【{}】".format(scoreMax, scoreMax))

    if scoreSet > scoreMax:  # 如果设置的评分值高于该活动的最高分，则将评分值修改为该活动最高分
        print("设置的分数超过满分，已将预评分数设置为【{}】分".format(scoreMax))
        scoreSet = scoreMax

    problemItems = wd.find_elements_by_xpath(r"//span[@data-appraise-status='EACH_OTHER']")  # 选择所有打分按钮（可能包含已经打过分）
    problemList = []
    for problem in problemItems:  # 将已经打过分的筛选掉
        if problem.find_element_by_xpath('./../span[2]').get_attribute('textContent') == '请评分':
            problemList.append(problem)

    print("共找到【{}】个评分对象".format(len(problemList)))

    index = 1
    for problem in problemList:  # 依次打分
        print("正在对第【{}】个对象进行评分".format(index))
        problem.click()
        time.sleep(0.5)

        scoreXPath = r"//li[@class='item-score-point'][@data-score={}]".format(scoreSet)
        wd.find_element_by_xpath(scoreXPath).click()
        time.sleep(1)

        wd.find_element_by_xpath(r"//button[@class='button-big ensure-score']").click()
        print("第{}个对象评分完成".format(index))
        time.sleep(1)

        index += 1

    wd.close()  # 关闭当前标签页
    wd.switch_to.window(windows[-2])  # 将窗口切换到初始标签页


if __name__ == '__main__':

    userInfo = getYamlData('userData.yml')  # 读取配置文件信息

    path = userInfo['path']  # 浏览器驱动位置
    wd = startBrowser(path)  # 启动浏览器

    url = 'https://www.mosoteach.cn/web'
    user, pwd = userInfo['user'], userInfo['pwd']  # 获取登录信息（user、pwd）
    login(wd, url, user, pwd)  # 登录账户

    teacherName, subjectName = userInfo['teacherName'], userInfo['subjectName']  # 获取课程信息（teacherName，subjectName）
    enterClass(wd, teacherName, subjectName)  # 进入课程

    urlItems = getEvaluation(wd)  # 获取 "活动" 页面中要互评的作业信息
    scoreSet = userInfo['scoreSet']  # 获取评分值
    for urlItem in urlItems:
        mark(wd, urlItem, scoreSet)  # 模拟打分
        time.sleep(1)
