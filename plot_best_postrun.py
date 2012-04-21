from scitools.std import *

def plot_last_thingie(f):
    infile = open('out.dat', 'r')
    values = []
    x = []
    all_data = []
    for line in infile:

        if line.startswith("newfunc"):
            all_data.append([x, values])
            x = []
            values = []
        else:
            split = line.split()
        
            x.append(float(split[0]))
            values.append(float(split[1]))
    for x, values in all_data:
        x = array(x)
        values = array(values)
        fx = f(x);
        figure(1)
     

        plot(x, fx, 'b', show=False)
        axis([min(x)*1.2, max(x)*1.2, min(fx)*1.2, max(fx)*1.2])

        hold("on")

        plot(x, values, 'g', show=True)
        hold("off")

        exact = fx

        match_factor = 0;
        for trueval, testval in zip(exact, values):
            match_factor += (trueval - testval)*(trueval - testval);

        print "Error: ", sqrt(match_factor)

        raw_input("Press a key")

f = lambda x:x*x*exp(-x*x)
plot_last_thingie(f)
