# coding: utf8
import sys
import unittest
from pathlib import Path
from jnp3.dict import get_with_chained_keys, append_dic
from jnp3.path import path_not_exist, get_log_dir
from jnp3.misc import deprecated, url2cn, group_by


class TestDict(unittest.TestCase):

    def test__get_with_chained_keys(self):
        dic = {
            "a": {
                "b": 2
            },
            "c": 3
        }
        # keys 为空
        #   不指定 default
        self.assertIsNone(get_with_chained_keys(dic, []))
        #   指定 default
        self.assertEqual(get_with_chained_keys(dic, [], default=-1), -1)
        # keys 只有 1 个
        #   这 1 个不存在
        #       不指定 default
        self.assertIsNone(get_with_chained_keys(dic, ["z"]))
        #       指定 default
        self.assertEqual(get_with_chained_keys(dic, ["z"], default=-1), -1)
        #   这 1 个存在
        self.assertEqual(get_with_chained_keys(dic, ["c"]), 3)
        # keys 有 2 个（多个）
        #   1 不存在，2 不存在
        self.assertIsNone(get_with_chained_keys(dic, ["z", "y"]))
        #   1 存在，2 不存在
        #       1 是个字典
        self.assertIsNone(get_with_chained_keys(dic, ["a", "z"]))
        #       1 不是字典
        self.assertIsNone(get_with_chained_keys(dic, ["c", "a"]))
        #   1 存在，2 存在
        self.assertEqual(get_with_chained_keys(dic, ["a", "b"]), 2)
        # dic 为空
        self.assertIsNone(get_with_chained_keys({}, ["a"]))

    def test__append_dic(self):
        # 这个函数是把新字典的 keys 都追加到源字典里

        # 新字典的 key 在源字典不存在
        #   源字典不为空
        dic1 = {"a": 1}
        dic2 = {"b": 2}
        append_dic(dic1, dic2)
        self.assertDictEqual(dic1, {"a": 1, "b": 2})
        #   源字典为空
        dic3 = {}
        dic4 = {"b": 2}
        append_dic(dic3, dic4)
        self.assertDictEqual(dic3, {"b": 2})
        # 新字典的 key 在源字典存在
        #   源不是字典，新不是字典
        dic5 = {"a": 1}
        dic6 = {"a": 2}
        append_dic(dic5, dic6)
        self.assertDictEqual(dic5, {"a": 2})
        #   源是字典，新不是字典
        dic7 = {"a": {"b": 2}}
        dic8 = {"a": 1}
        append_dic(dic7, dic8)
        self.assertDictEqual(dic7, {"a": 1})
        #   源不是字典，新是字典
        dic9 = {"a": 1}
        dic10 = {"a": {"b": 2}}
        append_dic(dic9, dic10)
        self.assertDictEqual(dic9, {"a": {"b": 2}})
        #   源是字典，新是字典
        dic11 = {"a": {"b": 2}}
        dic12 = {"a": {"c": 3}}
        append_dic(dic11, dic12)
        self.assertDictEqual(dic11, {"a": {"b": 2, "c": 3}})


class TestPath(unittest.TestCase):

    def test__path_not_exist(self):
        # 路径为空
        self.assertTrue(path_not_exist(""))
        if sys.platform == "win32":
            # 路径不存在
            self.assertTrue(path_not_exist("C:\\abcdefg"))
            self.assertTrue(path_not_exist(Path("C:\\abcdefg")))
            # 路径存在
            self.assertFalse(path_not_exist("C:\\Windows"))
            self.assertFalse(path_not_exist(Path("C:\\Windows")))
        elif sys.platform == "darwin":
            # 路径不存在
            self.assertTrue(path_not_exist("/tmp/abcdefg"))
            self.assertTrue(path_not_exist(Path("/tmp/abcdefg")))
            # 路径存在
            self.assertFalse(path_not_exist("/tmp"))
            self.assertFalse(path_not_exist(Path("/tmp")))
        # 不正确的类型
        self.assertTrue(path_not_exist(None))

    def test__get_log_dir(self):
        if sys.platform == "win32":
            self.assertEqual(get_log_dir(), r"C:\Users\Julian\AppData\Roaming")
        elif sys.platform == "darwin":
            self.assertEqual(get_log_dir(), "/Users/julian/Library/Application Support")


@deprecated("Use `ord`")
def char_utf8_to_unicode(char):
    """将 utf8 字符转换为 unicode

    对于 n 个字节的 utf8 编码，第一个字节的前 n 位为 1，第 n+1 位为 0，
    之后每个字节的前两位为 10，其它都是 unicode 编码

    :param char: the character
    :return: the unicode in decimal
    """
    return ord(char)


class TestMisc(unittest.TestCase):

    @deprecated("Use `chr`")
    def unicode_to_utf8_char(self, unicode):
        """将十进制 unicode 转换为 utf8 编码的字符

        :param unicode:
        :return:
        """
        return chr(unicode)

    def test_deprecated(self):
        self.assertWarns(DeprecationWarning, char_utf8_to_unicode, "a")
        self.assertWarns(DeprecationWarning, self.unicode_to_utf8_char, 97)

    def test_url2cn(self):
        url = "https://translate.google.com/?source=gtx&sl=auto&tl=en&text=%E6%9C%BA%E8%BA%AB%E8%B4%B4%E7%9D%80%E5%9C%B0%E9%9D%A2&op=translate"
        self.assertEqual(url2cn(url), "https://translate.google.com/?source=gtx&sl=auto&tl=en&text=机身贴着地面&op=translate")

    def test_group_by(self):
        group = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.assertListEqual(list(group_by(group, 2)), [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10), (11, 12)])
        self.assertListEqual(list(group_by(group, 3)), [(1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12)])
        self.assertListEqual(list(group_by(group, 4)), [(1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12)])
        self.assertListEqual(list(group_by(group, 6)), [(1, 2, 3, 4, 5, 6), (7, 8, 9, 10, 11, 12)])
        self.assertRaises(ValueError, group_by, group, 7)
