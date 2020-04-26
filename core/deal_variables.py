#coding=utf-8

from core import  common_data
from core import  function
import re

def deal_varibale(source_str):
    """
    处理参数化 先处理变量 后处理函数
    :param source_str:
    :return:
    """
    # 提取变量
    re_str =  "\$\{([A-Za-z0-9_]{1,100}?)\}"
    result = re.findall(re_str, source_str)
    for r in result:
        varibale = None
        varibale = common_data.testcase_vars.get(r)
        if varibale ==None:
            varibale = common_data.testsuite_vars.get(r)
            if varibale ==None:
                varibale = common_data.global_vars.get(r)
        if varibale !=None:
            #找到要替换的变量值
            source_str = source_str.replace("${"+r+"}", str(varibale))


    # 提取函数
    re_str_function = "\$\{{(\S{1,100}?)\}}"

    functions = re.findall(re_str_function,source_str)
    for function_str in functions:

        strs =function_str.split("(")
        function_name = strs[0]
        function_vars = strs[1][0:-1].split(",")

        result = function.excute_function(function_name,function_vars)

        source_str = source_str.replace("${{" + function_str + "}}", str(result))

    return source_str




