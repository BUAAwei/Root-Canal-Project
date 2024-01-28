from PIL import Image, ImageFilter

im = Image.open(r'C:\Users\Lenovo\Desktop\Root-Canal-Project\UNetProject\filterWaveTest\13.png')
om = im.filter(ImageFilter.DETAIL)
om.save(r'C:\Users\Lenovo\Desktop\Root-Canal-Project\UNetProject\filterWaveTest\result.png')
