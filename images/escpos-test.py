from escpos.printer import Usb


p = Usb(0x04b8, 0x0e15)

p.text("Hello World\n")
p.image("dms-logo-wide.png")
content = "https://storage.dallasmakerspace.org/12345"
p.qr(content)
p.text("\n\nSize 5\n")
p.qr(content, size=5)
p.text("\n\nCenter\n")
p.qr(content, center=False)

p.cut()
