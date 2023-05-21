import enum
import typing


class ID(enum.Enum):
    ISDICT = 0


def dict2list(var: dict[typing.Any, typing.Any]):
    to: list[typing.Any] = []
    to.append(ID.ISDICT)
    for key, value in var.items():
        to.append(key)
        if isinstance(value, dict):
            to.append(dict2list(value))
        else:
            to.append(value)
    return to


def list2dict(value: list[typing.Any]):
    if value[0] != ID.ISDICT:
        raise ValueError("Unknow value!")
    to: dict[typing.Any, typing.Any] = {}
    for i in range(1, len(value), 2):
        if isinstance(value[i+1], list):
            if value[i+1][0] == ID.ISDICT:
                to[value[i]] = list2dict(value[i+1])
            else:
                to[value[i]] = value[i+1]
        else:
            to[value[i]] = value[i+1]
    return to

def list2table(value: list[typing.Any]):
    if value[0] != ID.ISDICT:
        raise ValueError("Unknow value!")
    value_ = value
    for i in range(1,len(value_),2):
        if isinstance(value_[i+1],list) and value_[i+1][0] == ID.ISDICT:
            value_[i+1] = list2table(value_[i+1])
    return Table(value_)


class Table(object):
    def __init__(self, value: dict[typing.Any, typing.Any] | list[typing.Any] = {}) -> None:
        if isinstance(value, dict):
            self.__table = dict2list(value)
        else:
            if value[0] == ID.ISDICT and len(value) % 2 == 1:
                self.__table = value
            else:
                raise ValueError("Unknow value!")

    def __getitem__(self, key: typing.Any):
        for i in range(1, len(self.__table), 2):
            if key == self.__table[i]:
                return self.__table[i+1]
        else:
            raise KeyError(f"Key \"{key}\" isn't in this table.")

    def __setitem__(self, key: typing.Any, value: typing.Any):
        if key in self.__table:
            for i in range(1, len(self.__table), 2):
                if key == self.__table[i]:
                    self.__table[i+1] = value
                    break
        else:
            self.__table.append(key)
            self.__table.append(value)

    def __delitem__(self, key: typing.Any):
        if not key in self.__table:
            raise KeyError(f"Key \"{key}\" isn't in this table.")
        else:
            for i in range(1, len(self.__table), 2):
                if key == self.__table[i]:
                    self.__table = self.__table[:i] + self.__table[i+2:]
                    break

    def __len__(self):
        return int((len(self.__table) - 1) / 2)

    def __str__(self):
        return str(self.toDict())

    def __repr__(self) -> str:
        return f"Table({self.toDict()})"

    def toDict(self):
        return list2dict(self.__table)

    def toList(self):
        return self.__table

    def toTuple(self):
        return tuple(self.__table)

    def items(self):
        items: list[tuple[typing.Any, typing.Any]] = []
        for i in range(1, len(self.__table), 2):
            items.append((self.__table[i], self.__table[i+1]))
        return tuple(items)

    def clear(self):
        self.__table = [ID.ISDICT]
