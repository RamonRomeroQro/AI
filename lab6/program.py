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
    return sum(value * peso for value, peso in zip(values, weights))

def main():
    ''' Perceptron '''
    dimensionality=int(input())
    size_training=int(input())
    size_test=int(input())
    training=[]
    for i in range(size_training):
        a=[ float(x.strip()) for x in str(input()).split(',')]
        t=a[:-1], a[-1]
        training.append(t)
    #print (training)
    threshold = 0.5
    learning_rate = 0.01
    weights = [0] * dimensionality
    epochs=0
    limit=False


    while True:
        #print (epochs)
        epochs=epochs+1
        error_counter = 0
        for inputs, expected_output in training:

            result = dot_product(inputs, weights) > threshold
            error = expected_output - result
            if error != 0:
                error_counter += 1
                for index, value in enumerate(inputs):
                    weights[index] += learning_rate * error * value
        if error_counter == 0:
            break
        elif  epochs>1000:
            limit=True
            break

    test=[]
    for i in range(size_test):
        b=[ float(x.strip()) for x in str(input()).split(',')]
        test.append(b)

    if limit==False:
        #print(weights)

        for t in test:
            result = dot_product(t, weights) > threshold
            print(int(result))
    else:
        print("no solution found")
                
        

    
    


if __name__ == "__main__":
    main()