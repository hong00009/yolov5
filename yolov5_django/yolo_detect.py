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
    model = torch.hub.load('ultralytics/yolov5', 'custom', 'yolov5_model/yolov5L_best.pt')
    results = model(img_path, size=1028)

    detections = results.xyxy[0] 
    # detections[:,5] => tensor([ 1.,  50., 127.])
    detected_list = detections[:, 5].int().tolist() # [1, 50, 127]

    if not detected_list: # 검출객체없음
        return None # None 반환
    
    detected_list.sort()
    detect_result = ','.join(map(str, detected_list)) # 1,50,127
    print('검출번호:', detect_result)

    return detect_result # 숫자1개 또는 숫자,숫자인 문자열반환 