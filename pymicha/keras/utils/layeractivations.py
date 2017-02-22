import keras.backend as K


def get_layer_activations(model, X):
    """
    Evaluates the model on the given batch of data and returns output values
    for all layers in the model
    """
    get_activations = K.function([model.layers[0].input, K.learning_phase()],
                                 [layer.output for layer in model.layers])
    activations = get_activations([X, 0])
    return zip(model.layers, activations)
