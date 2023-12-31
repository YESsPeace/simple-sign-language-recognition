import pickle

import cv2
import mediapipe as mp

import numpy as np

horizontally_imgs_model = pickle.load(open('model/model.pickle', 'rb'))
vertically_imgs_model = pickle.load(open('model/model_vertically_imgs.pickle', 'rb'))

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

signs_dict = {
    '0': 'Like',
    '1': 'Like front',
    '2': 'Dislike',
    '3': 'Dislike front',
    '4': 'Ok',
    '5': 'Peace',
    '6': 'Rock',
    '7': 'YessPeace sign',
    '8': 'Shaka',
    '9': 'Fuck you',
    '10': 'Spock',
    '11': 'West Coast',
    '12': 'East Coast',
    '13': 'Crips',
}


def get_data_from_hand_landmarks(frame, hand_landmarks):
    data_aux = []  # data which model will predict
    x_ = []
    y_ = []

    # getting all coordinates of hands landmarks
    for i in range(len(hand_landmarks.landmark)):
        x = hand_landmarks.landmark[i].x
        y = hand_landmarks.landmark[i].y

        x_.append(x)
        y_.append(y)

    # getting relative coordinates of hands landmarks
    for i in range(len(hand_landmarks.landmark)):
        x = hand_landmarks.landmark[i].x
        y = hand_landmarks.landmark[i].y
        data_aux.append(x - min(x_))
        data_aux.append(y - min(y_))

    return frame, data_aux, x_, y_


def recognize_hand_sign(img, hand_landmarks):
    H, W, _ = img.shape

    if H > W:
        model = vertically_imgs_model

    else:
        model = horizontally_imgs_model

    img, inputs, x_, y_ = get_data_from_hand_landmarks(img, hand_landmarks)

    # preparing data for the model
    inputs = np.array(inputs).reshape(1, -1)

    inputs = [inputs[0][:model.n_features_in_]]

    # getting model prediction
    prediction = model.predict(inputs)[0]
    sign_name = signs_dict[prediction.split('_')[0]]

    similarity = model.predict_proba(inputs).max()
    similarity = np.round(similarity, 2)

    return prediction, sign_name, similarity, x_, y_
