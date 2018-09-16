from schafkopf.players.data.load_data import load_data_bidding
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint, TerminateOnNaN, TensorBoard, EarlyStopping
from keras.utils import np_utils


x_train, y_train = load_data_bidding('../data/train_data.p')
x_test, y_test = load_data_bidding('../data/test_data.p')
x_valid, y_valid = load_data_bidding('../data/valid_data.p')


def baseline_model():
    model = Sequential()
    model.add(Dense(units=200,
                    input_shape=(8, 32),
                    activation='elu',
                    kernel_initializer='he_uniform'))
    model.add(Flatten())
    model.add(Dense(units=200,
                    activation='elu',
                    kernel_initializer='he_uniform'))
    model.add(Dense(units=9,
                    activation='softmax',
                    kernel_initializer='he_uniform'))
    adam = Adam(lr=0.02, decay=0.01)
    model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])
    return model


filepath="bigger_classifier_sortedhands_lr0.02.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
early_stopping = EarlyStopping(patience=3)
tensorboard = TensorBoard(log_dir='./logs')
callback_list = [checkpoint, TerminateOnNaN(), early_stopping, tensorboard]

model = baseline_model()


model.fit(x_train, y_train,
          validation_data=(x_valid, y_valid),
          epochs=30,
          batch_size=100,
          verbose=1,
          callbacks=callback_list)
