import ast
import astor


class PropertyRemover(ast.NodeTransformer):
    def __init__(self):
        # 存储懒加载的属性及其对应的类
        self.lazy_properties = {}
        # 存储类实例的名称及其对应的类
        self.class_instances = {}

    def visit_ClassDef(self, node):
        # 遍历类定义，查找使用了@property的属性
        new_body = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                for decorator in item.decorator_list:
                    if isinstance(decorator, ast.Name) and decorator.id == 'property':
                        # 找到使用@property装饰器的属性
                        if node.name not in self.lazy_properties:
                            self.lazy_properties[node.name] = []
                        self.lazy_properties[node.name].append(item.name)
                        # 将装饰器移除，相当于将其还原为普通方法
                        item.decorator_list.remove(decorator)
            new_body.append(item)

        node.body = new_body
        return node

    def visit_Assign(self, node):
        # 查找类的实例化
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
            class_name = node.value.func.id
            if class_name in self.lazy_properties:
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        # 将实例名称与类名关联
                        self.class_instances[target.id] = class_name
        return self.generic_visit(node)

    def visit_Attribute(self, node):
        # 查找类的属性访问
        if isinstance(node.value, ast.Name):
            instance_name = node.value.id
            # 如果该属性属于某个懒加载类实例，将属性访问转换为方法调用
            if instance_name in self.class_instances:
                class_name = self.class_instances[instance_name]
                if node.attr in self.lazy_properties.get(class_name, []):
                    # 将属性访问（lazy.value）转换为方法调用（lazy.value()）
                    return ast.Call(func=node, args=[], keywords=[])
        return self.generic_visit(node)


def remove_property_and_transform(code):
    # 解析代码为AST
    tree = ast.parse(code)

    # 创建一个 PropertyRemover 实例
    remover = PropertyRemover()

    # 对 AST 进行转换
    transformed_tree = remover.visit(tree)

    # 将修改后的 AST 转回代码
    transformed_code = astor.to_source(transformed_tree)
    return transformed_code


# 示例代码
input_code = '''
import pymysql
from flask import Flask, request

class LazyLoad:
    def __init__(self, name):
        self._value = None  # 初始化为 None，表示值尚未加载
        self._value = name

    @property
    def value(self):
        if self._value is None:
            print("Loading value...")
            self._value = self._load_value()  # 仅在首次访问时加载
        return self._value

    def _load_value(self):
        # 模拟一个耗时的计算或数据加载过程
        return "This is the loaded value!"

if __name__ == '__main__':
    data = request.data
    # 使用示例
    lazy = LazyLoad(data)

    # 第一次访问属性时，触发加载
    print(lazy.value)  # 输出: Loading value... This is the loaded value!

    # 再次访问属性时，直接返回已加载的值
    print(lazy.value)  # 输出: This is the loaded value!
    pymysql.connect().cursor().execute(lazy.value)
'''

# 转换代码
output_code = remove_property_and_transform(input_code)
print(output_code)
