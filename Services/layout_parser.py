def extract_elements(node):
    elements = []

    for child in node.get("children", []):
        el = {
            "type": child["type"],
            "name": child.get("name", "")
        }
        # style extraction
        style = child.get("style", {})
        el["style"] = {
                "fontSize": style.get("fontSize"),
                "fontWeight": style.get("fontWeight"),
                "textAlign": style.get("textAlignHorizontal")
            }

        # FRAME layout
        if child["type"] == "FRAME":
            el["layout"] = {
                "direction": child.get("layoutMode"),
                "gap": child.get("itemSpacing"),
                "padding": child.get("paddingLeft")
            }

        if child["type"] == "TEXT":
            el["text"] = child.get("characters", "")

        # recursion
        el["children"] = extract_elements(child)

        elements.append(el)

    return elements

def parse_figma_layout(figma_json: dict) -> dict:
    document = figma_json["document"]
    page = document["children"][0]
    desktop = page["children"][0]

    layout = {
        "page": page["name"],
        "sections": []
    }

    for frame in desktop.get("children", []):
        if frame["type"] not in ["FRAME", "INSTANCE"]:
            continue

        section = {
            "name": frame.get("name", ""),
            "type": frame.get("type", ""),
            "children": extract_elements(frame)
        }

        layout["sections"].append(section)

    return layout
