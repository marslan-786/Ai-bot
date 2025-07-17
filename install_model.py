import os

# Download Real-ESRGAN model (X4 plus variant)
def download_model():
    if not os.path.exists("experiments/pretrained_models"):
        os.makedirs("experiments/pretrained_models")
    os.system("gdown https://drive.google.com/uc?id=1-r1Zp1ZV9Jw7dYv-Mb9YvO4u5lGU-sXg -O experiments/pretrained_models/RealESRGAN_x4plus.pth")

if __name__ == "__main__":
    download_model()