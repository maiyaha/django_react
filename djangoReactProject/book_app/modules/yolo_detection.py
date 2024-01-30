import yolov5
import torch
from PIL import Image 
import pathlib
from django.conf import settings

def detect(img, img_name):
    # 윈도우 경로 오류 문제 해결 : cannot instantiate 'PoxiPath
    pathlib.PosixPath = pathlib.WindowsPath

    # (1) best.pt 사용하는 경우
    model = yolov5.load('yolo_model/best.pt')
    model.conf = 0.5  # NMS confidence threshold
    model.iou = 0.45  # NMS IoU threshold
    model.agnostic = False
    model.multi_label = False
    model.max_det = 1000    
    model = torch.hub.load('ultralytics/yolov5', 'custom', 'yolo_model/best.pt')   

    # (2) yolov5s 사용하는 경우
    # model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

    # 파일 경로 및 파일명 : upload 폴더
    file_path = settings.MEDIA_ROOT
    img_file = file_path + '/' + img_name
    results = model(img_file, size=416)
    
    # print('results : ', results)
    # print('name : ', results.pandas().xyxy[0]['name'])
    print('objects : ', [name for name in results.pandas().xyxy[0]['name']])
    
    results.render()    
    
    # 바운딩 박스 그려진 결과 이미지 저장  
    # /upload/result_img 폴더에 저장
    for img in results.ims:
            img_base64 = Image.fromarray(img)
            img_base64.save(
                f"{file_path}/result_img/{img_name}")
    
 