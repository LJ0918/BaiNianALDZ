import os,sys
sys.path.append(os.getcwd())
import pytest
import allure
from Page.page_address import PageAddress
from Base.get_driver import get_driver
from Page.page_login import PageLogin
from Base.read_address import ReadYaml


# # 获取新增数据
# def get_data_new():
#     datas = ReadYaml("address.yaml").read_yaml()
#     arrs = []
#     for data in datas.get('new').values():
#         arrs.append((data.get('receipt_name'), data.get('phone'), data.get('province'), data.get('city'),
#                      data.get('region'), data.get('detail_addr'), data.get('post_code')))
#     return arrs
#
#
# # 获取修改数据
# def get_data_update():
#     datas = ReadYaml("address.yaml").read_yaml()
#     arrs = []
#     for data in datas.get('update').values():
#         arrs.append((data.get('receipt_name'), data.get('phone'), data.get('province'), data.get('city'),
#                      data.get('region'), data.get('detail_addr'), data.get('post_code'),data.get('expect_toast')))
#     return arrs

def get_data(text_type):
    datas = ReadYaml("address.yaml").read_yaml()
    arrs = []
    if text_type == 'new':
        for data in datas.get('new').values():
            arrs.append((data.get('receipt_name'), data.get('phone'), data.get('province'), data.get('city'),
                         data.get('region'), data.get('detail_addr'), data.get('post_code')))
        return arrs
    elif text_type == 'update':
        for data in datas.get('update').values():
            arrs.append((data.get('receipt_name'), data.get('phone'), data.get('province'), data.get('city'),
                         data.get('region'), data.get('detail_addr'), data.get('post_code'), data.get('expect_toast')))
        return arrs

class TestAddress():
    def setup_class(self):
        # 实例化地址管理页面
        self.address = PageAddress(get_driver())
        # 登录成功
        # 实例化登录页面
        self.login = PageLogin(get_driver())
        self.login.page_login('13331172859','123456')
        # 点击设置
        self.login.page_click_setting()
        # 点击地址管理
        self.address.page_click_address_manage()

    def teardown_class(self):
        # 退出
        self.address.driver.quit()

    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("receipt_name,phone,province,city,region,detail_addr,post_code", get_data('new'))
    def test_address(self, receipt_name, phone, province, city, region, detail_addr, post_code):
        # 点击新增地址
        self.address.page_click_new_address()
        # 输入收件人
        self.address.page_input_receipt_name(receipt_name)
        # 输入手机号
        self.address.page_input_phone(phone)
        # 选择地区
        self.address.page_click_area(province, city, region)
        # 输入详细地址
        self.address.page_input_detail_address(detail_addr)
        # 输入邮编
        self.address.page_input_post_code(post_code)
        # 设置默认地址
        self.address.page_click_address_default()
        # 点击保存
        self.address.page_click_save()
        # 断言方式一：新增地址设置默认，通过id定位取默认地址的用户名和电话
        # 因为添加的多个地址的用户名和电话 的id都是一样的，默认获取的是默认地址的信息
        # （如果新增的地址没有设置默认，那么新增成功，断言也会失败）

        # 断言方式二：find_elements获取地址管理中所有的用户名手机号的文本信息
        # base 封装个elemets方法
        # page 封装定位获取一组元素文本方法
        # 该文件中调用
        try:
            # assert receipt_name in self.address.page_get_receipt_name_phone()
            # print('新增用户名电话：',receipt_name,phone)
            info = receipt_name + '  ' + phone
            assert info in self.address.page_get_receipt_name_phone_s()
            print(self.address.page_get_receipt_name_phone_s())
        except:
            # 新增失败截图
            self.address.base_getImage()
            with open('./Image/failed.png', 'rb') as f:
                allure.attach("新增地址失败:", f.read(), allure.attach_type.PNG)
            # 抛异常
            raise

    @pytest.mark.run(order=2)
    @pytest.mark.parametrize("receipt_name,phone,province,city,region,detail_addr,post_code,expect_toast", get_data('update'))
    def test_address_change(self,receipt_name,phone,province,city,region,detail_addr,post_code,expect_toast):
        # 点击编辑
        self.address.page_click_ymtitlebar_right_btn()
        # 点击修改：默认第一个
        # self.address.page_click_modify()
        # 点击修改：列表下标
        self.address.page_click_modify_s()
        # 修改收件人
        self.address.page_input_receipt_name(receipt_name)
        # 修改电话
        self.address.page_input_phone(phone)
        # 修改所在地址
        self.address.page_click_area(province,city,region)
        # 修改详细地址
        self.address.page_input_detail_address(detail_addr)
        # 修改邮编
        self.address.page_input_post_code(post_code)
        # 点击保存
        self.address.page_click_button_send()

        try:
            """断言方式一：同新增的断言：判断修改后的用户名密码"""
            # info = receipt_name+'  '+phone
            # assert info in self.address.page_get_receipt_name_phone_s()
            # print(self.address.page_get_receipt_name_phone_s())
            """断言方式二：toast获取文本断言"""
            assert expect_toast in self.address.base_get_toast(expect_toast)
        except:
            # 修改失败截图
            self.address.base_getImage()
            with open('./Image/failed.png','rb') as f:
                allure.attach("新增地址失败:",f.read(),allure.attach_type.PNG)
            # 抛异常
            raise


    @pytest.mark.run(order=3)
    def test_address_delete(self):
        # 删除第一个地址
        # # 点击编辑
        # self.address.page_click_ymtitlebar_right_btn()
        # # 点击第一个删除
        # self.address.page_click_delete()
        # # 确认删除
        # self.address.page_click_delete_ok()
        # 删除所有地址(调用page中的方法(获取所有地址，进行循环遍历，逐个点击删除))
        self.address.page_click_delete_s()
        try:
            assert self.address.page_is_delete()
        except:
            # 截图
            self.login.base_getImage()
            with open("./Image/faild.png", "rb") as f:
                allure.attach("断言失败描述：", f.read(), allure.attach_type.PNG)
            # 抛异常
            raise

