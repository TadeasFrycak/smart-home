from PIL import Image
import random
import numpy


class ImageManager:
    IMG_PATH = "static/img/backgrounds"

    def __init__(self, fmng, console):
        self.__fmng = fmng
        self.__console = console
        self.main()

    def random_background(self, bg_type="light"):
        """
        Load backgrounds and choose one of them (randomly)
        :return:
        """

        tries = 0
        while True:
            # Browse directory and load backgrounds
            tries += 1
            backgrounds = []
            for file in self.__fmng.list_file_names(path=self.IMG_PATH):
                try:
                    if self.__fmng.img_data[file]["type"] == bg_type:
                        backgrounds.append(file)

                except Exception as e:
                    self.__console.print(data="Backgrounds changed due {0}".format(e), priority=1)
                    self.reclassify()
                    break
            else:
                return random.choice(backgrounds)

            if tries >= 5:
                self.__console.print(data="Fatal error in background chooser!", priority=2)
                break

    def reclassify(self):
        print(self.__console.FG_COLORS["green"] + self.__console.SPECIAL["bold"] + "Reinitialising..." + self.__console.END)
        self.__fmng.img_data = {}

        images = self.__fmng.list_file_names(path=self.IMG_PATH, full_path=True)
        self.__fmng.img_data = self.classify(images=images)

    def classify(self, images):
        img_data = {}

        for num, path in enumerate(images):
            image = Image.open(path)

            average = numpy.mean(image)
            filename = self.__fmng.get_filename_from_path(path)
            img_data[filename] = {}
            img_data[filename]["average_pix"] = round(average, 2)
            img_data[filename]["format"] = image.format
            img_data[filename]["mode"] = image.mode
            img_data[filename]["size"] = image.size

            if average <= 35:
                img_data[filename]["type"] = "dark"

            else:
                img_data[filename]["type"] = "light"

            print(self.__console.FG_COLORS["green"] + self.__console.SPECIAL["bold"] + "Initialise: " + self.__console.END + str(round((num+1)/len(images)*100, 1))+"%")
            # im.save(i)
        return img_data

    def main(self):
        if list(self.__fmng.img_data.keys()).sort() != self.__fmng.list_file_names(path=self.IMG_PATH).sort() or self.__fmng.img_data == {}:
            self.reclassify()
