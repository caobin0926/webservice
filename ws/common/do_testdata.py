# 随机生成有效手机号
import random
from faker import Faker


def phone():
    prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "150", "151", "152", "153",
               "155", "156", "157", "158", "159", "186", "187", "188"]
    return random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))


# 随机生成姓名和身份证号
class UserBase:
    def __init__(self):
        fake = Faker('zh_CN')
        dicts = {}
        for _ in range(10):
            dict1 = fake.simple_profile(sex=None)
            self.name = dict1.get('name')
            self.cardid = fake.ssn()
            dicts[self.name] = self.cardid


if __name__ == '__main__':
    print(phone())
