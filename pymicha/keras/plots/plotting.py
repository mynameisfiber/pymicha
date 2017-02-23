import matplotlib.pyplot as plt
import seaborn as sns  # NOQA
import numpy as np

import itertools
from functools import reduce

from ..utils import get_layer_activations


def plot_train_history(histories):
    """
    Plot a dictionary of keras history objects. The keys of the dictionaries
    acts as a way of naming and comparing the training performance of different
    models.

    >>> plot_train_history({
        "small_model": history_small_model,
        "large_model": history_large_model,
    })
    """
    fields = reduce(set.union, (set(h.history.keys())
                                for h in histories.values()))
    fields = sorted(list(fields))
    subplots = plt.subplots(len(fields))
    max_epoch = max(max(h.epoch) for h in histories.values())
    for key, ax in zip(fields, subplots[1]):
        ax.set_ylabel(key)
        ax.set_xlabel("Epoch")
        for name, history in histories.items():
            if key in history.history:
                ax.plot(history.epoch, history.history[key], label=name)
        ax.set_xlim(xmin=0, xmax=max_epoch)
    if len(histories) > 1:
        plt.legend()
    plt.show()


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.

    confusion matrix plotting routine from:
    http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()


def plot_activations(model, X):
    """
    Djanky function to plot output values of intermediate layers in the model
    """
    activations = list(get_layer_activations(model, [X]))
    print([a[1].shape for a in activations])
    for layer, activation in activations[1:]:
        if len(activation.shape) == 4:
            N = activation.shape[1]
            if N == 1:
                plt.imshow(activation[0, 0, :, :])
                plt.axis('off')
            else:
                fig, axes = plt.subplots(ncols=N)
                for i, ax in enumerate(axes):
                    ax.imshow(activation[0, i, :, :])
                    ax.axis('off')
        else:
            N = activation.shape[-1]
            y = 4
            x = int(N / y)
            while x*y != N and y < N:
                y += 1
                x = int(N/16)
            if x*y == activation.shape[-1]:
                act = activation[0, :].reshape((y, x))
                if layer.name != 'output':
                    plt.axis('off')
            else:
                act = activation
            plt.imshow(act)
        plt.title(layer.name)
        plt.show()
