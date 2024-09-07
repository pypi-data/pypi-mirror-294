#%%
from stainnet.stain_net import Stainnet
from PIL import Image 
import matplotlib.pyplot as plt


# mode = ["histopathology", "camelyon", "cytopathology"]
checkpoint_dir ="./StainNet/checkpoints/aligned_cytopathology_dataset/StainNet-3x0_best_psnr_layer3_ch32.pth"
# img_source=Image.open("./StainNet/assets/3_color_net_neg23570_ori.png")
img_source=Image.open("./test.png")

# plt.imshow(img_source)

model = Stainnet(checkpoint_dir)
normalized_image = model.transform(img_source)
normalized_image = Image.fromarray(normalized_image)

plt.imshow(normalized_image)
plt.show()