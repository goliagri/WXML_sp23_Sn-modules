from sage.all import *
import numpy as np

from graph_decomp import get_shape_and_Quot, perm_module_decom
'''
Indexing Note: We need to keep the indexes of graphs, permutations, and python lists consistent. We fix graph vertice and permutation indices as starting at 1 and python lists as starting at 0. Keep this in mind when converting between them (using permutation elements to index a list for example)
''' 
def main():
    #define X for testing here
    X=Graph() 
    X.add_edges([(1,2), (3,4), (5,6), (6,7), (8,9),(9,10)])
    #X.add_edges([(1,2),(2,3),(1,3),(4,5),(5,6),(4,6), (7,8),(9,10)])
    #X.add_edges([(1,2),(3,4),(5,6),(6,7)])
    #X.add_edges([(1,2),(2,3),(4,5),(5,6)])
    #print(X.automorphism_group().list())

    #spc = SymmetricGroupRepresentation([3,1], 'specht')
    #print(spc)
    
    #shape = [2,1]
    #content = [1,1,1]
    #print(symmetrica.kostka_number(shape, content))
    #print(symmetrica.kostka_tab(shape, content))

    #given a graph write it in terms of a quotient of a symmetric group





    shape, equiv_classes, quot_group = get_shape_and_Quot(X)
    #shape = [1,1,1]
    M_lam_decomp = perm_module_decom(shape)
    print('-----------------')
    print(X)
    print('Graph automorphism group: ' + str(X.automorphism_group()))
    print('-----------------')
    print('graph shape: ' + str(shape))
    print('equivalence classes making shape: ' + str(equiv_classes))
    print('G (acting on shape permutation module): ' + str(quot_group))
    print('-----------------')
    print('dominating partitions: ' + str(M_lam_decomp[0]))
    print('corresponding kostka numbers: ' + str(M_lam_decomp[1]))
    #print(M_lam_decomp[2])
    print('-----------------')
    print('This gives the transformation: M^X  -> M^(shape)/G')
    print('M^X  -> M^({})/{}'.format(shape, quot_group))


if __name__ == '__main__':
    main()