import torch
from PIL import Image

def y_detect(img_path):
    # 저장된 이미지 사이즈 확인
    with Image.open(img_path) as img:
        width, height = img.size
    size = max(width, height)

    # 32의 배수에 맞추기
    if size % 32 != 0:
        size = ((size // 32) + 1) * 32 

    # 최대 1600까지만 (이 이상은 너무 오래걸림)
    size = min(size, 1600)
    print('**객체검출 size:',size)

    model = torch.hub.load('ultralytics/yolov5', 'custom', 'yolov5_model/yolov5L_best.pt')
    results = model(img_path, size=size)

    detections = results.xyxy[0] 
    # detections[:,5] => tensor([ 1.,  50., 127.])
    detected_list = detections[:, 5].int().tolist() # [1, 50, 127]

    if not detected_list: # 검출객체없음
        return None # None 반환
    
    detected_list.sort()
    detect_result = ','.join(map(str, detected_list)) # 1,50,127
    print('검출번호:', detect_result)

    return detect_result # 숫자1개 또는 숫자,숫자인 문자열반환 