from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os

leaderboard = 666

img = Image.open(f"{os.getcwd()}/images/ranks/80.png")
I1 = ImageDraw.Draw(img)

textSize = len(str(leaderboard))

myFont = ImageFont.truetype('Keyboard.ttf', 40)
I1.text((130 - (15 * textSize), 190),
        f"{leaderboard}", fill=(255, 255, 255), font=myFont)
img.save(f"{os.getcwd()}/images/temp/90000.png")
