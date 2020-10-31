import json

with open("backgrounds_data.json", "r") as f:
    data = json.load(f)
    finalists = []
    for image in list(data.keys()):
        for num, i in enumerate(data[image]["common_colours"]):
            if i[0] < 80 and i[1] < 80 and i[2] > 150:
                finalists.append(image)

    print(finalists)
