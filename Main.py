from src.camera.camera import Camera


def main():
    # Camera parameters
    width=1920
    height=1080
    cam_channel=0

    # YOLO model parameters
    confidence_threshold=0.5
    model_path='C:/ML/Yolo_model/best.pt'


    webcam=Camera(width, height, cam_channel, confidence_threshold, model_path)
    webcam.main()

if __name__ == "__main__":
    main()