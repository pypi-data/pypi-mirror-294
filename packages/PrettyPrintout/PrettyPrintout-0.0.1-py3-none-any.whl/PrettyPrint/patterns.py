import sys

class ProgressBar:
    '''
    The ProgressBar class, meant to be init before a finite loop with known iteration count,
    to show the progress of the loop
    Consider that there should be no other prints during the use of this pattern, because that will fuck up the print with newlines
    '''
    def __init__(self, underlying_iterable, bins=10, symbol='='):
        # dtype checking lessgo
        try:
            iter(underlying_iterable)
        except TypeError:
            raise TypeError('Progress Bar expects an iterable but got {} instead'.format(type(underlying_iterable)))
        if type(bins) is not int:
            raise TypeError('bins must be a positive integer between 1 and 100')
        if bins <= 0:
            raise ValueError('bins must be a positive integer between 1 and 100')
        if bins > 100:
            raise ValueError('bins must be a positive integer between 1 and 100')
        if type(symbol) is not str:
            raise TypeError('symbol must be a char but got {}'.format(type(symbol)))

        # properties
        self.underlying_iterable = iter(underlying_iterable) # get the iterator of the underlying itrable
        self._length = sum(1 for e in underlying_iterable) # compute the length of the underlying iterable
        self._step = round(self._length/bins) # compute the stepsize (=amount of iterations to fill one bin
        self._sym = symbol # store the symbol with which the bar is printed
        self._index = 0 # count iterations for each step
        self._progress = 1 # track progress
        self._bins = bins # the number of bins
        self._perc_increment = 100/bins # the percentual increments for every bin
        self._formatter = "[%-"+str(bins)+"s] %d%%" # the formatter string to print each update
        # another error handling
        if bins > self._length:
            raise ValueError('the bar cant have more bins than iterations in the underlying iterable')

    def __next__(self):
        self._increment()
        return self.underlying_iterable.__next__()

    def __iter__(self):
        return self

    def __len__(self):
        return self.underlying_iterable.__len__()

    def _increment(self):
        '''
        increments the index, if step size is reached updates the printout and resets index
        :return:
        '''
        self._index += 1
        if self._index == self._step:
            self._update()
            self._index = 0

    def _update(self):
        '''
        Adds a tick to the progress bar. will simply stop updating if the loop goes out of bounds of the previously stated max iteration count
        :return:
        '''
        if self._progress <= self._bins:
            sys.stdout.write('\r') # resets the cursor
            sys.stdout.write((self._formatter) % (self._sym * self._progress, self._perc_increment * self._progress)) # writes the formatted string
            sys.stdout.flush() # flush buffer to print text immediately
            self._progress += 1

class LoadingDots:
    def __init__(self):
        return

class LoadingRotate:
    def __init__(self):
        return

class Table:
    def __init__(self):
        return

class Separator:
    def __init__(self):
        return

