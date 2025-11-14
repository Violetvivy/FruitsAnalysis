from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from app.models import FruitRecognitionModel
from app.schemas import FruitRecognitionDTO
import uvicorn

app = FastAPI(
    title="水果识别服务",
    description="基于YOLO模型的水果类型识别和目标检测服务",
    version="1.0.0"
)

# 全局模型实例
model = None

@app.on_event("startup")
async def startup_event():
    """服务启动时加载模型"""
    global model
    try:
        model = FruitRecognitionModel()
        print("YOLO模型加载成功!")
    except Exception as e:
        print(f"模型加载失败: {e}")
        raise e

@app.get("/")
async def root():
    return {"message": "水果识别服务 API"}

@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }

@app.post("/api/v1/fruit/detect", response_model=FruitRecognitionDTO)
async def detect_fruits(file: UploadFile = File(...)):
    """
    检测水果图片，返回水果类型识别和目标检测结果
    """
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="请上传图片文件")
    
    try:
        # 读取上传的图片
        image_bytes = await file.read()
        
        # 使用模型处理图片
        result = model.process_image(image_bytes)
        
        return JSONResponse(content=result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
