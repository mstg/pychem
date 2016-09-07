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
    def __init__(self, should_from, should_to, needed):
        self.should_from = should_from
        self.should_to = should_to
        self.symbol = "{0}{1}".format(should_from.symbol, should_to.symbol)
        self.name = self.symbol

        needed_c = needed
        removed = 0
        after_should_from = should_from.shell
        after_should_to = None

        compeln = should_from.comp_eln(should_to)
        wname = compeln["weakest"].name
        sname = compeln["strongest"].name
        diff = compeln["elndiff"]

        wval = len(compeln["weakest"].valence())
        sval = len(compeln["strongest"].valence())
        vlist = [wval, sval]

        cl = min(vlist, key=lambda x:abs(x-8))
        cl_ch = {wval: compeln["weakest"], sval: compeln["strongest"]}

        should_to = cl_ch[cl]
        vlist.remove(cl)
        should_from = cl_ch[vlist[-1]]

        ionic_min = 2
        polar_covalent_min = 0.4
        polar_covalent_max = 2
        covalent_max = 0.4

        self.j = {}
        self.j[should_from.name] = {
            "symbol": should_from.symbol,
            "shell": should_from.shell,
            "number": should_from.number,
        }

        if should_from.name != should_to.name:
            self.j[should_to.name] = {
                "symbol": should_to.symbol,
                "shell": should_to.shell,
                "number": should_to.number,
            }

        temp_should_from = Atom(should_from.number - needed, "", self.symbol, 0)
        after_should_from = temp_should_from.shell

        temp_should_to = Atom(should_to.number + needed, "", self.symbol, 0)
        after_should_to = temp_should_to.shell

        if diff == 0:
            self.j[should_from.name]["gets"] = 0
            self.j[should_from.name]["gets_from"] = wname
            self.j[should_from.name]["priority"] = 0
            self.j[should_from.name]["after"] = should_from.shell
        elif diff < covalent_max:
            self.j[should_to.name]["gets"] = needed
            self.j[should_to.name]["gets_from"] = wname
            self.j[should_to.name]["priority"] = 0

            self.j[should_from.name]["gets"] = needed
            self.j[should_from.name]["gets_from"] = sname
            self.j[should_from.name]["priority"] = 0
        elif diff > polar_covalent_min and diff < polar_covalent_max:
            temp_should_from = Atom(should_from.number + needed, "", self.symbol, 0)
            after_should_from = temp_should_from.shell

            temp_should_to = Atom(should_to.number - needed, "", self.symbol, 0)
            after_should_to = temp_should_to.shell

            self.j[should_to.name]["gets"] = needed
            self.j[should_to.name]["gets_from"] = should_from.name
            self.j[should_to.name]["priority"] = 0.5

            self.j[should_from.name]["gets"] = needed
            self.j[should_from.name]["gets_from"] = should_to.name
            self.j[should_from.name]["priority"] = 0.5
        elif diff > ionic_min:
            self.j[should_to.name]["gets"] = needed
            self.j[should_to.name]["gets_from"] = should_from.name
            self.j[should_to.name]["priority"] = 1

            self.j[should_from.name]["gives"] = needed
            self.j[should_from.name]["gives_to"] = should_to.name
            self.j[should_from.name]["priority"] = 0

        self.j[should_from.name]["after"] = after_should_from

        if should_from.name != should_to.name:
            self.j[should_to.name]["after"] = after_should_to

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
