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
    size: 900px 510px; /* Adjust height as needed */
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

def highlight(match):
    """
    - group(1) = 'FY\d+' (skip highlighting)
    - group(2) = everything else we do want to highlight:
         Q\d+, or the numeric patterns, or parentheses with digits
    """
    if match.group(1):
        # This is the 'FY\d+' match, so return it unaltered
        return match.group(1)
    else:
        # This is group(2), which we do want to highlight
        return f'<span class="stat">{match.group(2)}</span>'

def createCSS(ticker, avoid, consider):
    pattern = re.compile(
        r'(FY\d+)'    # group(1): "FY24", "FY2023", etc. (skip highlight)
        r'|'          # OR
        r'(Q\d+'      # group(2): "Q4", "Q1", ...
           r'|[~-]?\$?\(?\d+(?:\.\d+)?\)?[MBKG]?\+?%?'  
           r'(?:\s*-\s*[~-]?\$?\(?\d+(?:\.\d+)?\)?[MBKG]?\+?%?)?' 
           r'(?:\s*CAGR)?'
           r'|\([^)]*\)'  # highlight *anything* inside parentheses
        r')'
    )

    new_avoid = pattern.sub(highlight, avoid)
    new_consider = pattern.sub(highlight, consider)

    return avoidAndConsder(ticker, new_avoid, new_consider)
  
  
  
def specificCSS(green, text):
  for i in green:
    start = -1 
    for j in range(len(text) - len(i) + 1):
      if text[j:j+len(i)] == i:
        start = j
        break
    
    if start != -1:
        end = start + len(i) - 1 
        text = text[:start] + '<span class="stat">' + i + '</span>' + text[end + 1:]

    else:
        continue
        
        
  
  
  return text
  
  
company_name = "Oxford Industries"
ticker = "OXM"
symbol = "$" + ticker + "/" + company_name

avoid = "OXM's FY24 sales fell 3.5% to $1.5B amid a tough retail climate & inflation, with gross margin down 0.5%. Tommy Bahama and Lilly Pulitzer operating income declined 27% and 30%, respectively, indicating brand vulnerability despite DTC focus. Increased SG&A and investments in distribution center & stores pressures near-term profitability. High inventory and promotional environment signal further margin risks."

consider = "OXM is investing in DTC (81% of FY24 sales) & new distribution, aiming for long-term growth & efficiency. Emerging Brands sales rose 1.3%, showing portfolio potential. Johnny Was improved operating income by $96M YoY, recovering from impairment. Shareholder returns prioritized with consistent dividends & $50M recent buyback. Undervalued lifestyle brand portfolio in evolving retail."

cons_green = ["81%", "1.3%", "$96M", "$50M"]
cons = specificCSS(cons_green, consider)

avoid_green = ["3.5%", "$1.5B", "0.5%", "27%", "30%"]
avod = specificCSS(avoid_green, avoid)



output_path = ticker + ".png"

# html_to_image(createCSS(ticker, avoid, consider), output_path)

html_to_image(avoidAndConsder(ticker,cons, avod), output_path)






   





