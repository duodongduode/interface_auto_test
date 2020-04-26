#coding=utf-8
"""
存放用户的数据
全局变量
用例集变量
用例变量
"""
#全局变量
global_vars={}

#用例集变量，每个用例集运行时会初始化
testsuite_vars={}

#用例变量，每个用例执行时会初始化
testcase_vars={}


#api template的模板集合
api_template_dic = {}

#testsuite测试用例集数据保存的集合
testsuite_dic = {}

#testsuite测试用例集数据保存的集合
testsuite_list = []

#测试用例数据
testcase_list=[]

#当前执行的测试用例集名字,其实就是用例集的文件名
now_testsuite_name= None