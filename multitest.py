from multiprocessing import Process, Value, Array


def a(c):
    while True:
        print("a" + str(c.value))
        c.value = c.value + 1

def b(c):
    while True:
        print("b" + str(c.value))
        c.value = c.value/2

num = Value('d', 0.0)
asdf = Process(target=a, args=(num,))
bsdf = Process(target=b, args=(num,))
asdf.start()
bsdf.start()
asdf.join()
bsdf.join()
