import functools


def check_id_valid(id_number):
    """Checks if the ID number is valid
    :param id_number: ID number
    :type id_number: int
    :return: True if ID number is valid and False otherwise
    :rtype: bool
    """
    if len(str(id_number)) != 9:
        return False
    return functools.reduce(lambda x, y: x + sum([int(n) for n in str(y)]),
                            [x * y for x, y in zip([int(n) for n in str(id_number)], [1, 2, 1, 2, 1, 2, 1, 2, 1])],
                            0) % 10 == 0


class IDIterator:
    """
    A class used to represent an ID iterator
    """

    def __init__(self, input_id):
        """Initialization
        :param input_id: ID number
        :type input_id: int
        :return: None
        """
        self._id = input_id

    def __iter__(self):
        return self

    def __next__(self):
        """Finds the next valid ID
        :raise: StopIteration: raises an Exception
        :return: next valid ID
        :rtype: int
        """
        self._id += 1
        while not check_id_valid(self._id):
            self._id += 1
        if self._id > 999999999:
            raise StopIteration("No more valid ID numbers")
        return self._id


def id_generator(input_id):
    """ID generator, generates valid IDs
    :param input_id: ID number
    :type input_id: int
    :raise: StopIteration: raises an Exception
    :return: next valid ID number
    :rtype: int
    """
    while input_id <= 999999999:
        input_id += 1
        if check_id_valid(input_id):
            yield input_id
    raise StopIteration("No more valid ID number")


def main():
    input_id = int(input("Enter ID: "))
    input_type = input("Generator or Iterator? (gen/it)? ")
    if input_type == "it":
        id_iter = iter(IDIterator(input_id))
        for i in range(10):
            print(next(id_iter))
    elif input_type == "gen":
        id_gen = id_generator(input_id)
        for i in range(10):
            print(next(id_gen))


if __name__ == "__main__":
    main()
