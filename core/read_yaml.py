#coding=utf-8
from  core import  common_data
import yaml
import os
from copy import deepcopy
"""
读取excel的数据到测试用例集中
1、读取所有yaml文件 common文件夹中的数据中的数据
2、读取所有yaml文件  api_template 文件夹中的api 模板
3、读取所有yaml文件  testcase文件夹中的case ，每一个文件就是一个测试用例集
"""


def read_common(file_path):

    """
    读取全局变量
    :param file_path:
    :return:
    """
    data = _read_yaml_file(file_path)

    common_data.global_vars.update(data)



def  read_api_template(api_dir):
    """
    读取api 模板
    :param api_dir: api文件夹
    :return:
    """

    datas = os.walk(api_dir)
    for  path, dirs,file_names in  datas:
        for file_name in file_names:
            if file_name.endswith("yaml"):
                #按照api模板的方式读取文档
                api_data = _read_yaml_file(path+"/"+file_name)
                #遍历返回数组中的接口
                for api  in api_data:
                    if api.get("api_template") != None:
                        api_name = api.get("api_template").get("name")
                        #添加一个api模板到api集合中,对应的api key是 file_name_apiname
                        common_data.api_template_dic[file_name+"_"+api_name] = api.get("api_template")




def read_testcase(file_path):
    """
    读取测试用例
    :param file_path:
    :return:  返回测试用例集
    """
    if os.path.isfile( file_path):
        # 按照测试用例的方式读取文档
        testcase_data = _read_yaml_file(file_path)
        file_name_paths = os.path.split(file_path)
        file_name = file_name_paths[ len(file_name_paths)-1]
        common_data.testsuite_dic[file_name] = testcase_data
    else:
        datas = os.walk(file_path)
        for path, dirs, file_names in datas:
            for file_name in file_names:
                if file_name.endswith("yaml"):
                    # 按照测试用例的方式读取文档
                    testcase_data = _read_yaml_file(path + "/" + file_name)
                    common_data.testsuite_dic[file_name] = testcase_data


def _read_yaml_file(file_path):
    """
    读取yaml格式的文档，返回一个字典
    :param file_path:
    :return:
    """
    f =None
    try:
        f = open(file_path,'r', encoding='utf-8')
        cont = f.read()
    except:
        raise  Exception(file_path, " 文件路径不存在或者打不开")
    finally:
        if f:
            f.close()

    try:
        data = yaml.load(cont)
        return data
    except:
        raise Exception(file_path, " 文件中的内容yaml格式不正确")




def format_data_to_testcase_list():
    """
    把测试用例的数据格式化成  测试用例类能够执行的语句

    用例的名字是 文件名==setupclass==用例名字  文件名==testcase==用例名字 文件名==teardownclass==用例名字

    setupclass  teardownclass用例独立成一个用例

    setup  teardown的操作步骤整理到测试用例中

    :return:
    """
    for key in common_data.testsuite_dic.keys():
        testsuite_data = common_data.testsuite_dic.get(key)
        test_suite_name = key
        setup_case_data = None
        teardown_case_data =None

        #先找出setup 和teardown
        for case in testsuite_data:
            if "setup" in case.keys():
                casedata = case.get("setup")
                setup_case_data = _parase_case_data(casedata)

            elif "teardown" in case.keys():
                casedata = case.get("teardown")
                teardown_case_data = _parase_case_data(casedata)


        for case in testsuite_data:
            """
            """
            if "setupclass" in case.keys():
                casedata  = case.get("setupclass")
                testcase = _parase_case_data(casedata)
                print(test_suite_name,testcase.get("name") )
                case_name = test_suite_name+"=="+"setupclass"+"=="+testcase.get("name")
                testcase["name"] = case_name
                common_data.testcase_list.append(testcase)

            elif "testcase" in case.keys():
                variables={}
                steps =[]

                if setup_case_data != None:
                    v = setup_case_data.get("variables")
                    variables.update(v)

                    steps_temp = deepcopy(setup_case_data.get("steps"))
                    steps.extend(steps_temp)

                casedata = case.get("testcase")
                testcase_temp = _parase_case_data(casedata)
                case_name = test_suite_name + "==" + "testcase" + "==" + testcase_temp.get("name")
                variables.update(testcase_temp.get("variables"))
                steps.extend(testcase_temp.get("steps"))

                if teardown_case_data != None:
                    v = teardown_case_data.get("variables")
                    variables.update(v)
                    steps_temp = deepcopy(teardown_case_data.get("steps"))
                    steps.extend(steps_temp)

                testcase = {
                    "name":case_name,
                    "variables":variables,
                    "steps":steps
                }
                common_data.testcase_list.append(testcase)


            elif "teardownclass" in case.keys():
                casedata = case.get("teardownclass")
                testcase = _parase_case_data(casedata)
                case_name = test_suite_name + "==" + "teardownclass" + testcase.get("name")
                testcase["name"] = case_name
                common_data.testcase_list.append(testcase)


def _parase_case_data(case_data):
    """
    解析测试用例数据
    :param case_data:
    :return:
    """
    variables = {}
    steps = []
    name = ""
    for data in case_data:

        if "variable" in data.keys():
            variables.update(data.get("variable"))

        if "step" in data.keys():
            step_data = data.get("step")
            step = _parase_step(step_data)
            steps.append(step)

        if "name" in data.keys():
            name =data.get("name")


    case_data_temp = {
        "name":name,
        "variables":variables,
        "steps":steps
    }

    return  case_data_temp





def _parase_step(step_data):
    """
    解析测试用例步骤
    :param step_data:
    :return:
    """
    if "api" == step_data.get("type"):

        url = ""
        headers = {}
        cookies = {}
        method = ""
        data = {}
        verifys = []
        extractors = []

        api_name = step_data.get("api")
        #更新api里面的设置
        if api_name != None:
            #print("api_name", api_name)
            api_data = common_data.api_template_dic.get(api_name)
            if api_data !=None:
                url = api_data.get("url")
                if api_data.get("header") !=None:
                    headers.update(api_data.get("header"))
                if api_data.get("cookie") != None:
                    cookies.update(api_data.get("cookie"))
                method = api_data.get("method")
                if api_data.get("data")!=None:
                    data_temp = api_data.get("data")
                    data = deepcopy(data_temp) #拷贝一份新的，防止出错

                if api_data.get("verify") !=None:
                    verifys.extend(api_data.get("verify"))
                if api_data.get("extractor") != None:
                    extractors.extend(api_data.get("extractor"))
            else:
                raise Exception(api_name ," 找不到对应的api——name, 请检查引用的api是否正确")

        #更新用例步骤里面的设置
        if step_data.get("url") !=None:
            url = step_data.get("url")
        if step_data.get("header") != None:
            headers.update(step_data.get("header"))
        if step_data.get("cookie")!=None:
            cookies.update(step_data.get("cookie"))
        if step_data.get("method") !=None:
            method = step_data.get("method")
        if (cookies.get("Content-Type") !=None and cookies.get("Content-Type")=="application/json") :
            #如果传递是json格式数据 用例里面的数据格式直接替换api中的数据，
            if step_data.get("data") != None:
                data = step_data.get("data")
        else:
            if step_data.get("data") !=None:
                data.update(step_data.get("data"))



        if step_data.get("verify")!=None:
            verifys.extend(step_data.get("verify"))
        if step_data.get("extractor") != None:
            extractors.extend(step_data.get("extractor"))
        name = step_data.get("name")

        api_step_data_temp={}
        api_step_data_temp["url"] = url
        api_step_data_temp["method"] = method
        api_step_data_temp["headers"] = headers
        api_step_data_temp["cookies"] = cookies
        api_step_data_temp["data"] = data
        api_step_data_temp["verifys"] = verifys
        api_step_data_temp["extractors"] = extractors
        api_step_data_temp["type"] = "api"

        return api_step_data_temp
    elif "sql" == step_data.get("type"):
        name = step_data.get("name")
        sql = step_data.get("sql")
        verify = step_data.get("verify")
        extractor= step_data.get("extractor")

        sql_step_data_temp = {}
        sql_step_data_temp["sql"] = sql
        sql_step_data_temp["verifys"] = verify
        sql_step_data_temp["extractors"] =extractor
        sql_step_data_temp["type"] ="sql"
        return sql_step_data_temp




if __name__ == '__main__':
    read_testcase("E:\\培训\\测试小小\\培训内容\\接口自动化测试\\interface_autotest_with_excel\\test_data\\testcase")
    print(common_data.testsuite_dic)

