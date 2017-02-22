import keras.backend as K


def get_layer_activations(model, X_batch):
    get_activations = K.function([model.layers[0].input, K.learning_phase()],
                                 [layer.output for layer in model.layers])
    activations = get_activations([X_batch, 0])
    return zip(model.layers, activations)
