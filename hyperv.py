#                                                                            
#                                                                            
#    EEEEEEEEEEEEEEEEEEEEEEHHHHHHHHH     HHHHHHHHHVVVVVVVV           VVVVVVVV
#    E::::::::::::::::::::EH:::::::H     H:::::::HV::::::V           V::::::V
#    E::::::::::::::::::::EH:::::::H     H:::::::HV::::::V           V::::::V
#    EE::::::EEEEEEEEE::::EHH::::::H     H::::::HHV::::::V           V::::::V
#      E:::::E       EEEEEE  H:::::H     H:::::H   V:::::V           V:::::V 
#      E:::::E               H:::::H     H:::::H    V:::::V         V:::::V  
#      E::::::EEEEEEEEEE     H::::::HHHHH::::::H     V:::::V       V:::::V   
#      E:::::::::::::::E     H:::::::::::::::::H      V:::::V     V:::::V    
#      E:::::::::::::::E     H:::::::::::::::::H       V:::::V   V:::::V     
#      E::::::EEEEEEEEEE     H::::::HHHHH::::::H        V:::::V V:::::V      
#      E:::::E               H:::::H     H:::::H         V:::::V:::::V       
#      E:::::E       EEEEEE  H:::::H     H:::::H          V:::::::::V        
#    EE::::::EEEEEEEE:::::EHH::::::H     H::::::HH         V:::::::V         
#    E::::::::::::::::::::EH:::::::H     H:::::::H          V:::::V          
#    E::::::::::::::::::::EH:::::::H     H:::::::H           V:::V           
#    EEEEEEEEEEEEEEEEEEEEEEHHHHHHHHH     HHHHHHHHH            VVV            
#                                                                            
# EasyHyperV - by Wl13Proger9
# https://github.com/Wl13proger9/EasyHyperV       
                                                                                                                                                                                                                                                                                                                      
import subprocess
import ctypes
import json




class HyperVisor:
    def __init__(self):
        def run_from_powershell(command:str, is_command:bool = True, capture_type:type = bool) -> str:
            if is_command:
                result = subprocess.run(
                [ "powershell", "-Command", command ],
                capture_output=True,
                text=True
                )   
            else:
                result = subprocess.run(
                [ "powershell", command ],
                capture_output=True,
                text=True,
                encoding="cp866" 
                )   
                return result

            if result.returncode != 0:
                raise RuntimeError(f"PowerShell error: {result.stderr.strip()}")
        

            if capture_type == bool:
                return result.stdout.strip().lower() == "true"
            

            elif capture_type == dict:
                info = {}
                for line in result.stdout.splitlines():
                    if ":" in line:
                        key, value = line.split(":", 1)
                        info[key.strip()] = value.strip()
                            
                return info 


            elif capture_type == str:
                return result.stdout.strip()


            else:return result
                  
        def run_bcdedit(command:str) -> str:
            result = subprocess.run(["bcdedit", str( command )],
            capture_output=True,text=True)

            if result.returncode != 0:
                raise RuntimeError(f"BCDEdit error: {result.stderr.strip()}")


            return result


        options = {} 
        enum_result = run_bcdedit("/enum")


        for line in enum_result.stdout.splitlines():
            parts = line.split()
            if len(parts) >= 2:
                key = parts[0]
                value = " ".join(parts[1:])
                options[key] = value


        self.toggle              = self.toggle(self)
        self.options             = options
        self.run_bcdedit         = run_bcdedit
        self.run_from_powershell = run_from_powershell
        self.secureboot_status   = run_from_powershell('Confirm-SecureBootUEFI')
        self.processor_bit       = run_from_powershell('(Get-CimInstance Win32_Processor).AddressWidth')


    def is_admin() -> bool:
        try:
            return bool( ctypes.windll.shell32.IsUserAnAdmin() )
        
        except:
            return False
        

    def supported_system(self) -> None:
        if self.processor_bit == "64":
            return True

        return False


    def check_system(self) -> dict:   
        powershell_script = r"""
$cpu        = Get-CimInstance Win32_Processor
$board      = Get-CimInstance Win32_BaseBoard
$system     = Get-CimInstance Win32_ComputerSystem

@{
    ProcessorName           = $cpu.Name
    Bit                     = $cpu.AddressWidth
    ModeExtensions          = $cpu.VMMonitorModeExtensions
    VirtualizationFirmware  = $cpu.VirtualizationFirmwareEnabled
    HypervisorPresent       = $system.HypervisorPresent
    Manufacturer            = $board.Manufacturer, $board.Product 
    SecureBoot              = Confirm-SecureBootUEFI
} | ConvertTo-Json -Compress
"""

        powershell_output = json.loads(self.run_from_powershell(f"-NoProfile -ExecutionPolicy Bypass -Command {powershell_script}", is_command=False).stdout)


        output = {
            "loadoptions":                          self.options.get("loadoptions"),                
            "hypervisorlaunchtype":                 self.options.get("hypervisorlaunchtype"),
            "locale":                               self.options.get("locale"),

            "SecureBoot":                           self.secureboot_status,
            "Manufacturer":                         powershell_output["Manufacturer"],
            "VirtualizationFirmware":               powershell_output["VirtualizationFirmware"],

            "HypervisorPresent":                    powershell_output["HypervisorPresent"],
            "ModeExtensions":                       powershell_output["ModeExtensions"],
            "ProcessorName":                        powershell_output["ProcessorName"],
            "Bit":                                  powershell_output["Bit"]
        }
        
        return output


    def get_all_bcdedit_enum(self) -> str:
        options = {}
        result = self.run_bcdedit("/enum all")

        for line in result.stdout.splitlines():
            parts = line.split()
            if len(parts) >= 2:
                key = parts[0]
                value = " ".join(parts[1:])
                options[key] = value


        return options


    class toggle:
        def __init__(self, parent):
            self.parent = parent


        def test_mode(self) -> None:
            if self.parent.options.get("testsigning", "").lower() == "yes":
                self.parent.run_bcdedit('/set testsigning off')
            else:
                self.parent.run_bcdedit('/set testsigning on')


        def integrity_checks(self) -> None:
            if self.parent.options.get("loadoptions") == 'DISABLE_INTEGRITY_CHECKS':
                self.parent.run_bcdedit('/deletevalue loadoptions')
            else: 
                self.parent.run_bcdedit('/set loadoptions DISABLE_INTEGRITY_CHECKS')


        def hypervisor_launch(self) -> None:
            if self.parent.options.get("hypervisorlaunchtype", "").lower() == "auto":
                self.parent.run_bcdedit('/set hypervisorlaunchtype off')
            else:
                self.parent.run_bcdedit('/set hypervisorlaunchtype auto')




if __name__ == "__main__":
    h = HyperVisor()

    print( h.check_system() )

    #for key in h.check_system():print(f"{ key }:    { h.check_system()[key] }")

    



