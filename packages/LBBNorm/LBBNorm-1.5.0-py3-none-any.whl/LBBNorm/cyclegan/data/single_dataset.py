from .base_dataset import BaseDataset, get_transform
from .image_folder import make_dataset
from PIL import Image


class SingleDataset(BaseDataset):
    """This dataset class can load a set of images specified by the path --dataroot /path/to/data.

    It can be used for generating CycleGAN results only for one side with the model option '-model test'.
    """

    def __init__(self, opt, path_image):
        """Initialize this dataset class.

        Parameters:
            opt (Option class) -- stores all the experiment flags; needs to be a subclass of BaseOptions
        """
        BaseDataset.__init__(self, opt)
        # self.A_paths = sorted(make_dataset(opt.dataroot, opt.max_dataset_size))
        # self.A_paths = sorted(path_images)
        self.A_paths = path_image
        
        # print("I am here ", self.A_paths)
        input_nc = self.opt.output_nc if self.opt.direction == 'BtoA' else self.opt.input_nc
        self.transform = get_transform(opt, grayscale=(input_nc == 1))

    def __getitem__(self, index):
        """Return a data point and its metadata information.

        Parameters:
            index - - a random integer for data indexing

        Returns a dictionary that contains A and A_paths
            A(tensor) - - an image in one domain
            A_paths(str) - - the path of the image
        """
        # change A_paths to A_image 
        A_path = self.A_paths[index]
        # A_img = Image.open(A_path).convert('RGB')
        # A = self.transform(A_img)
        A_img = A_path.convert('RGB')
        A = self.transform(A_img)
        
        # return {'A': A, 'A_paths': A_path}
        
        return {'A': A, 'A_paths': ""}
    

    def __len__(self):
        """Return the total number of images in the dataset."""
        return len(self.A_paths)
