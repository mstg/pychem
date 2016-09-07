from libchem import Atom, CombineAtom

import sys
import csv
import json

def print_bonded_atom(a):
    l = json.loads(a.transfer_json())
    g = "gets"
    s = ""
    amount = 0
    ab = "from"
    rem1 = 0
    rem2 = 0

    p1 = l[a.should_from.name]["priority"]
    p2 = l[a.should_to.name]["priority"]

    if "gets_from" in l[a.should_from.name]:
        ss = a.should_from.name
        amount = l[a.should_from.name]["gets"]
    
    if "gets_from" in l[a.should_to.name]:
        ss = a.should_to.name
        amount = l[a.should_to.name]["gets"]

    if p1 == 0.5 or p2 == 0.5:
        g = "shares/gives"
        s = " but the electrons is more drawn to {0}".format(ss)
        ab = "with"

        rem2 = 8 - len(a.after_from["shell"][-1]["electrons"])
        rem1 = 8 - len(a.after_to["shell"][-1]["electrons"])
    elif p1 == 0 and p2 == 0:
        g = "shares"
        ab = "with"

    print "---"
    print a.should_to.name
    print "Valence electrons: {0}".format(len(a.should_to.valence()))
    print "Total electrons: {0}".format(a.should_to.total)
    print "Shell: {0}".format(a.should_to.shell)
    print ""
    print a.should_from.name
    print "Valence electrons: {0}".format(len(a.should_from.valence()))
    print "Total electrons: {0}".format(a.should_from.total)
    print "Shell: {0}".format(a.should_from.shell)
    print "---"
    print ""

    print g

    print ""
    print "After:"
    print "---"
    print a.should_to.name
    print "Valence electrons: {0}".format(len(a.after_to["shell"][-1]["electrons"]))
    print "Total electrons: {0}".format(a.after_to["total"])
    print "Shell: {0}".format(a.after_to["shell"])
    print ""
    print a.should_from.name
    print "Valence electrons: {0}".format(len(a.after_from["shell"][-1]["electrons"]))
    print "Total electrons: {0}".format(a.after_from["total"])
    print "Shell: {0}".format(a.after_from["shell"])
    print "---"
    print ""

    if rem1 > 0 or rem2 > 0:
        print "The remaining {0}/{1} electrons may be shared between the atoms".format(rem1, rem2)

    pass

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) < 3:
        print "[USAGE] {0} atom1 atom2".format(argv[0])
        sys.exit(-1)

    a_ = {}
    a2_ = {}

    with open("data/pt.csv") as pt:
        reader = csv.reader(pt, delimiter=",")
        for row in reader:
            for entry in row:
                ent = entry.strip()
                if argv[1] == ent:
                    a_ = {"number": int(row[2]), "symbol": row[1].strip(), "name": row[0].strip(), "eln": row[15]}

                if argv[2] == ent:
                    a2_ = {"number": int(row[2]), "symbol": row[1].strip(), "name": row[0].strip(), "eln": row[15]}

    if not a_:
        print "Atom with (number/symbol/name) {0} not found!".format(argv[1])
        sys.exit(-1)

    if not a2_:
        print "Atom with (number/symbol/name) {0} not found!".format(argv[2])
        sys.exit(-1)

    a = Atom(a_["number"], a_["name"], a_["symbol"], a_["eln"])
    a2 = Atom(a2_["number"], a2_["name"], a2_["symbol"], a2_["eln"])

    new_a = CombineAtom(a, a2)
    print_bonded_atom(new_a.new_atom)
