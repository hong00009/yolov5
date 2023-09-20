# 기학습된 yolo 모델 설정 후 진행
# detect 하기 위해 yolov5 파일 필요
# pytorch는 yolov5 패키지를 pip로 제공

import yolov5
from django.shortcuts import render
import torch
import os
from PIL import Image as I
from django.conf import settings 
from django.core.files.storage import FileSystemStorage
from uuid import uuid4 # 고유번호 생성

def y_detect(img, img_name):
    # model = yolov5.load('y5_model/best.pt')
    # model.conf = 0.5
    # model.iou = 0.45  # iou threshold
    # model.multi_label = False
    # model.max_det = 1000

    # torch를 이용하는 방법
    
    # 사용자 정의 모델 사용
    model = torch.hub.load('ultralytics/yolov5', 'custom', 'y5_model/yolov5s_best.pt' )

    # yolov5s 모델 사용
    # model = torch.hub.load('ultralytics/yolov5', 'yolov5s' )
    img = img
    results = model(img, size=416) # 객체 detect
    print(results.pandas().xyxy[0].value_counts('name')) # 검출된 객체의 이름을 시리즈로 반환

    results.render() # 출력된 결과의 이미지 사용할 수 있게 np.array 형식으로 렌더링(변환)

    # detect image 저장 경로
    static_folder = 'media/'
    inferenced_img_dir = os.path.join(static_folder, "inferenced_image")
    
    if not os.path.exists(inferenced_img_dir):
        os.makedirs(inferenced_img_dir)

    # 검출된 객체 숫자만큼 저장    
    for img in results.ims: # np.array 형식
            img_base64 = I.fromarray(img) # 이미지 형식으로 변환
            img_base64.save(f"{inferenced_img_dir}/{img_name}")
    # 객체 검출 결과 이미지 저장 경로
    res_url = "inferenced_image"+"/" + img_name
    return res_url




def rename_imagefile_to_uuid(filename): # 고유번호로 이미지파일명 변경
    ext = filename.split('.')[-1] # 파일 이름에서 확장자만 분리
    uuid = uuid4().hex
    filename = '{}.{}'.format(uuid,ext)

    return filename


# 전달된 이미지를 받아서 yolo 모델에 주입 후 검출된 결과 이미지를 클라이언트에게 전송
def detect(request):
    img = request.FILES.get('images') # 사용자가 전송한 이미지 파일 가져오기
    fs = FileSystemStorage() # 파일 저장소 접근 객체 생성

    # 전송된 파일명 변경해서 저장
    # 서버에서 사용할 유일한 파일면 생성
    file_name = rename_imagefile_to_uuid(img.name)
    img_up_url = fs.save(file_name, img) # media 디렉터리에 저장
    print(img_up_url)

    img = 'media/' + img_up_url

    # 이미지 객체 검출 함수 호출 yolov5_detect.py
    res_url = y_detect(img, img_up_url)

    context = {
         'image':res_url
    }
    return render(request, 'detect/result.html', context) 
