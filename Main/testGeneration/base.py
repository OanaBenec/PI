from re import split
from .ranges import IntegerRange, RealRange, CharacterRange, Range, StringRange

class Literal:

    def __init__(self, identifier, dataType, range):
        self.__identifier = identifier
        self.__dataType = dataType
        self.__range = self.__getDataRange(range)

    def getValue(self):
        return self.__range.getValue()

    def __getDataRange(self, dataRange):
        opener = dataRange[0]
        closer = dataRange[-1]
        
        # Remove brackets
        dataRange = dataRange[1:-1]

        if opener == '(' or opener == '[':
            limits = []

            for val in split(r',| ', dataRange):
                if not val:
                        continue
                limits.append(val)

            if self.__dataType == "Integer":
                return IntegerRange(int(limits[0]), int(limits[1]), 
                    (opener == '['), (closer == ']'), None)
            elif self.__dataType == "Real":
                    return RealRange(float(limits[0]), float(limits[1]),
                        (opener == '['), (closer == ']'), None)
            elif self.__dataType == "Character":
                    return CharacterRange(limits[0], limits[1],
                        (opener == '['), (closer == ']'), None)
            else:
                return StringRange(int(limits[0]), int(limits[1]),
                    (opener == '['), (closer == ']'), None)
        else:
            dataRange = split(r',| ', dataRange)
            newRange = []

            if self.__dataType == "Integer":
                for i in range(len(dataRange)):
                    if not dataRange[i]:
                        continue
                    newRange.append(int(dataRange[i]))
                return IntegerRange(0, 0, 0 , 0, newRange)
            elif self.__dataType == "Real":
                for i in range(len(dataRange)):
                    if not dataRange[i]:
                        continue
                    newRange.append(float(dataRange[i]))

                return RealRange(0, 0, 0 , 0, newRange)
            elif self.__dataType == "Character":
                for i in range(len(dataRange)):
                    if not dataRange[i]:
                        continue
                    newRange.append(dataRange[i])

                return CharacterRange(0, 0, 0 , 0, dataRange)
            else:
                return StringRange(0, 0, 0 , 0, dataRange)
            
