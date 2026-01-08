def extract_elements(node: dict) -> list:
    """
    Recursively extracts child elements from a Figma node.

    Captures:
    - type (FRAME, TEXT, etc.)
    - name
    - text (for TEXT nodes)
    - basic typography style
    - basic layout metadata (for FRAME nodes)
    """

    elements = []

    for child in node.get("children", []):
        node_type = child.get("type")

        el = {
            "type": node_type,
            "name": child.get("name", "")
        }

        # -------- TEXT STYLE EXTRACTION --------
        style = child.get("style", {})
        el["style"] = {
            "fontSize": style.get("fontSize"),
            "fontWeight": style.get("fontWeight"),
            "textAlign": style.get("textAlignHorizontal")
        }

        # -------- FRAME LAYOUT EXTRACTION --------
        if node_type == "FRAME":
            el["layout"] = {
                "direction": child.get("layoutMode"),      # HORIZONTAL / VERTICAL
                "gap": child.get("itemSpacing"),
                "padding": child.get("paddingLeft")
            }

        # -------- TEXT CONTENT --------
        if node_type == "TEXT":
            el["text"] = child.get("characters", "")

        # -------- RECURSION --------
        el["children"] = extract_elements(child)

        elements.append(el)

    return elements


def parse_figma_layout(figma_json: dict) -> dict:
    """
    Parses a full Figma file into a structured, app-ready layout:

    Output structure:
    - file_name
    - globals   -> shared components (header/footer/nav)
    - pages     -> page-specific sections

    This structure is suitable for:
    - HTML layouts
    - React / Angular routing
    """

    document = figma_json.get("document", {})

    layout = {
        "file_name": document.get("name", "Figma File"),
        "globals": {},     # shared layout components
        "pages": []
    }

    # Heuristic keywords for shared components
    GLOBAL_KEYS = ["header", "navbar", "nav", "footer"]

    for page in document.get("children", []):
        page_name = page.get("name", "")

        page_data = {
            "page_name": page_name,
            "slug": page_name.lower().replace(" ", "-"),
            "sections": []
        }

        for node in page.get("children", []):
            node_type = node.get("type")
            if node_type not in ["FRAME", "INSTANCE"]:
                continue

            name = node.get("name", "")
            name_lower = name.lower()

            extracted_children = extract_elements(node)

            # -------- GLOBAL COMPONENT DETECTION --------
            if any(key in name_lower for key in GLOBAL_KEYS):
                # store once only
                if name_lower not in layout["globals"]:
                    layout["globals"][name_lower] = {
                        "name": name,
                        "type": node_type,
                        "children": extracted_children
                    }
                continue

            # -------- PAGE-SPECIFIC SECTIONS --------
            page_data["sections"].append({
                "name": name,
                "type": node_type,
                "children": extracted_children
            })

        layout["pages"].append(page_data)

    return layout
