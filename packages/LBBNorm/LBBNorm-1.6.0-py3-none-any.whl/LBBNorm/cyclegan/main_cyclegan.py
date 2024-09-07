from cyclegan import CycleGAN
from PIL import Image
import matplotlib.pyplot as plt

load_path = "D:\\research\\articles\\code_template\\normalization\\cyclegan - static-checkpoint\\CycleGAN\\results\\mitos-atypia\\latest_net_G_A.pth"
path_image = "D:\\research\\articles\\code_template\\normalization\\cyclegan - static-checkpoint\\CycleGAN\\assets\\testA\\1001702_1.tif"
result_dir = "result-final-images"
image =Image.open(path_image)
result = CycleGAN().transform(load_path, image, result_dir)
normalized_image = Image.fromarray(result)

plt.imshow(normalized_image)
plt.show()
