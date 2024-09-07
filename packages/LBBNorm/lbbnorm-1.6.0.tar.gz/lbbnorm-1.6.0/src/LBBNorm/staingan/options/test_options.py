from .base_options import BaseOptions


class TestOptions(BaseOptions):
    def initialize(self, path_size,results_dir):
        BaseOptions.initialize(self, path_size=path_size)
        self.parser.add_argument('--ntest', type=int, default=float("inf"), help='# of test examples.')
        self.parser.add_argument('--results_dir', type=str, default=results_dir, help='saves results here.')
        self.parser.add_argument('--aspect_ratio', type=float, default=1.0, help='aspect ratio of result images')
        self.parser.add_argument('--phase', type=str, default='test', help='train, val, test, etc')
        # self.parser.add_argument('--which_epoch', type=str, default='latest', help='which epoch to load? set to latest to use latest cached model')
        # self.parser.add_argument('--how_many', type=int, default=1, help='how many test images to run')
        self.parser.set_defaults(model='test')
        self.parser.set_defaults(how_many=1)
        self.parser.set_defaults(which_epoch='latest')
        self.isTrain = False
