from multiprocessing import Process

c = 0

def a():
    global c
    while True:
        print("a" + str(c))
        c = c + 1

def b():
    while True:
        global c
        print("b" + str(c))
        c = c + 1

asdf = Process(target=a)
bsdf = Process(target=b)
asdf.start()
bsdf.start()
asdf.join()
bsdf.join()
