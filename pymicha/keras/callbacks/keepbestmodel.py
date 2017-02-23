from keras.callbacks import Callback


class KeepBestModel(Callback):
    """
    Keras callback to be used with EarlyStopping. When setting a high patience
    value for EarlyStopping, the resulting model object won't necissarily be
    the best one. This will save the weight values for the best intermidate
    models and reset the model back to the best state at the end of training
    """
    def __init__(self, monitor, how):
        self.monitor = monitor
        self.how = how

    def on_train_begin(self, logs=None):
        self.best_weights = None
        self.best_model = self.model.to_json()
        self.best_value = None
        self.best_epoch = None

    def on_epoch_end(self, epoch, logs=None):
        current = logs.get(self.monitor)
        if self.best_value is None or self.how(current, self.best_value):
            print("Copying model")
            self.best_weights = self.model.get_weights()
            self.best_value = current
            self.best_epoch = epoch + 1

    def on_train_end(self, logs=None):
        print(("Resetting model to epoch {} when {} read a"
               "value of {}").format(self.best_epoch, self.monitor,
                                     self.best_value))
        self.model.set_weights(self.best_weights)
