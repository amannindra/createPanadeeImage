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
    image = Image.new(mode="RGB", size = (width, height), color = "#FFFEF2")

    draw = ImageDraw.Draw(image)
    try: 
        path = os.path.join(cwd, "fonts/Roboto-VariableFont_wdth,wght.ttf")

        text_font = ImageFont.truetype(path, 20)

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

    draw.text((85, 15), "Panabee", fill=text_color, font=footer_font)
    image.paste(logo, (15,15), logo)

    avoid_text = "Avoid: " + avoid
    consider_text = "Consider: " + consider

    max_width = 90 # Adjust width for the length of the text

    lines = textwrap.wrap(avoid_text, width=max_width) 

    avoid_y_position = 80
    for line in lines:
        draw.text((20, avoid_y_position), line, font=text_font, fill="black")
        avoid_y_position += 45  

    lines = textwrap.wrap(consider_text, width=max_width) 

    consider_y_position = avoid_y_position + 20
    for line in lines:
        draw.text((20, consider_y_position), line, font=text_font, fill="black")
        consider_y_position += 45


    website_text = "Panabee.com"
    
    draw.text((width/2 - 100,  height - 50), website_text, font=footer_font, fill="black")

    image.show()

    image.save(file_name)

avoid_text = "FCX faces rising unit costs (+8% YoY to $2.49/lb copper) amid lower copper & moly production. New smelter fire adds risks & delays ramp-up. Grasberg's IUPK renewal post-2041 uncertain, limiting long-term value."

consider_text = "FCX's Grasberg underground output & leaching tech boost copper production. Gold output to ramp up w/ new PMR. Strong avg realized copper price ($4.21/lb, +9% YoY) & operating cash flow ($7.2B) signal value. Potential Bagdad expansion & IUPK extension offer upside."

file_name = "avoidAndConsider.png"

createImage(avoid_text, consider_text, file_name)

