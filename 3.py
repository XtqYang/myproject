class Animal:
    """动物基类"""
    # 类属性：所有动物共享的默认物种
    species = "未知"
    def __init__(self, name):
        self.name = name
    @classmethod
    def create_baby(cls, name_prefix):
        """类方法：创建一个幼崽，名字带前缀"""
        # 使用 cls 引用当前类（可能是 Animal 或其子类）
        baby_name = f"{name_prefix}_宝宝"
        return cls(baby_name)  # 动态调用当前类的构造函数
    @classmethod
    def change_species(cls, new_species):
        """类方法：修改当前类及其子类的物种"""
        cls.species = new_species
# ================== 子类继承 ==================
class Dog(Animal):
    """狗类，继承自动物"""
    species = "犬科"  # 覆盖类属性
class Cat(Animal):
    """猫类，继承自动物"""
    species = "猫科"
print(f"新创建的 Dog 实例物种: {Dog.create_baby('新狗').species}")  # 输出: 宠物犬