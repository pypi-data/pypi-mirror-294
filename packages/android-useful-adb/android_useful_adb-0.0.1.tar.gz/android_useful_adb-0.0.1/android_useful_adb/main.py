from libs.apk import APK
from libs.adb_base import AdbBase
from libs._aapt import AAPT

class UsefulAdb:
    def __init__(self,device=None,package_name = None,activity = None,apk_path=None) -> None:
        self.adb = AdbBase(device=device,package_name=package_name,activity=activity)
        self.aapt = AAPT(self.adb)
        self.apk = APK(apk_path)
        self.init_apk()
    
    def init_apk(self):
        if self.aapt.check_aapt():
            return
        self.aapt.push_aapt_arm_pie()
        self.aapt.chmod_aapt()
