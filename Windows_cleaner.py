"""
	###########################################################################
	#		                                                                  #
	#		Project: Windows_Cleaner                                          #
	#		                                                                  #
	#		Filename: Windows_cleaner.py                                      #
	#		                                                                  #
	#		Programmer: Vincent Holmes (Vincent_HolmesZ@outlook.com)          #
	#		                                                                  #
	#		Description: Clean the trash in your computer and you can recov   #
	#                     er it within 30 days.                               #
	#		                                                                  #
	#		Start_date: 2020-08-29                                            #
	#		                                                                  #
	#		Last_update: 2020-08-31                                           #
	#		                                                                  #
	###########################################################################
"""


import os
import shutil
import logging
import time
from json import loads, dumps


class Cleaner:
    """
        Func:
            1) find the empty directory and files, and you decide whether clean it.
            2) find the same-name file and show out the path.
            3) clean the cache in Wechat/ Chrome/ Firefox/ QQ/ DingDing.
            4) find all the Word/Excel/PPT files.
            5) keep cleaning log.
            6) restore-available within 30 days.
            7) GUI.
        
        Args:
            sector: The zone you wanna clean.
    """
    def __init__(self, sector = "c"):
        self.chosen_func = []
        self.empty_dir = []
        self.empty_files = []
        self.log = {}
        self.cache = {}
        
        # run the program
        self.catch_tree(sector)
        self.menu()
    
    # a start-up menu
    def menu(self):
        print("\t内置‘时光机’功能，删除的内容保存30天可恢复。\n")
        funcs = ["0. 恢复清理的空文件", "1. 清理空文件夹", "2. 清理空文件", "3. 清理网页缓存", "4. 清理微信缓存", "5. 清理QQ缓存", "6. 清理各个在线会议软件的缓存", "10. 清空时光机"]
        try:
            func = "!!"
            while func != "":
                func = int(input("\t你要执行的功能:\n\t\t%s\n\n" % ("\n\t\t".join(funcs))))
                self.chosen_func = self.add(self.chosen_func, func)
        except Exception as e:
            logging.debug(e)
        
        self.clean()
        
    # spider and return the path of all the files in the sector and find out all empty directories
    def catch_tree(self, sector):
        print("\n\t%s 遍历中,请稍等 %s" % ("**"*6, "**"*6))
        if len(sector) == 1:
            path = sector + ":\\"
        else:
            path = sector
        
        for dir_name,folder,file in os.walk(path):
            try:
                if len(folder) == 0 and len(file) == 0 and (not self.ignore(dir_name)):
                    self.empty_dir = self.add(self.empty_dir, dir_name)
                if ("Google" in dir_name) and ("Chrome" in dir_name) and ("Cache" in dir_name) and (not dir_name in self.cache.get("chrome")):
                    self.cache["chrome"] = self.add(self.cache["chrome"], dir_name)
                if ("Mozilla" in dir_name) and ("Firefox" in dir_name) and ("cache" in dir_name) and (not dir_name in self.cache.get("firefox")):
                    self.cache["firefox"] = self.add(self.cache["firefox"], dir_name)
                if ("360se" in dir_name) and ("Cache" in dir_name) and (not dir_name in self.cache.get("360se")):
                    self.cache["360se"] = self.add(self.cache["360se"], dir_name)
                if ("WeChat" in dir_name) and (r"\Files" in dir_name) and (not dir_name in self.cache.get("wechat")):
                    self.cache["wechat"] = self.add(self.cache["wechat"], dir_name)
                if ("FileRecv" in dir_name) and ("Tencent" in dir_name) and (not dir_name in self.cache.get("qq")):
                    self.cache["qq"] = self.add(self.cache["qq"], dir_name)
                for i in file:
                    t = "%s\%s"%(dir_name,i)
                    self.is_empty(t)
            except:
                continue
        print("\t遍历完成")
        print(self.empty)
        input(self.cache)
    
    # check if the dir is protected that need to ignore
    def ignore(self, file):
        current = os.getcwd()
        ig = current+r"\\backup\\"
        if ig in file:
            return True     # verified to be ignored
        else:
            return False    # verified not to be ignored
    
    # append a new element to the list
    def add(self, lst, e):
        """
            Func:
                append an element to the list. if the list doesn't exist, then creat a list.
                
            Args:
                lst: the list name.
                e: the element you wanna append.
        """
        try:
            lst.append(e)  # if the list exists
        except:
            lst = []       # if the list doesn't exist
            lst.append(e)
        return lst
    
    # judge whether the file is empty.
    def is_empty(self, path):
        if os.path.getsize(path) == 0:
            self.empty_files = self.add(self.empty_files, path)
    
    # make sure the path is right and log it
    def logger(self):
        t = str(time.strftime("%Y-%m-%d", time.localtime()))
        pth = ".\\backup\\%s\\empty.json" % (t)
        dic = {}
        
        # make sure the directory for logging backup is existing
        if not os.path.exists(".\\backup"):
            print("\n\tmaking directory 'backup'...")
            os.mkdir(".\\backup")
        self.log["date"] = t
        
        # logging
        if os.path.exists(".\\backup\\%s" % (t)):
            if os.path.exists(".\\backup\\%s\\empty.json" % (t)):
                mode = "r+"
            else:
                mode = "w+"
            with open(pth, mode) as f:
                if os.path.getsize(pth) == 0:
                    log = {}
                else:
                    log = loads(f.read())
            with open(pth, "w+") as f:
                for key, value in log.items():
                    if log.get(key) != self.log.get(key):
                        for i in value:
                            self.add(self.log[key], i)
                f.write(dumps(self.log))
        else:
            os.mkdir(".\\backup\\%s" % (t))
            with open(pth, "w+") as f:  
                if os.path.getsize(pth) == 0:
                    log = {}
                else:
                    log = loads(f.read())
                f.write(dumps(dict(log, **self.log)))
    
    # clean the empty directories and files
    def clean(self):
        if 0 in self.chosen_func:
            self.restore()
            print("\n\t恢复完成！")
        else:
            print("\n\t本次清理记录已被记录！")
            if 1 in self.chosen_func:
                self.log["empty_dir"] = self.empty_dir
                self.logger()
                print("\n\t开始清理~~")
                for i in self.empty_dir:
                    os.rmdir(i)
            if 2 in self.chosen_func:
                self.log["empty_files"] = self.empty_files
                self.logger()
                print("\n\t开始清理~~")
                for i in self.empty_files:
                    os.remove(i)
            #if 3 in self.chosen_func:
            
            
            print("\n\t清理完成！")
        
    # restore the files
    def restoreFile(self, file):
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
    
    # restore the directories
    def restoreDir(self, dir):
        try:
            os.mkdir(dir)
        except Exception as e:
            logging.warning("%s %s"%(e, dir))
    
    # restore the files/directories
    def restore(self):
        r_lst = os.listdir(".\\backup")  # get the backup records
        func = ["1. 空文件夹", "2. 空文件", "3. 网页缓存", "4. 微信缓存", "5. QQ缓存", "6. 各个在线会议软件的缓存"] 
        log_num = []
        content = "\n\t\t".join(["%s) %s" % (r_lst.index(i), i) for i in r_lst])
        if r_lst == []:
            print("\t无备份记录！")
        else:
            try:
                log_date = int(input("\n\t\t%s\n\n\t你要恢复的是(输入序号):" % (content)))
                s2i = "!!"
                while s2i != "":
                    s2i = input("\n\t\t%s\n\n\t你要恢复的是(输入序号):" % ("\n\t\t".join(func)))
                    if s2i == "":
                        break
                    log_num = self.add(log_num, int(s2i))
            except:
                print("\t\n非法输入，已设为默认值‘1’.")
                log_num = self.add(log_num, 1)
        
        # choose which to backup
        re_path = ".\\backup\\%s\\empty.json" % (r_lst[log_date])
        with open(re_path, "r", encoding="utf-8") as f:
            backup_log = loads(f.read())
        
        if 1 in log_num:                        # restore the empty directories
            for i in backup_log["empty_dir"]:
                self.restoreDir(i)
        if 2 in log_num:                        # restore the empty files
            for i in backup_log["empty_files"]:
                self.restoreFile(i)
        if 3 in log_num:
            pth = ".\\backup\\%s\\web_cache"%(backup_log["date"])
            for i in os.listdir(pth):
                for j in os.listdir(pth+"/"+i):
                    shutil.move(pth+"/"+i+"/"+j, self.cache[i]+"/"+j)
            os.rmdir(pth)
        if 4 in log_num:
            pth = ".\\backup\\%s\\wechat"%(backup_log["date"])
            for i in os.listdir(pth):
                shutil.move(pth+"/"+i, self.cache["wechat"])
            os.rmdir(pth)
        if 5 in log_num:
            pth = ".\\backup\\%s\\qq"%(backup_log["date"])
            for i in os.listdir(pth):
                shutil.move(pth+"/"+i, self.cache["qq"])
            os.rmdir(pth)
        if 6 in log_num:
            print("\t攻城狮正在努力中~~")
        
    
if __name__ == "__main__":
    if not os.path.exists("./log"):
        print("\tmaking directory 'log'...")
        os.mkdir("./log")
    
    logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', \
                        datefmt='%a, %d %b %Y %H:%M:%S', filename="log/debug.log", filemode='a')    # initialize the format  
    
    try:
        Cleaner(r"c")
    except Exception as e:
        logging.error(e)
    
