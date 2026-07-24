import random
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET = PROJECT_ROOT / "dataset"

TRAIN_IMAGES = DATASET / "train" / "images"
TRAIN_LABELS = DATASET / "train" / "labels"

VALID_IMAGES = DATASET / "valid" / "images"
VALID_LABELS = DATASET / "valid" / "labels"

# Prevent splitting twice
if any(VALID_IMAGES.iterdir()) or any(VALID_LABELS.iterdir()):
    print("Validation folder is not empty!")
    print("Dataset has probably already been split.")
    exit()

train_images = list(TRAIN_IMAGES.glob("*.jpg"))

print(len(train_images))

random.seed(42)

random.shuffle(train_images)

split_index = int(len(train_images) * 0.8)

new_train = train_images[:split_index]

valid = train_images[split_index:]


for image_path in valid:

    image_id = image_path.stem.replace("_test", "")
    label_name = image_id + ".txt"

    print(f"Moving Image : {image_path.name}")
    print(f"Moving Label : {label_name}")

    if not (TRAIN_LABELS / label_name).exists():
        print(f"Label not found: {label_name}")
        continue

    shutil.move(
        image_path,
        VALID_IMAGES / image_path.name
    )

    shutil.move(
        TRAIN_LABELS / label_name,
        VALID_LABELS / label_name
    )

print("=" * 40)

print(f"Training Images : {len(new_train)}")

print(f"Validation Images : {len(valid)}")

print("=" * 40)