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

        for tries in range(5):
            # Browse directory and load backgrounds
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
                if backgrounds:
                    return random.choice(backgrounds)

                else:
                    return None

        self.__console.print(data="Fatal error in background chooser!", priority=2)

    def reclassify(self):
        """
        Reclassify images
        :return: None
        """

        # print(self.__console.FG_COLORS["green"] + self.__console.SPECIAL["bold"] + "Reinitialising..." + self.__console.END)
        self.__fmng.img_data = {}

        images = self.__fmng.list_file_names(path=self.IMG_PATH, full_path=True)
        self.__fmng.img_data = self.classify(images=images)

    def classify(self, images):
        """
        Classify images
        :return: None
        """

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
            # TODO dark and ultra dark 255 - 60; 60-30; 30-0
            if 0 <= average <= int(self.__fmng.config["imng"]["limit-ultra-dark"]):
                img_data[filename]["type"] = "ultra-dark"

            elif int(self.__fmng.config["imng"]["limit-ultra-dark"]) < average <= int(self.__fmng.config["imng"]["limit-dark"]):
                img_data[filename]["type"] = "dark"

            elif int(self.__fmng.config["imng"]["limit-dark"]) < average:
                img_data[filename]["type"] = "light"

            else:
                self.__console.print("Fatal error in background classifier!", 2)
            print("{0}{1}Reinit{2}\tImg {3}/{4}\t{5}%".format(self.__console.FG_COLORS["green"],
                                                              self.__console.SPECIAL["bold"],
                                                              self.__console.END, num+1, len(images),
                                                              round((num+1)/len(images)*100, 1)))
            # im.save(i)
        return img_data

    def main(self):
        """
        Main of image classify
        :return: None
        """

        if list(self.__fmng.img_data.keys()).sort() != self.__fmng.list_file_names(path=self.IMG_PATH).sort() or self.__fmng.img_data == {} or self.__fmng.config["imng"].getboolean("reclassify"):
            self.reclassify()
