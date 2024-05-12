import os
import sys
from PIL import Image
from stegano import lsb
'''image = Image.open("static/upload/test.png")
print(f"Original size : {image.size}")  # 5464x3640

sunset_resized = image.resize((400, 400))
sunset_resized.save("static/upload/test.png")
hidedata = 'hai my pass 4567'
secret = lsb.hide("./static/upload/test.png", hidedata)

pathname, extension = os.path.splitext("static/upload/test.png")
filename = pathname.split('/')
imageName = filename[-1] + ".png"
secret.save("./static/Encode/" + imageName)


savedir = 'static/Split/'
filename = 'static/Encode/test.png'
img = Image.open(filename)
width, height = img.size
start_pos = start_x, start_y = (0, 0)
cropped_image_size = w, h = (200,200)

frame_num = 1
for col_i in range(0, width, w):
    for row_i in range(0, height, h):
        crop = img.crop((col_i, row_i, col_i + w, row_i + h))
        save_to= os.path.join(savedir, "testing_{:02}.png")
        crop.save(save_to.format(frame_num))
        frame_num += 1'''

files = [
  'static/Decrypt/4238_01.png',
  'static/Decrypt/4238_02.png',
  'static/Decrypt/4238_03.png',
  'static/Decrypt/4238_04.png']

result = Image.new("RGB", (400, 400))

for index, file in enumerate(files):
  path = os.path.expanduser(file)
  img = Image.open(path)
  img.thumbnail((200, 200), Image.ANTIALIAS)
  x = index // 2 * 200
  y = index % 2 * 200
  w, h = img.size
  print('pos {0},{1} size {2},{3}'.format(x, y, w, h))
  result.paste(img, (x, y, x + w, y + h))

result.save(os.path.expanduser('../../image.png'))

clear_message = lsb.reveal("image.png")
print(clear_message)