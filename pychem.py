from libchem import Atom

if __name__ == "__main__":
    a = Atom(12, "Magnesium", "Mg")
    v = a.valence()
    print a.octet_accuracy(v)
