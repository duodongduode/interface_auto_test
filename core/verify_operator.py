#coding=utf-8
"""
结果比较器
@author ceshixiaoxiao
2020-03-28
"""

support_operator =  [ "=","!=",">",">=","=<","<", "length","contains","not contains","none","not none" ]

def verify( operator,value, expect_value=None):
    """
    比较器
    :param value: 比较的值
    :param expect_value: 期望的值
    :param operator: 比较运算符
    :return: 返回比较的结果 true or  false
    :如果运算符错误，抛出异常
    """
    if operator not in support_operator:
        raise Exception( operator," 不是正确的比较器")

    else:
        if operator == "=":
            return equal(value,expect_value)
        elif operator == "!=":
            return not_equal(value,expect_value)
        elif operator ==">":
            return bigger(value,expect_value)
        elif operator==">=":
            return bigger_or_equal(value, expect_value)
        elif operator==">":
            return bigger(value,expect_value)
        elif operator=="=<":
            return little_or_equal(value,expect_value)
        elif operator=="<":
            return little(value, expect_value)
        elif operator =="contains":
            return contains(value,expect_value)
        elif operator == "not contains":
            return contains(value, expect_value)
        elif operator == "none":
            if value == None:
                return True
            else:
                return  False
        elif operator =="not none":
            if value == None:
                return False
            else:
                return True


def equal(value, expect_value):

    value =str(value)
    expect_value = str(expect_value)
    if value == expect_value:
        return True
    else:
        return False

def not_equal(value, expect_value):
    value = str(value)
    expect_value = str(expect_value)
    if value != expect_value:
        return True
    else:
        return False

def  contains( value, expect_value):
    value = str(value)
    expect_value = str(expect_value)
    if expect_value in value:
        return True
    else:
        return False

def  not_contains( value, expect_value):
    value = str(value)
    expect_value = str(expect_value)
    if expect_value in value:
        return False
    else:
        return True

def  bigger_or_equal( value, expect_value):
    value = int(value)
    expect_value = int(expect_value)
    if  value>=expect_value:
        return True
    else:
        return False

def  bigger( value, expect_value):
    value = int(value)
    expect_value = int(expect_value)
    if  value>expect_value:
        return True
    else:
        return False

def  little_or_equal( value, expect_value):
    value = int(value)
    expect_value = int(expect_value)
    if  value <= expect_value:
        return True
    else:
        return False

def  little( value, expect_value):
    value = int(value)
    expect_value = int(expect_value)
    if  value<expect_value:
        return True
    else:
        return False


if __name__ == '__main__':

    print(verify("not none",7,"6"))


