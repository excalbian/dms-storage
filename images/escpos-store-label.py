from escpos.printer import Usb


p = Usb(0x04b8, 0x0e15)

p.image("dms-logo-wide.png")
content = "https://storage.dallasmakerspace.org/12345"
p.qr(content)
p.set(align="CENTER", font="A", text_type="normal")
p.text("Storage area ")
p.set(text_type="B")
p.text(" A5 ")
p.set(text_type="normal")
p.text(" Reservation Ticket\n")
p.set(align="LEFT", font="B", text_type="normal")
p.text("Member: ")
p.set(text_type="B")
p.text("Adam Long Long Long Name Barrow")
p.set(text_type="normal")
p.text("\n")
p.text("Start: 09 July 2022\n")
p.text("End: ")
p.set(invert=True)
p.text("31 September 2022\n")





p.cut()
