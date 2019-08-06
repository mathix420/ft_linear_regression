import argparse

parser = argparse.ArgumentParser(description='Estimating program for linear regression gradient descent.')
parser.add_argument('kilometers', type=int, help='kilometers of the car')
parser.add_argument('--thetas', '-t', type=str, default='thetas.csv',
                        help='path of thetas.csv')
options = parser.parse_args()


def estimate_price(kilometers):
    """
    This function print the estimated price of the car.
    """
    try:
        with open(options.thetas, 'r') as fp:
            line = fp.read().split(';')
            theta0 = float(line[0])
            theta1 = float(line[1])
            scale = int(line[2])
    except:
        print('Error when trying to read thetas!')
        exit(1)

    return (theta0 + theta1 * kilometers / scale) * scale


if __name__ == "__main__":
    print('Estimate price :', estimate_price(options.kilometers))
