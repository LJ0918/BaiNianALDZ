import os,sys
sys.path.append(os.getcwd())
import pytest
import allure
from Page.page_login import PageLogin
from Base.get_driver import get_driver
from Base.read_yaml import ReadYaml

#调用读取数据方法 将读取的测试数据 按照规定的格式传值
def get_data():
    datas = ReadYaml("login.yaml").read_yaml()
    arrs=[]
    for data in datas.values():
        arrs.append((data.get('username'),data.get('password'),data.get('expect'),data.get('toast_expect')))
    return arrs


class TestLogin():
    def setup_class(self):
        # 实例化 登录页面类
        self.login=PageLogin(get_driver())
        # 点击我的
        self.login.page_click_me()
        # 点击已有账号登录
        self.login.page_click_info()

    def teardown_class(self):
        # 退出driver驱动
        self.login.driver.quit()

    # 参数化
    @pytest.mark.parametrize("username,password,expect,toast_expect",get_data())
    def test_login(self,username,password,expect,toast_expect):
        if expect:
            try:
                # 登录操作
                # self.login.page_login(username,password)
                self.login.page_input_user(username)
                self.login.page_input_pwd(password)
                self.login.page_click_login_btn()
                assert expect in self.login.page_get_nickname()
                allure.attach("登录状态：", "登录成功")
                # 退出操作
                self.login.page_login_logout()
                self.login.page_click_me()
                self.login.page_click_info()
            except:
                # 截图
                self.login.base_getImage()
                with open("./Image/failed.png","rb") as f:
                    allure.attach("登录失败描述：",f.read(),allure.attach_type.PNG)
                # 抛异常
                raise
        else:
            # 登录 不能使用登录的封装（因为逆向只有第一次需要点击我的和已有账户登录）
            # self.login.page_login(username,password)
            # 以下两个操作放到setup中（以至于正向的操作 也不能使用登录和退出的封装）
            # self.login.page_click_me()
            # self.login.page_click_info()
            self.login.page_input_user(username)
            self.login.page_input_pwd(password)
            self.login.page_click_login_btn()
            try:
                # 断言toast
                assert toast_expect in self.login.base_get_toast(toast_expect)
                allure.attach("登录状态：","逆向断言成功")
            except:
                # 截图
                self.login.base_getImage()
                with open('./Image/failed.png','rb') as f:
                    allure.attach("断言失败描述：", f.read(), allure.attach_type.PNG)
                # 抛异常
                raise



