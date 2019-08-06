import csv
import argparse
import matplotlib.pyplot as plt

#init plt size
plt.rcParams['figure.figsize'] = (12.0, 9.0)

#init options
parser = argparse.ArgumentParser(
    description='Learning program for linear regression gradient descent.'
)
parser.add_argument('path', help='path of the training data file')
parser.add_argument('--learning_rate', '-l',
    type=int,
    default=0.0001,
    help='learning rate (default: 0.0001)'
)
parser.add_argument('--passes', '-p',
    type=int,
    default=200000,
    help='number of passes (default: 200000)'
)
parser.add_argument('--scale', '-s',
    type=int,
    default=1000,
    help='scaling value (default: 1000)'
)
parser.add_argument('--graph', '-g',
    action='store_true',
    help='show graph'
)
options = parser.parse_args()


def reading_data(path):
    """
    This function read csv files.
    """
    try:
        with open(path, 'r') as csv_fd:
            file = csv.DictReader(csv_fd)
            out_1 = []
            out_2 = []
            for row in file:
                out_1.append(float(row['km']))
                out_2.append(float(row['price']))
        return out_1, out_2
    except:
        print('Fatal error when trying reading csv!')
        exit(1)


def scaling_data(data, scale):
    """
    Normalize the data.
    """
    _x, _y = data
    return [i / scale for i in _x], [i / scale for i in _y]


def loss(thetas, data):
    x, y = data
    n = len(x)
    new_y = lambda x: thetas[0] + thetas[1] * x
    return sum((y[i] - new_y(x[i])) ** 2 for i in range(n)) / n * 1000


def predict_y(data, thetas, scale=1):
    _x, _y = data
    return [(thetas[0] + thetas[1] * miles) * scale for miles in _x]


def training(data, learning_rate, steps):
    """
    This function train the machine, with model data.
    """
    #init variables
    _x, _y = data
    thetas = [0, 0]
    loss_list = []

    rng = range(len(_x))
    m = float(len(_x))

    new_y = lambda x: thetas[0] + thetas[1] * x

    #starting steps
    for i in range(steps):
        D_0 = (-1 / m) * sum([_y[i] - new_y(_x[i]) for i in rng])
        D_1 = (-1 / m) * sum([(_y[i] - new_y(_x[i])) * _x[i] for i in rng])

        thetas[0] -= learning_rate * D_0
        thetas[1] -= learning_rate * D_1

        loss_list.append(loss(thetas, data))
    return thetas, loss_list


if __name__ == "__main__":
    data = reading_data(options.path)
    data = scaling_data(data, options.scale)
    x, y = data

    #plotting inital values
    if options.graph:
        plt.title('Initial values')
        plt.scatter(x, y, color='blue')
        plt.xlabel('mileage (x %i km)' % options.scale)
        plt.ylabel('price (x %i €)' % options.scale)
        plt.show()

    thetas, losses = training(data, options.learning_rate, options.passes)
    print('Thetas found :: %s' % thetas)

    #plotting losses
    if options.graph:
        plt.title('Losses / steps')
        plt.plot(losses, color='red')
        plt.xlabel('steps')
        plt.ylabel('losses')
        plt.show()

    #plotting results
    if options.graph:
        #making predictions
        y_pred = [thetas[1] * i + thetas[0] for i in range(int(min(x)), int(max(x)))]

        plt.title('Results')
        plt.scatter(x, y)
        plt.plot(y_pred, color='red') # predicted
        plt.xlabel('mileage (x %i km)' % options.scale)
        plt.ylabel('price (x %i €)' % options.scale)
        plt.show()

    try:
        with open('thetas.csv', 'w+') as fp:
            fp.write('{};{};{}'.format(thetas[0], thetas[1], options.scale))
    except:
        print('Error on thetas saving!')
        exit(1)

    print('Thetas saved!')