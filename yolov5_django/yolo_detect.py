# 기학습된 yolo 모델 설정 후 진행
# detect 하기 위해 yolov5 파일 필요
# pytorch는 yolov5 패키지를 pip로 제공

import yolov5
from django.shortcuts import render
import torch
import os
import io
from PIL import Image as I
from django.conf import settings 
from django.core.files.storage import FileSystemStorage
from uuid import uuid4 # 고유번호 생성
from .models import UploadedImage, FoodNutrition

def y_detect(img_path):
    model = torch.hub.load('ultralytics/yolov5', 'custom', 'yolov5_model/yolov5l_best.pt')
    results = model(img_path, size=640)

    detections = results.xyxy[0]
    detected_classes = detections[:, 5].int().tolist()
    detected_classes.sort()
    detection_result = ','.join(map(str, detected_classes))
    print('detected_classes:', detected_classes)
    print('detection_result:', detection_result)

    return detection_result