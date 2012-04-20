from scitools.std import *

def plot_last_thingie(f):
    infile = open('out.dat', 'r')
    values = []
    x = []
    for line in infile:
        split = line.split()
        
        x.append(float(split[0]))
        values.append(float(split[1]))
    x = array(x)
    values = array(values)
    fx = f(x);
    figure()
    
    plot(x, fx, 'b')
    axis([min(x)*1.2, max(x)*1.2, min(fx)*1.2, max(fx)*1.2])
    hold("on")

    plot(x, values, 'g')
    hold("off")

f = lambda x:x*x*exp(-x*x)
plot_last_thingie(f)
