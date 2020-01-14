 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
class Vertex:
    def __init__(self, arr):
        self.out = arr[0]
        self.by = arr[1:-1]
        self.to = arr[-1]
    
    def set_all(self, arr):
        self.by = arr[1]
        self.out = str(arr[0])
        self.to = str(arr[2])
    
    def __repr__(self):
        return str(self.out) + ": " + str(self.by) + ": " + str(self.to)
    
class Automata:
    def __init__(self, str):
        arr =[]
        f = open(str)
        for line in f:
            arr.append(line)
        f.close()
        self.A = arr[0]
        self.S = arr[1]
        self.s0 = arr[2][0:-1]
        self.F = arr[3].split()[1:]
        rules = []
        vertFrom = []
        vertIn =[ ]
        alphabet = []
        for rule in arr[4:]:
            arr = rule.split()
            rules.append(Vertex(arr))
            alphabet.append(arr[1:-1])
            vertFrom.append(arr[0])
            vertIn.append(arr[-1])
        self.f = rules
        self.vertFrom = list(set(vertFrom))
        self.vertIn = list(set(vertIn))
        self.alphabet = (alphabet)
        self.allVert = list(set(vertFrom + vertIn))
        
    def deleteVert(self, arr):
        if len(arr)!=0:
            for rule in self.f:
                if rule.out in arr or rule.to in arr:
                    self.f.remove(rule)
            self.allVert = list(set(self.allVert) - set(arr))
            self.vertFrom = list(set(self.vertFrom) - set(arr))
            self.vertIn = list(set(self.vertIn) - set(arr))

    def unreachable(self):
        arr = [self.s0]
        for vert in arr:
            for rule in self.f:
                if rule.out in arr:
                    arr.append(rule.to)
                    arr = list(set(arr))
        return (list(set(self.allVert) - set(arr)))
    
    def tupik(self):
        arr = self.F.copy()
        for vert in arr:
            for rule in self.f:
                if rule.to in arr:
                    arr.append(rule.out)
                    arr = list(set(arr))
        return (list(set(self.allVert) - set(arr)))
            
    def minimize(self):
        self.deleteVert(self.unreachable())
        self.deleteVert(self.tupik())
        F = set(self.F.copy())
        S = set(set(self.allVert.copy()) - set(self.F.copy()))
        P = [F, S]  
        W = [F, S]
        while len(W)!=0:
            A = W[0]
            W.remove(A)
            X = set()
            for c in self.alphabet:
                for rule in self.f:
                    if rule.to in A and c in rule.by:
                        X.add(rule.out)
                for Y in P:
                    differenceY_X = set(set(Y) - X)
                    crossY_X = []
                    for symb in Y:
                        if symb in X:
                            crossY_X.append(symb)
                    crossY_X = set(crossY_X)
                    if len(differenceY_X)!=0 and len(crossY_X)!=0:
                        P.remove(Y)
                        P.append(crossY_X)
                        P.append(differenceY_X)
                        if Y in W:
                            W.remove(Y)
                            W.append(crossY_X)
                            W.append(differenceY_X)
                        else:
                            if len(crossY_X) <= len(differenceY_X):
                                W.append(crossY_X)
                            else:
                                W.append(differenceY_X)
        return P
        
    def uniteVertexes(self, P):
        def find(arr, x):
            for elem in arr:
                if x in elem:
                    return arr.index(elem)
        def unique(list1): 
            unique_list = [] 
            for x in list1: 
                if x not in unique_list: 
                    unique_list.append(x)
            return unique_list
    
        rules=[]
        
        for newVert in P:
            for vert in newVert:
                for rule in self.f:
                    if vert == rule.out:
                        rules.append([P.index(newVert), rule.by, find(P, rule.to)])
        
        rules = unique(rules)
        
        for rule in rules:
            for r in rules:
                if rule[0] == r[0] and rule[2]==r[2] and rule[1]!=r[1]:
                    rule[1] += r[1]
                    rules.remove(r)
        self.s0 = find(P, self.s0)      
        F = []
        for vert in self.F:
            F.append(find(P, vert))
        if len(F) == 1:
            self.F = F[0]
        else:
            self.F = list(set(F))
        array = []
        vertFrom = []
        vertIn =[ ]
        alphabet = []
        for rule in rules:
            rule[1] = list(set(rule[1]))
            vertex = Vertex("0 a 0")
            vertex.set_all(rule)
            array.append(vertex)
            vertFrom.append(vertex.out)
            vertIn.append(vertex.to)
            alphabet.append(rule[1][:])
        self.f = array
        self.vertFrom = list(set(vertFrom))
        self.vertIn = list(set(vertIn))
        self.alphabet = (alphabet)
        self.allVert = list(set(vertFrom + vertIn))
        self.S = len(self.allVert)
            
            
    def compare(self, other):
        def unique(list1): 
            unique_list = [] 
            for x in list1: 
                if x not in unique_list: 
                    unique_list.append(x)
            return unique_list
        self.uniteVertexes(self.minimize())
        other.uniteVertexes(other.minimize())
        self_vert = str(self.s0)
        all_ver = [self_vert]
        other_vert = str(other.s0)
        oth_ver = [other_vert]
        amount = 0
        while (True):
            flag = True
            for rule in self.f:
                if rule.out == str(self_vert):
                    for rul in other.f:
                        if rul.out == str(other_vert) and rule.by == rul.by:
                            amount+=1
                            flag = False
                            self_vert = rule.to
                            other_vert = rul.to
                            all_ver.append(self_vert)
                            oth_ver.append(other_vert)
                            break
            if amount == len(self.allVert) and \
            amount == len(other.allVert):
                return True    
            if flag:
                return False
            

if __name__ == "__main__":      
    auto1 = Automata("Auto1.txt")
    auto2 = Automata("Auto2.txt")
    print(auto1.compare(auto2))   
