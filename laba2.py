#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class Vertex:
    def __init__(self, arr):
        self.out = arr[0]
        self.by = arr[1:-1]
        self.to = arr[-1]
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
        vert = []
        for rule in arr[4:]:
            arr = rule.split()
            rules.append(Vertex(arr))
            vert.append(arr[0])
            vert.append(arr[-1])
        self.f = rules
        self.allVert = list(set(vert))
        
    def reachable(self):
        arr = [self.s0]
        for vert in arr:
            for rule in self.f:
                if rule.out in arr:
                    arr.append(rule.to)
                    arr = list(set(arr))
        return list(set(arr))
    
    def notDeadlock(self):
        arr = self.F.copy()
        for vert in arr:
            for rule in self.f:
                if rule.to in arr:
                    arr.append(rule.out)
                    arr = list(set(arr))

        return list(set(arr))
    
    def checkLet(self, pos, let):
        array = []
        for rule in self.f:
           if rule.out == pos and let in rule.by:
               array.append(rule.to)
        if len(array) == 0: 
           return False
        else:
            return array
    
    def AlgCheck(self, pos1, word):
        arr = [(pos1, 0)]
        lastArr = []
        amount = 0
        while(len(arr)!=0):
            possible = self.checkLet(arr[0][0], word[arr[0][1]])
            if possible!=False:
                position = arr[0][1]
                for symb in possible:
                    if self.checkLet(symb, word[position+1])!=False:
                        if position == len(word)-2:
                            return self.checkLet(symb, word[position+1])
                        arr.insert(0, (symb, position+1))

                if lastArr == arr:
                    amount +=1
                lastArr = arr
                if amount > 1000:
                    return False
            else:
                arr.pop(0)

        return False
        
    def Check(self):
        word = input("Введіть своє слово: ") 
        result = False
        for pos1 in self.allVert:
            if pos1 in self.reachable():
                res = self.AlgCheck(pos1, word)
                if res!=False:
                    for vert in res:
                        if vert in self.notDeadlock():
                            result = True 
                if result == True:
                    break
        if result:
            print('Початок слова у вершині:', pos1)
            print('Таке слово існує.')
        else:
            print('Таке слово не існує.')
        
auto1 = Automata("Auto1.txt")

print(auto1.Check())

