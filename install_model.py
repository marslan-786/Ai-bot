import os
import subprocess

def download_model():
    os.makedirs("experiments/pretrained_models", exist_ok=True)
    subprocess.run([
        "gdown",
        "https://drive.google.com/uc?id=1-r1Zp1ZV9Jw7dYv-Mb9YvO4u5lGU-sXg",
        "-O",
        "experiments/pretrained_models/RealESRGAN_x4plus.pth"
    ])

def clone_repo():
    if not os.path.exists("Real-ESRGAN"):
        subprocess.run(["git", "clone", "https://github.com/xinntao/Real-ESRGAN.git"])

if __name__ == "__main__":
    clone_repo()
    download_model()