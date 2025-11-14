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
    parser = argparse.ArgumentParser(
        description='水果检测模型远程调用脚本',
        epilog='''
使用示例:
  本地调用: python test.py peach.jpg
  指定主机: python test.py peach.jpg --host 192.168.1.100
  指定端口: python test.py peach.jpg --host 192.168.1.100 --port 8080
  使用环境变量: export FRUIT_DETECTION_URL=http://192.168.1.100:8000/api/v1/fruit/detect
                python test.py peach.jpg
        '''
    )
    parser.add_argument('image_path', help='要检测的图片文件路径')
    
    # 支持环境变量设置默认URL，便于外部调用
    default_url = os.getenv('FRUIT_DETECTION_URL', 'http://localhost:8000/api/v1/fruit/detect')
    parser.add_argument('--url', default=default_url,
                       help=f'模型服务API地址 (默认: {default_url},可通过环境变量FRUIT_DETECTION_URL设置)')
    parser.add_argument('--timeout', type=int, default=30, help='请求超时时间(秒)')
    parser.add_argument('--host', help='服务主机地址 (例如: 192.168.1.100)')
    parser.add_argument('--port', type=int, default=8000, help='服务端口 (默认: 8000)')
    
    args = parser.parse_args()
    
    # 如果指定了host参数，则覆盖URL
    if args.host:
        args.url = f"http://{args.host}:{args.port}/api/v1/fruit/detect"
    
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
