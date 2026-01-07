def extract_elements(node):
    """
    Recursively extracts all child elements of a Figma node,
    including type, name, text (for TEXT nodes), styles, and layout info (for FRAME nodes).
    """
    elements = []

    for child in node.get("children", []):
        el = {
            "type": child["type"],           # Node type (FRAME, TEXT, RECTANGLE, etc.)
            "name": child.get("name", "")    # Node name
        }

        # ----- Style extraction (for TEXT nodes and others if available) -----
        style = child.get("style", {})
        el["style"] = {
            "fontSize": style.get("fontSize"),
            "fontWeight": style.get("fontWeight"),
            "textAlign": style.get("textAlignHorizontal")
        }

        # ----- Layout extraction (for FRAME nodes) -----
        if child["type"] == "FRAME":
            el["layout"] = {
                "direction": child.get("layoutMode"),  # HORIZONTAL or VERTICAL
                "gap": child.get("itemSpacing"),       # spacing between children
                "padding": child.get("paddingLeft")    # padding (simplified)
            }

        # ----- Text content (for TEXT nodes) -----
        if child["type"] == "TEXT":
            el["text"] = child.get("characters", "")

        # ----- Recursively extract children -----
        el["children"] = extract_elements(child)

        elements.append(el)

    return elements


def parse_figma_layout(figma_json: dict) -> dict:
    """
    Parses an entire Figma file JSON into a structured layout dictionary
    that includes multiple pages, each page's frames/sections, 
    and all nested elements with style and layout info.
    """
    document = figma_json.get("document", {})

    layout = {
        "file_name": document.get("name", "Figma File"),  # optional: file name
        "pages": []  # store multiple pages
    }

    # ----- Loop over all pages in the Figma file -----
    for page in document.get("children", []):
        page_data = {
            "page_name": page.get("name", ""),
            "sections": []  # each top-level frame/instance on the page
        }

        # ----- Loop over all top-level nodes in the page -----
        for node in page.get("children", []):
            # Only treat FRAME and INSTANCE as sections
            if node["type"] not in ["FRAME", "INSTANCE"]:
                continue

            section = {
                "name": node.get("name", ""),
                "type": node.get("type", ""),
                "children": extract_elements(node)  # recursive extraction
            }

            page_data["sections"].append(section)

        layout["pages"].append(page_data)

    return layout
