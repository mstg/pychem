from libchem import Atom, CombineAtom

import sys
import csv

def print_atom(a):
    print "---"
    print "{0} - {1} - {2}".format(a.name, a.symbol, a.number)
    print a.shell
    print "Valence electrons: {0}".format(len(a.valence()))
    print "---"

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
                    a_ = {"number": int(row[0]), "symbol": row[1], "name": row[2].strip()}

                if argv[2] == ent:
                    a2_ = {"number": int(row[0]), "symbol": row[1], "name": row[2].strip()}

    if not a_:
        print "Atom with (number/symbol/name) {0} not found!".format(argv[1])
        sys.exit(-1)

    if not a2_:
        print "Atom with (number/symbol/name) {0} not found!".format(argv[2])
        sys.exit(-1)

    a = Atom(a_["number"], a_["name"], a_["symbol"])
    print_atom(a)

    a2 = Atom(a2_["number"], a2_["name"], a2_["symbol"])
    print_atom(a2)

    new_a = CombineAtom(a, a2)
    print_atom(new_a.new_atom)
