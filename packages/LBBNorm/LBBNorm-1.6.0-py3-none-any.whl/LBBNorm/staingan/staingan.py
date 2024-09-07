import time
import os, sys
from .options.test_options import TestOptions
from .data.data_loader import CreateDataLoader
from .models.models import create_model
from .util.visualizer_time import Visualizer
from .util import html
import requests
from tqdm import tqdm
import os
from ..image_handler import LoadImages

class StainGAN:
    
    
    def __init__(self, model_path=''):
        self.model_name = "staingan_model.pth"
        self.is_model_ready = model_path != ''
        self.model_path = model_path
        
        self._check_model(self._get_safe_path(self.model_name))
        
    def _get_safe_path(self,filename):
        home_dir = os.path.expanduser("~")
        dir_name = ".lbbnorm"
        safe_path = os.path.join(home_dir, dir_name)
        if not os.path.exists(safe_path):
            os.makedirs(safe_path)
        return os.path.join(safe_path, filename)
    
    def _check_model(self,model_path):
        
        if os.path.exists(model_path):
            self.model_path = model_path
            self.is_model_ready = True
            return True
        else:
            return False
    

    def download_model(self):
        public_url = "https://drive.google.com/file/d/1VzZeeUWDLpolY1_zECFD8MwSkbF1Ps37/view?usp=sharing"
        destination = self._get_safe_path(self.model_name)
        
        if self._check_model(destination):
            print('Model already exists.')
            return
        
        file_id = public_url.split('/')[-2]
        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        response = requests.get(download_url, stream=True)
        total_size_in_bytes= int(response.headers.get('content-length', 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        with open(destination, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print("ERROR, something went wrong, check your internet connection.")
            try:
                os.remove(destination)
            except:
                pass
        else:
            self.model_path = destination
            self.is_model_ready = True
  
    
    def transform(self, path_image, image_size,results_dir='./staingan_resluts/'):
        
        if not self._check_model(self.model_path) or len(self.model_path) < 1:
            print("""Pretrained model file not found, please download or specify it first.
Hint: you can download the pretrained model with `model.download_model()`, or you can specify it like this `StainGAN(model_path='../../../model.pth')` on creation time.""")
            FileNotFoundError()
            return
        
        _,_,path_image_list = LoadImages(path_image)
        
        print(path_image_list)
        
        output = []
        
        for path_image in tqdm(path_image_list):  
            opt = TestOptions().parse(image_size,results_dir)
            opt.nThreads = 1  # test code only supports nThreads = 1
            opt.batchSize = 1  # test code only supports batchSize = 1
            opt.serial_batches = True  # no shuffle
            opt.no_flip = True  # no flip
            
            data_loader = CreateDataLoader(opt,path_image)
            dataset = data_loader.load_data()
            model = create_model(opt,self.model_path)
            visualizer = Visualizer(opt)
            # create website
            # web_dir = os.path.join(opt.results_dir, opt.name, '%s_%s' % (opt.phase, opt.which_epoch))
            
            web_dir = os.path.join(opt.dataroot, '_StainGAN')
            if opt.results_dir:
                web_dir = opt.results_dir
            
            # #print("web_dir ", web_dir)
            # sys.exit()
            webpage = html.HTML(web_dir, 'Experiment = %s, Phase = %s, Epoch = %s' % (opt.name, opt.phase, opt.which_epoch))
            # test
            ##print("Dataset", len(dataset))
            start_time = time.time()
            
            for i, data in enumerate(dataset):
                if opt.how_many:
                    ##print("how_many", opt.how_many)
            
                    if i >= opt.how_many:
                        break
                model.set_input(data)
                model.test()
                visuals = model.get_current_visuals()
                img_path = model.get_image_paths()
                # #print('%04d: process image... %s' % (i, img_path))
                ##print('%04d: process image' % (i))
                img = visualizer.save_images(visuals, img_path, aspect_ratio=opt.aspect_ratio)
            
            output.append(img)
        
        if len(output)==1:
            return output[0]
        else:
            return output
        