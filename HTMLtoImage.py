from weasyprint import HTML
from pdf2image import convert_from_bytes
from PIL import Image
import re
import os

def html_to_image(html_content: str, output_file: str):
    
    pdf_bytes = HTML(string=html_content).write_pdf()

    pil_images = convert_from_bytes(pdf_bytes)
    if not pil_images:
        print("No pages found in PDF rendering. Check if HTML is empty or invalid.")
        return

    final_image = pil_images[0]

    output_file = os.path.join("Image", output_file)
    final_image.save(output_file, 'PNG')
    print(f"Image saved to {output_file}")

def avoidAndConsder(ticker,avoid, consider):
  html_content = f"""
<!DOCTYPE html>
<html>
<head>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Lalezar&display=swap" rel="stylesheet">
  <style>
  @page {{
    size: 900px 470px; /* Adjust height as needed */
    margin: 0;
  }}
    body {{
      margin: 0;
      padding: 0;
      background: #FFFEF2;
      font-family: 'Inter', sans-serif;
      -webkit-font-smoothing: antialiased;
    }}
    .container {{
      width: 900px;
      min-height: 400px;
      background: #FFFEF2;
      position: relative;
      padding-bottom: 40px;
    }}
    .top-bar {{
      width: 100%;
      height: 5px;
      background: #288362;
    }}
    .header {{
      padding-top: 5px;
      padding-left: 30px;
      display: flex;
      align-items:center;
      border-bottom: 1px solid rgba(40, 131, 98, 0.1);
    }}
    .logo {{
      width: 40px;
      height: 40px;
      position: relative;
    }}
    .wordmark {{
      margin-left: 10px;
      color: rgba(28, 28, 28, 0.8);
      font-family: 'Lalezar', 'Inter', sans-serif;
      font-size: 28px;
    }}
    .content {{
      padding: 30px 40px 40px;
    }}
    .ticker {{
      font-size: 22px;
      font-weight: 600;
      color: #288362;
      margin: 0 0 32px 0;
      letter-spacing: -0.5px;
    }}
    .analysis-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 40px;
      margin-top: 20px;
    }}
    .analysis-section-horizontal {{
      background: rgba(40, 131, 98, 0.03);
      border-radius: 16px;
      padding: 32px;
    }}
    .analysis-section-horizontal h2 {{
      font-size: 16px;
      font-weight: 600;
      margin: 0 0 16px 0;
      color: rgba(28, 28, 28, 0.9);
      display: inline-block;
      position: relative;
      padding-bottom: 15px;
    }}
    .analysis-section-horizontal h2::after {{
      content: '';
      position: absolute;
      bottom: 0;
      left: 0;
      width: 40px;
      height: 2px;
      background: #288362;
      border-radius: 2px;
      opacity: 0.8;
    }}
    .analysis-content {{
      font-size: 14px;
      line-height: 1.6;
      margin: 0;
      color: rgba(28, 28, 28, 0.8);
      font-weight: 400;
    }}
    .stat {{
      color: #288362;
      font-weight: 500;
    }}
    .titleSize{{
      font-size: 
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="top-bar"></div>
    <div class="header">
      <img src="https://www.panabee.com/images/logos/brandmark.svg" alt="Panabee Logo" class="logo">
      <div class="wordmark">Panabee</div>
    </div>
    <div class="content">
      <div class="ticker">{ticker}</div>
      <div class="analysis-grid">
        <div class="analysis-section-horizontal">
          <h2>BEAR</h2>
          <p class="analysis-content">{avoid}</p>
        </div>
        <div class="analysis-section-horizontal">
          <h2>BULL</h2>
          <p class="analysis-content">{consider}</p>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
"""
  return html_content
import re

def createCSS(ticker, avoid, consider):
    # This pattern has two main parts joined by '|':
    #   1) Your original numeric pattern
    #   2) A pattern to capture any parentheses that contain digits.
    pattern = (
        r'(?:'
        r'#?:'
        r'(?:[~-]?\$?\(?\d+(?:\.\d+)?\)?[MBK]?\+?%?)(?:\s*-\s*[~-]?\$?\(?\d+(?:\.\d+)?\)?[MBK]?\+?%?)?(?:\s*CAGR)?'
        r')'
        r'|\([^)]*\d+[^)]*\)'
    )

    new_avoid = re.sub(pattern, r'<span class="stat">\g<0></span>', avoid)
    new_consider = re.sub(pattern, r'<span class="stat">\g<0></span>', consider)

    return avoidAndConsder(ticker, new_avoid, new_consider)


company_name = "Progressive"

ticker = "PGR"
  
symbol = "$" + ticker + "/" + company_name

avoid = "Intense competition, cyclical insurance market, and potential for pricing pressure may squeeze margins. Catastrophe exposure and climate change uncertainty can lead to volatile earnings. Regulatory changes and cybersecurity risks add further complexity."

consider = "Market leader in commercial auto & #2 in personal auto. Strong brand & focus on competitive pricing. Continuous product innovation (models 8.9 & R17) and Destination Era strategy to bundle offerings may drive growth. High employee retention (89%) indicates strong culture."
output_path = ticker + ".png"


html_to_image(createCSS(symbol,avoid, consider), output_path)

   





