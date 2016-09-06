from __future__ import division
from calc import calc_2n2

import json

class Atom:
    def __init__(self, number, name, symbol, eln):
        self.number = number
        self.name = name
        self.symbol = symbol
        self.eln = float(eln)

        self.shell = []

        in_shell = 1
        shell = {}
        shell["electrons"] = []
        for x in range(1, self.number+1):
            space = calc_2n2(in_shell)
            shell["space"] = space

            if len(shell["electrons"]) < space:
                shell["electrons"].append(x)
            else:
                self.shell.append(shell)

                in_shell += 1
                space = calc_2n2(in_shell)

                shell = {}
                shell["space"] = space
                shell["electrons"] = []

                shell["electrons"].append(x)

        self.shell.append(shell)

    def valence(self):
        return self.shell[-1]["electrons"]

    def octet_accuracy(self, shell):
        return (len(shell["electrons"]) / shell["space"])

    # Deprecated
    def needed_should(self, valence):
        return True if len(valence) < 8 else False

    def comp_eln(self, a):
        t = {self.eln: self, a.eln: a}
        s = [self.eln, a.eln]

        e1 = max(s)
        e2 = min(s)

        p = e1 - e2

        return {"strongest": t[e1], "weakest": t[e2], "elndiff": p}


    def needed(self, a):
        compeln = self.comp_eln(a)
        wname = compeln["weakest"].name
        sname = compeln["strongest"].name
        diff = compeln["elndiff"]

        # Temporary
        return 8 - len(a.valence())

    def transfer_json(self):
        pass

class AtomBonding:
    def __init__(self, from_a, to_a, needed):
        self.from_a = from_a
        self.to_a = to_a
        self.symbol = "{0}{1}".format(from_a.symbol, to_a.symbol)
        self.name = self.symbol

        needed_c = needed
        removed = 0
        after_from_a = from_a.shell
        after_to_a = None

        compeln = from_a.comp_eln(to_a)
        wname = compeln["weakest"].name
        sname = compeln["strongest"].name
        diff = compeln["elndiff"]

        ionic_min = 2
        polar_covalent_min = 0.4
        polar_covalent_max = 2
        covalent_max = 0.4

        self.j = {}
        self.j[from_a.name] = {
            "symbol": from_a.symbol,
            "shell": from_a.shell,
            "number": from_a.number,
        }

        if from_a.name != to_a.name:
            self.j[to_a.name] = {
                "symbol": to_a.symbol,
                "shell": to_a.shell,
                "number": to_a.number,
            }

        temp_from_a = Atom(from_a.number - needed, "", self.symbol, 0)
        after_from_a = temp_from_a.shell

        temp_to_a = Atom(to_a.number + needed, "", self.symbol, 0)
        after_to_a = temp_to_a.shell

        if diff == 0:
            self.j[from_a.name]["gets"] = 0
            self.j[from_a.name]["gets_from"] = wname
            self.j[from_a.name]["priority"] = 0
            self.j[from_a.name]["after"] = from_a.shell
        elif diff < covalent_max:
            self.j[to_a.name]["gets"] = needed
            self.j[to_a.name]["gets_from"] = wname
            self.j[to_a.name]["priority"] = 0

            self.j[from_a.name]["gets"] = needed
            self.j[from_a.name]["gets_from"] = sname
            self.j[from_a.name]["priority"] = 0
        elif diff > polar_covalent_min and diff < polar_covalent_max:
            temp_from_a = Atom(from_a.number + needed, "", self.symbol, 0)
            after_from_a = temp_from_a.shell

            temp_to_a = Atom(to_a.number - needed, "", self.symbol, 0)
            after_to_a = temp_to_a.shell

            self.j[to_a.name]["gets"] = needed
            self.j[to_a.name]["gets_from"] = from_a.name
            self.j[to_a.name]["priority"] = 0.5

            self.j[from_a.name]["gets"] = needed
            self.j[from_a.name]["gets_from"] = to_a.name
            self.j[from_a.name]["priority"] = 0.5
        elif diff > ionic_min:
            self.j[to_a.name]["gets"] = needed
            self.j[to_a.name]["gets_from"] = from_a.name
            self.j[to_a.name]["priority"] = 1

            self.j[from_a.name]["gives"] = needed
            self.j[from_a.name]["gives_to"] = to_a.name
            self.j[from_a.name]["priority"] = 0

        self.j[from_a.name]["after"] = after_from_a

        if from_a.name != to_a.name:
            self.j[to_a.name]["after"] = after_to_a

    def transfer_json(self):
        return json.dumps(self.j, indent=4, sort_keys=True)

class CombineAtom:
    def __init__(self, a, a2):
        self.atom1 = a
        self.atom2 = a2
        v = a.valence()
        v2 = a2.valence()

        compeln = a.comp_eln(a2)
        a_te = compeln["weakest"]
        a_to = compeln["strongest"]

        transfer_el = a_te.needed(a_to)

        new_a = AtomBonding(a_to, a_te, transfer_el)
        self.new_atom = new_a 

    def share(self, valence, valence2):
        return True if len(valence) == len(valence2) else False
