import matplotlib.pyplot as plt
import numpy as np


class Flumph:
    def __init__(self, states, odds, initial_odds):
        self.states = states
        self.odds = odds
        self.initial_odds = initial_odds

    def calculate_odds(self):
        vec = self.initial_odds
        calculated_odds = {}
        for i in range(len(self.states)):
            calculated_odds[i] = [vec[i]]

        while 1:
            prev_vec = vec

            vec = np.dot(vec, self.odds)

            for i in range(len(vec)):
                calculated_odds[i].append(vec[i])

            # Ensuring the format of our list is appropriate.
            for i in range(len(vec)):
                if vec[i] > 0.99:
                    return calculated_odds

            if np.array_equal(prev_vec, vec):
                return calculated_odds

    def plot_condition(self):
        plot_data_types = self.calculate_odds()
        intervals = list(range(len(plot_data_types[0])))

        for i in range(len(plot_data_types)):
            plt.plot(intervals, plot_data_types[i], label=self.states[i])

        plt.xlabel('Elapsed Time')
        plt.legend(loc='lower right')
        plt.ylabel('Odds')
        plt.show()


states = [
    'Hungry',
    'Happy',
    'Hunted'
]

odds = [
    [0.8, 0.4, 0.6],
    [0.1, 0.5, 0.2],
    [0.1, 0.1, 0.2]
]

begin_vector = [0.1, 0.7, 0.2]

flumph = Flumph(states, odds, begin_vector)
flumph.plot_condition()

states2 = [
    'Hungry',
    'Happy',
    'Hunted',
    'Sad'
]

odds2 = [
    [0.8, 0.1, 0.05, 0.9],
    [0.4, 0.5, 0.05, 0.9],
    [0.6, 0.2, 0.1, 0.9],
    [0.1, 0.1, 0.1, 0.9],
]

tweede_begin_vector = [0.1, 0.65, 0.2, 0.01]

sad_flumph = Flumph(states2, odds2, tweede_begin_vector)
sad_flumph.plot_condition()
