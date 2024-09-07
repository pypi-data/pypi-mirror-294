import os
import cv2
import numpy as np
import time
import yaml
from skimage import color
from fitter import Fitter



class DatasetConfig:
    def __init__(self, data_dir, save_dir, dataset_name="", methods="", color_space="LAB", random=False, n=0):
        self.data_dir = data_dir
        self.save_dir = save_dir
        self.dataset_name = dataset_name
        self.methods = methods
        self.color_space = color_space
        self.random = random
        self.n = n

    def __str__(self):
        return (f"DatasetConfig(data_dir={self.data_dir}, save_dir={self.save_dir}, "
                f"dataset_name={self.dataset_name}, methods={self.methods}, "
                f"color_space={self.color_space}, random={self.random}, n={self.n})")





def getavgstd(image):
    avg = []
    std = []
    image_avg_l = np.mean(image[:, :, 0])
    image_std_l = np.std(image[:, :, 0])
    image_avg_a = np.mean(image[:, :, 1])
    image_std_a = np.std(image[:, :, 1])
    image_avg_b = np.mean(image[:, :, 2])
    image_std_b = np.std(image[:, :, 2])
    avg.append(image_avg_l)
    avg.append(image_avg_a)
    avg.append(image_avg_b)
    std.append(image_std_l)
    std.append(image_std_a)
    std.append(image_std_b)
    return (avg, std)


class RandStainPreprocess:

    
    def do(self, data_dir='', save_dir='', dataset_name="", methods="", color_space="LAB", random=False, n=0):
        args = DatasetConfig(data_dir, save_dir, dataset_name, methods, color_space, random, n)

        path_dataset = args.data_dir

        labL_avg_List = []
        labA_avg_List = []
        labB_avg_List = []
        labL_std_List = []
        labA_std_List = []
        labB_std_List = []

        t1 = time.time()
        i = 0

        
        if True:
            path_class_list = os.listdir(path_dataset)
            if args.random:
                random.shuffle(path_class_list)

            for image in path_class_list:
                if args.n == 0:  # n=0: all images each class
                    pass
                elif i < args.n:
                    i += 1
                else:
                    i = 0
                    break
                path_img = os.path.join(path_dataset, image)
                img = cv2.imread(path_img)
                try:  # debug
                    if args.color_space == "LAB":
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
                    elif args.color_space == "HED":
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        img = color.rgb2hed(img)
                    elif args.color_space == "HSV":
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                    else:
                        print("wrong color space: {}!!".format(args.color_space))
                    img_avg, img_std = getavgstd(img)
                except:
                    continue
                    #print(path_img)
                labL_avg_List.append(img_avg[0])
                labA_avg_List.append(img_avg[1])
                labB_avg_List.append(img_avg[2])
                labL_std_List.append(img_std[0])
                labA_std_List.append(img_std[1])
                labB_std_List.append(img_std[2])
        t2 = time.time()
        print(t2 - t1)
        l_avg_mean = np.mean(labL_avg_List).item()
        l_avg_std = np.std(labL_avg_List).item()
        l_std_mean = np.mean(labL_std_List).item()
        l_std_std = np.std(labL_std_List).item()
        a_avg_mean = np.mean(labA_avg_List).item()
        a_avg_std = np.std(labA_avg_List).item()
        a_std_mean = np.mean(labA_std_List).item()
        a_std_std = np.std(labA_std_List).item()
        b_avg_mean = np.mean(labB_avg_List).item()
        b_avg_std = np.std(labB_avg_List).item()
        b_std_mean = np.mean(labB_std_List).item()
        b_std_std = np.std(labB_std_List).item()

        std_avg_list = [
            labL_avg_List,
            labL_std_List,
            labA_avg_List,
            labA_std_List,
            labB_avg_List,
            labB_std_List,
        ]
        distribution = []
        for std_avg in std_avg_list:
            f = Fitter(std_avg, distributions=["norm", "laplace"])
            f.fit()
            distribution.append(list(f.get_best(method="sumsquare_error").keys())[0])

        yaml_dict_lab = {
            "random": args.random,
            "n_each_class": args.n,
            "color_space": args.color_space,
            "methods": args.methods,
            "{}".format(args.color_space[0]): {  # lab-L/hed-H
                "avg": {
                    "mean": round(l_avg_mean, 3),
                    "std": round(l_avg_std, 3),
                    "distribution": distribution[0],
                },
                "std": {
                    "mean": round(l_std_mean, 3),
                    "std": round(l_std_std, 3),
                    "distribution": distribution[1],
                },
            },
            "{}".format(args.color_space[1]): {  # lab-A/hed-E
                "avg": {
                    "mean": round(a_avg_mean, 3),
                    "std": round(a_avg_std, 3),
                    "distribution": distribution[2],
                },
                "std": {
                    "mean": round(a_std_mean, 3),
                    "std": round(a_std_std, 3),
                    "distribution": distribution[3],
                },
            },
            "{}".format(args.color_space[2]): {  # lab-B/hed-D
                "avg": {
                    "mean": round(b_avg_mean, 3),
                    "std": round(b_avg_std, 3),
                    "distribution": distribution[4],
                },
                "std": {
                    "mean": round(b_std_mean, 3),
                    "std": round(b_std_std, 3),
                    "distribution": distribution[5],
                },
            },
        }
        yaml_save_path = "{}/{}.yaml".format(
            args.save_dir,
            args.dataset_name
            if args.dataset_name != ""
            else "dataset_{}_random{}_n{}".format(args.color_space, args.random, args.n),
        )
        with open(yaml_save_path, "w") as f:
            yaml.dump(yaml_dict_lab, f)
            print("The dataset lab statistics has been saved in {}".format(yaml_save_path))
        
        return yaml_save_path