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





class HyperVisor:
    def __init__(self):
        def run_from_powershell(command:str, capture_type:type = bool) -> str:
            result = subprocess.run(
            [ "powershell", "-Command", command ],
            capture_output=True,
            text=True
            )          
            
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
            
    
            else:
                return result
        

        options = {}


        result = subprocess.run(
            ["bcdedit", "/enum"],
            capture_output=True,text=True,  
            )


        for line in result.stdout.splitlines():
            parts = line.split()
            if len(parts) >= 2:
                key = parts[0]
                value = " ".join(parts[1:])
                options[key] = value


        self.options             = options
        self.run_from_powershell = run_from_powershell
        self.secureboot_status   = run_from_powershell('Confirm-SecureBootUEFI')
        

    def check_system(self) -> dict:    
        output = {
            "loadoptions":                          self.options.get("loadoptions"),                
            "hypervisorlaunchtype":                 self.options.get("hypervisorlaunchtype"),
            "locale":                               self.options.get("locale"),
            "secureboot":                           self.secureboot_status,
            "VirtualizationFirmware":               self.run_from_powershell('(Get-CimInstance -ClassName Win32_Processor).VirtualizationFirmwareEnabled'),
            "Manufacturer":                        [self.run_from_powershell('Get-CimInstance Win32_BaseBoard', dict)['Manufacturer'], 
                                                    self.run_from_powershell('Get-CimInstance Win32_BaseBoard', dict)['Product']],
            "HypervisorPresent":                    self.run_from_powershell('Get-CimInstance Win32_ComputerSystem).HypervisorPresent'),
            "ModeExtensions":                       self.run_from_powershell('(Get-CimInstance Win32_Processor).VMMonitorModeExtensions'),
            "VirtualizationFirmwareEnabled":        self.run_from_powershell('(Get-CimInstance Win32_Processor).VirtualizationFirmwareEnabled'),
            "ProcessorName":                        self.run_from_powershell('(Get-CimInstance Win32_Processor).Name', str)
                                        
        }
        
        return output




if __name__ == "__main__":
    h = HyperVisor()

    print( h.check_system() )

    #for key in h.check_system():print(f"{ key }:    { h.check_system()[key] }")

    



