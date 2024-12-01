import math


def resulting_force(*args):
    """
        Calculates resulting force from given forces

        @param *args:    list of forces

        @return:         Vector of force
    """
    # TODO
    res_force = [0, 0, 0]
    for force in args:
        for i in range(3):
            res_force[i] += force[i]
    print('Resulting force: ', res_force)
    return res_force


def calculate_vector_magnitude(vector):
    """
        Calculates magnitude of a vector

        @param vector:    Vector

        @return:          Magnitude of a vector
    """

    vector_magnitude = math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)

    return vector_magnitude