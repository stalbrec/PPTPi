
#sense = SenseHat()
#sense.set_rotation(180)

g = (0, 255, 0)
b = (0, 0, 0)
w = (31, 101, 138)
r = (255, 0, 0)
a = (255, 255, 255)
y = (221, 165, 37)
h = (177, 119, 7)
c = (0, 0, 90)
x = (61, 140, 64)
l = (100, 0, 0)


kuh_pixels = [
    a, g, g, g, g, g, g, a,
    a, a, a, g, g, a, a, a,
    g, h, h, h, h, h, h, g,
    h, h, c, h, h, c, h, h,
    g, h, h, h, h, h, h, g, 
    g, h, h, h, h, h, h, g,
    g, g, b, a, a, b, g, g,
    g, g, a, a, a, a, g, g,
]
kuh1_pixels = [
    a, g, g, g, g, g, g, a,
    a, a, a, g, g, a, a, a,
    g, h, h, h, h, h, h, g,
    h, h, h, h, h, h, h, h,
    g, h, h, h, h, h, h, g, 
    g, h, h, h, h, h, h, g,
    g, g, b, a, a, b, g, g,
    g, g, a, a, a, a, g, g,
]
kuh_pixels = [
    a, g, g, g, g, g, g, a,
    a, a, a, g, g, a, a, a,
    g, h, h, h, h, h, h, g,
    h, h, c, h, h, c, h, h,
    g, h, h, h, h, h, h, g, 
    g, h, h, h, h, h, h, g,
    g, g, b, a, a, b, g, g,
    g, g, a, a, a, a, g, g,
]   
    
    
def animate_kuh(sense,n,t1=1,t2=0.3):
    #from sense_hat import SenseHat
    import time
    while n>0:
        sense.set_pixels(kuh_pixels)
        time.sleep(t1)
        sense.set_pixels(kuh1_pixels)
        time.sleep(t2)
        sense.set_pixels(kuh_pixels)
        n = n -1
        print(n)
    