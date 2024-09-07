import numpy as np
import torch
from .StainNet.models import StainNet as STNet
import requests
from tqdm import tqdm
import os
from ..image_handler import LoadImages


class StainNet:
    
    # def __init__(self, mode):
        
    #     self.model_stainnet = StainNet()
    #     if mode == "cytopathology":
    #         self.model_stainnet.load_state_dict(torch.load("./StainNet/checkpoints/aligned_cytopathology_dataset/StainNet-3x0_best_psnr_layer3_ch32.pth", map_location=torch.device('cpu')))
    #     if mode == "histopathology":
    #         self.model_stainnet.load_state_dict(torch.load("./StainNet/checkpoints/aligned_histopathology_dataset/StainNet-Public_layer3_ch32.pth", map_location=torch.device('cpu')))
    #     if mode == "camelyon":
    #         self.model_stainnet.load_state_dict(torch.load("./StainNet/checkpoints/camelyon16_dataset/StainNet-Public-centerUni_layer3_ch32.pth", map_location=torch.device('cpu')))

    def __init__(self, model_path='',model_pathr='', run_type='cpu'):
        self.model_name = "stainet_model.pth"
        self.is_model_ready = model_path != ''
        self.model_path = model_path
        self.run_type = run_type
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
        
        download_url = "http://s79.ir/lbb/stainnet_model.pth"
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
  
    
    def norm(self, image):
        image = np.array(image).astype(np.float32)
        image = image.transpose((2, 0, 1))
        image = ((image / 255) - 0.5) / 0.5
        image=image[np.newaxis, ...]
        image=torch.from_numpy(image)
        return image

    def un_norm(self, image):
        image = image.cpu().detach().numpy()[0]
        image = ((image * 0.5 + 0.5) * 255).astype(np.uint8).transpose((1,2,0))
        return image   
    
    
    def transform(self, path_image):
        
        if not self._check_model(self.model_path) or len(self.model_path) < 1:
            print("""Pretrained model file not found, please download or specify it first.
Hint: you can download the pretrained model with `model.download_model()`, or you can specify it like this `StainGAN(model_path='../../../model.pth')` on creation time.""")
            FileNotFoundError()
            return
        print(self.model_path)
        self.model_stainnet = STNet()
        self.model_stainnet.load_state_dict(torch.load(self.model_path, map_location=torch.device(self.run_type)))

        images,_,__ = LoadImages(path_image)
        
        output = []
        for img in images:
            image_net=self.model_stainnet(self.norm(img))
            image_net=self.un_norm(image_net)
            
            output.append(image_net)
        
        
        if len(output) == 1:
            return output[0]
        else:
            return image_net