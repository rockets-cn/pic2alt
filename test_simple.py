#!/usr/bin/env python3
"""
Test version - create CSV with sample data for testing
"""

import csv
import os
from pathlib import Path

def create_test_csv():
    """Create test CSV with sample alt text data"""
    
    # Sample alt text data for existing images
    test_data = [
        ["filename", "alt_text"],
        ["pose.jpg", "人物姿势演示图片"],
        ["显微镜.jpg", "实验室显微镜设备"],
        ["sen0486.jpg", "电子模块组件"],
        ["行空板扩展板.jpg", "行空板扩展板电路板"],
        ["IMG_8718.jpeg", "产品实物照片"],
        ["unihiker.jpg", "Unihiker开发板"]
    ]
    
    # Write to CSV
    with open('alt_texts.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(test_data)
    
    print("=== 测试完成 ===")
    print("已创建 alt_texts.csv 文件")
    print("包含以下数据:")
    for row in test_data[1:]:  # Skip header
        print(f"  {row[0]}: {row[1]}")

if __name__ == "__main__":
    create_test_csv()