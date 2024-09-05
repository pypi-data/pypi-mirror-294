from dataclasses import is_dataclass, fields
from types import GenericAlias


def _from_dict(data, cls):
    if isinstance(data, list):
        # 如果是列表, 循环进行转换
        elem_type = cls.__args__[0]
        return [_from_dict(item, elem_type) for item in data]
    if not is_dataclass(cls):
        # 判断是否是 dataclass
        return data
    if isinstance(data, dict):
        # 如果是字典的, 检查各个字段递归进行转换
        field_types = {_handling_identifier(f.name): f.type for f in fields(cls)}
        return cls(**{_handling_identifier(f): _from_dict(data[f], field_types[_handling_identifier(f)]) for f in data})
    else:
        return data


def _handling_identifier(identifier: str):
    # 将横线转换为下划线
    # yml 中定义一般使用的是横线, 但是变量标识符不可以
    return identifier.replace("-", "_")


def deserialize(data, cls):
    """
    反序列化 dataclass
    Args:
        data: 数据字典，json loads 出来的
        cls: 要转的 dataclass 类名称
    """
    return _from_dict(data, cls)
