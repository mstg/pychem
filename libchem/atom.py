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
        for x in range(1, self.number+1):
            space = calc_2n2(in_shell)

            if not shell:
                shell["space"] = space
                shell["electrons"] = []

            if parsed_electrons < space:
                shell["electrons"].append(x)
                parsed_electrons += 1
            else:
                self.shell.append(shell)

                in_shell += 1
                space = calc_2n2(in_shell)

                shell = {}
                shell["space"] = space
                shell["electrons"] = []

                shell["electrons"].append(x)
                parsed_electrons = 1

        self.shell.append(shell)

    def valence(self):
        return self.shell[-1]["electrons"]

    def octet_accuracy(self, shell):
        return (len(shell["electrons"]) / shell["space"])

    def needed_should(self, valence):
        return True if len(valence) < 8 else False

    def needed(self, valence):
        return 8 - len(valence)

class CombineAtom:
    def __init__(self, a, a2):
        self.atom1 = a
        self.atom2 = a2
        v = a.valence()
        v2 = a2.valence()

        a_te = a if a.needed_should(v) else a2
        a_to = a2 if a.needed_should(v) else a

        if a.needed_should(a_te.valence()):
            transfer_el = a.needed(a_te.valence())

            new_a = Atom(a_to.number + len(a_te.valence()), "Combined Atom", "{0}{1}".format(a_to.symbol, a_te.symbol))
            self.new_atom = new_a
        elif self.share(a_te, a_to):
            print "Share"

    def share(self, valence, valence2):
        return True if len(valence) == len(valence2) else False
