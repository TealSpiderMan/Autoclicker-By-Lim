from PIL import Image
img = Image.open("icon/acbl.png").convert("RGBA")
img.save("icon/acbl.ico", sizes=[(256,256),(128,128),(64,64),(48,48),(32,32),(16,16)])
print("Wrote icon/acbl.ico")