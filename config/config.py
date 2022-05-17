
TRAINING = 0
PREDICTING = 1

class Config:

    def __init__(self, mode):
        assert mode in {TRAINING, PREDICTING}, "Unknown mode: %i"%mode
        self.mode = mode
        if self.mode == TRAINING:

            ######################activitym######################
            self.lstm_train_dir = '/home/obayashi/Projects/obayashi_practice/4.AR_train/sample.csv'
            self.n_classes = 7
            self.data_dir = '/home/obayashi/Projects/obayashi_practice/dataset/'
            self.res_path = '/home/obayashi/Projects/obayashi_practice/4.AR_train/AR_train_result'
            self.nb_epochs_per_saving = 1
            self.pin_mem = True
            self.num_cpu_workers = 8
            self.nb_epochs = 100
            self.cuda = True
            # Optimizer
            self.lr = 1e-4
            self.weight_decay = 5e-5
            # Hyperparameters for our y-Aware InfoNCE Loss
            self.sigma = 5 # depends on the meta-data at hand
            self.temperature = 0.1
            self.tf = "all_tf"
            self.model = "UNet"
            self.num_classes = 2

            # Paths to the data
            #self.data_train_path = 

            self.input_size = (1, 121, 145, 121)
            self.label_name = "PTAGE"

            self.lstm_checkpoint_dir = ""
            ######################activitym######################

        elif self.mode == PREDICTING:
            ######################activitym######################
            ## We assume a classification task here
            self.batch_size = 8
            self.nb_epochs_per_saving = 10
            self.pin_mem = True
            self.num_cpu_workers = 1
            self.nb_epochs = 100
            self.cuda = True
            # Optimizer
            self.lr = 1e-4
            self.weight_decay = 5e-5

            self.pretrained_path = "/.h5"
            self.num_classes = 2
            self.model = "DenseNet"
            self.lstm_checkpoint_dir = ""
            ######################activitym######################

