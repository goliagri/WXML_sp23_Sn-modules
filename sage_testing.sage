from sage.all import *

X=Graph() 
X.add_edges([(0,1),(0,2),(3,4)])
print(X.automorphism_group().list())

spc = SymmetricGroupRepresentation([3,1], 'specht')
print(spc)

X.automorphism_group()
shape = [2,1]
content = [1,1,1]
print(symmetrica.kostka_number(shape, content))
print(symmetrica.kostka_tab(shape, content))

#given a graph write it in terms of a quotient of a symmetric group
def get_shape_and_Quot(X):
    aut = X.automorphism_group()
    two_cycles = list(filter(lambda perm: perm.cycle_type(singletons=False) == [2], aut.list()))
    two_cycle_sets = [set(two_cycle.cycle_tuples()[0]) for two_cycle in two_cycles]
    equiv_classes = []
    for cycle in two_cycle_sets:
        intersections = 
    print(two_cycles)
    print(two_cycle_sets)

    print(aut)
    print(aut.list())
    print(type(aut.list()[1]))
    print(aut.list()[1].cycle_type(singletons=False))



#module given a lambda for some M^lambda, computes all dominating partitions, kostka numbers, and semistandard tableuax per dominating partition
def perm_module_decom(lam):
    all_partitions = Partitions(sum(lam)) #all partitions of whatever integer lambda partitions
    shapes = list(filter(lambda p : Partition(p).dominates(lam), all_partitions)) #we keep only partitions which dominate lambda
    #shapes = Partition(lam).dominated_partitions() #is there a simpler way to get dominating partitions?

    #use symmetrica library to compute kostka number and semi-standard tableaux (kostka tableaux?)
    kostka_nums = [symmetrica.kostka_number(shape, lam) for shape in shapes]
    semistandard_tabs = [symmetrica.kostka_tab(shape, lam) for shape in shapes]
    return shapes, kostka_nums, semistandard_tabs


lam = [1,1,1]
M_lam_decomp = perm_module_decom(lam)
print('-----------------')
print(M_lam_decomp[0])
print(M_lam_decomp[1])
print(M_lam_decomp[2])
print('-----------------')

get_shape_and_Quot(X)

