import time
i=0
timer1 = time.time()
timer2 = time.time()
print(timer1)
while i<10:
    agora = time.time()
    print(agora)
    if timer1 - agora>5:
        break
    i+=1
    time.sleep(1)
