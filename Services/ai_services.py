import os
from google.genai import Client
from dotenv import load_dotenv

load_dotenv()

client = Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_code(page_layout: dict) -> str:
    prompt = f"""
You are a senior frontend developer.

TASK:
Convert the following SINGLE PAGE layout into a COMPLETE, PRODUCTION-READY HTML file.

OUTPUT RULES (STRICT):
- Output ONLY valid HTML
- NO JSON
- NO markdown
- NO explanations
- NO JavaScript
- NO custom CSS

HTML REQUIREMENTS:
- Must start with <!DOCTYPE html>
- Must include <html>, <head>, <body>
- Include Tailwind CDN inside <head>:
  <script src="https://cdn.tailwindcss.com"></script>

DESIGN RULES:
- Apply modern SaaS design principles
- Strong visual hierarchy
- Clean spacing and alignment
- Responsive layout using flex/grid
- Use Tailwind utility classes ONLY

SEMANTIC RULES:
- Header / Navbar → <header>
- Footer → <footer>
- Main content → <main> / <section>
- TEXT → h1 / h2 / p / button based on context
- Ignore VECTOR, ELLIPSE, RECTANGLE

LAYOUT → STYLE MAPPING:
- layout.direction:
  - HORIZONTAL → flex flex-row
  - VERTICAL → flex flex-col
- layout.gap → gap-[px]
- layout.padding → p-[px]
- fontSize → text-[px]
- fontWeight → font-normal | font-medium | font-semibold | font-bold
- textAlign → text-left | text-center

INPUT PAGE LAYOUT:
{page_layout}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text