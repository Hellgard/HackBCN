  ###################################### SimplifAI ##########################################
##                                File for HackBCN EVENT                                   ##
##                                     Author: Erwan                                       ##
##                                   Date: 2024-06-29                                      ##
##                                     Version: 1.0                                        ##
##                                Python Version: 3.10.11                                  ##
  ###################################### SimplifAI ##########################################

import cv2
import numpy as np
import torch
import torch.nn as nn
from torchvision.transforms import ToTensor
from torchvision.models import resnet18
import torch.nn.functional as F

class CustomCNN2(nn.Module):
    def __init__(self, num_classes=7):
        super(CustomCNN2, self).__init__()

        self.conv_block1 = nn.Sequential(
            nn.Conv2d(1, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Dropout(0.25)
        )

        self.conv_block2 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=5, padding=2),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Dropout(0.25)
        )

        self.conv_block3 = nn.Sequential(
            nn.Conv2d(128, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Dropout(0.25)
        )

        self.conv_block4 = nn.Sequential(
            nn.Conv2d(512, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Dropout(0.25)
        )

        self.flatten = nn.Flatten()

        self.fc1 = nn.Sequential(
            nn.Linear(512 * 3 * 3, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(0.25)
        )

        self.fc2 = nn.Sequential(
            nn.Linear(512, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(0.25)
        )

        self.fc3 = nn.Linear(512, num_classes)
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, x):
        x = self.conv_block1(x)
        x = self.conv_block2(x)
        x = self.conv_block3(x)
        x = self.conv_block4(x)
        x = self.flatten(x)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        x = F.relu(x)
        x = self.fc3(x)
        x = self.softmax(x)
        return x

def facial_algo():
    # Charger le modèle PyTorch pré-entraîné
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = CustomCNN2(num_classes=7)
    model.load_state_dict(torch.load("models/model2.pth", map_location=device))
    model.to(device)
    model.eval()

    emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

    face_classifier = cv2.CascadeClassifier(r'./haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    while True:
        _, img = cap.read()
        if not cap.isOpened():
            print("Erreur: Impossible d'ouvrir la webcam.")
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray)

        # Supprimer les visages détectés qui ne sont pas au premier plan
        if len(faces) > 1:
            # Tri des visages détectés par ordre de taille (w * h)
            faces = sorted(faces, key=lambda x: x[2] * x[3], reverse=True)
            # Garder uniquement le visage le plus grand (celui le plus proche de la caméra)
            faces = [faces[0]]

        labels = []
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 255), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

            if np.sum([roi_gray]) != 0:
                roi = roi_gray.astype('float32') / 255.0
                roi = ToTensor()(roi).unsqueeze(0).to(device)
                prediction = model(roi)
                _, predicted_label = torch.max(prediction.data, 1)
                label = emotion_labels[predicted_label.item()]
                label_position = (x, y)
                labels.append(emotion_labels[predicted_label.item()])
                cv2.putText(img, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(img, 'Pas de visages', (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Détection des émotions faciales', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Ajouter des étiquettes à une chaîne avec un séparateur "," et des crochets "[ ]"
        labels = str(labels).strip('[]')
        labels = "émotions faciales : [" + labels + "]"

        # Écrire les étiquettes dans un fichier
        with open('Preds/preds.txt', 'w') as f:
            f.seek(0)
            f.truncate()
            f.write("%s\n" % labels)
    cap.release()
    cv2.destroyAllWindows()
    