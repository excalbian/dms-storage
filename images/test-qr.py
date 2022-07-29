# import modules
import qrcode
from PIL import Image
from escpos.printer import Usb

logo = Image.open("dms-logo-wide.png")
 
# taking base width
## basewidth = 100
 
# adjust image size
## wpercent = (basewidth/float(logo.size[0]))
## hsize = int((float(logo.size[1])*float(wpercent)))
## logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
QRcode = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size = 2,
)
 
# taking url or text
url = 'https://storage.dallasmakerspace.org/ticket/123456#Adam%20Barrow;A5;20220707;20220907'
 
# adding URL or text to QRcode
QRcode.add_data(url)
 
# generating QR code
QRcode.make()
 
# adding color to QR code
QRimg = QRcode.make_image(
    fill_color="Black", back_color="white").convert('RGB')
 
print(QRimg.size)
print("logo:")
print(logo.size)




#resize, first image
#image1 = image1.resize((426, 240))
#image1_size = image1.size
#image2_size = image2.size
#new_image = Image.new('RGB',(2*image1_size[0], image1_size[1]), (250,250,250))
margin = 10 # space between images in pixels
tempImage = Image.new('RGB', ((logo.size[0] + QRimg.size[0] + margin), QRimg.size[1]), (255, 255, 255))
tempImage.paste(QRimg,(0,0))
logoOffsetY = int((QRimg.size[1] - logo.size[1]) / 2)
tempImage.paste(logo,(QRimg.size[0], logoOffsetY))


# save the QR code generated
tempImage.save('qr-temp.png')
 
print('QR code generated!')

p = Usb(0x04b8, 0x0e15)

p.image("qr-temp.png")
p.set(align="CENTER", font="A", text_type="normal")
p.text("\nStorage area ")
p.set(text_type="B")
p.text(" A5 ")
p.set(text_type="normal")
p.text(" Reservation Ticket\n\n")
p.set(align="LEFT", font="B", text_type="normal")
p.text("Member: ")
p.set(text_type="B")
p.text("Adam Long Long Long Name Barrow\n")
p.text("adam@thebarrows.com\n")
p.set(text_type="normal")
p.text("Start: 09 July 2022\n")
p.set(text_type="normal", width=2, height=2)
p.text("End: ")
p.set(invert=True, width=2, height=2)
p.text("31 September 2022\n")

p.cut()
