#coding=utf-8
"""
用户自定义函数模块
@author ceshixiaoxiao
2020-03-28
"""
import random


supports_function_name = ["random_choice","random_int","random_str"]

def excute_function( function_name, parameters):
    """
    执行函数
    :param function_name:
    :param parameters:  参数列表
    :return:
    """
    if function_name not in supports_function_name:
        raise Exception( function_name,"函数名错误")
    else:
        if function_name =="random_choice":
            return random_choice(parameters)
        elif function_name=="random_int":
            return random_int(parameters)
        elif function_name == "random_str":
            return random_str(parameters)



def random_choice( parameters):
    """
    从列表中随机选择一个数据
    :param parameters:
    :return:
    """
    return random.choice(parameters)

def random_int( parameters):
    """
    从范围中随机选择一个整数
    random_int([100,200]) 随机从100-200之间取一个整数
    :param parameters:
    :return:
    """
    try:
        return random.randint( int(parameters[0]), int(parameters[1]))
    except:
        raise  Exception(  parameters ," random_int 函数参数错误")


def random_str(parameters):
    """
    随机指定长度字符串，字符是字母和数字
    :param parameters:
    :return:
    """
    try:
        randomlength = int(parameters[0])
        random_str = ''
        base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
        length = len(base_str) - 1
        for i in range(randomlength):
            random_str += base_str[random.randint(0, length)]
        return random_str
    except:
        raise Exception(parameters, "  random_str 函数参数错误")
