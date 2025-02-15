from PIL import Image, ImageDraw, ImageFont
import cairosvg
from io import BytesIO
import requests
import textwrap
import os 


width = 960
height = 540

def createImage(avoid, consider, file_name):
    cwd = os.getcwd()
    print(cwd)
    image = Image.new(mode="RGB", size = (width, height), color = "white")

    draw = ImageDraw.Draw(image)
    try: 
        path = os.path.join(cwd, "fonts/Roboto-VariableFont_wdth,wght.ttf")

        text_font = ImageFont.truetype(path, 30)

        print("header_font good")
    except OSError:
        text_font = ImageFont.load_default()
        print("using default font")

    try:
        path = os.path.join(cwd, "fonts/Lalezar-Regular.ttf")
        footer_font = ImageFont.truetype(path, 40)
        print("footer_font good")
    except OSError:
        footer_font  = ImageFont.load_default()
        print("no footer lalezer")

    text_color = (28, 28, 28)

    draw.rectangle([(0, 0), (width, 5)], fill="#288362")

    logo_url = "https://www.panabee.com/images/logos/brandmark.svg"
    response = requests.get(logo_url)
    logo_svg = response.content
    png_data = cairosvg.svg2png(bytestring=logo_svg)
    logo = Image.open(BytesIO(png_data)).convert("RGBA").resize((60, 60))

    draw.text((80, 0), "Panabee", fill=text_color, font=footer_font)
    image.paste(logo, (10,0), logo)

    avoid_text = "Avoid: " + avoid
    consider_text = "Consider: " + consider

    max_width = 90 # Adjust width for the length of the text

    lines = textwrap.wrap(avoid_text, width=max_width) 

    avoid_y_position = 70
    for line in lines:
        draw.text((20, avoid_y_position), line, font=text_font, fill="black")
        avoid_y_position += 45  

    lines = textwrap.wrap(consider_text, width=max_width) 

    consider_y_position = avoid_y_position + 20
    for line in lines:
        draw.text((20, consider_y_position), line, font=text_font, fill="black")
        consider_y_position += 45


    website_text = "See link for full article: https://www.panabee.com/"
    
    draw.text((50,  height - 50), website_text, font=footer_font, fill="black")

    image.show()

    image.save(file_name)

avoid_text = "Rising credit costs & expenses offset revenue growth, causing net income to decline 20% YoY to $509M. Net charge-off ratio rose to 8.12%. High provision for loan losses ($2.04B) signals increased credit risk in nonprime consumer lending."

consider_text = "Revenue up 9% to $4.99B, driven by 9% growth in net finance receivables to $23.6B. Strategic Foursight acquisition expands auto finance presence. Shareholder returns via dividends ($494M in 2024) and buybacks ($35M in 2024) continue."

file_name = "avoidAndConsider.png"

createImage(avoid_text, consider_text, file_name)

