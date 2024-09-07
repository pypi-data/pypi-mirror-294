import time
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from monisys.Managers.Systeminfo import SystemInfo


class SystemInfoCLI:
    def __init__(self):
        self.cpu_info = SystemInfo("cpu_info")
        self.kernel_info = SystemInfo("kernel_info")
        self.os_version = SystemInfo("os_version")
        self.system_info = SystemInfo("system_info")
        self.loadaverage = SystemInfo("load_average")
        self.usb_devices = SystemInfo("usb_devices")
        self.periferal_com = SystemInfo("pci_devices")
        self.uptime = SystemInfo("uptime")
        self.console = Console()

    def get_cpuinfo(self):
        address_width = self.cpu_info.get_values_by_key("address_width")
        cpu_status = self.cpu_info.get_values_by_key("cpu_status")
        current_clock_speed = self.cpu_info.get_values_by_key("current_clock_speed")
        device_id = self.cpu_info.get_values_by_key("device_id")
        logical_processors = self.cpu_info.get_values_by_key("logical_processors")
        manufacturer = self.cpu_info.get_values_by_key("manufacturer")
        max_clock_speed = self.cpu_info.get_values_by_key("max_clock_speed")
        model = self.cpu_info.get_values_by_key("model")
        number_of_cores = self.cpu_info.get_values_by_key("number_of_cores")
        processor_type = self.cpu_info.get_values_by_key("processor_type")
        socket_designation = self.cpu_info.get_values_by_key("socket_designation")

        return (
            address_width,
            cpu_status,
            current_clock_speed,
            device_id,
            logical_processors,
            manufacturer,
            max_clock_speed,
            model,
            number_of_cores,
            processor_type,
            socket_designation,
        )

    def get_kernel_info(self):
        arguments = self.kernel_info.get_values_by_key("arguments")
        device = self.kernel_info.get_values_by_key("device")
        path = self.kernel_info.get_values_by_key("path")
        version = self.kernel_info.get_values_by_key("version")

        return arguments, device, path, version

    def get_os_info(self):
        arch = self.os_version.get_values_by_key("arch")
        build = self.os_version.get_values_by_key("build")
        codename = self.os_version.get_values_by_key("major")
        minor = self.os_version.get_values_by_key("minor")
        name = self.os_version.get_values_by_key("name")
        patch = self.os_version.get_values_by_key("patch")
        platform = self.os_version.get_values_by_key("platform")
        platform_like = self.os_version.get_values_by_key("platform_like")
        version = self.os_version.get_values_by_key("version")

        return (
            arch,
            build,
            codename,
            minor,
            name,
            patch,
            platform,
            platform_like,
            version,
        )

    def get_system_info(self):
        computer_name = self.system_info.get_values_by_key("computer_name")
        cpu_brand = self.system_info.get_values_by_key("cpu_brand")
        cpu_logical_cores = self.system_info.get_values_by_key("cpu_logical_cores")
        cpu_microcode = self.system_info.get_values_by_key("cpu_microcode")
        cpu_physical_cores = self.system_info.get_values_by_key("cpu_physical_cores")
        cpu_sockets = self.system_info.get_values_by_key("cpu_sockets")
        physical_memory = self.system_info.get_values_by_key("physical_memory")
        cpu_type = self.system_info.get_values_by_key("cpu_type")

        return (
            computer_name,
            cpu_brand,
            cpu_logical_cores,
            cpu_microcode,
            cpu_physical_cores,
            cpu_sockets,
            physical_memory,
            cpu_type,
        )

    def get_load_average(self):
        totalload = self.loadaverage.get_all_data()
        onemin = totalload[0].get("average")
        fivmin = totalload[1].get("average")
        fifteenmin = totalload[2].get("average")
        return onemin, fivmin, fifteenmin

    def get_usb_devices(self):
        usbdevices = self.usb_devices.get_values_by_key("model")
        return usbdevices

    def get_peripheral_devices(self):
        peripheral_com = self.periferal_com.get_values_by_key("driver")
        return peripheral_com

    def get_cpu_uptime(self):
        uptime = self.uptime.get_all_data()
        days = uptime[0].get("days")
        hours = uptime[0].get("hours")
        minutes = uptime[0].get("minutes")
        seconds = uptime[0].get("seconds")
        total_seconds = uptime[0].get("total_seconds")
        return days, hours, minutes,seconds, total_seconds

    def display_uptime(self):
        try:
            cpu_info = self.get_cpuinfo()
            cpu_info_str = (
                f"Current Clock Speed: {cpu_info[2]}\n"
                f"Device id : {cpu_info[3]}\n"
                f"Number of cores: {cpu_info[8]}\n"
                f"Model: {cpu_info[7]}\n"
                f"Manufacturer: {cpu_info[5]}"
            )
            panel = Panel(
                "[bold]" + cpu_info_str + "[/bold]",
                title="CPU INFO",
                style="white",
                expand=False,
            )
            self.console.print(panel)
        except KeyboardInterrupt:
            print("[*] Closed")

    def display_kernel_info(self):
        try:
            kernel_info = self.get_kernel_info()
            kernel_info_string = (
                f"Arguments : {kernel_info[0]}\n"
                f"Device : {kernel_info[1]}\n"
                f"Path : {kernel_info[2]}\n"
                f"Version : {kernel_info[3]}"
            )
            panel = Panel(
                "[bold]" + kernel_info_string + "[/bold]",
                title="Kernal Info",
                style="white",
                expand=False,
            )
            self.console.print(panel)
        except KeyboardInterrupt:
            print("[*] Closed")

    def display_osinfo_info(self):
        try:
            os_info = self.get_os_info()
            os_info_str = (
                f"Arch: {os_info[0]}\n"
                f"Build : {os_info[1]}\n"
                f"Codename : {os_info[2]}\n"
                f"Minor : {os_info[3]}\n"
                f"Name : {os_info[4]}\n"
                f"Patch : {os_info[5]}\n"
                f"Platform : {os_info[6]}\n"
                f"Platform_like : {os_info[7]}\n"
                f"Version : {os_info[8]}\n"
            )
            panel = Panel(
                "[bold]" + os_info_str + "[/bold]",
                title="OS INFO",
                style="white",
                expand=False,
            )
            self.console.print(panel)
        except Exception as e:
            print(e)

    def display_system_info(self):
        try:
            system_info = self.get_system_info()
            system_info_str = (
                f"Computer Name: {system_info[0]}\n"
                f"CPU Brand : {system_info[1]}\n"
                f"CPU Logical cores : {system_info[2]}\n"
                f"CPU micro codes : {system_info[3]}\n"
                f"CPU Physical Cores  : {system_info[4]}\n"
                f"CPU Sockets : {system_info[5]}\n"
                f"Physical Memory : {system_info[6]}\n"
                f"CPU type : {system_info[7]}\n"
            )
            panel = Panel(
                "[bold]" + system_info_str + "[/bold]",
                title="System INFO",
                style="white",
                expand=False,
            )
            self.console.print(panel)
        except Exception as e:
            print(e)

    def display_loadaverage_info(self):
        try:
            loadavg_info = self.get_load_average()
            loadavg_info_str = (
                f"One Min: {loadavg_info[0]}\n"
                f"Five Min : {loadavg_info[1]}\n"
                f"Fifteen Min : {loadavg_info[2]}\n"
            )
            panel = Panel(
                "[bold]" + loadavg_info_str + "[/bold]",
                title="Loadavg INFO",
                style="white",
                expand=False,
            )
            self.console.print(panel)
        except Exception as e:
            print(e)

    def display_usb_devices(self):
        try:
            usbdevices = self.get_usb_devices()
            usbdevices_str = "\n".join(usbdevices)
            panel = Panel(
                "[bold]" + usbdevices_str + "[/bold]",
                title="USB Info",
                style="white",
                expand=False,
            )
            self.console.print(panel)
        except Exception as e:
            print(e)

    def display_peripheral_compo(self):
        try:
            peripheral_compo = self.get_peripheral_devices()
            peripheral_compo_str = "\n".join(peripheral_compo)
            panel = Panel(
                "[bold]" + peripheral_compo_str + "[/bold]",
                title="Pci Comp Info",
                style="white",
                expand=False,
            )
            self.console.print(panel)
        except Exception as e:
            print(e)

    def display_uptime(self):
        try:
            deviceuptime = self.get_cpu_uptime()
            deviceuptimestr = (
                f"Days : {deviceuptime[0]}\n"
                f"Hours : {deviceuptime[1]}\n"
                f"Minutes : {deviceuptime[2]}\n"
                f"Seconds : {deviceuptime[3]}\n"
                f"Total Seconds : {deviceuptime[4]}\n"
            )
            panel = Panel(
                "[bold]" + deviceuptimestr + "[/bold]",
                title="UP TIME",
                style="white",
                expand=False,
            )
            self.console.print(panel)
        except Exception as e:
            print(e)
