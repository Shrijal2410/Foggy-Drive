import os
from PIL import Image
import matplotlib.pyplot as plt
from ultralytics import YOLO

WORK_DIR = "/kaggle/working/"
TEST_FOLDER = os.path.join(WORK_DIR, "testdata")
MODEL_PATH = os.path.join(WORK_DIR, "runs/detect/train_v1/weights/best.pt")


def load_model():
    model = YOLO(MODEL_PATH)
    return model


def perform_predictions(trained_model, test_folder):
    results = trained_model.predict(
        source=os.path.join(test_folder, "images"),
        save=True,
    )
    return list(results)


if __name__ == "__main__":
    trained_model = load_model()
    predictions = perform_predictions(trained_model, TEST_FOLDER)
