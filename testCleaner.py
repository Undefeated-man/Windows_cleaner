import os
import Windows_cleaner as wc
import unittest
from json import loads, dumps

class TestCleaner(unittest.TestCase):
    """
        Func:
            Test my Windows_cleaner.py
    """    
    def __init__(self):
        self.expect = {"empty_files": [], "empty_dir": [r"D:\github\Windows_cleaner/test/test0/test1", r"D:\github\Windows_cleaner/test/test0"]}
        self.expect["empty_files"] = [r"D:\github\Windows_cleaner/test/test0/test1/%s"%i for i in range(3)]
    
    def create(self, file):
        """ create the empty files and directories """
        while 1:
            try:
                f = open(file, "a+")
                f.close()
                break
            except Exception as e:
                file_path = file.split("\\")[:-1]
                if len(file_path) == 0:
                    print("\n\t没有权限在当前目录下创建文件夹，恢复空文件夹失败！")
                    logging.warning("%s %s"%(e, i))
                    break
                print("\n\t正在恢复上一级的文件夹")
                self.restoreDir("\\".join(file_path))
    
    def test_emptyFiles(self):
        """ test the function for cleaning the empty_files """
        for i in range(3)
            self.create("./test/test0/test1/%s" % i)
        wc.Cleaner("./test")
        
        with open("./log/2020-09-18/empty.json", "r") as f:
            self.assertEqual(self.expect["empty_files"], loads(f.read())["empty_files"])
    
    def test_emptyDir(self):
        """ test the function for cleaning the empty_dirs """
        wc.Cleaner("./test")
        
        with open("./log/2020-09-18/empty.json", "r") as f:
            self.assertEqual(self.expect["empty_dir"], loads(f.read())["empty_dir"])
