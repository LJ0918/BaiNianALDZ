from Base.base import Base
import Page


class PageAddress(Base):
    # 点击地址管理
    def page_click_address_manage(self):
        self.base_click(Page.address_manage)
    # 点击新增地址
    def page_click_new_address(self):
        self.base_click(Page.address_add_new_btn)

    # 输入收件人
    def page_input_receipt_name(self,receipt_name):
        self.base_input(Page.address_receipt_name,receipt_name)

    # 输入电话
    def page_input_phone(self,phone):
        self.base_input(Page.address_add_phone,phone)

    # 选择所在地区
    def page_click_area(self,province,city,region):
        self.base_click(Page.address_province)
        self.base_xpath_click(province)
        # 文本形式定位市（没办法定位直辖市）
        # self.base_xpath_click(city)
        # class+id形式定位直辖市
        self.base_click(Page.address_zhixiashi_father)
        self.base_click(Page.address_zhixiashi)
        self.base_xpath_click(region)
    # 详细地址
    def page_input_detail_address(self,detail_addr):
        self.base_input(Page.address_detail_addr_info,detail_addr)

    # 邮编
    def page_input_post_code(self,post_code):
        self.base_input(Page.address_post_code,post_code)

    # 点击默认地址
    def page_click_address_default(self):
        self.base_click(Page.address_default)

    # 点击保存
    def page_click_save(self,save="保存"):
        self.base_xpath_click(save)

    # 获取新增成功后的姓名电话
    def page_get_receipt_name_phone(self):
        return self.base_get_text(Page.address_receipt_name_phone)

    # 获取定位的添加地址的一组地址信息
    def page_get_receipt_name_phone_s(self):
        elements = self.base_find_elements(Page.address_receipt_name_phone)
        return [i.text for i in elements]
    """修改地址"""
    # 点击编辑
    def page_click_ymtitlebar_right_btn(self):
        self.base_click(Page.address_ymtitlebar_right_btn)

    # 点击修改：默认取第一个地址进行修改
    # def page_click_modify(self,modify="修改"):
    #     self.base_xpath_click(modify)

    # 点击修改：定位一组修改
    def page_click_modify_s(self,modify="修改"):
        # 获取一组元素
        elements = self.base_xpath_s(modify)
        # 点击一组元素中的第一个
        self.base_click_elements(elements)

    # 点击修改后的保存
    def page_click_button_send(self):
        self.base_click(Page.address_button_send)

    """删除地址"""
    # 点击删除按钮：删除第一个地址
    def page_click_delete(self,delete="删除"):
        self.base_xpath_click(delete)
    # 点击确认删除
    def page_click_delete_ok(self):
        self.base_click(Page.address_ymdialog_left_button)
    # 获取一组地址的删除文本
    def page_click_delete_s(self,delete="删除"):
        # 获取所有的地址
        elements = self.base_find_elements(Page.address_receipt_name_phone)
        # 遍历地址，逐个点击删除
        for i in range(len(elements)):
            # 点击编辑
            self.page_click_ymtitlebar_right_btn()
            # 获取所有删除元素
            elements = self.base_xpath_s(delete)
            # 点击第一个删除元素
            self.base_click_elements(elements)
            # 点击确认删除
            self.page_click_delete_ok()

    # 断言调用：获取地址中值，有值则FALSE代表删除失败，没有值在TRUE代表删除成功
    def page_is_delete(self):
        try:
            self.base_find_elements(Page.address_receipt_name_phone,timeout=3)
            return False
        except:
            return True

