import os
from google.genai import Client
from dotenv import load_dotenv

load_dotenv()

client = Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_code(layout: dict, framework: str) -> str:
    prompt = f"""
You are a senior frontend developer.

TASK:
Convert the following parsed Figma layout JSON into PRODUCTION-READY frontend code.

TARGET FRAMEWORK:
{framework}

GENERAL RULES (ALWAYS):
- Use semantic structure
- TEXT → h1/h2/p/button based on context
- Ignore VECTOR, ELLIPSE, RECTANGLE
- No explanation
- Output ONLY code

DESIGN QUALITY RULES:
- Apply modern SaaS design principles
- Strong visual hierarchy
- Proper spacing and alignment
- Sensible font sizes
- Clean responsive layout

IF framework == "html-tailwind":
- Output a COMPLETE HTML file
- Must start with <!DOCTYPE html>
- Include <html>, <head>, <body>
- Include Tailwind CDN:
  <script src="https://cdn.tailwindcss.com"></script>
- Use Tailwind utility classes only
- No JS
- No custom CSS

IF framework == "react":
- Output a COMPLETE React component (App.jsx)
- Use functional components
- JSX only
- Tailwind classes allowed
- No React imports explanation
- No comments

IF framework == "angular":
- Output:
  1. app.component.html
  2. app.component.ts
- Use Angular best practices
- Tailwind classes allowed
- No explanation

LAYOUT → STYLE MAPPING:
- layout.direction:
    HORIZONTAL → flex flex-row
    VERTICAL → flex flex-col
- layout.gap → gap-[px]
- layout.padding → p-[px]
- fontSize → text-[px] or nearest Tailwind size
- fontWeight → font-normal | font-medium | font-semibold | font-bold
- textAlign → text-left | text-center

INPUT LAYOUT:
{layout}
"""


    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text
