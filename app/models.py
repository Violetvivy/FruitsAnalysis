import torch
import cv2
import numpy as np
from ultralytics import YOLO
import time
import requests
from io import BytesIO

class FruitRecognitionModel:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"使用设备: {self.device}")
        
        # 加载 YOLO 模型 
        self.detector = YOLO('models/yolo.pt')
        print("YOLO模型加载成功!")
    
    def process_image(self, image_bytes: bytes):
        """处理上传的图片 - 仅使用YOLO进行水果检测和分类"""
        # 将字节转换为OpenCV格式
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("无法解码图片")
        
        # YOLO模型检测 - 降低置信度阈值并添加调试信息
        print(f"图片尺寸: {image.shape}")
        results = self.detector.predict(
            source=image,
            imgsz=640,      # 输入图像尺寸
            conf=0.1,       # 降低置信度阈值
            iou=0.3,        # 降低IoU阈值
            device=self.device,
            verbose=True    # 输出详细信息
        )
        
        fruits = []
        
        for result in results:
            for box in result.boxes:
                # 获取检测信息
                confidence = box.conf.item()
                class_id = int(box.cls.item())
                class_name = self.detector.names[class_id]
                
                # 获取边界框坐标
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                
                # 构建水果信息（仅包含检测信息，不包含质量分析）
                fruit_info = {
                    'fruitType': class_name,
                    'boundingBox': {
                        'xmin': x1,
                        'ymin': y1,
                        'xmax': x2,
                        'ymax': y2
                    },
                    'confidence': round(confidence, 4)
                }
                fruits.append(fruit_info)
        
        return {
            'fruits': fruits,
            'totalFruits': len(fruits),
            'timestamp': time.time()
        }
    
    def process_image_from_url(self, image_url: str):
        """从URL处理图片 - 仅使用YOLO进行水果检测和分类"""
        try:
            # 从URL下载图片
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            # 将响应内容转换为OpenCV格式
            image_bytes = np.frombuffer(response.content, np.uint8)
            image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
            if image is None:
                raise ValueError("无法从URL解码图片")
        
        # YOLO模型检测 - 降低置信度阈值并添加调试信息
        print(f"图片尺寸: {image.shape}")
        results = self.detector.predict(
            source=image,
            imgsz=640,      # 输入图像尺寸
            conf=0.1,       # 降低置信度阈值
            iou=0.3,        # 降低IoU阈值
            device=self.device,
            verbose=True    # 输出详细信息
        )
        
        fruits = []
        
        for result in results:
            for box in result.boxes:
                # 获取检测信息
                confidence = box.conf.item()
                class_id = int(box.cls.item())
                class_name = self.detector.names[class_id]
                
                # 获取边界框坐标
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                
                # 构建水果信息（仅包含检测信息，不包含质量分析）
                fruit_info = {
                    'fruitType': class_name,
                    'boundingBox': {
                        'xmin': x1,
                        'ymin': y1,
                        'xmax': x2,
                        'ymax': y2
                    },
                    'confidence': round(confidence, 4)
                }
                fruits.append(fruit_info)
        
        return {
            'fruits': fruits,
            'totalFruits': len(fruits),
            'timestamp': time.time()
        }
