#encoding=gbk
'''
python StartApp.py --start --name="QQ Chrome"
                    -s -n QQ Chrome
python StartApp.py --kill --config=conf.xml
                    -k -c conf.xml
'''

import os
import sys
import getopt
import xml.dom.minidom
import win32api

shortopts = "hskc:n:"
longopts = ["help", "start", "kill", "name=", "config="]

operation = "start"
config = os.path.join(os.path.dirname(__file__), r"config\conf.xml")
toStart = []
auto = True
appmap = {}

# 解析命令行参数
def ParseArgs():
    try:
        options, args = getopt.getopt(sys.argv[1:], shortopts, longopts)
        for name, value in options:
            if name in ("-h", "--help"):
                print "usage:"
                print "\t python StartApp.py --start --name=QQ Chrome \n\t -s -n QQ Chrome"
                print "\t python StartApp.py --kill --config=conf.xml \n\t -k -c conf.xml"
                return False
            elif name in ("-k", "--kill"):
                global operation
                operation = "kill"
            elif name in ('-n', "--name"):
                global auto
                global toStart
                auto = False
                toStart = value.split()
            elif name in ("-c", "--config"):
                global config
                config = value
    except Exception as e:
        print "Exception: ", e
    return True

# 解析配置文件
def ParseConf():
    filetuple = []
    while True:
        # 打开xml文档
        global config
        global appmap
        global auto
        global toStart
        if config == None:
            break
        if not os.path.exists(config):
            print "配置文件不存在"
            break
        try:
            dom = xml.dom.minidom.parse(config)
            #得到文档元素对象
            root = dom.getElementsByTagName("AppSet")[0]
            apps = root.getElementsByTagName("App")
            for node in apps:
                key = node.getAttribute("name")
                appmap[key] = node.getAttribute("path")
                if auto and "True" == node.getAttribute("auto"):
                    toStart.append(key)
            break
        except Exception as e:
            print "Exception: ", e

def StartApp():
    global operation
    global appmap
    global toStart
    if "start" == operation:
        for app in toStart:
            if not appmap.has_key(app):
                print "没有配置%s"%app
            else:
                win32api.ShellExecute(0, 'open', appmap[app], '','',1)
    elif "kill" == operation:
        for app in toStart:
            if not appmap.has_key(app):
                print "没有配置%s" % app
            else:
                os.system("taskkill /F /IM %s" % os.path.basename(appmap[app]))
    
if __name__ == "__main__":
    if ParseArgs():
        ParseConf()
        StartApp()