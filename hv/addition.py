POWERSHELL_SYSTEM_INFO_CHECK = r"""
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

#HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management
#0x0 is True
#0x3 is False
# REGEDIT_MELTDOWN_CHECK = {
#                         'check':  r'query "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" /v FeatureSettingsOverride',
#                         'add':    r'add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" /v "FeatureSettingsOverride" /t REG_DWORD /d 0 /f', 
#                         'remove': r'add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" /v "FeatureSettingsOverride" /t REG_DWORD /d 3 /f'  
#                         }


# REGEDIT_SPECTRE_CHECK = {
#                         'check':  r'query "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" /v FeatureSettingsOverrideMask',
#                         'add':    r'add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" /v "FeatureSettingsOverrideMask" /t REG_DWORD /d 0 /f', 
#                         'remove': r'add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" /v "FeatureSettingsOverrideMask" /t REG_DWORD /d 3 /f'  
# }


REGEDIT_MELTDOWN_SPECTRE_CHECK = {
                        'check':  [
                            r'query "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" /v FeatureSettingsOverride',
                            r'query "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" /v FeatureSettingsOverrideMask'
                            ],

                        'add':   [
                            r'add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" /v "FeatureSettingsOverride" /t REG_DWORD /d 0 /f',
                            r'add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" /v "FeatureSettingsOverrideMask" /t REG_DWORD /d 0 /f'
                            ], 

                        'remove': [
                            r'add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" /v "FeatureSettingsOverride" /t REG_DWORD /d 3 /f',
                            r'add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" /v "FeatureSettingsOverrideMask" /t REG_DWORD /d 3 /f'
                            ]  
}


DEBUG_MODE = False