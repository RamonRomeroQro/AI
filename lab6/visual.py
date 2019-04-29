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
import matplotlib.pyplot as plt
import numpy as np


def dot_product(values, weights):
    ''' Dot Product operation'''
    return sum(v * w for v, w in zip(values, weights))

class Perceptron():
    def __init__(self, dimensionality):
        ''' Perceptron initializer '''
        self.threshold = 0.03
        self.learning_rate = 0.1
        self.weights = [0] * dimensionality
        self.epoch_limit = 10000
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

                b=dot_product(inputs, self.weights)
                if error != 0:
                    error_counter += 1
                    for index, value in enumerate(inputs):
                        self.weights[index] += self.learning_rate * \
                            error * value
            if error_counter == 0:
                #print("f")
                return self.weights, b
            elif  epochs > self.epoch_limit :
                return None, None

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
    ptx=[]
    pty=[] 
    ntx=[]
    nty=[]
    for i in range(size_training):
        a = [float(x.strip()) for x in str(input()).split(',')]
        if a[-1] == 1:

            ptx.append(a[0])
            pty.append(a[1])
        else:
            ntx.append(a[0])
            nty.append(a[1])

        t = a[:-1], a[-1]
        training.append(t)
    
    
    plt.plot(ptx, pty, "bo") 
    plt.plot(ntx, nty, "ro") 
    # ditto
    #plt.scatter(tx, ty)
    # print (training)
    # Create Perceptron
    p = Perceptron(dimensionality)
    # Train Perceptron
    pvx=[]
    pvy=[]
    nvx=[]
    nvy=[]

    weights, pb = p.training(training)
    #print(pb)
    if  weights != None:
     
        for i in range(size_test):
            b = [float(x.strip()) for x in str(input()).split(',')]
            # Precict Output
            
            prediction=p.predict(b)
            print(prediction)
            if prediction==1:
                pvx.append(b[0])
                pvy.append(b[1])
            else:
                nvx.append(b[0])
                nvy.append(b[1])
                
     
        #plt.plot([0, - 2/ weights[0]], [-2 / weights[1], 0], 'go-')
        
        #xintercept = (0, ( weights[1]) )
        #yintercept = ( ( weights[0]), 0)
        #plt.plot([xintercept[0], yintercept[0] ], [xintercept[1], yintercept[1] ], 'go-')

        my=weights[1]
        mx=-weights[0]
        m=my/mx
        x = np.linspace(-2,2,100)
        y = m*x+pb
        plt.plot(x, y, '-g', label='ono')
        
        print("w, bias = ", weights, pb)

        print("y = "+str(m)+"x"+"+"+str(pb))

    else:
        print("no solution found")
    
    plt.plot(pvx, pvy, "yo") # and y using blue circle markers
    plt.plot(nvx, nvy, "co") # and y using blue circle markers
    plt.show()


if __name__ == "__main__":
    main()
