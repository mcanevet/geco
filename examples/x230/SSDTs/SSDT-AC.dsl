/*
 * Intel ACPI Component Architecture
 * AML/ASL+ Disassembler version 20200925 (64-bit version)
 * Copyright (c) 2000 - 2020 Intel Corporation
 * 
 * Disassembling to symbolic ASL+ operators
 *
 * Disassembly of SSDT-AC.aml, Tue May 25 21:04:28 2021
 *
 * Original Table Header:
 *     Signature        "SSDT"
 *     Length           0x00000074 (116)
 *     Revision         0x02
 *     Checksum         0xA0
 *     OEM ID           "X230"
 *     OEM Table ID     "AC"
 *     OEM Revision     0x00000000 (0)
 *     Compiler ID      "INTL"
 *     Compiler Version 0x20180427 (538444839)
 */
DefinitionBlock ("", "SSDT", 2, "X230", "AC", 0x00000000)
{
    External (_SB_.PCI0.LPC_.EC__.AC__, DeviceObj)

    Scope (\_SB.PCI0.LPC.EC.AC)
    {
        If (_OSI ("Darwin"))
        {
            Name (_PRW, Package (0x02)  // _PRW: Power Resources for Wake
            {
                0x18, 
                0x03
            })
        }
    }
}

