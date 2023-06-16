import os



folders = sorted(os.listdir())


for f in folders:
    if f.startswith("data-cregion_A2"):
        for file in sorted(os.listdir(f)):
            print(f)
            os.system("python3 regionpercent.py " + f)
