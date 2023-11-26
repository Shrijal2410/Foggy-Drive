OUTPUT_DIR = os.path.join(WORK_DIR, "runs/detect/predict")


def display_predictions():
    image_files = [
        filename for filename in os.listdir(OUTPUT_DIR) if filename.endswith(".jpg")
    ]

    if not image_files:
        print("No images found in the specified folder.")
        return

    num_images = min(len(image_files), 4)
    fig, axes = plt.subplots(2, 2, figsize=(8, 8))

    for i in range(num_images):
        image_path = os.path.join(OUTPUT_DIR, image_files[i])
        image = Image.open(image_path)
        row, col = divmod(i, 2)
        axes[row, col].imshow(image)
        axes[row, col].grid(False)
        axes[row, col].axis("off")

    plt.show()


if __name__ == "__main__":
    display_predictions()