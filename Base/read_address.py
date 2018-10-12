import yaml
import os


class ReadYaml():
    def __init__(self,filename):
        self.filepath =  os.getcwd()+os.sep+"Data"+os.sep+filename

    def read_yaml(self):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            return yaml.load(f)

    def read_yaml01(self):
        with open('../Data/address.yaml', 'r', encoding='utf-8') as f:
            return yaml.load(f)

if __name__ == '__main__':
    def get_data(text_type):
        datas = ReadYaml("address.yaml").read_yaml01()
        arrs = []
        if text_type == 'new':
            for data in datas.get('new').values():
                arrs.append((data.get('receipt_name'),data.get('phone'),data.get('province'),data.get('city'),data.get('region'),data.get('detail_addr'),data.get('post_code')))
            print(arrs)
        elif text_type == 'update':
            for data in datas.get('update').values():
                arrs.append((data.get('receipt_name'), data.get('phone'), data.get('province'), data.get('city'),
                             data.get('region'), data.get('detail_addr'), data.get('post_code'),data.get('expect_toast')))
            print(arrs)

    get_data('new')
    get_data('update')