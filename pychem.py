from libchem import Atom, CombineAtom

import sys
import csv
import json

def print_atom(a):
    print a.transfer_json()

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
    print_atom(new_a.new_atom)
