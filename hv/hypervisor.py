#                  Sounds like Gordon Freeman's suit                                                           
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
   
from   addition import *                                                                                                                                                                                                                                                                                                                 
import subprocess
import ctypes
import json
import re




class HyperVisor:
    __version__ = "1"


    def __init__(self):
        def powershell_wrapper(command:str, is_command:bool = True, capture_type:type = bool) -> str:
            if is_command:
                result = subprocess.run(
                [ "powershell", "-Command", command ],
                capture_output=True,
                text=True,
                encoding="cp866" 
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
                  
        def bcdedit_wrapper(command:str) -> str:
            try:

                result = subprocess.run(["bcdedit", *command.split() ],
                capture_output=True,text=True)
       
                return result
            
            except Exception as e:return f"BCDEdit error: {e}"

        def cmd_wrapper(command:str) -> str:
            result = subprocess.run(
                [command],
                capture_output=True,
                text=True)

            if result.returncode != 0:
                raise RuntimeError(f"CMD error: {result.stderr.strip()}")


            return result.stdout

        def reg_wrapper(command:str, stdout:bool = True) -> str | None:
            try: 
                result = subprocess.run(
                    f"reg {command}",
                    shell=True,
                    capture_output=True,
                    text=True,
                    encoding="cp866"
                )

                if result.returncode != 0:
                    raise RuntimeError(result.stderr.strip())

                if stdout: return result.stdout  
                else:      return result

            

            except: return None

        def meltdown_spectre_protection() -> bool | str:
            try:
                protection = 0


                #Override
                override = reg_wrapper(REGEDIT_MELTDOWN_SPECTRE_CHECK['check'][0])
                if override:
                    match = re.search(r'0x[0-9a-fA-F]+', override)
                    if match:
                        code = match.group(0).lower()  
                        
                        if code == "0x0":   protection += 1
                        elif code == "0x3": protection += 0
                        else:               protection += 1


                #mask
                override_mask = reg_wrapper(REGEDIT_MELTDOWN_SPECTRE_CHECK['check'][1])
                if override_mask:
                    match = re.search(r'0x[0-9a-fA-F]+', override_mask)
                    if match:
                        code = match.group(0).lower()  
                        
                        if code == "0x0":   protection += 1
                        elif code == "0x3": protection += 0
                        else:               protection += 1


                match protection:
                    case 2: return True
                    case _: return False

            except Exception as e: return str(e)

        def debug_print(message:str) -> None:
            if DEBUG_MODE:
                print(f"DEBUG: {message}")

                

        options = {} 
        enum_result = bcdedit_wrapper("/enum")


        for line in enum_result.stdout.splitlines():
            parts = line.split()
            if len(parts) >= 2:
                key = parts[0]
                value = " ".join(parts[1:])
                options[key] = value


        #Creating keys
        if not reg_wrapper( REGEDIT_MELTDOWN_SPECTRE_CHECK['check'][0] ):  reg_wrapper( REGEDIT_MELTDOWN_SPECTRE_CHECK['add'][0] )  #Override
        if not reg_wrapper( REGEDIT_MELTDOWN_SPECTRE_CHECK['check'][1] ):  reg_wrapper( REGEDIT_MELTDOWN_SPECTRE_CHECK['add'][1] )  #OverrideMask
               
    


        self.options           = options
        self.meltdown_spectre  = REGEDIT_MELTDOWN_SPECTRE_CHECK

        self.bcdedit_wrapper     = bcdedit_wrapper
        self.powershell_wrapper  = powershell_wrapper
        self.cmd_wrapper         = cmd_wrapper
        self.reg_wrapper         = reg_wrapper
        self.debug_print         = debug_print

        self.secureboot_status           = powershell_wrapper('Confirm-SecureBootUEFI')
        self.processor_bit               = powershell_wrapper('(Get-CimInstance Win32_Processor).AddressWidth')
        self.meltdown_spectre_protection = meltdown_spectre_protection

        self.MeltdownSpectreProtection = self.MeltdownSpectreProtection(self)
        self.TestMode                  = self.TestMode(self)
        self.IntegrityChecks           = self.IntegrityChecks(self)
        self.HypervisorLaunch          = self.HypervisorLaunch(self)



    @staticmethod
    def is_admin() -> bool:
        try:
            return bool( ctypes.windll.shell32.IsUserAnAdmin() )
        except: return False

    @staticmethod   
    def reboot() -> None:
        subprocess.run(["shutdown", "/r", "/t", "0"])

    @staticmethod
    def reboot_to_bios() -> None:
        subprocess.run(["shutdown", "/r", "/fw", "/t", "0"])



    def refresh(self) -> None:
        options = {} 
        enum_result = self.bcdedit_wrapper("/enum")


        for line in enum_result.stdout.splitlines():
            parts = line.split()
            if len(parts) >= 2:
                key = parts[0]
                value = " ".join(parts[1:])
                options[key] = value

        self.options             = options
        self.secureboot_status   = self.powershell_wrapper('Confirm-SecureBootUEFI')
        self.processor_bit       = self.powershell_wrapper('(Get-CimInstance Win32_Processor).AddressWidth')

        self.debug_print("Refreshed system info.")

   
    def supported_system(self) -> bool:
        if self.processor_bit == "64":
            return True

        return False


    def system_info(self) -> dict:   
        powershell_output = json.loads(self.powershell_wrapper(f"-NoProfile -ExecutionPolicy Bypass -Command {POWERSHELL_SYSTEM_INFO_CHECK}", is_command=False).stdout)

        if self.options.get("testsigning", "").lower() == "yes":
            testsigning = True
        else: testsigning = False

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
            "Bit":                                  powershell_output["Bit"],

            "MeltdownSpectreProtection":            self.meltdown_spectre_protection(),
            "Testsigning":                          testsigning
        }
        
        return output


    def get_all_bcdedit_enum(self) -> str:
        options = {}
        result = self.bcdedit_wrapper("/enum all")

        for line in result.stdout.splitlines():
            parts = line.split()
            if len(parts) >= 2:
                key = parts[0]
                value = " ".join(parts[1:])
                options[key] = value


        return options


    class TestMode:
        def __init__(self, parent):
            self.parent = parent
    
        def __call__(self):
            if self.parent.options.get("testsigning", "").lower() == "yes":
                self.parent.bcdedit_wrapper('/set testsigning off')

                self.parent.debug_print("Setting testsigning to OFF.")
                self.parent.refresh()
            else:
                self.parent.bcdedit_wrapper('/set testsigning on')

                self.parent.debug_print("Setting testsigning to ON.")
                self.parent.refresh()


        def enable(self)-> None | str:
            try:
                self.parent.bcdedit_wrapper('/set testsigning on')

                self.parent.debug_print("Setting testsigning to ON.")
                self.parent.refresh()
            except Exception as e: return str(e)

        def disable(self) -> None | str:
            try:
                self.parent.bcdedit_wrapper('/set testsigning off')

                self.parent.debug_print("Setting testsigning to OFF.")
                self.parent.refresh()
            except Exception as e: return str(e)


    class IntegrityChecks:
        def __init__(self, parent):
            self.parent = parent
    
        def __call__(self):
            if self.parent.options.get("loadoptions") == 'DISABLE_INTEGRITY_CHECKS':
                self.parent.bcdedit_wrapper('/deletevalue loadoptions')

                self.parent.debug_print("Deleted DISABLE_INTEGRITY_CHECKS from loadoptions.")
                self.parent.refresh()
            else: 
                self.parent.bcdedit_wrapper('/set loadoptions DISABLE_INTEGRITY_CHECKS')

                self.parent.debug_print("Added DISABLE_INTEGRITY_CHECKS to loadoptions.")
                self.parent.refresh()


        def enable(self) -> None | str:
            try:
                self.parent.bcdedit_wrapper('/set loadoptions DISABLE_INTEGRITY_CHECKS')

                self.parent.debug_print("Added DISABLE_INTEGRITY_CHECKS to loadoptions.")
                self.parent.refresh()
            except Exception as e: return str(e)

        def disable(self) -> None | str:
            try:
                self.parent.bcdedit_wrapper('/deletevalue loadoptions')

                self.parent.debug_print("Deleted DISABLE_INTEGRITY_CHECKS from loadoptions.")
                self.parent.refresh()
            except Exception as e: return str(e)


    class HypervisorLaunch:
        def __init__(self, parent):
            self.parent = parent
    
        def __call__(self):
            if self.parent.options.get("hypervisorlaunchtype", "").lower() == "auto":
                self.parent.bcdedit_wrapper('/set hypervisorlaunchtype off')

                self.parent.debug_print("Set hypervisorlaunchtype to OFF.")
                self.parent.refresh()
            else:
                self.parent.bcdedit_wrapper('/set hypervisorlaunchtype auto')

                self.parent.debug_print("Set hypervisorlaunchtype to auto.")
                self.parent.refresh()


        def enable(self) -> None | str:
            try:
                self.parent.bcdedit_wrapper('/set hypervisorlaunchtype auto')

                self.parent.debug_print("Set hypervisorlaunchtype to auto.")
                self.parent.refresh()
            except Exception as e: return str(e)

        def disable(self) -> None | str:
            try:
                self.parent.bcdedit_wrapper('/set hypervisorlaunchtype off')

                self.parent.debug_print("Set hypervisorlaunchtype to OFF.")
                self.parent.refresh()
            except Exception as e: return str(e)
 

    class MeltdownSpectreProtection:
        def __init__(self, parent):
            self.parent = parent
            
        def __call__(self):
            if not self.parent.meltdown_spectre_protection():  #if False
                self.parent.reg_wrapper( self.parent.meltdown_spectre['add'][0] ) #Override
                self.parent.reg_wrapper( self.parent.meltdown_spectre['add'][1] ) #OverrideMask

                self.parent.debug_print("Set Meltdown and Spectre key to 0x0. It's True.")
                self.parent.refresh()
            else:   #if True
                self.parent.reg_wrapper( self.parent.meltdown_spectre['remove'][0] ) #Override
                self.parent.reg_wrapper( self.parent.meltdown_spectre['remove'][1] ) #OverrideMask

                self.parent.debug_print("Set Meltdown and Spectre key to 0x3. It's False.")
                self.parent.refresh()


        def enable(self) -> None | str:
            try:
                self.parent.reg_wrapper( self.parent.meltdown_spectre['add'][0] ) #Override
                self.parent.reg_wrapper( self.parent.meltdown_spectre['add'][1] ) #OverrideMask

                self.parent.debug_print("Set Meltdown and Spectre key to 0x0. It's True.")
                self.parent.refresh()
            except Exception as e: return str(e)

        def disable(self) -> None | str:
            try:
                self.parent.reg_wrapper( self.parent.meltdown_spectre['remove'][0] ) #Override
                self.parent.reg_wrapper( self.parent.meltdown_spectre['remove'][1] ) #OverrideMask

                self.parent.debug_print("Set Meltdown and Spectre key to 0x3. It's False.")
                self.parent.refresh()
            except Exception as e: return str(e)
 



if __name__ == "__main__":
    h = HyperVisor()

    print( h.meltdown_spectre_protection() )
    #print( h.system_info() )
    #for key in h.system_info():print(f"{ key }:    { h.system_info()[key] }")

    

