from sage.all import *
import numpy as np

# given a graph X, return the shape lambda which parameterzies the permutation module and
# the group G acting on rows of the permutation module such that we have M^X -> M^lambda/G
def get_shape_and_Quot(X):
    aut = X.automorphism_group()
    X_size = len(X.vertices())
    two_cycles = list(filter(lambda perm: perm.cycle_type(singletons=False) == [2], aut.list()))
    #we use all 2-cycles to construct the equivalence classes determining the shape
    two_cycle_sets = [set(two_cycle.cycle_tuples()[0]) for two_cycle in two_cycles]
    equiv_classes = []
    #invariant: equiv classes mutually disjoint sets, each el is subset of some true equivalence class, given by first n 2-cycles.
    for cycle in two_cycle_sets:
        found_class = False
        for i in range(len(equiv_classes)):
            if len(cycle.intersection(equiv_classes[i])) > 0:
                if found_class == False:
                    #first class which shares an element, add other cycle element to
                    class_idx = i
                    equiv_classes[class_idx] = cycle.union(equiv_classes[class_idx])
                    found_class = True
                else:
                    #If matches a second class, combine with first matching class
                    equiv_classes[i] = equiv_classes[i].union(equiv_classes[class_idx])
                    #since we only consider 2-cycles, we can break after finding 2nd match
                    equiv_classes.remove(i) 
                    break 
        #if disjoint from all existing classes, create a new one
        if not found_class:
            equiv_classes.append(cycle)
    #lastly add singlular elements, elements not in any 2-cycle
    for i in X.vertices():
        if not np.any([i in equiv_class for equiv_class in equiv_classes]):
            equiv_classes.append({i})
    
    equiv_classes.sort(reverse=True, key = lambda s : len(s))
    shape = [len(equiv_class) for equiv_class in equiv_classes]
    
    #print(equiv_classes)
    #For each pair of equal length equivalence classes, we choose an arbitrary representative of both and check if a map from one to the other is in aut(x)
    quot_els = []
    augmented_representative_maps = []
    for c1idx, c1 in enumerate(equiv_classes):
        #our graphs and permutations are 1-base indexed
        c1idx += 1
        for c2idx, c2 in enumerate(equiv_classes[c1idx:]):
            c2idx += 1 + c1idx
            #picks out all pairs of equivalence classes with identical lengths
            if len(c1) != len(c2):
                break
            #pick an arbitrary order on the sets
            c1 = list(c1)
            c2 = list(c2)
            #create bijection taking c1 -> c2, c2 -> c1 fixing everything outside c1 \cup c2
            #Permutation expects vals > 0, so have to shift indices by 1
            one_line_perm = list(range(1,X_size+1))
            for i in range(len(c1)): 
                one_line_perm[c1[i]-1] = c2[i]
                one_line_perm[c2[i]-1] = c1[i]
            #print(one_line_perm)
            #the idea is that we create (1) a permutation from a representative of an equivalence class to another
            #(2) a cycle from the index of the equivalence class to the other, displaced so that the values don't overlap with (1)
            #we then combine (1) and (2) into one permutation, essentially with an active component and a label component
            #later we decompose again and use the (1) component to check if in the automorphism group, and if so we add (2) to result
            c1_c2_representative_map = Permutation(one_line_perm)
            augment_perm = Permutation('({},{})'.format(X_size + c1idx, X_size + c2idx))
            augmented_c1_c2_representative_map = Permutation.left_action_product(c1_c2_representative_map, augment_perm)
            augmented_representative_maps.append(augmented_c1_c2_representative_map)
    #print(augmented_representative_maps)

    #generate permutation group from augmented representative element bijections
    equivalence_class_representatives = PermutationGroup(augmented_representative_maps)
    for perm_on_equiv_class_reps in equivalence_class_representatives.list():
        #list of tuples representing cycles
        cycle_tuples = perm_on_equiv_class_reps.cycle_tuples()
        #seperate representative and label components
        rep_tuples = list(filter(lambda tup : tup[0] <= X_size , cycle_tuples))
        aug_tuples = list(filter(lambda tup : tup[0] > X_size , cycle_tuples))
        #shift labels back to original
        aug_tuples = [tuple([el-X_size for el in tup]) for tup in aug_tuples]

        #Permutation constructor requires cycle notation to be given as a string
        rep_perm_str = ''
        for tup in rep_tuples:
            rep_perm_str += str(tup)
        rep_perm = Permutation(rep_perm_str)

        aug_perm_str = ''
        for tup in aug_tuples:
            aug_perm_str += str(tup)
        aug_perm = Permutation(aug_perm_str)
        #print('--------------------')
        #print(perm_on_equiv_class_reps)
        #print(rep_perm)
        #print(aug_perm)

        #note: I don't entirely understand when we have to do this perm -> perm group el conversion
        #if we don't do it here, the code seems to work unless X has >=10 vertices, then it breaks.
        if rep_perm.to_permutation_group_element() in aut:
            quot_els.append(aug_perm)

            #print('!?!')
            #print(rep_perm)
            #print(aug_perm)
            

    #quot_group acts on the elements of the equivalences classes indexed by the given order
    #note: permutations are defined base 1, python lists are defined base 0, need to keep that in mind.
    quot_group = PermutationGroup(quot_els)

    #debugging outputs
    #print(quot_group)
    #print(two_cycles)
    #print(two_cycle_sets)

    #
    #print(aut.list())
    #print(type(aut.list()[1]))
    #print(aut.list()[1].cycle_type(singletons=False))

    return shape, equiv_classes, quot_group

#module given a lambda for some M^lambda, computes all dominating partitions, kostka numbers, and semistandard tableuax per dominating partition
def perm_module_decom(lam):
    all_partitions = Partitions(sum(lam)) #all partitions of whatever integer lambda partitions
    shapes = list(filter(lambda p : Partition(p).dominates(lam), all_partitions)) #we keep only partitions which dominate lambda
    #shapes = Partition(lam).dominated_partitions() #is there a simpler way to get dominating partitions?

    #use symmetrica library to compute kostka number and semi-standard tableaux (kostka tableaux?)
    kostka_nums = [symmetrica.kostka_number(shape, lam) for shape in shapes]
    semistandard_tabs = [symmetrica.kostka_tab(shape, lam) for shape in shapes]
    return shapes, kostka_nums, semistandard_tabs

#Given a semi-standard tableaux (Kostka_tab), we produce its orbit under G
def get_orbit_tableauxs(tab, G):
    res = set()
    for perm in G.list():
        res.add(tab.symmetric_group_action_on_entries(Permutation(perm)))
    #print('-----------------------')
    #print(len(G.list()))
    #print(len(res))
    #print(res)
    #print('-----------------------')
    return res

#Given a not-necesarily semistandard tableaux Tab, decompose it as sum of semistandard tableaux
#See brosh Thesis pgs 179-184
#Briefly: we find all semistandard tableaux we can get from first permuting rows, then columns.
def decompose_tableau_into_sum_of_semistandard(Tab):
    max_content = max(Tab.entries())
    Viable_partials = [Tab]
    decomp = {}
    while viable_partials != []:
        new_viable_partials = []
        for i in range(1, max_content):
            new_viable_partials = gen_viable_partials(viable_partials, i)

            viable_partials = new_viable_partials
            new_viable_partials = []
    return 

def gen_viable_partials(viable_partials, i):
    new_viable_partials = []
    for partial_hom in viable_partials: 
        
    
    return None

def col_sorted_and_restricted_to_i_is_semistandard(tab, i):

    return False

#X is the graph defining a graph module M^X
def decompose_graph_module(X):
    #eventually this method will run the full pipeline
    return None
    

if __name__ == '__main__':
    import sage_testing
    sage_testing.main()