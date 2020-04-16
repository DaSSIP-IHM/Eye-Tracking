import numpy


def fixation_detection(x, y, time, maxdist=25, mindur=50):
    """Detects fixations, defined as consecutive samples with an inter-sample
    distance of less than a set amount of pixels (disregarding missing data)

    arguments

    x		-	numpy array of x positions
    y		-	numpy array of y positions
    time		-	numpy array of EyeTribe timestamps

    keyword arguments

    missing	-	value to be used for missing data (default = 0.0)
    maxdist	-	maximal inter sample distance in pixels (default = 25)
    mindur	-	minimal duration of a fixation in milliseconds; detected
                fixation cadidates will be disregarded if they are below
                this duration (default = 100)

    returns
    Sfix, Efix
                Sfix	-	list of lists, each containing [starttime]
                Efix	-	list of lists, each containing [starttime, endtime, duration, endx, endy]

    author : Edwin Dalmaijer

    Add of pupil dilatation mean by Alphonse Terrier
    """

    # x, y, time = remove_missing(x, y, time, missing)

    # empty list to contain data
    Sfix = []
    Efix = []

    # loop through all coordinates
    si = 0
    fixstart = False
    for i in range(1, len(x)):
        # calculate Euclidean distance from the current fixation coordinate
        # to the next coordinate

        squared_distance = ((x[si] - x[i]) ** 2 + (y[si] - y[i]) ** 2)
        dist = 0.0
        if squared_distance > 0:
            dist = squared_distance ** 0.5
        # check if the next coordinate is below maximal distance
        if dist <= maxdist and not fixstart:
            # start a new fixation
            si = 0 + i
            fixstart = True
            Sfix.append([time[i]])
        elif dist > maxdist and fixstart:
            # end the current fixation
            fixstart = False
            # only store the fixation if the duration is ok
            if time[i - 1] - Sfix[-1][0] >= mindur:
                Efix.append([Sfix[-1][0], time[i - 1], time[i - 1] - Sfix[-1][0], x[si], y[si]])
            # delete the last fixation start if it was too short
            else:
                Sfix.pop(-1)
            si = 0 + i
        elif not fixstart:
            si += 1
    # add last fixation end (we can lose it if dist > maxdist is false for the last point)
    if len(Sfix) > len(Efix):
        Efix.append([Sfix[-1][0], time[len(x) - 1], time[len(x) - 1] - Sfix[-1][0], x[si], y[si]])
    return Sfix, Efix
