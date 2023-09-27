import torch

def y_detect(img_path):
    model = torch.hub.load('ultralytics/yolov5', 'custom', 'yolov5_model/yolov5L_best.pt')
    results = model(img_path, size=1056)

    detections = results.xyxy[0] 
    # detections[:,5] => tensor([ 1.,  50., 127.])
    detected_list = detections[:, 5].int().tolist() # [1, 50, 127]

    if not detected_list: # 검출객체없음
        return None # None 반환
    
    detected_list.sort()
    detect_result = ','.join(map(str, detected_list)) # 1,50,127
    print('검출번호:', detect_result)

    return detect_result # 숫자1개 또는 숫자,숫자인 문자열반환 