import os
from PIL import Image
import matplotlib.pyplot as plt
from ultralytics import YOLO

WORK_DIR = "/kaggle/working/"
TEST_FOLDER = os.path.join(WORK_DIR, "testdata")
MODEL_PATH = os.path.join(WORK_DIR, "runs/detect/train_v1/weights/best.pt")
OUTPUT_DIR = os.path.join(WORK_DIR, "predictions")


def load_model():
    model = YOLO(MODEL_PATH)
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def perform_predictions(trained_model, test_folder, output_dir):
    results = trained_model.predict(
        source=os.path.join(test_folder, "images"),
        save=True,
        save_dir=output_dir,
        stream=True,
    )
    return results


def display_predictions(predictions, n):
    for i, result in enumerate(predictions):
        if i >= n:
            break

        prediction_image_path = result["prediction_path"]
        prediction_image = Image.open(prediction_image_path)
        plt.imshow(prediction_image)
        plt.grid(False)
        plt.show()


if __name__ == "__main__":
    trained_model = load_model()
    predictions = perform_predictions(trained_model, TEST_FOLDER, OUTPUT_DIR)
    display_predictions(predictions, 5)