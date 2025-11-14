import sys
import os

# 检查requests库是否已安装
try:
    import requests
except ImportError:
    print("错误: 需要安装requests库")
    print("请运行: pip install requests")
    sys.exit(1)

def main():
    # 图片路径
    image_path = "peach.jpg"
    url = "http://120.46.71.74:8000/api/v1/fruit/detect"
    timeout = 30
    
    # 检查图片文件是否存在
    if not os.path.exists(image_path):
        print(f"错误: 图片文件 '{image_path}' 不存在")
        sys.exit(1)
    
    # 验证文件是否为图片
    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
    file_ext = os.path.splitext(image_path)[1].lower()
    if file_ext not in valid_extensions:
        print(f"错误: 不支持的图片格式 '{file_ext}'，支持的格式: {', '.join(valid_extensions)}")
        sys.exit(1)
    
    print(f"正在检测图片: {image_path}")
    print(f"使用服务地址: {url}")
    
    try:
        with open(image_path, "rb") as image_file:
            files = {"file": (os.path.basename(image_path), image_file, "image/jpeg")}
            response = requests.post(url, files=files, timeout=timeout)
        
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
        print("连接失败: 无法连接到服务器")
    except requests.exceptions.Timeout:
        print(f"请求超时: 服务响应时间超过{timeout}秒")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()
