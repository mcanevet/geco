/*
 * Intel ACPI Component Architecture
 * AML/ASL+ Disassembler version 20200925 (64-bit version)
 * Copyright (c) 2000 - 2020 Intel Corporation
 * 
 * Disassembling to symbolic ASL+ operators
 *
 * Disassembly of SSDT-KBD.aml, Tue May 25 21:04:28 2021
 *
 * Original Table Header:
 *     Signature        "SSDT"
 *     Length           0x00000372 (882)
 *     Revision         0x02
 *     Checksum         0xD7
 *     OEM ID           "X230"
 *     OEM Table ID     "KBD"
 *     OEM Revision     0x00000000 (0)
 *     Compiler ID      "INTL"
 *     Compiler Version 0x20200925 (538970405)
 */
DefinitionBlock ("", "SSDT", 2, "X230", "KBD", 0x00000000)
{
    External (_SB_.PCI0.LPC_.EC__, DeviceObj)
    External (_SB_.PCI0.LPC_.KBD_, DeviceObj)

    Scope (_SB.PCI0.LPC.KBD)
    {
        Method (_DSM, 4, NotSerialized)  // _DSM: Device-Specific Method
        {
            If (!Arg2)
            {
                Return (Buffer (One)
                {
                     0x03                                             // .
                })
            }

            Return (Package (0x04)
            {
                "RM,oem-id", 
                "LENOVO", 
                "RM,oem-table-id", 
                "Thinkpad_TrackPad"
            })
        }

        Name (RMCF, Package (0x02)
        {
            "Keyboard", 
            Package (0x04)
            {
                "Custom PS2 Map", 
                Package (0x03)
                {
                    Package (0x00){}, 
                    "e038=e05b", 
                    "e037=64"
                }, 

                "Synaptics TouchPad", 
                Package (0x3A)
                {
                    "BogusDeltaThreshX", 
                    0x0320, 
                    "BogusDeltaThreshY", 
                    0x0320, 
                    "Clicking", 
                    ">y", 
                    "DragLockTempMask", 
                    0x00040004, 
                    "DisableDeepSleep", 
                    ">y", 
                    "DynamicEWMode", 
                    ">n", 
                    "FakeMiddleButton", 
                    ">n", 
                    "HWResetOnStart", 
                    ">y", 
                    "PalmNoAction When Typing", 
                    ">y", 
                    "ScrollResolution", 
                    0x0320, 
                    "SmoothInput", 
                    ">y", 
                    "UnsmoothInput", 
                    ">y", 
                    "Thinkpad", 
                    ">y", 
                    "DivisorX", 
                    One, 
                    "DivisorY", 
                    One, 
                    "FingerZ", 
                    0x2F, 
                    "MaxTapTime", 
                    0x05F5E100, 
                    "MomentumScrollThreshY", 
                    0x10, 
                    "MouseMultiplierX", 
                    0x08, 
                    "MouseMultiplierY", 
                    0x08, 
                    "MouseScrollMultiplierX", 
                    0x02, 
                    "MouseScrollMultiplierY", 
                    0x02, 
                    "MultiFingerHorizontalDivisor", 
                    0x04, 
                    "MultiFingerVerticalDivisor", 
                    0x04, 
                    "Resolution", 
                    0x0C80, 
                    "ScrollDeltaThreshX", 
                    0x0A, 
                    "ScrollDeltaThreshY", 
                    0x0A, 
                    "TrackpointScrollYMultiplier", 
                    One, 
                    "TrackpointScrollXMultiplier", 
                    One
                }
            }
        })
    }
}

