from monisys.Managers.systeminfocli import SystemInfoCLI
from monisys.Managers.Arguments import Arguments
system = SystemInfoCLI()

class Managers:
    def __init__(self,args:Arguments):
        self.args = args

        if self.args.hasOptions(["--cpulive"]) or self.args.hasOptions(["-ci"]):
            system.display_uptime()
        if self.args.hasOptions(["--kernal-info"]) or self.args.hasOptions(["-ki"]):
            system.display_kernel_info()
        if self.args.hasOptions(["--os-info"]) or self.args.hasOptions(["-ov"]):
            system.display_osinfo_info()
        if self.args.hasOptions(["--system-info"]) or self.args.hasOptions(["-si"]):
            system.display_system_info()
        if self.args.hasOptions(["--load-average"]) or self.args.hasOptions(["-la"]):
            system.display_loadaverage_info()
        if self.args.hasOptions(["--display-usbdevices"]) or self.args.hasOptions(["-ud"]):
            system.display_usb_devices()
        if self.args.hasOptions(["--display-peripheral_compo"]) or self.args.hasOptions(["-dp"]):
            system.display_peripheral_compo()
        if self.args.hasOptions(["--display-uptime"]) or self.args.hasOptions(["-ut"]):
            system.display_uptime()