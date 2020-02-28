from time import gmtime, strftime


def time_helper():
    """
    Get the current time
    :return: formatted time string
    """

    curr_time = strftime("%H:%M", gmtime())
    return curr_time


def date_helper():
    """
    Get the current date
    :return: formatted date string
    """

    curr_date = strftime("%m-%d-%Y", gmtime())
    return curr_date


if __name__ == "__main__":
    time_helper()
    date_helper()
