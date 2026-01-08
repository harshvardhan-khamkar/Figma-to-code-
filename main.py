from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from models import ConvertRequest
from Services.figma_service import get_figma_file
from Services.layout_parser import parse_figma_layout
from Services.ai_services import generate_code
from storedb import save_figma_file, get_cached_figma
import os
import zipfile
import shutil

app = FastAPI()

@app.get("/")
def root():
    return {"message": "welcome to figma to code"}

@app.post("/convert")
def convert_design(req: ConvertRequest):
    try:
        figma_url = str(req.figma_url)

        # ---------- 1. Fetch or cache Figma ----------
        cached = get_cached_figma(figma_url, req.framework)

        if cached:
            print("[DEBUG] Cache hit its from mongo db")
            layout = cached["parsed_layout"]
        else:
            figma_json = get_figma_file(figma_url)
            layout = parse_figma_layout(figma_json)

            save_figma_file(
                figma_url=figma_url,
                figma_json=figma_json,
                layout=layout,
                code=None,  # we generate per-page
                framework=req.framework
            )

        # ---------- 2. Prepare output ----------
        output_dir = "output"
        zip_path = "figma-html-tailwind.zip"

        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir)

        # ---------- 3. Generate HTML per page ----------
        for page in layout["pages"]:
            page_name = page["page_name"].lower().replace(" ", "-")

            html = generate_code(page)  # ONE PAGE → ONE HTML

            file_name = "index.html" if page_name == "home" else f"{page_name}.html"
            file_path = os.path.join(output_dir, file_name)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html)

        # ---------- 4. Zip ----------
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for file in os.listdir(output_dir):
                zipf.write(
                    os.path.join(output_dir, file),
                    arcname=file
                )

        return FileResponse(
            path=zip_path,
            media_type="application/zip",
            filename="figma-html-tailwind.zip"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))