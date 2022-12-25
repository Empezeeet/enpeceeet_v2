import os
import random
import time

RUNCODE = f"RUN-{random.randint(100, 999)}"



def reinit():
    print("REINIT")
    os.system("python3 modules/reinitialize.py")
    exit()




def main():
    while True:
        x = random.randint(1, 25)
        print(x)
        if x % 2 == 0 and x % 4 == 0:
            reinit()
            exit()
        time.sleep(3)
    
    
if __name__ == "__main__":
    print(f"RUNNIN: {RUNCODE}")
    main()





