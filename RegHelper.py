#encoding:gbk
from _winreg import *
import sys
import getopt
import xml.dom.minidom

shortopts = "c:"
longopts = ["conf="]

def ParseArgs():
    try:
        options, args = getopt.getopt(sys.argv[1:], shortopts, longopts)
        for name, value in options:
            if name in ("-c", "--conf"):
                return value
    except Exception as e:
        print "Exception: ", e

class RegMgr:
    def __init__(self, config_file_path):
        self._config_file_path = config_file_path
        self.opmap = {}

    def _ConvertKeyType(self, keystr):
        keyTypeMap = {
            "HKEY_CLASSES_ROOT": HKEY_CLASSES_ROOT,
            "HKEY_CURRENT_CONFIG": HKEY_CURRENT_CONFIG,
            "HKEY_CURRENT_USER": HKEY_CURRENT_USER,
            "HKEY_DYN_DATA": HKEY_DYN_DATA,
            "HKEY_LOCAL_MACHINE": HKEY_LOCAL_MACHINE,
            "HKEY_PERFORMANCE_DATA": HKEY_PERFORMANCE_DATA,
            "HKEY_USERS": HKEY_USERS,
        }
        return keyTypeMap[keystr]

    def _ReConvertRegValueType(self, type):
        valueTypeMap = {
            "REG_NONE":REG_NONE,
            "REG_SZ":REG_SZ,
            "REG_EXPAND_SZ":REG_EXPAND_SZ,
            "REG_BINARY":REG_BINARY,
            "REG_DWORD":REG_DWORD,
            "REG_DWORD_BIG_ENDIAN":REG_DWORD_BIG_ENDIAN,
            "REG_LINK":REG_LINK,
            "REG_MULTI_SZ":REG_MULTI_SZ
        }
        return valueTypeMap[type]

    def _ConvertRegValueType(self, type):
        valueTypeMap = {
            REG_NONE: "REG_NONE",
            REG_SZ: "REG_SZ",
            REG_EXPAND_SZ: "REG_EXPAND_SZ",
            REG_BINARY: "REG_BINARY",
            REG_DWORD: "REG_DWORD",
            REG_DWORD_BIG_ENDIAN: "REG_DWORD_BIG_ENDIAN",
            REG_LINK: "REG_LINK",
            REG_MULTI_SZ: "REG_MULTI_SZ"
        }
        return valueTypeMap[type]

    def _ReadRegValue(self):
        try:
            regargs = self.opmap["ReadValues"]
            for reg in regargs:
                rootkey = reg[0]
                subkey = reg[1]
                valuenames = reg[2].split(',')
                print "rootkey=" + rootkey + "\nsubkey=" + subkey
                key = OpenKey(self._ConvertKeyType(rootkey), subkey, 0, KEY_ALL_ACCESS)
                print "Operate: ReadRegValue"
                for valuename in valuenames:
                    value, type = QueryValueEx(key, valuename)
                    regtype = self._ConvertRegValueType(type)
                    print "\tvaluename=" + valuename + "\n\tvaluetype=" + \
                          regtype + "\n\tvalue=" + str(value)
                CloseKey(key)
        except Exception as e:
            print "Exception:", e

    def _CreateKey(self):
        try:
            regargs = self.opmap["CreateKey"]
            for reg in regargs:
                rootkey = reg[0]
                subkey = reg[1]
                keynames = reg[2].split(',')
                print "rootkey=" + rootkey + "\nsubkey=" + subkey
                key = OpenKey(self._ConvertKeyType(rootkey), subkey)
                print "Operate: CreateKey"
                for keyname in keynames:
                    CreateKey(key, keyname)
                    print "\tkeyname=" + keyname
                CloseKey(key)
        except Exception as e:
            print "Exception:", e

    def _SetKeyValue(self):
        try:
            regargs = self.opmap["SetKeyValue"]
            for reg in regargs:
                rootkey = reg[0]
                subkey = reg[1]
                print "rootkey=" + rootkey + "\nsubkey=" + subkey
                key = OpenKey(self._ConvertKeyType(rootkey), subkey, 0, KEY_ALL_ACCESS)
                values = reg[2].split(',')
                print "Operate: SetKeyValue"
                for value in values:
                    v = value.split('|')
                    SetValueEx(key, v[0], 0, self._ReConvertRegValueType(v[2]), v[1])
                    print "\tvaluename=" + v[0] + "\n\tvaluetype=" + \
                              v[2]+ "\n\tvalue=" + v[1]
                CloseKey(key)
        except Exception as e:
            print "Exception:", e

    def _DelKeyValue(self):
        try:
            regargs = self.opmap["DelKeyValue"]
            for reg in regargs:
                rootkey = reg[0]
                subkey = reg[1]
                print "rootkey=" + rootkey + "\nsubkey=" + subkey
                key = OpenKey(self._ConvertKeyType(rootkey), subkey, 0, KEY_ALL_ACCESS)
                values = reg[2].split(',')
                print "Operate: DeleteKeyValue"
                for value in values:
                    DeleteValue(key, value)
                    print "\tvaluename=" + value
                CloseKey(key)
        except Exception as e:
            print "Exception:", e

    def _DelKey(self):
        try:
            regargs = self.opmap["DelKey"]
            for reg in regargs:
                rootkey = reg[0]
                subkey = reg[1]
                print "rootkey=" + rootkey + "\nsubkey=" + subkey
                key = OpenKey(self._ConvertKeyType(rootkey), subkey, 0, KEY_ALL_ACCESS)
                values = reg[2].split(',')
                print "Operate: DeleteKey"
                for value in values:
                    DeleteKey(key, value)
                    print "\tkeyname=" + value
                CloseKey(key)
        except Exception as e:
            print "Exception:", e

    def DoOperate(self):
        self._ReadRegValue()
        self._CreateKey()
        self._SetKeyValue()
        self._DelKeyValue()
        self._DelKey()


    def _Parse(self, regops, keyname, name):
        regargs = []
        try:
            ops = regops.getElementsByTagName(keyname)
            for op in ops:
                reg = []
                tagkey = op.getElementsByTagName("Key")
                keyvalue = tagkey[0].childNodes[0].data
                reg.append(keyvalue)
                #print keyvalue
                tagkey = op.getElementsByTagName("SubKey")
                keyvalue = tagkey[0].childNodes[0].data
                reg.append(keyvalue)
                #print keyvalue
                tagkey = op.getElementsByTagName(name)
                keyvalue = tagkey[0].childNodes[0].data
                reg.append(keyvalue)
                #print keyvalue
                regargs.append(reg)
            self.opmap[keyname] = regargs
        except Exception as e:
            print "Exception: ", e

    def ConfigParse(self):
        try:
            #打开xml文档
            if self._config_file_path == None:
                print "配置文件不存在"
                return
            dom = xml.dom.minidom.parse(self._config_file_path)
            # 得到文档元素对象
            regops = dom.getElementsByTagName("RegOperates")[0]
            # 读取
            self._Parse(regops, "ReadValues", "ValueName")
            # 创建键
            self._Parse(regops, "CreateKey", "KeyName")
            # 创建键值
            self._Parse(regops, "SetKeyValue", "Value")
            # 删除值
            self._Parse(regops, "DelKeyValue", "Value")
            # 删除键
            self._Parse(regops, "DelKey", "KeyName")
        except Exception as e:
            print "Exception: ", e

    
if __name__ == '__main__':
    print 'Hello lxjsword!\n'

    conffile = ParseArgs()
    mgr = RegMgr(conffile)
    mgr.ConfigParse()
    mgr.DoOperate()
    raw_input("输入任意字符结束...")
    
