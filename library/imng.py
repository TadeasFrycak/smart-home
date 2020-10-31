from sklearn.cluster import KMeans, MiniBatchKMeans
from PIL import Image, ImageFilter
import random
import numpy
import cv2


class ImageManager:
    IMG_PATH = "static/img/backgrounds/original"
    IMG_PATH_BLUR = "static/img/backgrounds"

    def __init__(self, fmng, terminal):
        self.__fmng = fmng
        self.__terminal = terminal
        self.main()

    def random_background(self, bg_type="light", background="smart"):
        """
        Load backgrounds and choose one of them (randomly)
        :return:
        """

        if background != "random" and background != "smart":
            return background

        for tries in range(5):
            # Browse directory and load backgrounds
            backgrounds = []
            for file in self.__fmng.list_file_names(path=self.IMG_PATH):
                try:
                    if background == "random" or (background == "smart" and self.__fmng.backgrounds_data[file]["type"] == bg_type):
                        backgrounds.append(file)

                except Exception as e:
                    self.__terminal.warning(data="Backgrounds changed due {0}".format(e))
                    self.reclassify()
                    break
            else:
                if backgrounds:
                    return random.choice(backgrounds)

                else:
                    return None  # Black background

        self.__terminal.error(data="Fatal error in background chooser!")

    def classify(self, images):
        """
        Classify images
        :return: None
        """

        def print_state(num_img, total_num, state, message):
            whitespace = "                             "
            self.__terminal.print("{0}{1}State{2}\tImg {3}/{4} ({5}%) \t{6}% ... {7}{8}\r".format(self.__terminal.FG_COLORS["green"],
                                                                               self.__terminal.SPECIAL["bold"],
                                                               self.__terminal.END, num_img + 1,
                                                               total_num, round((num_img+1) / total_num * 100, 1),
                                                               state, message, whitespace), end="")
        print()
        # todo original bude v backgrounds, blur ve složce blur, redukovanáí kvalita v reduce/, ....
        for num, path in enumerate(images):
            print_state(num, len(images), 0, "Loading image")
            image = Image.open(path)

            print_state(num, len(images), 30, "Averaging pixels")
            average = numpy.mean(image)
            filename = self.__fmng.get_filename_from_path(path)
            self.__fmng.backgrounds_data[filename] = {}
            self.__fmng.backgrounds_data[filename]["avg_pixel"] = round(float(average))
            self.__fmng.backgrounds_data[filename]["format"] = image.format
            self.__fmng.backgrounds_data[filename]["mode"] = image.mode
            self.__fmng.backgrounds_data[filename]["size"] = image.size

            if "dark" in filename.lower():
                self.__fmng.backgrounds_data[filename]["type"] = "dark"

            elif "light" in filename.lower():
                self.__fmng.backgrounds_data[filename]["type"] = "light"

            else:
                if 0 <= average <= int(self.__fmng.config["imng"]["limit-dark"]):
                    self.__fmng.backgrounds_data[filename]["type"] = "dark"

                elif int(self.__fmng.config["imng"]["limit-dark"]) < average:
                    self.__fmng.backgrounds_data[filename]["type"] = "light"

                else:
                    self.__terminal.error("Fatal error in background classifier!")

            print_state(num, len(images), 60, "Bluring image")
            blur = image.filter(ImageFilter.GaussianBlur(18))
            blur.save(self.__fmng.path_join(self.IMG_PATH_BLUR, filename))
            print_state(num, len(images), 80, "Common colors")
            self.__fmng.backgrounds_data[filename]["common_colours"] = self.get_most_common_colors(path=path)
            print_state(num, len(images), 100, "Completed")
            print()
        print("\n")
        self.__fmng.backgrounds_data = self.__fmng.backgrounds_data

    def main(self):
        """
        Main of image classify
        :return: None
        """

        images = self.__fmng.list_file_names(path=self.IMG_PATH)
        for image in list(self.__fmng.backgrounds_data.keys()):
            if image not in images:
                del self.__fmng.backgrounds_data[image]

        images_temp = list(self.__fmng.backgrounds_data.keys())
        to_classify = []

        for image in images:
            if image not in images_temp:
                to_classify.append(self.__fmng.path_join(self.IMG_PATH, image))

        self.__fmng.backgrounds_data = self.__fmng.backgrounds_data

        if to_classify or self.__fmng.config["imng"].getboolean("reclassify"):
            self.classify(to_classify)

    @staticmethod
    def make_histogram(cluster):
        """
        Count the number of pixels in each cluster
        :param: KMeans cluster
        :return: numpy histogram
        """

        num_labels = numpy.arange(0, len(numpy.unique(cluster.labels_)) + 1)
        hist, _ = numpy.histogram(cluster.labels_, bins=num_labels)
        hist = hist.astype('float32')
        hist /= hist.sum()
        return hist

    def get_most_common_colors(self, path, count=5):
        """
        Use k-means clustering to find the most-common colors in an image
        :param path:
        :param count:
        :return:
        """

        img = cv2.imread(path)
        height, width, _ = numpy.shape(img)
        image = img.reshape((height * width, 3))  # Reshape the image to be a simple list of RGB pixels

        clusters = MiniBatchKMeans(n_clusters=count, batch_size=1000, max_iter=5)
        clusters.fit(image)

        histogram = self.make_histogram(clusters)  # Count the dominant colors and put them in "buckets"

        combined = zip(histogram, clusters.cluster_centers_)  # Then sort them, most-common first
        combined = sorted(combined, key=lambda x: x[0], reverse=True)

        all_colors = []
        for index, rows in enumerate(combined):
            all_colors.append(list(rows[1]))

        return all_colors
