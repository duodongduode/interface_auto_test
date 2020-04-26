#coding=utf-8
from  core import  common_data
import xlrd

"""
读取excel的数据到测试用例集中
1、读取所有excel文件 common包中的数据
2、读取所有excel文件 api 模板
3、读取所有excel文件中的case ，每一个case sheet页相当于一个测试用例集，
"""


def read_common(file_path):
    """
    读取全局变量
    :param file_path:
    :return:
    """

    common_sheet = xlrd.open_workbook(file_path).sheet_by_name("common")

    row_count =common_sheet.nrows
    #从第二行开始读取数据， 第一行是表头
    for i  in range(1,row_count):
        name = str(common_sheet.cell_value(i,0))
        value = str(common_sheet.cell_value(i,1))
        if name != "":
            #添加数据到全局变量
            common_data.global_vars[name] =value




def  read_api_template(file_path):
    """
    读取api 模板
    :param file_path:
    :return:
    """
    data = xlrd.open_workbook(file_path)
    all_sheet_names = data.sheet_names()
    for name in all_sheet_names:
        name=name.strip(" ")
        if name.startswith("api"):
            #开始读取一个sheet中的api_template
            api_template_sheet_data={}
            api_sheet = data.sheet_by_name(name)
            row_count = api_sheet.nrows
            #初始化两个值
            api_template = None
            api_template_name =None
            #从第三行开始读取数据
            i=2
            while i < row_count:
                api_name = str(api_sheet.cell_value(i, 0)).strip(" ")
                if api_name != "" :
                    if api_template != None:
                        #把api添加到对应sheet的api模板字典中
                        api_template_sheet_data[api_template_name] = api_template

                    #开始一个新api模板的读取
                    api_template = {}
                    api_template_name = api_name

                elif api_template_name != None:
                    pass










def read_testcase(file_path):
    """
    读取测试用例
    :param file_path:
    :return:  返回测试用例集
    """
    pass


if __name__ == '__main__':

    read_api_template("E:\\培训\\测试小小\\培训内容\\接口自动化测试\\接口自动化用例demo.xlsx")


