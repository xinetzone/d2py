from tensorflow.keras import layers, models, activations

def conv_layer(x, filters, kernel_size, strides, batchnorm, training, name,
               reuse, activation='relu'):
    x = layers.Conv2D(
        filters,
        kernel_size,
        strides=strides,
        padding='same',
        activation=None,
        name=name,
        trainable=not reuse)(x)

    if batchnorm:
        batchnorm_name = name + "_batchnorm"
        x = layers.BatchNormalization(
            name=batchnorm_name,
            trainable=not reuse)(x, training=training)

    if activation == 'relu':
        x = layers.LeakyReLU(alpha=0.01)(x)
    else:
        raise Exception("Unknown activation for conv_layer", activation)

    return x

def dense_layer(x, units, name, reuse, activation=None):
    x = layers.Dense(units, activation=None, name=name, trainable=not reuse)(x)

    if activation is None:
        pass
    elif activation == 'relu':
        x = layers.LeakyReLU(alpha=0.01)(x)
    else:
        raise Exception("Unknown activation for dense_layer", activation)

    return x
