import sys
import os
import argparse

# 检查requests库是否已安装
try:
    import requests
except ImportError:
    print("错误: 需要安装requests库")
    print("请运行: pip install requests")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='水果检测模型远程调用脚本')
    parser.add_argument('image_path', help='要检测的图片文件路径')
    parser.add_argument('--url', default='http://120.46.71.74:8000/api/v1/fruit/detect',
                       help='模型服务API地址 (默认: http://120.46.71.74:8000/api/v1/fruit/detect)')
    parser.add_argument('--timeout', type=int, default=30, help='请求超时时间(秒)')
    
    args = parser.parse_args()
    
    # 检查图片文件是否存在
    if not os.path.exists(args.image_path):
        print(f"错误: 图片文件 '{args.image_path}' 不存在")
        sys.exit(1)
    
    # 验证文件是否为图片
    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
    file_ext = os.path.splitext(args.image_path)[1].lower()
    if file_ext not in valid_extensions:
        print(f"错误: 不支持的图片格式 '{file_ext}'，支持的格式: {', '.join(valid_extensions)}")
        sys.exit(1)
    
    print(f"正在检测图片: {args.image_path}")
    print(f"使用服务地址: {args.url}")
    
    try:
        with open(args.image_path, "rb") as image_file:
            files = {"file": (os.path.basename(args.image_path), image_file, "image/jpeg")}
            response = requests.post(args.url, files=files, timeout=args.timeout)
        
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
        print("连接失败: 无法连接到服务，请检查:")
        print("  1. 服务地址是否正确")
        print("  2. 网络连接是否正常")
        print("  3. 服务是否正在运行")
    except requests.exceptions.Timeout:
        print(f"请求超时: 服务响应时间超过{args.timeout}秒")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()
