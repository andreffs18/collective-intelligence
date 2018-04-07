import time
from tqdm import tqdm
from random import randint, random
import math


def get_flights_schedule(filename='schedule.txt'):
    flights = {}
    for line in open(filename).readlines():
        origin, dest, depart, arrive, price = line.strip().split(',')
        flights.setdefault((origin, dest), [])

        # Add details to the list of possible flights
        flights[(origin, dest)].append((depart, arrive, int(price)))
    return flights

def get_minutes(t):
    x = time.strptime(t, '%H:%M')
    return x[3] * 60 + x[4]


def print_schedule(scores, people, flights, destination='LGA'):
    for s in range(len(scores) / 2):
        name = people[s][0]
        origin = people[s][1]
        out = flights[(origin, destination)][int(scores[s * 2])]
        ret = flights[(destination, origin)][int(scores[s * 2 + 1])]
        print('%10s%10s %5s-%5s $%3s %5s-%5s $%3s \t(Total: $%s)' % (name, origin, out[0], out[1], out[2], ret[0], ret[1], ret[2], out[2] + ret[2]))


def schedule_cost(scores, people, flights, destination="LGA"):
    total_price = 0

    latest_arrival = 0
    earliest_departure = 24 * 60

    # Iter for every person a figure out which is the latest and earliest flight
    for s in range(len(scores) / 2):
        # Get the inbound and outbound flights
        origin = people[s][1]
        outbound_f = flights[(origin, destination)][int(scores[s * 2])]
        inbound_f = flights[(destination, origin)][int(scores[s * 2 + 1])]
        # Total price is the price of all outbound and return flights
        total_price += outbound_f[2] + inbound_f[2]
        # Track the latest arrival and earliest departure
        if latest_arrival < get_minutes(outbound_f[1]):
            latest_arrival = get_minutes(outbound_f[1])

        if earliest_departure > get_minutes(inbound_f[0]):
            earliest_departure = get_minutes(inbound_f[0])

    # Every person must wait at the airport until the latest person arrives.
    # They also must arrive at the same time and wait for their flights.
    total_wait = 0
    for s in range(len(scores) / 2):
        # Get the inbound and outbound flights
        origin = people[s][1]
        outbound_f = flights[(origin, destination)][int(scores[s * 2])]
        inbound_f = flights[(destination, origin)][int(scores[s * 2 + 1])]

        # Sum all total wait time
        total_wait += latest_arrival - get_minutes(outbound_f[1])
        total_wait += get_minutes(inbound_f[0]) - earliest_departure

    # Does this solution require an extra day of car rental? That'll be $50!
    if latest_arrival > earliest_departure:
        total_price += 50
    return total_price + total_wait



def random_optimize(domain, people, flights, destination="LGA", cost_func=schedule_cost, guesses=1000):
    best = 999999999
    best_scores = None

    for i in tqdm(range(guesses)):
        # Create a random solution
        r = [float(randint(domain[j][0], domain[j][1]))  for j in range(len(domain))]

        # Get the cost
        cost = cost_func(r, people, flights, destination)

        # Compare it to the best one so far
        if cost < best:
            best = cost
            best_scores = r
    return best_scores


def hillclimb_optimize(domain, people, flights, destination="LGA", cost_func=schedule_cost):
    # Create a random solution
    scores = [randint(domain[i][0], domain[i][1])
              for i in range(len(domain))]
    # Main loop
    while 1:
        # Create list of neighboring scores
        neighbors = []

        for j in range(len(domain)):
            # One away in each direction
            if scores[j] > domain[j][0]:
                neighbors.append(scores[0:j] + [scores[j] + 1] + scores[j + 1:])
            if scores[j] < domain[j][1]:
                neighbors.append(scores[0:j] + [scores[j] - 1] + scores[j + 1:])

        # See what the best solution amongst the neighbors is
        current = cost_func(scores, people, flights, destination)
        best = current
        for j in range(len(neighbors)):
            cost = cost_func(neighbors[j], people, flights, destination)
            if cost < best:
                best = cost
                scores = neighbors[j]

        # If there's no improvement, then we've reached the top
        if best == current:
            break
    return scores


def annealing_optimize(domain, people, flights, destination="LGA", cost_func=schedule_cost, T=10000.0, cool=0.95, step=1):
    # Initialize the values randomly
    vec = [float(randint(domain[i][0], domain[i][1]))
           for i in range(len(domain))]

    while T > 0.1:
        # Choose one of the indices
        i = randint(0, len(domain) - 1)

        # Choose a direction to change it
        direction = randint(-step, step)

        # Create a new list with one of the values changed
        vecb = vec[:]
        vecb[i] += direction
        if vecb[i] < domain[i][0]:
            vecb[i] = domain[i][0]
        elif vecb[i] > domain[i][1]:
            vecb[i] = domain[i][1]

        # Calculate the current cost and the new cost
        ea = cost_func(vec, people, flights, destination)
        eb = cost_func(vecb, people, flights, destination)
        p = pow(math.e, (-eb - ea) / T)

        # Is it better, or does it make the probability cutoff?
        if eb < ea or random() < p:
            vec = vecb

        # Decrease the temperature
        T *= cool
    return vec


def genetic_optimize(domain, people, flights, destination="LGA", cost_func=schedule_cost, popsize=50, step=1, mutprob=0.2, elite=0.2, maxiter=100, repeat_min_score=10):
    # Mutation Operation
    def mutate(vec):
        i = randint(0, len(domain) - 1)
        if random() < 0.5 and vec[i] > domain[i][0]:
            return vec[0:i] + [vec[i] - step] + vec[i + 1:]
        elif vec[i] < domain[i][1]:
            return vec[0:i] + [vec[i] + step] + vec[i + 1:]

    # Crossover Operation
    def crossover(r1, r2):
        i = randint(1, len(domain) - 2)
        return r1[0:i] + r2[i:]

    # Build the initial population
    pop = []
    for i in range(popsize):
        vec = [randint(domain[i][0], domain[i][1])
               for i in range(len(domain))]
        pop.append(vec)

    # How many winners from each generation?
    topelite = int(elite * popsize)

    last_score = None
    last_score_count = 0

    # Main loop
    for _ in tqdm(range(maxiter)):
        scores = [(cost_func(v, people, flights, destination), v) for v in pop if v]
        scores.sort()
        ranked = [v for (s, v) in scores]

        # Start with the pure winners
        pop = ranked[0:topelite]

        # Add mutated and bred forms of the winners
        while len(pop) < popsize:
            if random() < mutprob:
                # Mutation
                c = randint(0, topelite)
                pop.append(mutate(ranked[c]))
            else:
                # Crossover
                c1 = randint(0, topelite)
                c2 = randint(0, topelite)
                pop.append(crossover(ranked[c1], ranked[c2]))

        # If score doesn't change for more than repeat_min_score times, skip for loop
        if scores[0][0] == last_score:
            last_score_count += 1

        if last_score_count > repeat_min_score:
            break

        last_score = scores[0][0]


    return scores[0][1]
