import subprocess







class HyperVisor:
    def __init__(self):
        result = subprocess.run(
            ["bcdedit", "/enum"],
            capture_output=True,
            text=True,
            #encoding="utf-8"
            )

        options = {}

        for line in result.stdout.splitlines():
            parts = line.split()
            if len(parts) >= 2:
                key = parts[0]
                value = " ".join(parts[1:])
                options[key] = value

        secureboot = subprocess.run(
            [
                "powershell",
                "-Command",
                "Confirm-SecureBootUEFI"
            ],
            capture_output=True,
            text=True
            ).stdout.strip().lower() == "true"
        
        self.secureboot_status = secureboot
        self.options           = options


    def check_system(self) -> dict:
        
        output = {
            "loadoptions":          self.options.get("loadoptions"),                
            "hypervisorlaunchtype": self.options.get("hypervisorlaunchtype"),
            "locale":               self.options.get("locale"),
            "secureboot":           self.secureboot_status
            
        }
        
        return output





if __name__ == "__main__":
    h = HyperVisor()


    print( h.check_system() )

    for key in h.check_system():
        print(f"\n{key}:_____{h.check_system()[key]}______{type( h.check_system()[key] )}")




