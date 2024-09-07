import os
from randstainna import RandStainNA
import cv2

if __name__ == "__main__":

    """
    Usage1: Demo(for visualization)
    """
    # Setting: is_train = False
    randstainna = RandStainNA(
        yaml_file = '/home/thecapitanprice/driveA/python/LLB/LBBNorm/src/LBBNorm/randstain/randstainna/CRC.yaml',
        std_hyper = 0.0,
        distribution = 'normal',
        probability = 1.0,
        is_train = False
    )

    img_path_list = os.listdir('./data/')
    save_dir_path = './visualization'
    if not os.path.exists(save_dir_path):
        os.mkdir(save_dir_path)

    for img_path in img_path_list:
        img = randstainna(cv2.imread('./data/'+img_path))
        save_img_path = save_dir_path + '/{}'.format(img_path.split('/')[-1])
        cv2.imwrite(save_img_path,img)

    """
    Usage2：torchvision.transforms (for training)
    """
    # # Setting: is_train = True
    # from torchvision import transforms

    # #### calling the randstainna
    # transforms_list = [
    #     RandStainNA(
    #         yaml_file="/home/thecapitanprice/driveA/python/LLB/LBBNorm/src/LBBNorm/randstain/randstainna/CRC.yaml",
    #         std_hyper=-0.3,
    #         probability=1.0,
    #         distribution="normal",
    #         is_train=True,
    #     )
    # ]
    # transforms.Compose(transforms_list)