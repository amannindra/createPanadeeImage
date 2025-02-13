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

        text_font = ImageFont.truetype(path, 20)

        print("header_font good")
    except OSError:
        font = ImageFont.load_default()
        print("using default font")

    try:
        path = os.path.join(cwd, "fonts/Lalezar-Regular.ttf")
        header_font = ImageFont.truetype(path, 35)
        print("text_font good")
    except OSError:
        text_font  = ImageFont.load_default()
        print("no lalezer")

    try:
        path = os.path.join(cwd, "fonts/Lalezar-Regular.ttf")
        footer_font = ImageFont.truetype(path, 40)
        print("footer_font good")
    except OSError:
        footer_font  = ImageFont.load_default()
        print("no footer lalezer")

    text_color = (28, 28, 28)

    draw.rectangle([(0, 0), (width, 50)], fill="#288362")

    logo_url = "https://www.panabee.com/images/logos/brandmark.svg"
    response = requests.get(logo_url)
    logo_svg = response.content
    png_data = cairosvg.svg2png(bytestring=logo_svg)
    logo = Image.open(BytesIO(png_data)).convert("RGBA").resize((60, 60))

    draw.text((80, 0), "Panabee", fill=text_color, font=footer_font)
    image.paste(logo, (10,-5), logo)

    avoid_text = "Avoid: " + avoid
    consider_text = "Consider: " + consider

    max_width = 90 # Adjust width for the length of the text

    lines = textwrap.wrap(avoid_text, width=max_width) 

    avoid_y_position = 60
    for line in lines:
        draw.text((5, avoid_y_position), line, font=text_font, fill="black")
        avoid_y_position += 45  

    lines = textwrap.wrap(consider_text, width=max_width) 

    consider_y_position = avoid_y_position + 20
    for line in lines:
        draw.text((5, consider_y_position), line, font=text_font, fill="black")
        consider_y_position += 45

    draw.rectangle([(0, height - 50), (width, height)], fill="#288362")

    website_text = "See link for full article: https://www.panabee.com/"
    
    draw.text((50,  height - 50), website_text, font=footer_font, fill="black")

    image.show()

    # image.save(file_name)

avoid_text = " Net income declined 36% YoY for Q3 despite 31% sales growth, due to 36% surge in SG&A. Operating margin contracted from 12% to 10%. Increased marketing spend & admin costs may not yield proportional profit gains."

consider_text = "Net sales soared 31% YoY in Q3 to $355M, driven by 34% growth in retailer channels and 21% in e-commerce. Gross margin remained strong at 71%. Strong brand and effective execution in a competitive beauty market."

file_name = "avoidAndConsider.png"

createImage(avoid_text, consider_text, file_name)

