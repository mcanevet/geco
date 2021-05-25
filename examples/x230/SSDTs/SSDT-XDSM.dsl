/*
 * Intel ACPI Component Architecture
 * AML/ASL+ Disassembler version 20200925 (64-bit version)
 * Copyright (c) 2000 - 2020 Intel Corporation
 * 
 * Disassembling to symbolic ASL+ operators
 *
 * Disassembly of SSDT-XDSM.aml, Tue May 25 21:04:28 2021
 *
 * Original Table Header:
 *     Signature        "SSDT"
 *     Length           0x000002A0 (672)
 *     Revision         0x02
 *     Checksum         0xB5
 *     OEM ID           "X230"
 *     OEM Table ID     "XDSM"
 *     OEM Revision     0x00000000 (0)
 *     Compiler ID      "INTL"
 *     Compiler Version 0x20180427 (538444839)
 */
DefinitionBlock ("", "SSDT", 2, "X230", "XDSM", 0x00000000)
{
    External (_SB_.PCI0.EXP1, DeviceObj)
    External (_SB_.PCI0.EXP1.XDSM, MethodObj)    // 4 Arguments
    External (_SB_.PCI0.EXP3, DeviceObj)
    External (_SB_.PCI0.EXP3.XDSM, MethodObj)    // 4 Arguments
    External (_SB_.PCI0.IGBE, DeviceObj)
    External (_SB_.PCI0.IGBE.XDSM, MethodObj)    // 4 Arguments
    External (_SB_.PCI0.LPC_, DeviceObj)
    External (_SB_.PCI0.LPC_.XDSM, MethodObj)    // 4 Arguments
    External (_SB_.PCI0.SAT1, DeviceObj)
    External (_SB_.PCI0.SAT1.XDSM, MethodObj)    // 4 Arguments
    External (_SB_.PCI0.SMBU, DeviceObj)
    External (_SB_.PCI0.SMBU.XDSM, MethodObj)    // 4 Arguments
    External (_SB_.PCI0.XHCI, DeviceObj)
    External (_SB_.PCI0.XHCI.XDSM, MethodObj)    // 4 Arguments

    If (!_OSI ("Darwin"))
    {
        Scope (\_SB.PCI0.LPC)
        {
            Method (_DSM, 4, NotSerialized)  // _DSM: Device-Specific Method
            {
                Return (\_SB.PCI0.LPC.XDSM (Arg0, Arg1, Arg2, Arg3))
            }
        }

        Scope (\_SB.PCI0.IGBE)
        {
            Method (_DSM, 4, Serialized)  // _DSM: Device-Specific Method
            {
                Return (\_SB.PCI0.IGBE.XDSM (Arg0, Arg1, Arg2, Arg3))
            }
        }

        Scope (\_SB.PCI0.EXP1)
        {
            Method (_DSM, 4, Serialized)  // _DSM: Device-Specific Method
            {
                Return (\_SB.PCI0.EXP1.XDSM (Arg0, Arg1, Arg2, Arg3))
            }
        }

        Scope (\_SB.PCI0.EXP3)
        {
            Method (_DSM, 4, Serialized)  // _DSM: Device-Specific Method
            {
                Return (\_SB.PCI0.EXP3.XDSM (Arg0, Arg1, Arg2, Arg3))
            }
        }

        Scope (\_SB.PCI0.SMBU)
        {
            Method (_DSM, 4, Serialized)  // _DSM: Device-Specific Method
            {
                Return (\_SB.PCI0.SMBU.XDSM (Arg0, Arg1, Arg2, Arg3))
            }
        }

        Scope (\_SB.PCI0.SAT1)
        {
            Method (_DSM, 4, Serialized)  // _DSM: Device-Specific Method
            {
                Return (\_SB.PCI0.SAT1.XDSM (Arg0, Arg1, Arg2, Arg3))
            }
        }

        Scope (\_SB.PCI0.XHCI)
        {
            Method (_DSM, 4, NotSerialized)  // _DSM: Device-Specific Method
            {
                Return (\_SB.PCI0.XHCI.XDSM (Arg0, Arg1, Arg2, Arg3))
            }
        }
    }
}

