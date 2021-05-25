/*
 * Intel ACPI Component Architecture
 * AML/ASL+ Disassembler version 20200925 (64-bit version)
 * Copyright (c) 2000 - 2020 Intel Corporation
 * 
 * Disassembling to symbolic ASL+ operators
 *
 * Disassembly of SSDT-THINK.aml, Tue May 25 21:04:28 2021
 *
 * Original Table Header:
 *     Signature        "SSDT"
 *     Length           0x00000205 (517)
 *     Revision         0x02
 *     Checksum         0x27
 *     OEM ID           "X230"
 *     OEM Table ID     "Think"
 *     OEM Revision     0x00000000 (0)
 *     Compiler ID      "INTL"
 *     Compiler Version 0x20210331 (539034417)
 */
DefinitionBlock ("", "SSDT", 2, "X230", "Think", 0x00000000)
{
    External (_SB_.PCI0.LPC_.EC__, DeviceObj)
    External (_SB_.PCI0.LPC_.EC__.HFNI, FieldUnitObj)
    External (_SB_.PCI0.LPC_.EC__.HFSP, FieldUnitObj)
    External (_SB_.PCI0.LPC_.EC__.HKEY, DeviceObj)
    External (_SB_.PCI0.LPC_.EC__.VRST, FieldUnitObj)
    External (_SI_._SST, MethodObj)    // 1 Arguments
    External (LNUX, IntObj)
    External (WNTF, IntObj)

    Scope (\)
    {
        If (_OSI ("Darwin"))
        {
            LNUX = One
            WNTF = One
        }
    }

    Scope (\_SB.PCI0.LPC.EC.HKEY)
    {
        Method (CSSI, 1, NotSerialized)
        {
            \_SI._SST (Arg0)
        }
    }

    Scope (_SB.PCI0.LPC.EC)
    {
        OperationRegion (ESEN, EmbeddedControl, Zero, 0x0100)
        Field (ESEN, ByteAcc, Lock, Preserve)
        {
            Offset (0x78), 
            EST0,   8, 
            EST1,   8, 
            EST2,   8, 
            EST3,   8, 
            EST4,   8, 
            EST5,   8, 
            EST6,   8, 
            EST7,   8, 
            Offset (0xC0), 
            EST8,   8, 
            EST9,   8, 
            ESTA,   8, 
            ESTB,   8, 
            ESTC,   8, 
            ESTD,   8, 
            ESTE,   8, 
            ESTF,   8
        }
    }

    Scope (\_SB.PCI0.LPC.EC.HKEY)
    {
        Method (CFSP, 1, NotSerialized)
        {
            \_SB.PCI0.LPC.EC.HFSP = Arg0
        }

        Method (CFNI, 1, NotSerialized)
        {
            \_SB.PCI0.LPC.EC.HFNI = Arg0
        }

        Method (CRST, 1, NotSerialized)
        {
            \_SB.PCI0.LPC.EC.VRST = Arg0
        }
    }
}

