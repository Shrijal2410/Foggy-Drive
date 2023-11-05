import os
import random
import shutil
import yaml
import glob
import numpy as np
import pandas as pd
from PIL import Image
import seaborn as sns
import matplotlib.pyplot as plt
from ultralytics import YOLO

# Constants
IMG_SIZE = (224, 224)

# Folders
OUTPUT_DIR = "/kaggle/working/"
DATASET_FOLDER = "/kaggle/input/vehicle-detection-8-classes-object-detection/train"
TRAIN_FOLDER = os.path.join(OUTPUT_DIR, "traindata")
TEST_FOLDER = os.path.join(OUTPUT_DIR, "testdata")
VALID_FOLDER = os.path.join(OUTPUT_DIR, "validdata")
VEHICLE_CLASS = 8
VEHICLE = [
    "Motorcycle",
    "Auto",
    "Car",
    "Bus",
    "Small Car",
    "Truck",
    "Tractor",
    "Multi-Axle",
]


def create_folders(folders):
    for folder in folders:
        os.makedirs(os.path.join(folder, "images"), exist_ok=True)
        os.makedirs(os.path.join(folder, "labels"), exist_ok=True)


def copy_images_with_label(
    src_folder, dest_train_folder, dest_test_folder, dest_valid_folder
):
    image_files = [
        filename
        for filename in os.listdir(os.path.join(src_folder, "images"))
        if filename.endswith(".jpg")
    ]
    random.shuffle(image_files)

    # Determine split sizes
    train_size = int(0.7 * len(image_files))
    test_size = int(0.15 * len(image_files))
    valid_size = len(image_files) - train_size - test_size

    for i, filename in enumerate(image_files):
        image_path = os.path.join(src_folder, "images", filename)
        label_path = os.path.join(
            src_folder, "labels", filename.replace(".jpg", ".txt")
        )

        if i < train_size:
            destination_folder = TRAIN_FOLDER
        elif i < train_size + test_size:
            destination_folder = TEST_FOLDER
        else:
            destination_folder = VALID_FOLDER

        shutil.copy(image_path, os.path.join(destination_folder, "images"))
        shutil.copy(label_path, os.path.join(destination_folder, "labels"))


def create_yaml():
    data = {
        "train": os.path.join(OUTPUT_DIR, "traindata"),
        "val": os.path.join(OUTPUT_DIR, "validdata"),
        "test": os.path.join(OUTPUT_DIR, "testdata"),
        "nc": VEHICLE_CLASS,
        "names": VEHICLE,
    }

    with open(os.path.join(OUTPUT_DIR, "vehicledata.yaml"), "w+") as file:
        yaml.dump(data, file)


def vehicle_class_statistics():
    class_idx = {str(i): VEHICLE[i] for i in range(VEHICLE_CLASS)}
    class_stat = {}
    data_len = {}

    for mode in ["traindata", "validdata", "testdata"]:
        vehicle_class_counts = {VEHICLE[i]: 0 for i in range(VEHICLE_CLASS)}
        path = os.path.join(OUTPUT_DIR, mode, "labels")

        for file in os.listdir(path):
            with open(os.path.join(path, file)) as f:
                lines = f.readlines()

                for cls in set([line[0] for line in lines]):
                    vehicle_class_counts[class_idx[cls]] += 1

        data_len[mode] = len(os.listdir(path))
        class_stat[mode] = vehicle_class_counts

    # Visualize class statistics
    fig, ax = plt.subplots(1, 3, figsize=(15, 5), sharey=True)

    for i, mode in enumerate(["traindata", "validdata", "testdata"]):
        sns.barplot(
            pd.DataFrame({mode: class_stat[mode]}).T / data_len[mode] * 100, ax=ax[i]
        )
        ax[i].set_title(mode)
        ax[i].tick_params(rotation=90)
        ax[i].set_ylabel("Percentage of vehicles")

    plt.show()


def resize_img(folder_path):
    image_files = [
        filename for filename in os.listdir(folder_path) if filename.endswith(".jpg")
    ]
    for filename in image_files:
        image_path = os.path.join(folder_path, filename)
        image = Image.open(image_path)
        resized_image = image.resize(IMG_SIZE)
        resized_image.save(image_path)


def resize_all_img():
    print(f"\nResizing images to target size: {IMG_SIZE}")
    for mode in ["traindata", "validdata", "testdata"]:
        folder_path = os.path.join(OUTPUT_DIR, mode, "images")
        resize_img(folder_path)
        resized_image_count = len(os.listdir(folder_path))

        print(f"\nNumber of images in {mode} set after resizing: {resized_image_count}")
        unique_sizes = set()
        for file in glob.glob(os.path.join(folder_path, "*")):
            image = Image.open(file)
            size = image.size
            unique_sizes.add(size)
        if len(unique_sizes) == 1:
            print(f"All images in {mode} set have the same size: {unique_sizes.pop()}")
        else:
            print(f"Image sizes in {mode} set are not consistent: {unique_sizes}")


def train_model(epochs):
    model = YOLO("yolov8n.pt")
    model.train(
        data=os.path.join(OUTPUT_DIR, "vehicledata.yaml"),
        task="detect",
        imgsz=224,
        epochs=epochs,
        batch=32,
        mode="train",
        name="train_v1",
    )


def load_model():
    model = YOLO("/kaggle/working/runs/detect/train_v1/weights/best.pt")
    return model


def perform_predictions(trained_model, test_folder):
    results = trained_model.predict(
        source=os.path.join(test_folder, "images"), save=True, stream=True
    )
    return results


def display_predictions(predictions, n):
    predictions_path = glob.glob(
        os.path.join(OUTPUT_DIR, "runs/detect/predict", "*")
    )
    for _ in range(n):
        idx = np.random.randint(0, len(predictions_path))
        image = Image.open(predictions_path[idx])
        plt.imshow(image)
        plt.grid(False)
        plt.show()


def display_predictions(predictions, n):
    predictions_path = glob.glob(
        os.path.join(OUTPUT_DIR, "runs/detect/predict", "*")
    )
    num_cols = 3
    num_rows = (n + num_cols - 1) // num_cols  # Calculate the number of rows needed

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5 * num_rows))
    axes = axes.flatten()

    for i in range(n):
        idx = np.random.randint(0, len(predictions_path))
        image = Image.open(predictions_path[idx])
        axes[i].imshow(image)
        axes[i].grid(False)
        axes[i].axis("off")  # Hide axis
        axes[i].set_title(f"Image {i+1}")

    # Remove empty subplots if n is not a multiple of 3
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    create_folders([TRAIN_FOLDER, TEST_FOLDER, VALID_FOLDER])
    copy_images_with_label(DATASET_FOLDER, TRAIN_FOLDER, TEST_FOLDER, VALID_FOLDER)
    create_yaml()
    vehicle_class_statistics()
    resize_all_img()
    train_model(10)
    trained_model = load_model()
    predictions = perform_predictions(trained_model, TEST_FOLDER)
    display_predictions(predictions, 10)