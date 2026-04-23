'''
Based on mesograph.py Created on 9 juin 2016

@author: jojo, zarpe
'''
#import numpy as np
#import scipy.spatial.distance as dist
import networkx as nx
#import community as comu
#from python_tools import *
# 
#
#from operator import itemgetter, attrgetter

class NESSGraph(nx.DiGraph):
    """
    Un graphe visant à représenter les 'non-equilibrium steady states'.
    """

    def to_graphviz(self):

        return nx.nx_agraph.to_agraph(self)

#    def is_cycle(self, cycle):
#        """
#        Test pour savoir si un graphe dirigé est un cycle ou non.
#        
#        cycle : un graphe dirigé (type : nx.DiGraphe) 
#        
#        return bool
#        """
#        e = cycle.edges()
#        cope = cycle.edges()
#        
#        for tup in e:
#            
#            trouver = 0
#            
#            for put in cope:
#                
#                if(tup[1]==put[0]):
#                    trouver=1
#                    break
#                
#            if(trouver!=1):
#                return False
#            
#        return True
#
#    def total_flux(self):
#        """
#        Renvoie la somme de tous les fluxs présent dans le graph original
#        
#        return float64 (?)
#        """
#        return np.sum(nx.to_numpy_matrix(self, weight='flux'))
#
#    def spatial_extension(self):
#        """
#        calcul les extensions spatiales maximales
#        
#        return float64 (?)
#        """
#        coord = np.array([n.coord for n in self.nodes()])
#        Y = dist.pdist(coord, 'euclidean')
#        return np.max(Y) # maxex
#
#
#class MesoGraph(GraphNESS):
#    """
#    Un graphe de meso-états (centroïdes)
#    """
#    
#    def remove_trivial(self):
#        """
#        Elimine tous les cycles triviaux du graphe en enlevant l'arête de plus faible poids.
#        """
#        for edge in self.edges():
#    
#            if (self.has_edge(edge[0], edge[1]) and self.has_edge(edge[1], edge[0])):
#                diff = self[edge[0]][edge[1]]['flux'] - self[edge[1]][edge[0]]['flux']
#
#                if (diff > 0): 
#                    self[edge[0]][edge[1]]['flux'] = diff
#                    self.remove_edge(edge[1], edge[0])
#
#                elif (diff < 0): 
#                    self[edge[1]][edge[0]]['flux'] = -diff
#                    self.remove_edge(edge[0], edge[1])
#
#                elif (diff == 0): # FIXME: à tester...
#                        
#                    if (edge[0] != edge[1]): 
#                        self.remove_edge(edge[1], edge[0])
#                        self.remove_edge(edge[0], edge[1])
#    
#                    elif (edge[0] == edge[1]):
#                        self.remove_edge(edge[1], edge[0])
#    
#    def get_cycles(self):
#        """
#        Renvoie la liste de tous les cycles trouvé à partir du maximum spanning tree. Un cycle
#        est ajouté s'il est trouvé sur le maximum spanning tree après avoir ajouté une seule 
#        arête n'appartenant pas à l'arbre
#        
#        return cycle
#        """
#        stree = nx.maximum_spanning_arborescence(self)
#        #try:
#        #    stree = nx.maximum_spanning_arborescence(self)
#                
#        #except nx.NetworkXException:#si l'on a pas d'arbre, la copie sera impossible
#            # raise 'No tree found'  # FIXME: check this...
#            # or return None or something to be used in the outer program
#            #print("pas d'arbre")
#            #return 0
#            
#        gdiff = nx.difference(self, stree)
#        all_cycles = []
#            
#        for nf, nt in gdiff.edges_iter():
#             
#            stree.add_edge(nf, nt)
#
#            try:
#                all_cycles.append(nx.find_cycle(stree, source=nf))
#                    
#            except nx.NetworkXNoCycle:
#                pass
#
#            stree.remove_edge(nf, nt)
#            
#        return all_cycles # as list of lists of edges
#
#class Cycle(GraphNESS):
#    """
#    Un graphe de cycle. Il faut rajouter un test pour savoir s'il s'agit bien d'un cycle lors de l'initialisation.
#    En attendant, utilisation user-friendly requise
#    """
#
#    def __init__(self, edges, graph):
#        # FIXME: check that is is really a cycle...
#        """
#        Initialise le cycle à partir d'un graphe et d'une liste d'arête. Pour chacune des arêtes dans la liste edge, 
#        récupère les données de cette arête dans le graphe principal, et construit une arête pour le cycle.
#        
#        edge : liste des arêtes [type : meso-state] servant à construire le cycle (type : list)
#        graph : graphe à partir duquel est construit le cycle 
#        """
##       http://stackoverflow.com/questions/16150557/networkxcreating-a-subgraph-induced-from-edges
#        
#        nx.DiGraph.__init__(self)
#        self.affinity = 1 #FIX ME
#        
#        
#        
#        for nf, nt in edges:
#
#            #print("boucle cycle")
#            
#            data = graph.get_edge_data(nf, nt, default=None)
#            self.add_edge(nf, nt, data)
#            
#        nodes = self.nodes()
#        nodes = tuple(nodes)
#        self.permutations = self.cyclic_permutation(nodes)
#        # We normalize the states so that we get the lower symbol first
#        self.setnodes = self.permutations[0]    
#        
#    def cyclic_permutation(self, nodes):
#        """
#        Construit toutes les permutations de noeud pour un cycle (ex : 1, 2, 3 où 2, 3, 1 où 3, 1, 2). Ces permutations 
#        sont utilisées comme critère afin de comparer la correspondance de deux cycles. Elle est donc la base qui permet d'utiliser 
#        les cycles comme des clés de dictionnaires. 
#        
#        nodes : une liste de meso-états (type : Meso)
#        
#        Rappel : afin d'utiliser un objet comme une clef, il est nécéssaire de pouvoir faire le test 
#        d'équivalence (objet1==objet2).
#
#        return tuple
#        """
#
#        ll = len(nodes)
#        perms = []
#        
#        for idx in range(ll):
#            
#            start = list(nodes[idx:ll])
#            start.extend(nodes[0:idx])
#            perms.append(tuple(start))
#            
#        perms.sort()#Pourquoi cette étape est indispensable déjà?
#        
#        #perms = sorted(perms, key=attrgetter('coord'))
#        #perms = sorted(perms, key=itemgetter(0))
#
#        return tuple(perms)
#
#    
#    def __hash__(self):
#        return hash(self.setnodes)
#    
#    def __eq__(self, other):
#        """
#        Permet de comparer les ensemble de noeuds construit à l'aide de la fonction cyclic_permutation.
#        Cette fonction permet de faire le test :  cycle1==cycle2, indispensable pour un objet afin de pouvoir 
#        être utilisé comme une clé dans un dictionnaire.
#        
#        return bool
#        """
#        
#        if len(self.setnodes) != len(other.setnodes):
#            return False
#        if type(other) is not Cycle:
#            return False
#        if self.setnodes in other.permutations:
#            return True
#        else:
#            return False
#        #modification??
#
#    def decomposition(self):
#        """
#        Permet de décomposer un cycle d'après Knoch et Speck 2015. Ici la valeur du flux de probabilité minimal 
#        est récupérée, puis soustrait à chacun des fluxs de probabilité dans la liste new_fluxes. Si le flux de probabilité d'une arête tombe à zéro, 
#        l'arête sera éliminée dans la copy du cycle G. L'algorithme élimine ainsi au moins une arête dans G.
#        G est alors reconstruit en pondérant ses arêtes par les valeurs contenues dans new_fluxes.
#        
#        retourne une copie du graphe de cycle auquel a été soustrait le flux de probabilité minimal. 
#        Les valeurs des fluxs de probabilités des arêtes du graphe principal serons mise-à-jour avec les 
#        valeurs de la copie du cycle.
#        
#        return decomposed (type : cycle)   
#        """
#        
#        G = self.copy()
#        
#        lofe = list(G.edges())
#        
#        fluxes = np.array([G.get_edge_data(*edge)['flux'] for edge in lofe])
#        minflux = np.min(fluxes)
#        new_fluxes = fluxes - minflux
#        assert(np.sum(fluxes == minflux) >= 1)
#
## FIXME: construct the decomposed  copy of create a new one
#        
#        
#        for ne, ee in enumerate(lofe): #bug....?
#            if new_fluxes[ne] <= 0.:
#                d = ee[0]
#                f = ee[1]
#                G.remove_edge(d, f)
#            else:
#                d = ee[0]
#                f = ee[1]
#                G[d][f]['flux'] = new_fluxes[ne]
#        
#        lofe = list(G.edges())#inutile???
#        
#        fluxes = np.array([G.get_edge_data(*edge)['flux'] for edge in lofe]) #inutile?
#        
#        decomposed = G #c'est juste pour avoir une meilleur compréhension
#        
#        return decomposed
#
#    def is_similar(self, other, affinity=False, xi=1./2.):
#        """
#        Permet de voir si deux cycles sont similaires.
#        Ici nous prennons deux grandeurs qui sont les affinités ainsi que les extensions spatiales.
#        Parmi ces deux grandeurs nous discernons les valeurs maximal et minimal appartenant à l'un ou l'autre des cycles.
#        La fonction renvois True si le rapport des valeurs maximale et minimale est > à 0.5 pour chacune des deux grandeurs.
#        
#        Nb : les tests sur les affinités ne sont pas implémentés 
#        
#        return bool
#        """
#        
#        c1sp = self.spatial_extension()
#        c2sp = other.spatial_extension()
#        spatialcoef = min(c1sp, c2sp) / max(c1sp, c2sp) 
#
#        #FIXME: implement!
#        if affinity:
#            raise NotImplementedError
#            # affcoef = min(self.affinity, other.affinity) / max(self.affinity, other.affinity) 
#        else:
#            pass
#            
#        if spatialcoef<=xi:# or affcoef <= xi:
#            return False
#        else: # FIXME: check this!
##            if(affcoef<=xi):
#            return True
#
#    def node_intersection(self, other):
#        """
#        Retourne la liste des noeuds communs entre deux cycles/graphe. Si aucun noeud n'est partagés entre les cycles, la liste est vide.  
#        
#        return list
#        """
#
#        s1 = self.nodes()
#        s2 = other.nodes()
#
#        if len(s1) < len(s2):
#            li_inter = [node for node in s1 if node in s2]
#            
#        else: 
#            li_inter = [node for node in s2 if node in s1]
#        
#        return li_inter
#
#    def weight_link(self, other, inter): #, w_inter):
#        """
#        Permet de définir la valeur pondérant les arêtes entre deux cycles liés dans le graphe de cycle.
#        
#        return float
#        """
#        
#        w_inter = [node.pi for node in inter]
#        w_self = [node.pi for node in self.nodes()]
#        w_other = [node.pi for node in other.nodes()]
#        
#        #return 2. * sum([node[].pi  for node in w_inter]) / (sum(w_other) + sum(w_self))
#        return 2. * sum(w_inter) / (sum(w_other) + sum(w_self))
#
#def graph_of_cycles(listofcycles):
#    """
#    Construit le graphe de cycle et le retourne. Les noeuds du graphes ne sont lié entre-eux que s'ils possèdent au moins un noeud commun, et des caractéristiques communes.
#    La présence de noeud commun est testée avec la fonction node_intersection et les caractéristiques communes avec is_similar. 
#    
#    listeofcycle : une liste de cycle (type : cycle) type : list
#    
#    return nx.Graph
#    """
#
#    G = nx.Graph()
#        
#    print('nb cycles: ', len(listofcycles))
#    for node1 in listofcycles:
#
#        G.add_node(node1)
#        #self.node[no_node]['cycle'] = cycle
#        #son1 = node1.nodes()
#
#        for node2 in G.nodes():
#
#            if (node1 != node2) and node1.is_similar(node2):
#                inter = node1.node_intersection(node2)
#
#                if inter: #and node1.is_similar(node2):
#                        G.add_edge(node1, node2, weight=node1.weight_link(node2, inter))#, inter))
#    return G
#
#        #self.g = M
#
#def get_communities(goc): #, dynamic):
#    """
#    Permet d'avoir les communauté d'un graphe de cycle. et de renvoyer un dictionnaire avec pour clé une communauté
#    et pour valeur le graphe contenant tous les noeuds et les edges de cette communauté.
#    
#    goc : un graphe de cycle 
#    
#    return  : dictionnaire de graphe 
#    """
#
#    parti = comu.best_partition(goc, partition=None, weight='weight', resolution=1.0)#Flux?!!!!!
#
#    # {0: 1, 1: 0, 2: 4, ... node: community...} node = cycle
#    
#    comm = {}
#    
#    
#    # affich = afficheur()
#    
#    GLedges = goc.edges()
#
#    for nn, cc in parti.items():
#
#        #if not comm.has_key(cc):
#
#        if not cc in comm:
#
#            comm[cc] = [nn]
#        else:
#            comm[cc].append(nn)
#
#    return dict([(c, subCycleGraph(lon, goc)) for c, lon in comm.items()])#Tester si l'on peut utiliser Subgraph de nx
#
#
#def subCycleGraph(nbunch, goc):
#    """
#    Construit un sous-graphe de cycle contenant tous les noeuds d'une communauté
#    
#    nbunch : un ensemble de noeud
#    goc : le graphe de cycle principal
#    
#    return H : le sous-graphe de cycle
#    """
#    
#    #bunch = Cyclesbunch_iter(goc, nbunch)
#    # create new graph and copy subgraph into it
#    H = nx.Graph()
#    # copy node and attribute dictionaries
#    #Gadj = goc.adj
#    #gnodes = goc.nodes()
#    d = {}
#
#    for n1 in nbunch:#bunch:
#
#        subd = {}
#        for n2 in nbunch:#Cyclesbunch_iter(goc, nbunch):# à remplacer par nbunch?
#
#            if goc.has_edge(n1, n2):
#                #d[n1] = Gadj[n]
#                #d[n1] = Gadj[n]#subd = subd + edge(n1, n2)
#                data = goc.get_edge_data(n1, n2)
#                ####################
#                ###########
#                ###### Faire la même expérience avec 
#                subd[n2] = data
#                #subd[n2] = data['weight'] #rajouté le 6/07/2016
#        d[n1] = subd
#    H = nx.from_dict_of_dicts(d)
#    return H
#
##def find_representative(comm, gr, goc, commud):
#def find_representative(gr, goc, commud):
#    """
#    Permet de trouver les cycles représentatifs d'une communauté en se basant sur la fomule de la modularité de Knoch et Speck
#    2015. Pour chaque noeud nn dans lon, on fait la somme kgamma du poids de chacune des arêtes en relation avec ce noeud. Suivant la redéfinition de la modularité
#    par Knoch et Speck, nous calculons la différence de modularité avec ou sans le noeud nn à l'aide de kgamma. Nous retournons alors le noeud (type : cycle) se trouvant à l'indice
#    du maximum dans la liste mod_idx qui référence la valeur des différences de modularité pour chacun des noeuds.  
#    
#    gr : Graphe contenant toutes les arêtes et tous les noeuds d'une communauté
#    commud : Le dictionnaire contenant les communautés en clef (type : int) et les graphes (type : nx.graphe) de cycles contenant toutes les arêtes et tous les noeuds (type : cycle) de 
#    cette communauté en valeur. (type : dict)
#       
#    return : cycle
#    """
#    
#    m = 0
#    
#    for subg in commud.values():
#        
#        m += sum([subg[ed[0]][ed[1]]['weight']
#                 for ed in subg.edges()]) / 2.     
#
#
#    kalpha = sum([gr[ed[0]][ed[1]]['weight']
#                  for ed in gr.edges()])
#    
#    lon = list(gr.nodes())
#    mod_idx = []
#    
#    for nn in lon:
#        
#        kgamma = sum([gr[ed[0]][ed[1]]['weight'] for ed in nx.edges(gr, [nn])])#Ici c'est un graphe de cycle, nous recherchons les 'weight' et non les 'flux' comme dans le graphe de centroïde
#        mod_idx.append((kgamma / m) * (1. + (kgamma + kalpha) / m))
#               
#    return lon[mod_idx.index(max(mod_idx))]
