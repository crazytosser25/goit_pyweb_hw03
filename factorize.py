"""Factorize, task 2"""
from multiprocessing import Pool, cpu_count
from time import time


def calculate(number: int) -> list:
    """This function takes an input number as a parameter and returns a list
    of its factors. The function iterates over all numbers from 1 to the given
    number, checks if the current number is a factor of the input number (i.e.,
    the input number divided by the current number gives a whole number), and
    appends the current number to the list of factors if it is a factor.

    Args:
        number (int): The input number for which we want to find the factors.

    Returns:
        List[int]: A list containing the factors of the input number.
    """
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors

def factorize_normal(*numbers: int) -> list:
    """This function takes multiple numbers as input parameters and returns
    a list containing the factorization results for each input number.
    The function uses a list comprehension to call the `calculate()` function
    for each input number, passing it as an argument. The returned factors are
    then appended to a new list, which is eventually returned.

    Args:
        *numbers (int): Multiple numbers for which we want to find the
        factorization results.

    Returns:
        List[List[int]]: A list containing factorization results for each input
        number. Each sub-list contains the factors of a corresponding input
        number.
    """
    result = []
    for number in numbers:
        result.append(calculate(number))
    return result

def factorize_multiprocess(*numbers: int) -> list:
    """This function takes multiple numbers as input parameters and returns
    a list containing the factorization results for each input number.
    The function uses multiprocessing to perform the calculations in parallel
    using separate processes, which can provide better performance on multi-core
    systems (in theory).

    Args:
        *numbers (int): Multiple numbers for which we want to find the
        factorization results.

    Returns:
        List[List[int]]: A list containing factorization results for each input
        number. Each sub-list contains the factors of a corresponding
        input number.
    """
    result = []
    with Pool(processes=cpu_count()) as pool:
        for number in pool.map(calculate, numbers):
            result.append(number)

    return result


if __name__ == '__main__':
    # tests of single core
    start_time1 = time()
    a1, b1, c1, d1  = factorize_normal(128, 255, 99999, 10651060)
    end_time1 = time()
    print(f"Standart calculating: {end_time1 - start_time1}s")

    assert a1 == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b1 == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c1 == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d1 == [
        1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
        380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530,
        10651060
    ]

    # tests of multi-core
    start_time2 = time()
    a2, b2, c2, d2  = factorize_multiprocess(128, 255, 99999, 10651060)
    end_time2 = time()
    print(f"Miltiprosessing calculating: {end_time2 - start_time2}s " \
        f"with {cpu_count()} cores.")

    assert a2 == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b2 == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c2 == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d2 == [
        1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
        380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530,
        10651060
    ]
