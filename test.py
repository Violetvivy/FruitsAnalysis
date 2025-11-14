import requests
import os

url = "http://117.50.160.102:8000/api/v1/fruit/detect"

# 检查图片文件是否存在
image_path = "peach.png"
if not os.path.exists(image_path):
    print(f"错误: 图片文件 '{image_path}' 不存在")
    exit(1)

print(f"正在检测图片: {image_path}")

try:
    with open(image_path, "rb") as image_file:
        files = {"file": ("peach.png", image_file, "image/jpeg")}
        response = requests.post(url, files=files, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        print("检测成功!")
        print(f"检测到 {result['totalFruits']} 个水果:")
        
        for i, fruit in enumerate(result['fruits'], 1):
            print(f"  {i}. {fruit['fruitType']} - 置信度: {fruit['confidence']:.2f}")
            bbox = fruit['boundingBox']
            print(f"     位置: ({bbox['xmin']:.1f}, {bbox['ymin']:.1f}, {bbox['xmax']:.1f}, {bbox['ymax']:.1f})")
            
    else:
        print(f"请求失败: {response.status_code}")
        print(f"错误信息: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("连接失败: 无法连接到服务,请确保Docker容器正在运行")
except requests.exceptions.Timeout:
    print("请求超时: 服务响应时间过长")
except Exception as e:
    print(f"发生错误: {e}")
