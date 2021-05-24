DefinitionBlock ("", "SSDT", 2, "T460s", "PTWK", 0x00000000)
{
    External (_SB_.LID_, DeviceObj)
    External (_SB_.PCI0, DeviceObj)
    External (_SB_.PCI0._LPC.EC__._LED, IntObj)
    External (_SB_.PCI0._LPC.EC__.HKEY.MMTS, MethodObj)    // 1 Arguments
    External (_SB_.PCI0.LPC_, DeviceObj)
    External (_SB_.PCI0.LPC_.EC__, DeviceObj)
    External (_SB_.PCI0.XHCI.PMEE, FieldUnitObj)
    External (ZPTS, MethodObj)    // 1 Arguments
    External (ZWAK, MethodObj)    // 1 Arguments

    Scope (_SB)
    {
        Device (PCI9)
        {
            Name (_ADR, Zero)  // _ADR: Address
            Name (FNOK, Zero)
            Name (MODE, Zero)
            Name (TPTS, Zero)
            Name (TWAK, Zero)
            Method (_STA, 0, NotSerialized)  // _STA: Status
            {
                If (_OSI ("Darwin"))
                {
                    Return (0x0F)
                }
                Else
                {
                    Return (Zero)
                }
            }
        }
    }

    Scope (\_SB.PCI0.LPC.EC)
    {
        OperationRegion (WRAM, EmbeddedControl, Zero, 0x0100)
        Field (WRAM, ByteAcc, NoLock, Preserve)
        {
            Offset (0x36),
            WAC0,   8,
            WAC1,   8
        }

        Method (WACH, 0, NotSerialized)
        {
            Return ((WAC0 | (WAC1 << 0x08)))
        }
    }

    Method (_PTS, 1, NotSerialized)  // _PTS: Prepare To Sleep
    {
        If (_OSI ("Darwin"))
        {
            \_SB.PCI9.TPTS = Arg0
            If ((\_SB.PCI9.FNOK == One))
            {
                Arg0 = 0x03
            }

            If (((0x05 == Arg0) && CondRefOf (\_SB.PCI0.XHCI.PMEE)))
            {
                \_SB.PCI0.XHCI.PMEE = Zero
            }
        }

        ZPTS (Arg0)
    }

    Method (_WAK, 1, NotSerialized)  // _WAK: Wake
    {
        If (_OSI ("Darwin"))
        {
            \_SB.PCI9.TWAK = Arg0
            If ((\_SB.PCI9.FNOK == One))
            {
                \_SB.PCI9.FNOK = Zero
                Arg0 = 0x03
            }

            If (((Arg0 < One) || (Arg0 > 0x05)))
            {
                Arg0 = 0x03
            }

            If ((0x03 == Arg0))
            {
                Notify (\_SB.LID, 0x80) // Status Change
            }
        }

        Local0 = ZWAK (Arg0)
        Return (Local0)
    }

    Method (_TTS, 1, NotSerialized)  // _TTS: Transition To State
    {
        If (_OSI ("Darwin"))
        {
            If (CondRefOf (\_SB.PCI0._LPC.EC._LED))
            {
                If (((Arg0 == Zero) & (\_SB.PCI0._LPC.EC._LED == One)))
                {
                    \_SB.PCI0._LPC.EC.HKEY.MMTS (0x02)
                }
            }
        }
    }
}
