import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


rank = 81
img = Image.open(f"{os.getcwd()}/images/ranks/{rank}.png")
I1 = ImageDraw.Draw(img)
textSize = 4
myFont = ImageFont.truetype('arial.ttf', 40)
I1.text((145 - (15 * textSize), 190),
        f"4000", fill=(255, 255, 255), font=myFont)
img.save(f"{os.getcwd()}/images/temp/temp.png")
img.show()