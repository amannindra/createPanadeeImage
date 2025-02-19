from weasyprint import HTML
from pdf2image import convert_from_bytes
from PIL import Image

def html_to_image(html_content: str, output_file: str):
    
    pdf_bytes = HTML(string=html_content).write_pdf()

    pil_images = convert_from_bytes(pdf_bytes)
    if not pil_images:
        print("No pages found in PDF rendering. Check if HTML is empty or invalid.")
        return

    final_image = pil_images[0]


    final_image.save(output_file, 'PNG')
    print(f"Image saved to {output_file}")


html_content = """
<!DOCTYPE html>
<html>
<head>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Lalezar&display=swap" rel="stylesheet">
  <style>
  @page {
    size: 900px 500px; 
    margin: 0;
  }
    body {
      margin: 0;
      padding: 0;
      background: #FFFEF2;
      font-family: 'Inter', sans-serif;
      -webkit-font-smoothing: antialiased;
    }
    .container {
      width: 900px;
      min-height: 400px;
      background: #FFFEF2;
      position: relative;
      padding-bottom: 40px;
    }
    .top-bar {
      width: 100%;
      height: 5px;
      background: #288362;
    }
    .header {
      padding: 5px 40px;
      display: flex;
      align-items: center;
      gap: 12px;
      border-bottom: 1px solid rgba(40, 131, 98, 0.1);
    }
    .logo {
      width: 40px;
      height: 40px;
      position: relative;
      top: -2px;
    }
    .wordmark {
      color: rgba(28, 28, 28, 0.8);
      font-family: 'Lalezar', 'Inter', sans-serif;
      font-size: 28px;
    }
    .content {
      padding: 30px 40px 40px;
    }
    .ticker {
      font-size: 22px;
      font-weight: 600;
      color: #288362;
      margin: 0 0 32px 0;
      letter-spacing: -0.5px;
    }
    .analysis-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 40px;
      margin-top: 20px;
    }
    .analysis-section-horizontal {
      background: rgba(40, 131, 98, 0.03);
      border-radius: 16px;
      padding: 32px;
    }
    .analysis-section-horizontal h2 {
      font-size: 16px;
      font-weight: 600;
      margin: 0 0 16px 0;
      color: rgba(28, 28, 28, 0.9);
      display: inline-block;
      position: relative;
      padding-bottom: 15px;
    }
    .analysis-section-horizontal h2::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 0;
      width: 40px;
      height: 2px;
      background: #288362;
      border-radius: 2px;
      opacity: 0.8;
    }
    .analysis-content {
      font-size: 16px;
      line-height: 1.6;
      margin: 0;
      color: rgba(28, 28, 28, 0.8);
      font-weight: 400;
    }
    .stat {
      color: #288362;
      font-weight: 500;
    }
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
      <div class="ticker">$FCX</div>
      <div class="analysis-grid">
        <div class="analysis-section-horizontal">
          <h2>AVOID</h2>
          <p class="analysis-content">FCX faces rising unit costs (<span class="stat">+8% YoY</span> to <span class="stat">$2.49/lb</span> copper) amid lower copper & moly production. New smelter fire adds risks & delays ramp-up. Grasberg's IUPK renewal post-2041 uncertain, limiting long-term value.</p>
        </div>
        <div class="analysis-section-horizontal">
          <h2>CONSIDER</h2>
          <p class="analysis-content">FCX's Grasberg underground output & leaching tech boost copper production. Gold output to ramp up w/ new PMR. Strong avg realized copper price (<span class="stat">$4.21/lb</span>, <span class="stat">+9% YoY</span>) & operating cash flow (<span class="stat">$7.2B</span>) signal value. Potential Bagdad expansion & IUPK extension offer upside.</p>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
"""

output_path = "output.png"
html_to_image(html_content, output_path)
