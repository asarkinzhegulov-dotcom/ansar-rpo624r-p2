# Real-Time Object Detection — YOLOv8 Pipeline

**Автор:** Ansar Kinzhegulov
**Дисциплина:** Компьютерное зрение · Практическая работа 3

## Структура проекта

- detector.py — главный скрипт
- speed_test.py — бенчмарк PT vs ONNX
- config.py — настройки
- utils/ — вспомогательные модули
- train_notebook.ipynb — обучение в Colab
- requirements.txt — зависимости

## Установка

pip install -r requirements.txt

## Запуск

python detector.py --source webcam
python detector.py --source video.mp4
python detector.py --source image.jpg
python speed_test.py --model yolov8n.pt
