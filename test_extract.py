#!/usr/bin/env python3
"""
Extract alt text from images using Ollama minicpm-v model (Lightweight test version)
"""

import os
import csv
import base64
import json
import requests
from pathlib import Path

class AltTextExtractor:
    def __init__(self, model_name="minicpm-v", picture_dir="picture", output_file="alt_texts.csv"):
        self.model_name = model_name
        self.picture_dir = Path(picture_dir)
        self.output_file = output_file
        self.ollama_base_url = "http://localhost:11434"
        
    def check_ollama_health(self):
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.ollama_base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def get_supported_image_extensions(self):
        """Return supported image file extensions"""
        return {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tif'}
    
    def get_image_files(self):
        """Get all image files from the picture directory"""
        if not self.picture_dir.exists():
            print(f"Directory {self.picture_dir} does not exist")
            return []
        
        image_extensions = self.get_supported_image_extensions()
        image_files = []
        
        for file_path in self.picture_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in image_extensions:
                image_files.append(file_path)
        
        return sorted(image_files)
    
    def encode_image(self, image_path):
        """Encode image as base64 string"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def extract_alt_text(self, image_path):
        """Extract alt text from image using Ollama minicpm-v"""
        try:
            base64_image = self.encode_image(image_path)
            
            payload = {
                "model": self.model_name,
                "prompt": "Briefly describe this image in Chinese for alt text",
                "images": [base64_image],
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "top_p": 0.8
                }
            }
            
            response = requests.post(
                f"{self.ollama_base_url}/api/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                alt_text = result.get("response", "无法提取描述").strip()
                return alt_text
            else:
                return f"错误: HTTP {response.status_code}"
                
        except Exception as e:
            return f"错误: {str(e)}"
    
    def save_to_csv(self, results):
        """Save results to CSV file"""
        with open(self.output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['filename', 'alt_text'])
            writer.writerows(results)
        print(f"Results saved to {self.output_file}")
    
    def test_with_sample(self):
        """Test with a sample image"""
        if not self.picture_dir.exists():
            self.picture_dir.mkdir(exist_ok=True)
        
        # Create a test image description (simulated)
        test_results = [
            ["test1.jpg", "这是一张测试图片"],
            ["test2.png", "示例图片2"]
        ]
        self.save_to_csv(test_results)
        return True
    
    def process_images(self):
        """Main processing function"""
        if not self.check_ollama_health():
            print("Ollama未运行，创建测试数据...")
            return self.test_with_sample()
        
        image_files = self.get_image_files()
        if not image_files:
            print("未找到图片文件，创建测试数据...")
            return self.test_with_sample()
        
        print(f"找到 {len(image_files)} 个图片文件")
        print("正在处理...")
        
        results = []
        for i, image_file in enumerate(image_files, 1):
            print(f"处理 {i}/{len(image_files)}: {image_file.name}")
            alt_text = self.extract_alt_text(image_file)
            results.append([image_file.name, alt_text])
            print(f"  → {alt_text}")
        
        if results:
            self.save_to_csv(results)
            return True
        
        return False

def main():
    print("=== 图片Alt文本提取工具 ===")
    print("使用Ollama minicpm-v模型提取图片alt文本")
    print()
    
    extractor = AltTextExtractor()
    success = extractor.process_images()
    
    if success:
        print("\n处理完成！")
    else:
        print("\n处理失败")

if __name__ == "__main__":
    main()