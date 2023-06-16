import os



folders = os.listdir()


for f in folders:
    if f.startswith("data-dif_A2"):
        for file in sorted(os.listdir(f)):
            os.system("python3 difus.py " + f)
