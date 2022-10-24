import random
tab =[[" " for i in range(17)] for ii in range(11)]
# funkcja rozruchowa
def main():
    x=input("Wybierz co chcesz zrobic:\n1. Nowa gra\n2. Auto rozwiazywanie\n")
    try:
        x=int(x)
    except:
        x=int(input("Podaj liczbe!!\n"))
    createTable()
    createSolution()
    if x==1:
        lvl=input("Wybierz poziom trudnosci:\n1. Latwy\n2. Sredni\n3. Trudny\n")
        try:
            lvl=int(lvl)
        except:
            lvl=int(input("Podaj liczbe!!\n"))
        if lvl==1:
            delNum(45)
            game(45)
        elif lvl==2:
            delNum(51)
            game(51)
        elif lvl==3:
            delNum(57)
            game(57)
        else:
            print('Nie ma takiego numeru')
            main()
    elif x==2:
        delNum(51)
        autoSolver()
    else:
        main()
# sprawdza czy sa 0
def zeroChecker(tab):
    for i in range(9):
        for ii in tab[i]:
            if ii==0:
                return False
    return True
# tablica majaca rozwiazanie
def solution():
    tabk = [[0 for ii in range(9)] for i in range(9)]
    for i in range(9):
        for ii in range(9):
            # stworzenie mniejszej tablicy 3x3
            if i < 3:
                if ii < 3:
                    tabTrojki = [[tabk[zz][z] for z in range(3)] for zz in range(3)]
                elif ii >= 6:
                    tabTrojki = [[tabk[zz][z] for z in range(6, 9)] for zz in range(3)]
                else:
                    tabTrojki = [[tabk[zz][z] for z in range(3, 6)] for zz in range(3)]
            elif i >= 6:
                if ii < 3:
                    tabTrojki = [[tabk[zz][z] for z in range(3)] for zz in range(6, 9)]
                elif ii >= 6:
                    tabTrojki = [[tabk[zz][z] for z in range(6, 9)] for zz in range(6, 9)]
                else:
                    tabTrojki = [[tabk[zz][z] for z in range(3, 6)] for zz in range(6, 9)]
            else:
                if ii < 3:
                    tabTrojki = [[tabk[zz][z] for z in range(3)] for zz in range(3, 6)]
                elif ii >= 6:
                    tabTrojki = [[tabk[zz][z] for z in range(6, 9)] for zz in range(3, 6)]
                else:
                    tabTrojki = [[tabk[zz][z] for z in range(3, 6)] for zz in range(3, 6)]
            tabT = []
            for xx in range(3):
                for x in range(3):
                    tabT.append(tabTrojki[xx][x])
            tabCol = [tabk[j][ii] for j in range(i)]  # tablica zawierajaca liczby z kolumny
            tabSum = tabCol + tabk[i] + tabT
            tabReszta = []
            for z in range(1, 10):
                if z not in tabSum:
                    tabReszta.append(z)
            if len(tabReszta) > 1:
                tabk[i][ii] = random.choice(tabReszta)
            elif len(tabReszta) == 1:
                tabk[i][ii] = tabReszta[0]
    return tabk
# stworzenie pustej tablicy sudoku
def createTable():
    global tab
    for i in range(11):
        for ii in range(17):
            if i!=0:
                if i%4==3 and ii%6==5 and ii!=0:
                    tab[i][ii]='+'
                elif i%4==3:
                    tab[i][ii]='-'
                elif ii%6==5 and ii!=0:
                    tab[i][ii]='|'
                elif ii%2==1:
                    tab[i][ii] = ' '
            else:
                if ii%6==5 and ii!=0:
                    tab[i][ii]='|'
                elif ii % 2 == 1 and ii != 0:
                    tab[i][ii] = ' '
# wypisywanie tablicy
def printTable():
    global tab
    for i in range(11):
        for ii in range(17):
            print(tab[i][ii], end="")
        print()
# wypelnienie tablicy, w taki sposob, by pasowala do zasad sudoku
def createSolution():
    global tab
    global tabk
    tabk=solution()
    while not zeroChecker(tabk):
        tabk=solution()
    j=0
    jj=0
    for i in range(11):
        if i%4!=3:
            for ii in range(17):
                if ii%2==0:
                   tab[i][ii]=tabk[j][jj]
                   jj+=1
                   if jj==9:
                       j+=1
                       jj=0
# usuwanie danej ilosci cyfr
def delNum(n):
    global tab
    outSource=open('solution.txt', 'w')
    for i in range(11):
        for ii in range(17):
            print(tab[i][ii], end="", file=outSource)
        print("", file=outSource)
    outSource.close()
    delWhat=[True for i in range(n)]
    for i in range(81-n):
        index=random.randint(0, len(delWhat))
        delWhat=delWhat[:index]+[False]+delWhat[index:]
    j=0
    for i in range(11):
        if i%4!=3:
            for ii in range(17):
                if ii%2==0:
                    if j>=81:
                        break
                    if delWhat[j]:
                        tab[i][ii]=' '
                    j+=1
    j=0
    for i in range(9):
        for ii in range(9):
            if delWhat[j]:
                tabk[i][ii]=' '
            j+=1

    printTable()
    print('Powodzenia')
#gra
def game(n):
    print("Podaj nr wiersza, nr kolumny oraz cyfre \n(w jednym wierszu, po spacji)")
    while n!=0:
        a,b,c=input().split()
        a=int(a)
        b=int(b)
        c=int(c)
        if a <= 3:
            if b <= 3:
                tabTrojki = [[tabk[zz][z] for z in range(3)] for zz in range(3)]
            elif b >= 7:
                tabTrojki = [[tabk[zz][z] for z in range(6, 9)] for zz in range(3)]
            else:
                tabTrojki = [[tabk[zz][z] for z in range(3, 6)] for zz in range(3)]
        elif a >= 7:
            if b <= 3:
                tabTrojki = [[tabk[zz][z] for z in range(3)] for zz in range(6, 9)]
            elif b >= 7:
                tabTrojki = [[tabk[zz][z] for z in range(6, 9)] for zz in range(6, 9)]
            else:
                tabTrojki = [[tabk[zz][z] for z in range(3, 6)] for zz in range(6, 9)]
        else:
            if b <= 3:
                tabTrojki = [[tabk[zz][z] for z in range(3)] for zz in range(3, 6)]
            elif b >= 7:
                tabTrojki = [[tabk[zz][z] for z in range(6, 9)] for zz in range(3, 6)]
            else:
                tabTrojki = [[tabk[zz][z] for z in range(3, 6)] for zz in range(3, 6)]
        tabT = []
        for xx in range(3):
            for x in range(3):
                tabT.append(tabTrojki[xx][x])
        tabCol = [tabk[j][b-1] for j in range(a)]  # tablica zawierajaca liczby z kolumny
        tabSum = tabCol + tabk[a-1] + tabT
        if c in set(tabSum) or tabk[a-1][b-1]!=' ':
            print('Nie mozesz wpisac tej cyfry')
        else:
            tabk[a-1][b-1]=c
            if a<=3:
                tab[a-1][2*b-2]=c
            elif a>=7:
                tab[a+1][2*b-2]=c
            else:
                tab[a][2*b-2]=c
            n-=1
        printTable()
        if n==0:
            print("Gratulacje ukonczyles sudoku!!!")
            break
#autosolver - backtracking
def autoSolver():
    global tabk
    for ii in range(9):
        for iii in range(9):
            if tabk[ii][iii]==' ':
                for i in range(1, 10):
                    if ii < 3:
                        if iii < 3:
                            tabTrojki = [[tabk[zz][z] for z in range(3)] for zz in range(3)]
                        elif iii >= 6:
                            tabTrojki = [[tabk[zz][z] for z in range(6, 9)] for zz in range(3)]
                        else:
                            tabTrojki = [[tabk[zz][z] for z in range(3, 6)] for zz in range(3)]
                    elif ii >= 6:
                        if iii < 3:
                            tabTrojki = [[tabk[zz][z] for z in range(3)] for zz in range(6, 9)]
                        elif iii >= 6:
                            tabTrojki = [[tabk[zz][z] for z in range(6, 9)] for zz in range(6, 9)]
                        else:
                            tabTrojki = [[tabk[zz][z] for z in range(3, 6)] for zz in range(6, 9)]
                    else:
                        if iii < 3:
                            tabTrojki = [[tabk[zz][z] for z in range(3)] for zz in range(3, 6)]
                        elif iii >= 6:
                            tabTrojki = [[tabk[zz][z] for z in range(6, 9)] for zz in range(3, 6)]
                        else:
                            tabTrojki = [[tabk[zz][z] for z in range(3, 6)] for zz in range(3, 6)]
                    tabT = []
                    for xx in range(3):
                        for x in range(3):
                            tabT.append(tabTrojki[xx][x])
                    tabCol = [tabk[ii][iii] for j in range(ii)]  # tablica zawierajaca liczby z kolumny
                    tabSum = tabCol + tabk[ii] + tabT
                    if i not in tabSum:
                        tabk[ii][iii]=i
                        autoSolver()
                        tabk[ii][iii]=' '
                return
    for i in range(9):
        for ii in tabk[i]:
            print(ii, end=' ')
        print()
    input('Chcesz wiecej?')
main()