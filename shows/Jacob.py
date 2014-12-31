from random import random, randint, choice
from HelperFunctions import *

class SparseSparkRed(object):
    def __init__(self, trimodel, color="red"):
        self.name = "SparseSpark"
        self.tri = trimodel
        self.strobers = []
        self.speed = 0.1
        self.num_strobers_lower = 10
        self.num_strobers_upper = randint(25, 50)
        self.num_strobers = 14
        self.growing = True

    def next_frame(self):
        while (True):
            if len(self.strobers) < self.num_strobers:
                self.strobers.append(self.new_fader())

            for f in self.strobers:
                self.tri.set_cell(f.pos, self.color_for(f))
                f.advance(randint(10, 40))

            yield self.speed

    def new_fader(self):
        return StrobingFader(self, self.tri.get_rand_cell(), 255, 0, 255, False)

    def remove(self, strober):
        self.tri.set_cell(strober.pos, (0, 0, 0))
        self.strobers.remove(strober)
        
        if self.growing == True:
            self.num_strobers += 1
            if self.num_strobers > self.num_strobers_upper:
                self.growing = False
        else:
            self.num_strobers -= 1
            if self.num_strobers < self.num_strobers_lower:
                self.growing = True


    def color_for(self, strober):
       return (strober.value, 0, 0)

class SparseSparkWhite(SparseSparkRed):
    def color_for(self, strober):
        return (strober.value, strober.value, strober.value)


class SparseSparkYellow(SparseSparkRed):
    def color_for(self, strober):
        return (strober.value, strober.value/1.2, 0)

class SparseSparkBlue(SparseSparkRed):
    def color_for(self, strober):
        return (0, 0, strober.value)

class SparseSparkPurple(SparseSparkRed):
    def color_for(self, strober):
        return (strober.value/2.5, 0, strober.value)

class SparseSparkGreen(SparseSparkRed):
    def color_for(self, strober):
        return (0, strober.value, strober.value/6)


class StrobingFader(object):
    def __init__(self, parent, pos, initial=0, lower=0, upper=255, growing=True):
        self.parent = parent
        self.pos = pos
        self.value = initial
        self.growing = growing
        self.lower = lower
        self.upper = upper
        self.cycles = 0
        self.die_at = randint(1, 10)

    def advance(self, difference=10):
        if self.growing:
            self.value += difference
            if self.value > self.upper:
                self.value = self.upper
                self.switch()
        else:
            self.value -= difference
            if self.value < self.lower:
                self.value = self.lower
                self.switch()

    def switch(self):
        self.growing = not self.growing
        self.cycles += 1

        if self.cycles >= self.die_at:
            self.parent.remove(self)