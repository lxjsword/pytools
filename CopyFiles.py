#encoding=gbk
'''
python CopyFiles.py --confFile=config.xml
python CopyFiles.py -c config.xml
'''

import os
import sys
import getopt
import xml.dom.minidom
import shutil

shortopts = "hc:"
longopts = ["help", "confFile="]

# 解析命令行参数
def ParseArgs():
    try:
        options, args = getopt.getopt(sys.argv[1:], shortopts, longopts)
        for name, value in options:
            if name in ("-h", "--help"):
                print "usage:"
                print "     python CopyFiles.py --confFile=config.xml"
                print "     python CopyFiles.py -c config.xml"
                return None
            elif name in ("-c", "--confFile"):
                return value
    except Exception as e:
        print "Exception: ", e

# 解析配置文件
def ParseConf(confFile):
    filetuple = []
    while True:
        # 打开xml文档
        if confFile == None:
            break
        if not os.path.exists(confFile):
            print "配置文件不存在"
            break
        try:
            dom = xml.dom.minidom.parse(confFile)
            #得到文档元素对象
            fs = dom.getElementsByTagName("FileSet")
            for node in fs:
                ft = node.getElementsByTagName("FileTuple")
                for childnode in ft:
                    src = childnode.getElementsByTagName("SrcFile")[0]
                    dest = childnode.getElementsByTagName("DestFile")[0]
                    filetuple.append((src.childNodes[0].data, dest.childNodes[0].data))
            break
        except Exception as e:
            print "Exception: ", e
    return filetuple

# 拷贝文件
def CopyFiles(filetuple):
    try:
        for tuple in filetuple:
            if not os.path.exists(tuple[0]):
                print "源文件路径%s不存在" % tuple[0]
                break
            if os.path.isfile(tuple[0]):
                shutil.copy(tuple[0], tuple[1])
            elif os.path.isdir(tuple[0]):
                shutil.copytree(tuple[0], tuple[1])  
    except Exception as e:
        print "Exception: ", e

if __name__ == "__main__":
    confFile = ParseArgs()
    filetuple = ParseConf(confFile)
    CopyFiles(filetuple)
    raw_input("输入任意字符结束...")