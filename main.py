import subprocess
import sys
import os

def run():
    try:
        uvicorn_path = os.path.join(os.getcwd(), "venv", "Scripts", "uvicorn.exe")
        subprocess.run(
            [uvicorn_path, "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
            check=True,
            env=os.environ.copy()
        )
    except subprocess.CalledProcessError as e:
        print(f"Error launching Fast API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()