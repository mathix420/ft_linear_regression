import csv
import argparse


parser = argparse.ArgumentParser(description='Calculate prediction precision.')
parser.add_argument('path', help='path of the reference data file')
parser.add_argument('--thetas', '-t', type=str, default='thetas.csv',
                    help='path of thetas.csv')
options = parser.parse_args()


def reading_data(path):
    """
    This function read csv files.
    """
    out_1 = []
    out_2 = []
    try:
        with open(path, 'r') as csv_fd:
            file = csv.DictReader(csv_fd)
            for row in file:
                out_1.append(float(row['km']))
                out_2.append(float(row['price']))
    except:
        print('Fatal error when trying reading csv!')
        exit(1)
    return out_1, out_2


def estimate_price(kilometers, thetas, scale):
    """
    This function return the estimated price of the car.
    The estimate is generated via the thetas.
    """
    theta0, theta1 = thetas
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


def get_deviation(reference, thetas, scale):
    """
    This function estimate the price for each mileage in the reference,
    then calculate the absolute deviation of the two prices
    and finally return the sum of these deviations.
    """
    ecarts = []
    for kil, price in zip(reference[0], reference[1]):
        ecarts.append(abs(price - estimate_price(kil, thetas, scale)) / price)

    return sum(ecarts) / len(ecarts) * 100


if __name__ == "__main__":
    with open(options.thetas, 'r') as fp:
        line = fp.read().split(';')

    thetas = float(line[0]), float(line[1])
    scale = int(line[2])

    ref = reading_data(options.path)
    precision = 100 - get_deviation(ref, thetas, scale)

    print(f'Predictions have an accuracy of {precision}%')
