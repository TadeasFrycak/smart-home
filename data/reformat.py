with open("names.txt", mode="r") as f:
    data = f.readlines()

    for i in data:
        data2 = i.strip().split(" ")
        real_data2 = []

        for j in data2:
            if j != "" and len(j) > 1:
                real_data2.append(j.strip())

        if real_data2 != []:
            print(real_data2)
