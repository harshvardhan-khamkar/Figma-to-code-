from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from models import ConvertRequest
from Services.figma_service import get_figma_file
from Services.layout_parser import parse_figma_layout
from Services.ai_services import generate_code
from storedb import save_figma_file, get_cached_figma
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "welcome to figma to code"}

@app.post("/convert")
def convert_design(req: ConvertRequest):
    try:
        # ---------- 1. Check MongoDB cache ----------
        figma_url = str(req.figma_url)
        cached = get_cached_figma(req.figma_url, req.framework)

        if cached:
            print(f"[DEBUG] Cache hit — using MongoDB for {figma_url} / {req.framework}")
            code = cached["code"]
        else:
            # ---------- 2. Fetch Figma JSON ----------
            figma_json = get_figma_file(str(req.figma_url))

            # ---------- 3. Parse layout (multi-page supported) ----------
            layout = parse_figma_layout(figma_json)

            # ---------- 4. Generate code ----------
            code = generate_code(layout, req.framework)

            # ---------- 5. Save everything to MongoDB ----------
            save_figma_file(
               figma_url=figma_url,
               figma_json=figma_json,
               layout=layout,
               code=code,
               framework=req.framework

            )

        # ---------- 6. Return downloadable file ----------
        if req.framework == "html-tailwind":
            file_path = "index.html"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)

            return FileResponse(
                path=file_path,
                media_type="text/html",
                filename="index.html"
            )

        return {"status": "success", "code": code}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
