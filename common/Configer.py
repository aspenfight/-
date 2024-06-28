import configparser
import os
import platform

class MyConf(configparser.ConfigParser):
    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=None)

    def optionxform(self, optionstr):
        return optionstr


configHandle = MyConf()

if platform.system().lower() == 'windows':
    cpath = 'C:/ProgramData/Cabbage/'
    pathUartConfig = cpath+"ConfigFile/Device.ini"
    pathDutType = cpath+"ConfigFile/DutType.ini"
    pathRunConfig = cpath+"ConfigFile/RunConfig.ini"
    optionfilePath = cpath+"ConfigFile/Option.ini"
    pathInsideVariable = 'C:/ProgramData/Cabbage/ConfigFile/InsideVariable.ini'
    pathOutCsv = cpath+"Log"
    pathSummary = cpath+"Summary"
    sequenceFilePath = cpath+"Sequence/"
    pathSystemLog = cpath+"System log/"
    pathSystemLogBuffer = cpath+"System log/Buffer/"
    pathToolSummary = "D:/CabbageTool/SummaryLog"
    pathScript = 'D:/Cabbage_release/script/'
    pathResource = 'D:/Cabbage_release/Resources/'
else:
    mpath = '/System/Volumes/Data/vault/Cabbage/'
    pathUartConfig = mpath+"ConfigFile/Device.ini"
    pathDutType = mpath+"ConfigFile/DutType.ini"
    pathRunConfig = mpath+"ConfigFile/RunConfig.ini"
    optionfilePath = mpath+"ConfigFile/Option.ini"
    pathInsideVariable = mpath+"ConfigFile/InsideVariable.ini"
    pathOutCsv = mpath+"Log"
    pathSummary = mpath+"Summary"
    sequenceFilePath = mpath+"Sequence/"
    pathSystemLog = mpath+"System log/"
    pathSystemLogBuffer = mpath+"System log/Buffer/"
    pathToolSummary = mpath+"CabbageTool/SummaryLog"
    pathScript = '/System/Volumes/Data/vault/Cabbage/script'
    pathResource = '/System/Volumes/Data/vault/Cabbage/resource/'


