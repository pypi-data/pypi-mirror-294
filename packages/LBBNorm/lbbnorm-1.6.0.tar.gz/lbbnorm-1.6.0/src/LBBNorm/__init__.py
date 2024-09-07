import importlib
from .macenko import Macenko
from .vahadane import Vahadane
from .reinhard import Reinhard
from .modified_reinhard import ModifiedReinhard
from .adaptive_color_deconvolution import AdaptiveColorDeconvolution
from .staingan.staingan import StainGAN
from .cyclegan.cyclegan import CycleGAN
from .stainnet.stain_net import StainNet
from .randstain.randstainna import RandStain


#from .slide_patcher import SlidePatcher


# def __getattr__(name):
#     if name == 'Macenko':
#         sub_class_module = importlib.import_module('.macenko', __name__)
#         sub_class = getattr(sub_class_module, name)
#         return sub_class
#     elif name == 'Vahadane':
#         sub_class_module = importlib.import_module('.vahadane', __name__)
#         sub_class = getattr(sub_class_module, name)
#         return sub_class
#     elif name == 'AdaptiveColorDeconvolution':
#         sub_class_module = importlib.import_module('.adaptive_color_deconvolution', __name__)
#         sub_class = getattr(sub_class_module, name)
#         return sub_class
#     elif name == 'Reinhard':
#         sub_class_module = importlib.import_module('.reinhard', __name__)
#         sub_class = getattr(sub_class_module, name)
#         return sub_class
#     elif name == 'ModifiedReinhard':
#         sub_class_module = importlib.import_module('.modified_reinhard', __name__)
#         sub_class = getattr(sub_class_module, name)
#         return sub_class
#     elif name == 'StainGAN':
#         sub_class_module = importlib.import_module('.staingan.staingan', __name__)
#         sub_class = getattr(sub_class_module, name)
#         return sub_class
#     elif name == 'RandstainNA':
#         sub_class_module = importlib.import_module('.randstain', __name__)
#         sub_class = getattr(sub_class_module, name)
#         return sub_class
    
#     raise AttributeError(f"module {__name__} has no attribute {name}")