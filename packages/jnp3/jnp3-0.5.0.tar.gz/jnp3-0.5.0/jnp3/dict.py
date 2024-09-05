# coding: utf8


def get_with_chained_keys(dic: dict, keys: list, default=None):
    """
    调用 get_with_chained_keys(d, ["a", "b", "c"])
    等同于 d["a"]["b"]["c"] ，
    只不过中间任意一次索引如果找不到键，则返回 default

    :param dic: 目标字典
    :param keys: 键列表
    :param default: 找不到键时的默认返回值
    :return:
    """
    if not isinstance(dic, dict):
        return default
    if len(keys) == 0:
        return default
    k = keys[0]
    if k not in dic:
        return default
    if len(keys) == 1:
        return dic[k]
    return get_with_chained_keys(dic[k], keys[1:], default)


def append_dic(dic: dict, sub_dic: dict):
    """
    不同于 dict.update 只会简单替换（更新）最顶层的键的值，
    该函数如果发现某顶层键的值也是字典，则不会直接替换整个值（字典），
    而是尝试用新字典里该键的值更新该字典，
    对顶层下的任意一层字典，都重复该行为

    :param dic: 源字典
    :param sub_dic: 新字典
    :return:
    """
    for k in sub_dic:
        if not ((k in dic and isinstance(dic[k], dict)) and isinstance(sub_dic[k], dict)):
            # 如果新字典中的键在源字典中不存在，则直接添加该键值对
            # 如果键存在，但是源字典中该键的值不是字典，则直接替换为新字典该键的值
            # 如果是字典，但新字典中该键的值不是字典，也直接替换
            dic[k] = sub_dic[k]
            continue
        # 此时说明该键在源字典存在，且源字典和新字典中该键的值都是字典
        # 因此递归调用该函数更新该字典的键值
        append_dic(dic[k], sub_dic[k])
