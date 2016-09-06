from __future__ import division
from calc import calc_2n2

class Atom:
    def __init__(self, number, name, symbol):
        self.number = number
        self.name = name
        self.symbol = symbol

        self.shell = []

        in_shell = 1
        parsed_electrons = 0
        shell = {}
        for x in range(1, number+1):
            space = calc_2n2(in_shell)

            if not shell:
                shell["space"] = space
                shell["electrons"] = []

            if parsed_electrons < space:
                shell["electrons"].append(x)
                parsed_electrons += 1
            else:
                self.shell.append(shell)
                shell = {}
                shell["space"] = space
                shell["electrons"] = []
                in_shell += 1

                shell["electrons"].append(x)
                parsed_electrons = 1

        self.shell.append(shell)

    def valence(self):
        return self.shell[-1]

    def octet_accuracy(self, shell):
        return (len(shell["electrons"]) / shell["space"])
