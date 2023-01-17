from random import uniform
from random import randint

class Range:

    def getValue(self):
        """Bae method for concrete ranges

        Returns:
            _type_: A random generated value
        """

class RealRange(Range):

    def __init__(self, min, max, minInclusive, maxInclusive, dataRange):
        self.__min = min
        self.__max = max
        self.__minInclusive = minInclusive
        self.__maxInclusive = maxInclusive
        self.__dataRange = dataRange

    def getValue(self):
        if self.__dataRange:
            pick = round(uniform(0, len(self.__dataRange)))

            return self.__dataRange[pick]
    
        pick = uniform(self.__min, self.__max)

        if not self.__minInclusive:
            while pick == self.__min:
                pick = uniform(self.__min, self.__max)
        elif not self.__maxInclusive:
            while pick == self.__max:
                pick = uniform(self.__min, self.__max)
        
        return pick

class IntegerRange(Range):
    def __init__(self, min, max, minInclusive, maxInclusive, dataRange):
        if not minInclusive:
            min += 1
        if maxInclusive:
            max += 1

        if not dataRange:
            self.__range = range(min, max)
        else:
            self.__range = dataRange

    def getValue(self):
        pick = randint(0, len(self.__range)-1)

        return self.__range[pick]

class CharacterRange(Range):
    def __init__(self, min, max, minInclusive, maxInclusive, dataRange):
        if not minInclusive:
            min = chr(ord(min) + 1) 
        if maxInclusive:
            max = chr(ord(max) + 1)

        self.__range = dataRange

        if not dataRange:
            self.__range = []
            for i in range(0, ord(max) - ord(min)):
                self.__range.append(chr(ord(min) + i))

    def getValue(self):
        pick = randint(0, len(self.__range)-1)

        return self.__range[pick]

class StringRange(Range):
    def __init__(self, min, max, minInclusive, maxInclusive, dataRange):
        if not minInclusive:
            min += 1
        if maxInclusive:
            max += 1

        if not dataRange:
            self.__rangeType = "Integer"
            self.__range = range(min, max)
        else:
            self.__rangeType = "String"
            self.__range = dataRange

    def getValue(self):
        pick = randint(0, len(self.__range)-1)

        if self.__rangeType == "String":
            return self.__range[pick]

        random_string = ""
        for i in range(self.__range[pick]):
            flip_bit = randint(0, 1)
            random_string += chr(randint(97, 122) - 32 * flip_bit)

        return random_string