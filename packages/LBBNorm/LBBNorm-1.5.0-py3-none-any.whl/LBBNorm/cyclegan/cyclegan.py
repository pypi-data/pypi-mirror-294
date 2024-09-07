import os
from .options.test_options import TestOptions
from .data import create_dataset
from .models import create_model
from .util.visualizer import save_images
from .util import html
import requests
from tqdm import tqdm
from ..image_handler import LoadImages
from PIL import Image
from tqdm import tqdm

class CycleGAN:
  
    def __init__(self, model_path=''):
        self.model_name = "cyclegan_model.pth"
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
        destination = self._get_safe_path(self.model_name)
        
        if self._check_model(destination):
            print('Model already exists.')
            return
        
        download_url = "http://s79.ir/lbb/cyclegan_model.pth"
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



    def transform(self, path_image, result_dir='./cyclegan_results/'):
        if not self._check_model(self.model_path) or len(self.model_path) < 1:
            print("""Pretrained model file not found, please download or specify it first.
Hint: you can download the pretrained model with `model.download_model()`, or you can specify it like this `StainGAN(model_path='../../../model.pth')` on creation time.""")
            FileNotFoundError()
            return
        
        images,_,_ = LoadImages(path_image)
        
        image_objects = []
        for img in images:
            image_objects.append(Image.fromarray(img.astype('uint8'), 'RGB'))

        output = []
        # data_root = "assets"
        for img_ in tqdm(image_objects):
            img_ = [img_]
            opt = TestOptions().parse(result_dir)  # get test options
            # hard-code some parameters for test
            opt.num_threads = 0   # test code only supports num_threads = 0
            opt.batch_size = 1    # test code only supports batch_size = 1
            opt.serial_batches = True  # disable data shuffling; comment this line if results on randomly chosen images are needed.
            opt.no_flip = True    # no flip; comment this line if results on flipped images are needed.
            opt.display_id = -1   # no visdom display; the test code saves the results to a HTML file.
            dataset = create_dataset(opt, img_)  # create a dataset given opt.dataset_mode and other options
            model = create_model(opt)      # create a model given opt.model and other options
            model.setup(opt, self.model_path)               # regular setup: load and print networks; create schedulers
            # create a website
            web_dir = os.path.join(opt.results_dir, opt.name, '{}_{}'.format(opt.phase, opt.epoch))  # define the website directory
            if opt.suffix != '':
                web_dir += '_{}'.format(opt.suffix)
            if opt.load_iter > 0:  # load_iter is 0 by default
                web_dir = '{:s}_iter{:d}'.format(web_dir, opt.load_iter)
            #print('creating web directory', web_dir)
            webpage = html.HTML(web_dir, 'Experiment = %s, Phase = %s, Epoch = %s' % (opt.name, opt.phase, opt.epoch))
            # test with eval mode. This only affects layers like batchnorm and dropout.
            # For [pix2pix]: we use batchnorm and dropout in the original pix2pix. You can experiment it with and without eval() mode.
            # For [CycleGAN]: It should not affect CycleGAN as CycleGAN uses instancenorm without dropout.
            if opt.eval:
                model.eval()
            for i, data in enumerate(dataset):
                if i >= opt.num_test:  # only apply our model to opt.num_test images.
                    break
                
                model.set_input(data)  # unpack data from data loader
                model.test()           # run inference
                visuals = model.get_current_visuals()  # get image results
                img_path = model.get_image_paths()     # get image paths
                ims = save_images(webpage, visuals, img_path, aspect_ratio=opt.aspect_ratio, width=opt.display_winsize)
                
            webpage.save()  # save the HTML
            output.append(ims)
            
        if len(output) == 1:
            return output[0]
        else:
            return output