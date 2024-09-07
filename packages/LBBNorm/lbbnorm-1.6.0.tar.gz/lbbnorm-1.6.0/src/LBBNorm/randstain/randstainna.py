from .preprocess import RandStainPreprocess
from .convertor import RandStainNAConvertor
import cv2
from ..image_handler import LoadImages



class RandStain():
    def __init__(self, yaml_file=None) -> None:
        self.yaml_file = yaml_file
    
    def fit(self, data_dir='', save_dir='./', dataset_name="", methods="", color_space="LAB", random=False, n=0):
        
        self.yaml_file = RandStainPreprocess().do( data_dir, save_dir, dataset_name, methods, color_space, random, n)
        
    def transform(self,image_paths,yaml_file=None,
            std_hyper = 0.0,
            distribution = 'normal',
            probability = 1.0,
            is_train = False
                  ):
        
        if yaml_file == None and self.yaml_file == None:
            print('You have to fit the model first.')
            AssertionError()
            return
        if yaml_file != None:
            self.yaml_file = yaml_file
        
        _,_,image_paths_list = LoadImages(image_paths)
        
        
        randstainna = RandStainNAConvertor(
            yaml_file = self.yaml_file,
            std_hyper = std_hyper,
            distribution = distribution,
            probability = probability,
            is_train = is_train
        )
        
        output = []
        for img_path in image_paths_list:
            img = randstainna(cv2.imread(img_path))
            output.append(img)
        
        if len(output) == 1:
            return output[0]
        else:
            return output
        
        
        
        
        