from scitools.std import *

class function:
    def __init__(self, parameters, f):
        self.parameters = parameters
        self.n = len(parameters);
        self.f = f;
        
    def set_region(self, x_min, x_max, reset = False,res=200):
        self.x = linspace(x_min, x_max, res)
        if reset:
            self.values = zeros(res)
            self.get_values()
            self.get_rank();
            
    def get_values(self):
        self.values = zeros(shape=self.values.shape);
        
        for k in range(self.n):
            self.values += self.basis_function(k);
            
    def basis_function(self, k):
        """Implement"""
    def evolve_parameter(self):
        """Implement"""
        

    def get_rank(self):
        exact = self.f(self.x)

        match_factor = 0;
        for trueval, testval in zip(exact, self.values):
            match_factor += (trueval - testval)*(trueval - testval);

        self.rank = sqrt(match_factor)
    

class sinebased(function):
    def basis_function(self, k):

        x = self.x
        if k == 0:
            return 0.5*self.parameters[0][0];
        else:
            return self.parameters[k][0]*cos(k*x) \
                   + self.parameters[k][1]*sin(k*x)

    def evolve_parameter(self, k):

        i = random.randint(self.n)
        j = random.randint(2)

        if k == max_num_kids:
            self.parameters[i][j] = random.random()*2 - 1;
            self.get_values()
            self.get_rank()
            return None

        old = self.rank
        tmp = self.parameters[i][j]
        
        self.parameters[i][j] = self.parameters[i][j]*random.normal(loc=1)
        self.get_values()

        self.get_rank()
        
        if self.rank > old:
            self.rank = old;
            self.parameters[i][j] = tmp;
            self.evolve_parameter(k+1)
        

        

        

def evolved(population, ranks):
    n = len(population)
    tmp = [0]*n
    ranks.sort()
    
    #Sort by how good the fit were
    for i in range(n):
        rank = ranks[i]
        for person in population:
            if person.rank == rank:
                tmp[i] = person;


    #Bottom half doesn't make it. They are replaced by a mean over the survivors
    mean_genetic_code = zeros(shape=tmp[0].parameters.shape)
    for person in tmp[:10]:
        mean_genetic_code += person.parameters;
    mean_genetic_code *= 1./10;
        
    for i in range(n/2, n):
        person = eval(population[0].__class__.__name__ + "(mean_genetic_code, population[0].f)");
        person.set_region(-2,2, reset=True)
        for j in range(mutation_thresh):
            person.evolve_parameter(1);

        
        tmp[i] = person;

    

    return tmp;



def simple_population(f, method, para_dim, n=1000, basis_size=20):

    population = [0]*n;
    ranks = [0]*n;

    
    for N in range(n):
        parameters = random.random(size=[basis_size, para_dim])*2 - 1
        
        person = method(parameters, f);
        person.set_region(-2,2, reset=True)

        #perform mutation_tresh positive evolutions
        for i in range(mutation_thresh):
            person.evolve_parameter(1);

        population[N] = person
        ranks[N] = person.rank

    tmp = evolved(population, ranks);
    return tmp;


def iterate(population):
    n = len(population)

    ranks = [0]*n
    for N in range(n):
       
        #perform mutation_tresh positive evolutions
        for i in range(mutation_thresh):
            population[N].evolve_parameter(1);

        ranks[N] = population[N].rank

    tmp = evolved(population, ranks)

    return tmp;






def copy_list(list1):
    list0 = [0]*len(list1)
    for i in range(len(list1)):
        tmp = list1[i]
        list0[i] = tmp
    return list0








##GLOBALS
mutation_thresh = 20
max_num_kids = mutation_thresh/2;

def main():
    ofile = open('out.dat', 'w')
    showplots = False;

    f = lambda x: x*x*exp(-x*x)
    threshold = 1.2 #a decrease in functionality by (threshold - 1)*100% will not make your population die.
    N_iter = 10;

    
    population = simple_population(f, sinebased, 2, n=1000, basis_size=mutation_thresh)
    best = population[0].rank;
    all_time_best = best;
    
    print "Best: ", best

    
    avg = 0;
    for person in population:
        avg += person.rank;
    avg /= len(population)

    best_avg = avg;
    print "Avg: ", avg, "\n-----------------------"

    
    genetic_elite = copy_list(population)
    
    for i in range(N_iter):
        population = iterate(population)

        new_best = population[0].rank
        print "Best: ", new_best

        avg = 0;
        for person in population:
            avg += person.rank;
        avg /= len(population)
        print "Avg: ", avg


        if new_best < all_time_best:
            all_time_best = new_best;
            for X, Value in zip(population[0].x, population[0].values):
                ofile.write(str(X) +"\t" + str(Value) + "\n")
            ofile.write("newfunc\n")

                
        #Evolution made the wrong turn...
        if new_best*avg > best*threshold*best_avg:
            population = copy_list(genetic_elite)        


        else:   
            best = new_best
            best_avg = avg
            genetic_elite = copy_list(population)

            if showplots:
                x = population[0].x
                fx = f(x);
                figure(1)
                
                plot(x, fx, 'b')
                axis([min(x)*1.2, max(x)*1.2, min(fx)*1.2, max(fx)*1.2])
                hold("on")
           
                plot(x, population[0].values, 'g')
                hold("off")

            
        print "-----------%d/%d----------" % (i+1,N_iter) 

 
    ofile.close()
    

if __name__ == "__main__":
    main()
    
    


        


    
    
