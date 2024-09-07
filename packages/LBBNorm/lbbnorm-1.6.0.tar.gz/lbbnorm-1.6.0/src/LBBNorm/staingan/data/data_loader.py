
def CreateDataLoader(opt , path_image):
    from ..data.custom_dataset_data_loader import CustomDatasetDataLoader
    data_loader = CustomDatasetDataLoader()
    #print(data_loader.name())
    data_loader.initialize(opt, path_image)
    return data_loader
