import json

with open("devices.json", "r") as f:
    content = json.load(f)

# Get pages (number and content)
for page_num, page_content in enumerate(content):
    # Get tiles (number and content)
    for item_num, item_content in enumerate(page_content["children"]):
        # If that tile is current opened tile, rewrite
        content[page_num]["children"][item_num]["protocols"] = []
        for item_num2, item_content2 in enumerate(item_content["modal"]):
            content[page_num]["children"][item_num]["modal"][item_num2]["protocols"] = []

with open("devices.json", "w") as f:
    json.dump(content, f)
