#coding=utf-8
"""
测试用例执行的类

1、读取excel or yaml格式测试用例数据， 先读取common 页，然后读取api模板， 然后读取测试用例，
2、执行测试用例集
3、生成测试报告

"""
from core import  read_yaml
from core import common_data
import os
from unittest import  defaultTestLoader
from core.HTMLTestRunner_cn import HTMLTestRunner
import logging
import time
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
def read_data( run_path):
    """
    根据执行路径查找自动化测试用例数据
    :param run_path:
    :return:
    """
    path = os.getcwd()
    #读取全局变量
    logging.info("读取全局变量:"+path+"/../test_data/common/common.yaml")
    read_yaml.read_common(path+"/../test_data/common/common.yaml")
    #读取api模板
    logging.info("读取api模板： "+path+"/../test_data/api_template")
    read_yaml.read_api_template(path+"/../test_data/api_template")
    #读取测试用例
    logging.info("读取测试用例数据： "+run_path)
    read_yaml.read_testcase(run_path)
    #格式化成标准的测试用例
    logging.info("读取的测试用例数据标准化成框架能够识别的数据格式 ")
    read_yaml.format_data_to_testcase_list()




def run(run_path):
    read_data(run_path)
    path = os.getcwd()
    cases = defaultTestLoader.discover(path, pattern="testcase.py")
    time_str = time.strftime("%Y%m%d_%H%M%S", time.localtime())  # 生成一个年月日时分秒的时间戳
    report_path = path+"/../report/自动化测试报告"+time_str+".html"
    f = open(report_path,"wb")
    h = HTMLTestRunner(f,verbosity=2,title="接口自动化")
    h.run(cases)
    f.close()





if __name__ == '__main__':

    path = os.getcwd()

    run(path+"/../test_data//testcase")
