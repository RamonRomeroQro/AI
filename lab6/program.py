'''
    Copyright 2019 
    © Ramon Romero   @RamonRomeroQro

    Intelligent Systems, ITESM.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    Special thanks to: 
    Ruben Stranders @rhomeister and the FLOSS/SUDO comunity.
    Python 3.7.2 (PEP8)

'''


def dot_product(values, weights):
    ''' Dot Product operation'''
    return sum(v * w for v, w in zip(values, weights))

class Perceptron():
    def __init__(self, dimensionality):
        ''' Perceptron initializer '''
        self.threshold = 0.5
        self.learning_rate = 0.01
        self.weights = [0] * dimensionality
        self.epoch_limit = 1000
        self.limit = False

    def training(self, train_expected):
        ''' Train perceptron with array of values, expectation'''
        epochs = 0
        while True:
            #print (epochs)
            epochs = epochs+1
            error_counter = 0
            for inputs, expected_output in train_expected:

                result = dot_product(inputs, self.weights) > self.threshold
                error = expected_output - result
                if error != 0:
                    error_counter += 1
                    for index, value in enumerate(inputs):
                        self.weights[index] += self.learning_rate * \
                            error * value
            if error_counter == 0:
                break
            elif self.epoch_limit > 1000:
                return None

    def predict(self, inputs):
        ''' Predict output for a given input '''
        result = dot_product(inputs, self.weights) > self.threshold
        return (int(result))


def main():
    # Parsing input
    dimensionality = int(input())
    size_training = int(input())
    size_test = int(input())
    training = []
    for i in range(size_training):
        a = [float(x.strip()) for x in str(input()).split(',')]
        t = a[:-1], a[-1]
        training.append(t)
    # print (training)
    # Create Perceptron
    p = Perceptron(dimensionality)
    # Train Perceptron
    if p.training(training) != None:
        for i in range(size_test):
            b = [float(x.strip()) for x in str(input()).split(',')]
            # Precict Output
            print(p.predict(b))
    else:
        print("no solution found")

if __name__ == "__main__":
    main()
