import os #using for navigating folders
import shutil # using to copy images
from pathlib import Path # A modern way to work with file paths.
import cv2 # using OpenCV to read image dimensions.
from tqdm import tqdm

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SOURCE_DATASET = PROJECT_ROOT / "DeepPCB-master" / "PCBData"
OUTPUT_DATASET = PROJECT_ROOT / "dataset"

folders = [
    "train/images",
    "train/labels",
    "valid/images",
    "valid/labels",
    "test/images",
    "test/labels"
]

for folder in folders:
    (OUTPUT_DATASET / folder).mkdir(parents=True, exist_ok=True)


def get_image_size(image_path):

    image = cv2.imread(str(image_path))

    if image is None:
        raise FileNotFoundError(f"Cannot read {image_path}")

    height, width = image.shape[:2]

    return width, height

def convert_to_yolo(x1, y1, x2, y2, img_width, img_height):

    box_width = x2 - x1
    box_height = y2 - y1

    center_x = x1 + box_width / 2
    center_y = y1 + box_height / 2

    center_x /= img_width
    center_y /= img_height

    box_width /= img_width
    box_height /= img_height

    return center_x, center_y, box_width, box_height

def convert_annotation(label_path, image_width, image_height):
    """
    Reads one DeepPCB annotation file and converts
    it into YOLO format.
    """

    yolo_labels = []

    with open(label_path, "r") as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            x1, y1, x2, y2, class_id = map(int, line.split())

            cx, cy, w, h = convert_to_yolo(
                x1,
                y1,
                x2,
                y2,
                image_width,
                image_height,
            )

            # DeepPCB classes start from 1
            # YOLO classes start from 0

            class_id -= 1

            yolo_labels.append(
                f"{class_id} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}"
            )

    return yolo_labels

def save_yolo_label(output_path: Path, labels):
    """
    Saves converted YOLO annotations.
    """

    with open(output_path, "w") as file:

        for label in labels:
            file.write(label + "\n")

def get_split(image_id):

    if image_id in TRAIN_IDS:
        return "train"

    elif image_id in TEST_IDS:
        return "test"

    else:
        return None

def load_split(file_path: Path):
    """
    Reads trainval.txt or test.txt and extracts only the image IDs.
    """

    ids = set()

    with open(file_path, "r") as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            # Split the line into image path and label path
            image_path, _ = line.split()

            # Example:
            # group00041/00041/00041140.jpg

            image_name = Path(image_path).stem

            ids.add(image_name)

    return ids

def process_dataset():

    total_images = 0
    skipped = 0

    for group_folder in tqdm(group_folders):

        image_folder = None
        label_folder = None

        for folder in group_folder.iterdir():

            if folder.is_dir():

                if folder.name.endswith("_not"):
                    label_folder = folder

                else:
                    image_folder = folder

        if image_folder is None or label_folder is None:
            continue

        for image_path in image_folder.rglob("*_test.jpg"):

            image_id = image_path.stem.replace("_test", "")


            print("First TRAIN ID :", next(iter(TRAIN_IDS)))
            print("Image Name     :", image_path.name)
            print("Image ID       :", image_id)
  

            split = get_split(image_id)
            if split is None:
                skipped += 1
                continue

            label_files = list(label_folder.rglob(f"{image_id}.txt"))

            if not label_files:
                skipped += 1
                continue

            label_path = label_files[0]

            width, height = get_image_size(image_path)

            yolo_labels = convert_annotation(
                label_path,
                width,
                height
)
          

            output_image = (
                OUTPUT_DATASET
                / split
                / "images"
                / f"{image_id}.jpg"
            )

            output_label = (
                OUTPUT_DATASET
                / split
                / "labels"
                / f"{image_id}.txt"
            )

            shutil.copy(image_path, output_image)

            save_yolo_label(
                output_label,
                yolo_labels
            )

            total_images += 1

    print("\n")

    print("=" * 50)

    print("Conversion Complete")

    print("=" * 50)

    print(f"Images Converted : {total_images}")

    print(f"Skipped          : {skipped}")

    print("=" * 50)

TRAIN_IDS = load_split(
    SOURCE_DATASET / "trainval.txt"
)

TEST_IDS = load_split(
    SOURCE_DATASET / "test.txt"
)

group_folders = sorted(

    folder
    for folder in SOURCE_DATASET.iterdir()

    if folder.is_dir() and folder.name.startswith("group")

)

if __name__ == "__main__":

    print("=" * 50)

    print(f"Training Images : {len(TRAIN_IDS)}")

    print(f"Testing Images  : {len(TEST_IDS)}")

    print(f"Group Folders   : {len(group_folders)}")

    print("=" * 50)

process_dataset()
