#!/usr/bin/env python3
"""
Extract alt text from images using Ollama minicpm-v model
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
            # Encode image to base64
            base64_image = self.encode_image(image_path)
            
            # Prepare request payload
            payload = {
                "model": self.model_name,
                "prompt": "请描述这张图片的内容，用简洁的中文描述，适合作为alt属性文本。",
                "images": [base64_image],
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "top_p": 0.8
                }
            }
            
            # Send request to Ollama
            response = requests.post(
                f"{self.ollama_base_url}/api/generate",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                alt_text = result.get("response", "").strip()
                return alt_text
            else:
                print(f"Error: Ollama returned status code {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error processing {image_path.name}: {str(e)}")
            return None
    
    def save_to_csv(self, results):
        """Save results to CSV file"""
        with open(self.output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['filename', 'alt_text'])
            writer.writerows(results)
        print(f"Results saved to {self.output_file}")
    
    def process_images(self):
        """Main processing function"""
        # Check if Ollama is available
        if not self.check_ollama_health():
            print("Error: Ollama is not running or not accessible")
            print("Please start Ollama with: ollama serve")
            return False
        
        # Get image files
        image_files = self.get_image_files()
        if not image_files:
            print("No image files found in the picture directory")
            return False
        
        print(f"Found {len(image_files)} image files")
        
        # Process each image
        results = []
        for i, image_file in enumerate(image_files, 1):
            print(f"Processing {i}/{len(image_files)}: {image_file.name}")
            
            alt_text = self.extract_alt_text(image_file)
            if alt_text:
                results.append([image_file.name, alt_text])
                print(f"  → {alt_text}")
            else:
                results.append([image_file.name, "无法提取描述"])
                print("  → 无法提取描述")
        
        # Save results to CSV
        if results:
            self.save_to_csv(results)
            return True
        
        return False

def main():
    """Main function"""
    print("=== 图片Alt文本提取工具 ===")
    print("使用Ollama minicpm-v模型提取图片alt文本")
    print()
    
    extractor = AltTextExtractor()
    success = extractor.process_images()
    
    if success:
        print("\n处理完成！")
    else:
        print("\n处理失败，请检查错误信息")

if __name__ == "__main__":
    main()