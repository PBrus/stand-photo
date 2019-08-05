from math import sqrt
from scipy import odr


class PointsRegression:

    def __init__(self, points):
        self.points = points
        self.line_parameters = self._initial_regression_parameters()

    @staticmethod
    def regression_function(points, x):
        return points[0]*x + points[1]

    @staticmethod
    def line_point_distance(line_parameters, point_coordinates):
        A, B = line_parameters
        x, y = point_coordinates

        return abs(A*x - y + B)/sqrt(A ** 2 + 1)

    def _initial_regression_parameters(self):
        result = self._odr_wrapper([0, 0])
        result = self._odr_wrapper(result.beta)

        return result.beta

    def _odr_wrapper(self, beta):
        result = odr.ODR(
            odr.Data(
                self.points.iloc[:, 0],
                self.points.iloc[:, 2],
                1./(self.points.iloc[:, 1] ** 2),
                1./(self.points.iloc[:, 3] ** 2)),
            odr.Model(PointsRegression.regression_function),
            beta0=beta).run()

        return result

    def weight_errors(self, error):
        return 1./sqrt(error[0]**2 + error[1]**2)

    def rms(self):
        distances = [
            PointsRegression.line_point_distance(self.line_parameters, point)**2
            for point in zip(self.points.iloc[:, 0], self.points.iloc[:, 2])]
        weights = [
            self.weight_errors(error)
            for error in zip(self.points.iloc[:, 1], self.points.iloc[:, 3])]
        weighted_distances = [el[0]*el[1] for el in zip(weights, distances)]

        return sqrt(sum(weighted_distances)/sum(weights))
