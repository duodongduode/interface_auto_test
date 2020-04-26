#coding=utf-8
from unittest import  TestCase
import unittest
from core import  common_data
from core import deal_variables
from core import  db_uitls
from core import  verify_operator
import requests
import jsonpath
import json
import ddt
import logging
"""
author xhz
date 2020-04-16
"""


@ddt.ddt
class MyTestcase(TestCase):


    @ddt.data(*common_data.testcase_list)
    def test_ddt(self,case_data):
        """
        不管测试用例集的前置步骤还是测试用例的前置步骤，还是测试用例，在这里都看成一个用例
        执行的过程都是  参数化(引用替换)，执行（api 或者 sql）,比较预期结果， 变量提取

        每个用例都有名字
        {
          "name":"xxx",
          "variables":{"xx":"yy", "aa":"bb"},
          "steps":[]

        }

        用例名字格式: 文件名==setupclass==用例名字  文件名==testcase==用例名字 文件名==teardownclass==用例名字

        :param value:
        :return:
        """

        print("testcase",case_data)
        self.logger = logging.getLogger(__name__)
        self.casedata = case_data #给用例绑定一个属性主要是为了生成测试报告时，用例的名字使用

        #拿出当前用例所在的测试用例集名称
        variables = case_data.get("variables")

        #变量的变量替换
        variables_str = json.dumps(variables)
        variables_str = deal_variables.deal_varibale(variables_str)
        variables = json.loads(variables_str)

        case_name = case_data.get("name")
        suite_name = case_name.split("==")[0]
        if common_data.now_testsuite_name != None and suite_name == common_data.now_testsuite_name:
            self.ready_to_run_new_testcase(variables)
        elif common_data.now_testsuite_name == None :
            common_data.now_testsuite_name = suite_name
            self.logger.info("开始执行测试集："+ suite_name)
            self.ready_to_run_new_testsuite(variables)
        elif common_data.now_testsuite_name != None and suite_name != common_data.now_testsuite_name:
            self.logger.info("开始执行测试集："+ suite_name)
            common_data.now_testsuite_name = suite_name
            self.ready_to_run_new_testsuite(variables)

        #开始执行测试用例的步骤
        self.logger.info("开始执行测试用例："+case_name.replace("==", "_"))
        steps_data = case_data.get("steps")

        for step_data in steps_data:
            self.run_step(step_data)






    def ready_to_run_new_testsuite(self,variables):
        """
        做开始执行新测试用例集的准备工作
        1、初始化测试用例集的变量
        :return:
        """
        common_data.testsuite_vars = variables

    def ready_to_run_new_testcase(self,variables):
        """
        做开始执行新测试用例的准备工作
        1、初始化测试用例的变量
        :return:
        """
        common_data.testcase_vars =variables

    def run_step(self, step_data):
        """
        执行测试用例的步骤
        sql:
        {
        type:sql
        sql :
        verifys:[]
        extractors:[]
        }

        api:
        {
        type:api
        url:
        method:
        headers:
        cookies:
        data:
        verifys:[]
        extractors:[]
        }
        :return:
        """
        self.logger.info("执行测试用例步骤数据： "+str(step_data))
        print("执行测试用例步骤数据： ", step_data)
        if step_data.get("type") =='sql':
            self.run_sql_step(step_data)
        elif step_data.get("type")=="api":
            self.run_api_step(step_data)
        else:
            raise ("步骤类型错误， 步骤数据：",step_data)


    def run_sql_step(self,sql_step_data):
        """
        执行sql步骤，先执行引用变量值替换，执行sql语句，然后自动调用验证和参数提取
        :param sql_step_data:
        :return:
        """


        self.excute_sql(sql_step_data)


    def  run_api_step(self,api_step_data):
        """
        执行api接口调用， 变量替换， 执行接口调用，执行验证，执行参数提取
        :param api_step_data:
        :return:
        """
        self.excute_api(api_step_data)



    def run_sql_var_replace(self,sql_step_data):
        """
        替换sql语句中的引用变量
        :param sql_step_data:
        :return:
        """
        sql_step_data_temp = {}



        if sql_step_data.get("sql") != None:
            sql_operator = deal_variables.deal_varibale(sql_step_data.get("sql"))
            sql_step_data_temp["sql"] = sql_operator

        if sql_step_data.get("verifys") != None:
            verify_str = json.dumps(sql_step_data.get("verifys"))
            verify_str = deal_variables.deal_varibale(verify_str)
            sql_step_data_temp["verifys"] = json.loads(verify_str)

        if sql_step_data.get("extractors") != None:
            extractors_str = json.dumps(sql_step_data.get("extractors"))
            extractors_str = deal_variables.deal_varibale(extractors_str)
            sql_step_data_temp["extractors"] = json.loads(extractors_str)

        return sql_step_data_temp

    def excute_sql(self, sql_step_data):
        """
        执行sql步骤中的sql调用
        :param sql_step_data:
        :return:
        """
        #替换变量
        sql_step_data = self.run_sql_var_replace(sql_step_data)
        self.logger.info("步骤替换完变量后的sql步骤："+str(sql_step_data))
        print("步骤替换完变量后的sql步骤：", sql_step_data)
        #执行sql
        sql_operator = sql_step_data.get("sql")
        if sql_operator.lower().startswith("select"):
            result = db_uitls.select_data(sql_operator)
            sql_step_data["sql_result"] = result
            print("执行sql语句的结果: ", result)
            self.logger.info("执行sql语句的结果: "+ str(result))
            #执行验证
            self.run_sql_verifys(sql_step_data)
            #执行参数提取
            self.run_sql_extractors(sql_step_data)

        else:
            #执行验证
            db_uitls.insert_delete_update(sql_operator)
            #非查询不执行验证和参数提取

        print("==============================================================================")
        self.logger.info("==============================================================================")


    def run_sql_verifys(self,sql_step_data):
        """
        执行sql步骤中的验证
        :param sql_step_data:
        :return:
        """
        verifys = sql_step_data.get("verifys")
        result = sql_step_data.get("sql_result")
        if verifys != None:
            for v in verifys:
                value_path = v.get("value_path").strip(" ")
                operator = v.get("operator").strip(" ")
                expect_value = str(v.get("expect_value"))
                value_paths = value_path.split(".")
                verify_result = True
                value= ""
                if len(value_paths) == 1:
                    value = result
                    verify_result = verify_operator.verify(operator, result, expect_value)
                elif (len(value_paths) == 2):
                    value = result[int(value_paths[1])]
                    verify_result = verify_operator.verify(operator, result[int(value_paths[1])], expect_value)
                elif (len(value_paths) == 3):
                    value= result[int(value_paths[1])][int(value_paths[2])]
                    verify_result = verify_operator.verify(operator,
                                                           result[int(value_paths[1])][int(value_paths[2])],
                                                           expect_value)
                msg = "value_path: " + value_path + "\t operator:" + operator + "\t value：" + str(value) + " \t expect_value:" + expect_value
                self.logger.info("验证记录： "+ msg)
                print("验证记录： ", msg)

                self.assertTrue(verify_result)


    def run_sql_extractors(self,sql_step_data):
        """
        执行sql步骤中的参数提取
        :param sql_step_data:
        :return:
        """
        extractors = sql_step_data.get("extractors")
        result = sql_step_data.get("sql_result")

        if extractors != None:
            for e in extractors:
                try:
                    value_path = e.get("value_path").strip(" ")
                    name = e.get("name").strip(" ")
                    parameter_level = e.get("parameter_level").strip(" ")
                    value_paths = value_path.split(".")
                    if len(value_paths) == 1:
                        value =result
                    elif (len(value_paths) == 2):
                        value = result[int(value_paths[1])]
                    elif (len(value_paths) == 3):
                        value = result[int(value_paths[1])][int(value_paths[2])]
                    else:
                        value = None

                    e["real_value"] = value

                    msg =  "name:" + name+"\t value_path: " + value_path + "\t parameter_level:" + parameter_level + "\t value：" + str(value)
                    self.logger.info("参数提取："+ msg)
                    print("参数提取：", msg)

                    if parameter_level =="testcase":
                        common_data.testcase_vars[name] = value

                    if parameter_level == "testsuite":
                        common_data.testsuite_vars[name] = value

                    if parameter_level == "global":
                        common_data.testsuite_vars[name] = value
                except:
                    print(value_path," 提取参数值失败")

    def run_api_var_replace(self, api_step_data):
        """
        替换api语句中的引用变量
        :param api_step_data:
        :return:
        """
        api_step_data_temp = {}
        url = api_step_data.get("url")
        method = api_step_data.get("method")
        headers = api_step_data.get("headers")
        cookies = api_step_data.get("cookies")
        data = api_step_data.get("data")
        verifys = api_step_data.get("verifys")
        extractors = api_step_data.get("extractors")

        if url !=None:
            url = deal_variables.deal_varibale(url)

        if headers != None:
            headers_str = json.dumps(headers)
            headers_str = deal_variables.deal_varibale(headers_str)
            headers = json.loads(headers_str)

        if cookies != None:
            cookies_str = json.dumps(cookies)
            cookies_str = deal_variables.deal_varibale(cookies_str)
            cookies = json.loads(cookies_str)

        if data != None:
            data_str = json.dumps(data)
            data_str = deal_variables.deal_varibale(data_str)
            data = json.loads(data_str)

        if verifys != None:
            verify_str = json.dumps(verifys)
            verify_str = deal_variables.deal_varibale(verify_str)
            verifys = json.loads(verify_str)

        if extractors != None:
            extractor_str = json.dumps(extractors)
            extractor_str = deal_variables.deal_varibale(extractor_str)
            extractors = json.loads(extractor_str)

        api_step_data_temp["url"] =url
        api_step_data_temp["method"] = method
        api_step_data_temp["headers"] = headers
        api_step_data_temp["cookies"] = cookies
        api_step_data_temp["data"] = data
        api_step_data_temp["verifys"] = verifys
        api_step_data_temp["extractors"] = extractors

        return api_step_data_temp


    def excute_api(self, api_step_data):
        """
        执行api步骤中的api调用
        :param api_step_data:
        :return:
        """
        api_step_data  = self.run_api_var_replace(api_step_data)
        url = api_step_data.get("url")
        method = api_step_data.get("method")
        headers = api_step_data.get("headers")
        cookies = api_step_data.get("cookies")
        data = api_step_data.get("data")

        request_data = "url: "+ url+ "\n"+"method: "+method+"\n headers: "+ str(headers)+"\n cookies: "+str(cookies)+ "\n data: "+ str(data)
        self.logger.info("接口请求参数: \n"+ request_data)
        print("接口请求参数: \n", request_data)




        # 执行接口调用之前需要把接口所有的数据参数化完成
        if method.lower() == 'get':
            response = requests.get(url, params=data, headers=headers, cookies=cookies)
        elif method.lower() == 'post':
            if headers != None and headers.get("Content-type") != None and 'json' in headers.get("Content-type"):
                response = requests.post(url, json=data, headers=headers, cookies=cookies)
            else:
                response = requests.post(url, data=data, headers=headers, cookies=cookies)
        elif method.lower() == 'put':
            response = requests.put(url, data=data, headers=headers, cookies=cookies)
        else:
            response = requests.delete(url, headers=headers, cookies=cookies)

        # 执行验证方法

        code = response.status_code
        headers = response.headers
        content = response.text
        response_data = "code："+str(code)+"\n headers: "+str(headers)+"\n content: "+str(content)
        self.logger.info("响应数据: "+ response_data)
        print("响应数据: ", response_data)



        self.run_api_verifys(response, api_step_data)
        # 执行参数提取器
        self.run_api_extractors(response,api_step_data)

        print("==============================================================================")
        self.logger.info("==============================================================================")

    def run_api_verifys(self,response,api_step_data):
        """
        执行api步骤中的验证
        :param api_step_data:
        :return:
        """
        verifys = api_step_data.get("verifys")
        if verifys != None:
            for v in verifys:
                value_path = v.get("value_path")
                module = v.get("module").strip(" ")
                operator = v.get("operator").strip(" ")
                expect_value = str(v.get("expect_value")).strip(" ")
                value = self.get_value(response,module, value_path)


                result = verify_operator.verify(operator, value, expect_value)

                msg =  "value_path: "+str(value_path)+" \t module:"+module+"\t operator:"+ operator+"\t value："+str(value)+" \t expect_value:"+expect_value
                self.logger.info("执行验证：" +msg)
                print("执行验证：" ,msg)
                self.assertTrue(result,msg)

    def run_api_extractors(self,response, api_step_data):
        """
        执行api步骤中的参数提取
        :param api_step_data:
        :return:
        """
        extractors = api_step_data.get("extractors")
        if extractors != None:
            for e in extractors:
                value_path = e.get("value_path").strip(" ")
                name = e.get("name").strip(" ")
                module = e.get("module").strip(" ")
                parameter_level = e.get("parameter_level").strip(" ")

                value = self.get_value(response,module, value_path)
                e["real_value"] = value

                if parameter_level == "testcase":
                    common_data.testcase_vars[name] = value

                if parameter_level == "testsuite":
                    common_data.testsuite_vars[name] = value

                if parameter_level == "global":
                    common_data.testsuite_vars[name] = value

                msg = "name:" + name + "\t module: " + module+ "value_path: " + value_path + "\t parameter_level:" + parameter_level + "\t value：" + str(
                    value)
                self.logger.info("参数提取："+ msg)
                print("参数提取：", msg)

    def get_value(self,response,module, value_path):
        """
        根据取值方式和取值表达式获取值
        : param response  接口调用响应类实例
        :param module:   response_code,header,cookie,response_content
        :param value_path:$.XXX.YYY.zzz[0]
        :return:
        """
        if module == "response_code":
            return response.status_code


        value_path = value_path.strip(" ")

        if module == "header":
            return response.headers.get(value_path[2:])
        if module == "cookie":
            return response.cookies.get_dict().get(value_path[2:])
        if module == "response_content":
            if value_path=="$" or value_path=="$":
                return response.text
            else:
                jsondata = response.json()
                result_value = jsonpath.jsonpath(jsondata, value_path)
                if result_value == False:
                    raise Exception(value_path ," 取值表达式错误 ")
                else:
                    if len(result_value) ==1:
                        return result_value[0]
                    else:
                        return str(result_value)


if __name__ == '__main__':
    unittest.main()