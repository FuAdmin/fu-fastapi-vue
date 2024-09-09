#!/bin/python
# coding: utf-8
# +-------------------------------------------------------------------
# | django-vue3-lyadmin
# +-------------------------------------------------------------------
# | Author: lybbn
# +-------------------------------------------------------------------
# | QQ: 1042594286
# +-------------------------------------------------------------------

# ------------------------------
# 系统命令封装
# ------------------------------

import platform

plat = platform.system().lower()
if plat == "windows":
    from .server import windows as myos
else:
    from .server import linux as myos


class System:

    isWindows = False

    def __init__(self):
        self.isWindows = self.isWindows()

    def isWindows(self):
        plat = platform.system().lower()
        if plat == "windows":
            return True
        return False

    def GetSystemAllInfo(self):
        """
        获取系统所有信息
        """
        data = {
            "mem": self.GetMemInfo(),
            "load_average": self.GetLoadAverage(),
            "network": self.GetNetWork(),
            "cpu": self.GetCpuInfo(1),
            "disk": self.GetDiskInfo(),
            "time": self.GetBootTime(),
            "system": self.GetSystemVersion(),
            "is_windows": self.isWindows,
        }
        return data

    def GetMemInfo(self):
        memInfo = myos.GetMemInfo()
        return memInfo

    def GetLoadAverage(self):
        data = myos.GetLoadAverage()
        return data

    def GetNetWork(self):
        data = myos.GetNetWork()
        return data

    def GetCpuInfo(self, interval=1):
        data = myos.GetCpuInfo(interval)
        return data

    def GetBootTime(self):
        data = myos.GetBootTime()
        return data

    def GetDiskInfo(self):
        data = myos.GetDiskInfo()
        return data

    def GetSystemVersion(self):
        data = myos.GetSystemVersion()
        return data
