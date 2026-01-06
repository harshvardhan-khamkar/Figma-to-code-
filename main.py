from fastapi import FastAPI, HTTPException
from models import ConvertRequest
from Services.figma_service import get_figma_file
from Services.layout_parser import parse_figma_layout
from Services.ai_services import generate_code
from fastapi.responses import FileResponse


app = FastAPI()

@app.get("/")
def root():
    return {"message": "welcome to figma to code"}

@app.post("/convert")
def convert_design(req: ConvertRequest):
    try:
        figma_json = get_figma_file(str(req.figma_url))  # Ensure figma_url is a string
        layout = parse_figma_layout(figma_json)
        code = generate_code(layout, req.framework)
        
        """
        print("TOP LEVEL KEYS:", figma_json.keys())     
        doc = figma_json["document"]
        print("DOCUMENT TYPE:", doc["type"])
        print("DOCUMENT NAME:", doc["name"])
        print("CHILD COUNT:", len(doc["children"]))

        page = figma_json["document"]["children"][0]

        print("PAGE TYPE:", page["type"])
        print("PAGE NAME:", page["name"])
        print("PAGE CHILD COUNT:", len(page["children"]))
        for idx, frame in enumerate(page["children"]):
            print(f"{idx}. FRAME NAME:", frame["name"])
            print("   TYPE:", frame["type"])
            print("   CHILD ELEMENTS:", len(frame.get("children", [])))
        frame = page["children"][0]

        for idx, element in enumerate(frame["children"]):
            print(f"\nElement {idx}")
            print("TYPE:", element["type"])
            print("NAME:", element["name"])
        header_frame = None

        for el in frame["children"]:
            if el["type"] == "FRAME" and el["name"].lower() == "header":
                header_frame = el
                break
        for idx, child in enumerate(header_frame.get("children", [])):
            print(idx, child["type"], child["name"])

        """  # Debugging prints to explore figma_json structure
        
        if req.framework == "html-tailwind":
            file_path = "index.html"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)

            return FileResponse(
                file_path,
                media_type="text/html",
                filename="index.html"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
