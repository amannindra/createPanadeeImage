from weasyprint import HTML
from pdf2image import convert_from_bytes
from PIL import Image
import re
import os
import math

def html_to_image(html_content: str, output_file: str):
    
    pdf_bytes = HTML(string=html_content).write_pdf()

    pil_images = convert_from_bytes(pdf_bytes)
    if not pil_images:
        print("No pages found in PDF rendering. Check if HTML is empty or invalid.")
        return

    final_image = pil_images[0]
    
    if not os.path.exists("Image"):
      os.makedirs("Image")

    output_file = os.path.join("Image", output_file)
    final_image.save(output_file, 'PNG')
    print(f"Image saved to {output_file}")

def avoidAndConsder(ticker,avoid, consider, height):
  html_content = f"""
<!DOCTYPE html>
<html>
<head>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Lalezar&display=swap" rel="stylesheet">
  <style>
  @page {{
    size: 900px {height}; /* Adjust height as needed */
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
      min-height: [min_container_height_value_from_css]px;
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
  min_container_height_value_from_css = 400 # Example, matching the default
  # html_content = html_content.replace(
  #       f"min-height: {[min_container_height_value_from_css]}px;", # placeholder in my f-string
  #       f"min-height: {min_container_height_value_from_css}px;"   # actual replacement
  # )
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

def card_height(avoid: str, consider: str,
                base: int = 320,
                chars_per_line: int = 40,
                line_height: int = 22) -> int:
    lines_avoid = math.ceil(len(avoid) / chars_per_line)
    lines_cons  = math.ceil(len(consider) / chars_per_line)
    return base + line_height * max(lines_avoid, lines_cons)


def calculate_image_height(
    max_text_length: int,
    base_height: float = 306.0,
    chars_per_line: int = 40,
    line_height_px: float = 22.4,
    min_container_height: float = 400.0
) -> float:
    """
    Calculates the optimal image height to fit text based on a predefined HTML/CSS structure.

    The formula is: H = max(H_min_container, B + ceil(L_max / CPL) * H_L)

    Args:
        max_text_length: The maximum character length of the raw text in the
                         dynamic content sections (e.g., BEAR or BULL).
        base_height: The sum of all fixed vertical dimensions (heights, paddings,
                     margins) of static elements in pixels. Default is 306.0px,
                     based on the provided CSS analysis.
        chars_per_line: Estimated characters that fit on a single line within
                        the text content area. Default is 45.
        line_height_px: The height of a single line of text in pixels.
                        Default is 22.4px (14px font size * 1.6 line-height).
        min_container_height: The minimum height of the main content container
                              in pixels, as defined in CSS (`.container { min-height: ... }`).
                              Default is 400.0px.

    Returns:
        The calculated optimal image height in pixels. This value can be a float.
    """

    if chars_per_line <= 0:
        raise ValueError("Characters per line (chars_per_line) must be positive.")
    if line_height_px <= 0:
        raise ValueError("Line height (line_height_px) must be positive.")

    # Calculate the number of lines needed for the longest text block
    num_lines = math.ceil(max_text_length / chars_per_line)

    # Calculate the height required by the content (fixed base + dynamic text height)
    content_height = base_height + (num_lines * line_height_px)

    # The final image height is the greater of the container's min_height or the calculated content_height
    image_height = max(min_container_height, content_height)

    return image_height



company_name = "Recursion Pharmaceuticals"

ticker = "RXRX"
  
symbol = "$" + ticker + "/" + company_name

avoid = "RXRX burned $132M cash in Q1, up 29% Y/Y. Ending cash of $500.5M provides limited runway at this rate. Net loss doubled to $202.5M. Discontinued 3 clinical programs (REC-2282, REC-994, REC-3964) signaling R&D setbacks despite high platform spend. Integration risks from Exscientia acquisition evident in material weakness disclosure."

consider = "RXRX validates TechBio model with Sanofi partnership milestone ($7M) and progress on Roche/Genentech collaborations, leveraging a massive 171TB dataset. Strategic reprioritization focuses spend on remaining high-potential pipeline assets (REC-4881, REC-617, etc.). Cash balance of $500.5M and $496M available on ATM provide near-term liquidity."

avoid_green = ["$132M", "29%", "$500.5M", "$202.5M"]
avod = specificCSS(avoid_green, avoid)

cons_green = ["($7M)", "171TB", "$500.5M", "$496M"]
cons = specificCSS(cons_green, consider)



height_px = card_height(avoid, consider)       

# print(len(avoid))
# print(len(consider))

max_length = max(len(avoid), len(consider))

calculated_page_height = calculate_image_height(max_length)

print(f"Calculated optimal page height: {calculated_page_height}px")


calculated_page_height = 490

print(f"Final page height set to: {calculated_page_height}px")

output_path = ticker + ".png"
html_to_image(avoidAndConsder(symbol,avod, cons, f"{calculated_page_height}px"), output_path)






   





