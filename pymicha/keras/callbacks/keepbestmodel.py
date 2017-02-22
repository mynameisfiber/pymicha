from keras.callbacks import Callback


class KeepBestModel(Callback):
    def __init__(self, monitor):
        self.monitor = monitor

    def on_train_begin(self, logs=None):
        self.best_weights = None
        self.best_model = self.model.to_json()
        self.best_value = None
        self.best_epoch = None

    def on_epoch_end(self, epoch, logs=None):
        current = logs.get(self.monitor)
        if self.best_value is None or current > self.best_value:
            print("Copying model")
            self.best_weights = self.model.get_weights()
            self.best_value = current
            self.best_epoch = epoch + 1

    def on_train_end(self, logs=None):
        print(("Resetting model to epoch {} when monitored "
               "value was {}").format(self.best_epoch, self.best_value))
        self.model.set_weights(self.best_weights)
