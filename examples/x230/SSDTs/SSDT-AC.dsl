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
