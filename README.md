# Yolov5-HandSign-Detection
A lightweight implementation of YOLOv5 trained on a custom dataset with six emergency assistance classes (NeedHelp, NeedMedicine, NeedWater, ComeHere, Washroom, and one additional). Includes training scripts, dataset configuration, and real‑time webcam tracking for rapid detection and response.

YOLOv5 Custom Object Detection – Emergency Assistance Classes
This repository contains a custom YOLOv5 implementation trained on a 6‑class dataset for real‑time object detection and tracking. The project was developed to recognize specific emergency assistance gestures and scenarios.

🔍 Dataset
Total images: 180+ labeled samples

Resolution: 640×480

Classes:

NeedHelp

NeedMedicine

NeedWater

ComeHere

Washroom

[Your 6th class name]

Images and labels are organized in YOLO format under:

Code
dataset/images/train
dataset/labels/train
⚙️ Training Setup
Framework: YOLOv5 (Ultralytics)

Pretrained weights: yolov5s.pt (transfer learning)

Training command:

bash
python train.py --img 640 --batch 16 --epochs 300 --data data.yaml --weights yolov5s.pt --device 0 --cos-lr --augment
Output:

Trained weights → runs/train/exp6/weights/best.pt

Training logs & metrics → runs/train/exp6/results.png

🚀 Inference & Real‑Time Tracking
Run detection on webcam:

bash
python detect.py --weights runs/train/exp6/weights/best.pt --img 640 --source 0 --device 0
Run detection on dataset images:

bash
python detect.py --weights runs/train/exp6/weights/best.pt --img 640 --source dataset/images/train --device 0
🎯 Goals
Achieve high accuracy with limited dataset size using augmentation and transfer learning.

Enable real‑time emergency assistance detection via webcam tracking.

Provide a reproducible workflow for small custom datasets.

📈 Future Work
Expand dataset with more diverse samples.

Experiment with larger YOLOv5 models (yolov5m, yolov5l) for improved accuracy.

Deploy trained model in edge devices for real‑time assistance systems.
