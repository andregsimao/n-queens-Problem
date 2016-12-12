import random
from random import randint
numQueens = 8



lenPopulation = 12    # número de elementos em uma populacao ( >= 4 )
CR = 0.1  # quanto menor, mais parecido com o XBefore. Pertence a [0,1]    
F = 0.5   # pertence a [0,2]

#state[i] is the line of column i
def sumLists(X,Y):
	return [x + y for x, y in zip(X, Y)]

def productList(a,X):
	return [a*x for x in X]

def changeToInt(X):
	return [(int)(x) for x in X]

def calculateResultfitness(state):
    h = 0
    for i in range(numQueens):
        for j in range(i + 1, numQueens):
            if isAttacked(state[i], i, state[j], j)==True:
                h += 1
    return h

def fitness(state):
    h = 0
    for i in range(numQueens):
        for j in range(i + 1, numQueens):
            if isAttacked(state[i], i, state[j], j)==False:
                h += 1
    return h

def isAttacked(pos1X, pos1Y, pos2X, pos2Y):
    # same line
    if pos1X == pos2X:
        return True
    # same column
    if pos1Y == pos2Y:
        return True
    # same ascending diag
    if pos1X + pos1Y == pos2X + pos2Y:
        return True
    # same descending diag
    if pos1X - pos2X == pos1Y - pos2Y:
        return True
    return False

def getThreeDistinctIndexes(i, N):	
	a=randint(0,N-1)
	while (a==i):
		a=randint(0,N-1)
	b=randint(0,N-1)
	while (b==i or b==a):
		b=randint(0,N-1)		
	c=randint(0,N-1)
	while (c==i or c==a or c==b):
		c=randint(0,N-1)
	return [a,b,c]

def getOffSpring(Xbefore, Vafter):
	T=[]		
	Irand=randint(0,numQueens-1)
	#print(Irand)
	for j in range(numQueens):		
		randJI=random.uniform(0, 1)
		#print(randJI)
		if randJI<=CR or j==Irand:
			T.insert(len(T),Vafter[j])
		else:
			T.insert(len(T),Xbefore[j])
	return T

def getEvaluatedPopulationElement(Xbefore, Tafter):
	fitnessX=fitness(Xbefore)
	fitnessT=fitness(Tafter)
	if(fitnessT>=fitnessX):
		return Tafter
	else:
		return Xbefore

def getRandomPopulation(N, D):
	randomPop=[]
	for i in range(N):
		randomPop.insert(len(randomPop), getRandomElement(D))
	return randomPop

def getRandomElement(D):
	randomElem=[]
	for i in range(D):
		elem=randint(0,D-1)
		while elem in randomElem:
			elem=randint(0,D-1)
		randomElem.insert(len(randomElem), elem)
	return randomElem

def getDonorVector(pop):
	donorV=[]
	for i in range(lenPopulation):
		threeIndexes=getThreeDistinctIndexes(i, lenPopulation)
		#print(threeIndexes)
		Xr1=pop[threeIndexes[0]]
		Xr2=pop[threeIndexes[1]]
		Xr3=pop[threeIndexes[2]]
		#donorElem=(1-F)* Xr1  +  F* ((Xr2+Xr3)/2)
		med_Xr2_Xr3=productList(0.5,sumLists(Xr2,Xr3))
		#print(diff_Xr2_Xr3)
		donorElem=sumLists(productList(1-F, Xr1),productList(F,med_Xr2_Xr3))
		#print(donorElem)
		donorV.insert(len(donorV),changeToInt(donorElem))
	return donorV

def getOffspringVector(X, V):
	length=len(X)
	T=[]
	for i in range(length):
		T.insert(len(T), getOffSpring(X[i],V[i]))
	return T
def getNewPopulation(X,T):
	length=len(X)
	newP=[]
	for i in range(length):
		newP.insert(len(newP), getEvaluatedPopulationElement(X[i],T[i]))
	return newP
def printPop(pop):
	length=len(pop)
	print("----------------------------------")
	for i in range(length):
		print(pop[i], end=' ')
		print(fitness(pop[i]))
	print("----------------------------------")

def hasResult(pop):   # to 8 queens, resultFitness = 28
	length=len(pop)
	for i in range(length):
		if(fitness(pop[i])==resultFitness):
			return True
	return False

def missingElems(array):
	length=len(array)
	answ=[]
	hasElement=[]
	for i in range(length):
		hasElement.insert(len(hasElement), False)
	for i in range(length):
		hasElement[array[i]]=True
	for i in range(length):
		if(hasElement[i]==False):
			answ.insert(len(answ), i)
	return answ


def elemOptimized(array):
	length=len(array)
	newArray=[]
	currentIndex=0
	elemMissing= missingElems(array)
	for i in range(length):
		if array[i] in newArray:
			newArray.insert(len(newArray),elemMissing[currentIndex])
			currentIndex+=1
		else:
			newArray.insert(len(newArray),array[i])
	return newArray

def xOptimized(X):   # to 8 queens, resultFitness = 28
	length=len(X)
	newX=[];
	for i in range(length):
		newX.insert(len(newX), elemOptimized(X[i]))
	return newX

def printResult(popWithResult):
	length=len(popWithResult)
	for i in range(length):
		if(fitness(popWithResult[i])==resultFitness):
			print ('Resultado: ', popWithResult[i])
			printResultTable(popWithResult[i])
			return

def printResultTable(tableResult):
	length=len(tableResult)
	print("----------------------------------")
	for i in range(length):
		for j in range(length):
			if tableResult[j]==i:
				print('Q',end=' ')
			else:
				print('.',end=' ')
		print()	
	print("----------------------------------")

aux=[]
for i in range(numQueens):
	aux.insert(0,1)
resultFitness = calculateResultfitness(aux) 

print('Numero de rainhas: ', numQueens,' (para mudar o numero de rainhas basta mudar a variavel numQueens): ')
print('Numero de elementos na populacao: ', lenPopulation,' (para mudar o numero de elementos na populacao basta mudar a variavel lenPopulation): ')

X=getRandomPopulation(lenPopulation, numQueens)
#print("X:")
#printPop(X)
nIterations=0
while hasResult(X)==False:#--------------------------------------------------
	V=getDonorVector(X)	
	T=getOffspringVector(X,V)
	X=getNewPopulation(X,T)
	X=xOptimized(X)
	nIterations+=1;
	if(nIterations%100==0):
		print(nIterations)
#--------------------------------------------------
print('\nNumero de iteracoes ate o resultado: ', nIterations)
printResult(X)
print('\nPopulacao com o resultado: ')
printPop(X)



print(nIterations)