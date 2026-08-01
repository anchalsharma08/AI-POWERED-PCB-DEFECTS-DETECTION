from predictor import predict_image

detections = predict_image("test_images/pcb2.jpg")

print("=" * 60)

for d in detections:
    print(d)

print("=" * 60)