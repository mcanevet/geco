# GECO: OpenCore EFI Generator

## Explanation
GECO is a program that allows you to generate and EFI for OpenCore.
The purpose of this project is to create the `EFI` directory to place in the `EFI` partition of your disk or an USB key.
It is mainly an automaton of what is decribed here: https://dortania.github.io/OpenCore-Install-Guide/installer-guide/

The resulting directory will have this structure:
```
EFI
 |- BOOT
 |    BOOTX64.efi
 |- OC
    |- ACPI
    |- Drivers
    |- Kexts
    |- Resources
    |- Tools
```

## Reference
### Usage
```shell
./geco.py --path /path/to/profile
```
### Profile
A profile is a directory containing:
- a YAML file that describes the EFI,
- some SSDTs files to compile,
- some Augeas transformation to apply to the config.plist,
- optionaly a checksum file of the attended result.
#### YAML file
```yaml
---
version: "1"

opencore:
  version: "0.6.6"
  variant: "RELEASE"  # RELEASE or DEBUG
  OcBinaryData-ref: "ccf3d0c"  # git reference of https://github.com/acidanthera/OcBinaryData/

kexts:
  - source: "https://github.com/acidanthera/Lilu/releases/download/1.5.3/Lilu-1.5.3-RELEASE.zip"
    files:
      - "Lilu.kext"
  - source: "https://github.com/acidanthera/VirtualSMC/releases/download/1.2.3/VirtualSMC-1.2.3-RELEASE.zip"
    files:
      - "Kexts/VirtualSMC.kext"
      - "Kexts/SMCBatteryManager.kext"
      - "Kexts/SMCProcessor.kext"
```

### SSDTs
This files will be compiled using iasl.
```
# SSDT/SSDT-PNLF.dsl
DefinitionBlock ("", "SSDT", 2, "X230", "PNLF", 0x00000000)
{
    External (_SB_.PCI0.VID_, DeviceObj)
    External (RMCF.BKLT, IntObj)
    External (RMCF.FBTP, IntObj)
    External (RMCF.GRAN, IntObj)
    External (RMCF.LEVW, IntObj)
    External (RMCF.LMAX, IntObj)

...

}
```

## Tutorials

## How-to guides
