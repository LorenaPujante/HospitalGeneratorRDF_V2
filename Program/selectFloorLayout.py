
import statistics as st
import random 



#########
# 1 ROW #
#########

def bck_1R_getRandomBestLayout(allSolutions, b):
    # Get metricas de las soluciones
    allSolutions_st = []
    for s in allSolutions:
        corridors = bck_1R_getCorridorsList(s)
        corrMean = st.fmean(corridors)
        corrMedian = st.median(corridors)
        corrQuantiles = st.quantiles(corridors)
        corrQuantilesMean = st.mean(corrQuantiles)
        sol_st = [s,corridors,corrMean,corrMedian,corrQuantiles,corrQuantilesMean]
        allSolutions_st.append(sol_st)
    allSolutions_st = sorted(allSolutions_st, key=lambda x: (x[5], x[2], x[3]))
    
    # Get Layouts que cumplen que sus estadisticas mas importantes son 'b'
    bestLayouts = bck_1R_getLayoutsByStatistics(allSolutions_st, b)

    # De todos los layouts, elegir uno aleatoriamente
    randIndex = random.randint(0,len(bestLayouts)-1)
    bestLayout = bestLayouts[randIndex][0] 
    
    return bestLayout
    
def bck_1R_getCorridorsList(solution):
    corridors = []

    for i in range(len(solution)):
        pos = solution[i]
        if pos[0] in ['A', 'B', 'C', 'D']:
            corridors.append(2)
        elif pos[0] in ['E', 'F', 'G', 'H']:
            corridors.append(3)
        elif pos[0] == 'I':
            corridors.append(4)
        elif pos[0] == 'J':
            corridors.append(1)

    return corridors    

def bck_1R_getLayoutsByStatistics(allSolutions_st, b):
    
    # Media de los cuartiles
    a = allSolutions_st
    c = [x for x in a if x[5]==b]
    
    if len(c) == 0:
        d = [x for x in a if x[5]<b]
            # Por si no hay ninguna configuración cuya media sea menor a la dada
        b_aux = b
        while len(d)==0  and  b_aux<b+10:
            b_aux += 0.5            
            d = [x for x in a if x[5]<b_aux]
        if len(d) == 0:
            raise SolutionNotFoundError()
        maxQC = max(d, key=lambda x: x[5])  # Nos quedamos con el máximo de pasillos
        c = [x for x in d if x[5]==maxQC[5]]
        
    # Mediana
    a = c
    c = [x for x in a if x[3]==b]

    if len(c) == 0:
        d = [x for x in a if x[3]<b]
            # Por si no hay ninguna configuración cuya media sea menor a la dada
        b_aux = b
        while len(d)==0  and  b_aux<b+10:
            b_aux += 0.5            
            d = [x for x in a if x[3]<b_aux]
        if len(d) == 0:
            raise SolutionNotFoundError()
        maxMd = max(d, key=lambda x: x[3])  # Nos quedamos con el máximo de pasillos
        c = [x for x in d if x[3]==maxMd[3]]

    # Media
    a = c
    c = [x for x in a if x[2]==b]

    if len(c) == 0:
        d = [x for x in a if x[2]<b]
            # Por si no hay ninguna configuración cuya media sea menor a la dada
        b_aux = b
        while len(d)==0  and  b_aux<b+10:
            b_aux += 0.5            
            d = [x for x in a if x[2]<b_aux]
        if len(d) == 0:
            raise SolutionNotFoundError()
        maxMn = max(d, key=lambda x: x[2])  # Nos quedamos con el máximo de pasillos
        c = [x for x in d if x[2]==maxMn[2]]

    return c


#########
# 2 ROW #
#########

def bck_2R_getRandomBestLayout(allSolutions, b):
    
    # Get metricas de las soluciones
    allSolutions_st = []
    for s in allSolutions:
        corridors, corridors_1, corridors_2 = bck_2R_getCorridorsList(s)
        
        corrMean = st.fmean(corridors)
        corrMedian = st.median(corridors)
        corrQuantiles = st.quantiles(corridors)
        corrQuantilesMean = st.mean(corrQuantiles)

        corrMean_1 = st.fmean(corridors_1)
        corrMedian_1 = st.median(corridors_1)
        corrQuantiles_1 = st.quantiles(corridors_1)
        corrQuantilesMean_1 = st.mean(corrQuantiles_1)

        corrMean_2 = st.fmean(corridors_2)
        corrMedian_2 = st.median(corridors_2)
        corrQuantiles_2 = st.quantiles(corridors_2)
        corrQuantilesMean_2 = st.mean(corrQuantiles_2)

        diffQMean = abs(corrQuantilesMean_1-corrQuantilesMean_2)
        diff_Q3Q1_1 = corrQuantiles_1[2]-corrQuantiles_1[0]
        diff_Q3Q1_2 = corrQuantiles_2[2]-corrQuantiles_2[0]

        sol_st = [s,corridors, corrMean,corrMedian,corrQuantiles,corrQuantilesMean, corrMean_1,corrMedian_1,corrQuantiles_1,corrQuantilesMean_1, corrMean_2,corrMedian_2,corrQuantiles_2,corrQuantilesMean_2, diffQMean, diff_Q3Q1_1,diff_Q3Q1_2]
        
        allSolutions_st.append(sol_st)
    
    allSolutions_st_veryLimited = [x for x in allSolutions_st if x[14]<=0.5 and (abs(x[16]-x[15])<=0.5)]
    if len(allSolutions_st_veryLimited) > 0:
        allSolutions_st = allSolutions_st_veryLimited
    else:
        allSolutions_st_limited = [x for x in allSolutions_st if x[14]<=0.5]
        if len(allSolutions_st_limited) > 0:
            allSolutions_st = allSolutions_st_limited

                                                            # x[14] = diffQMean
    allSolutions_st = sorted(allSolutions_st, key=lambda x: (x[14], x[5], x[2], x[3]))
    
    # Get Layouts que cumplen que sus estadisticas mas importantes son 'b'
    bestLayouts = bck_2R_getLayoutsByStatistics(allSolutions_st, b)
    
    # De todos los layouts, elegir uno aleatoriamente
    randIndex = random.randint(0,len(bestLayouts)-1)
    bestLayout = bestLayouts[randIndex][0] 

    return bestLayout
    
def bck_2R_getCorridorsList(solution):
    corridors = []
    corridors_1 = []
    corridors_2 = []
    for i in range(len(solution)):
        row = solution[i]
        for j in range(len(row)):
            pos = row[j]
            if pos[0] in ['A', 'B', 'C', 'D']:
                corridors.append(2)
                if i == 0:
                    corridors_1.append(2)
                elif i == 1:
                    corridors_2.append(2)
            elif pos[0] in ['E', 'F', 'G', 'H']:
                corridors.append(3)
                if i == 0:
                    corridors_1.append(3)
                elif i == 1:
                    corridors_2.append(3)
            elif pos[0] == 'I':
                corridors.append(4)
                if i == 0:
                    corridors_1.append(4)
                elif i == 1:
                    corridors_2.append(4)
            elif pos[0] == 'J':
                corridors.append(1)
                if i == 0:
                    corridors_1.append(1)
                elif i == 1:
                    corridors_2.append(1)

    return corridors, corridors_1, corridors_2    

def bck_2R_getLayoutsByStatistics(allSolutions_st, b):      # Ídem a la versión 1R
    
    # Media de los cuartiles
    a = allSolutions_st
    c = [x for x in a if x[5]==b]
    
    if len(c) == 0:
        d = [x for x in a if x[5]<b]
            # Por si no hay ninguna configuración cuya media sea menor a la dada
        b_aux = b
        while len(d)==0  and  b_aux<b+10:
            b_aux += 0.5            
            d = [x for x in a if x[5]<b_aux]
        if len(d) == 0:
            raise SolutionNotFoundError()
        maxQC = max(d, key=lambda x: x[5])  # Nos quedamos con el máximo de pasillos
        c = [x for x in d if x[5]==maxQC[5]]
        
    # Mediana
    a = c
    c = [x for x in a if x[3]==b]

    if len(c) == 0:
        d = [x for x in a if x[3]<b]
            # Por si no hay ninguna configuración cuya media sea menor a la dada
        b_aux = b
        while len(d)==0  and  b_aux<b+10:
            b_aux += 0.5            
            d = [x for x in a if x[3]<b_aux]
        if len(d) == 0:
            raise SolutionNotFoundError()
        maxMd = max(d, key=lambda x: x[3])  # Nos quedamos con el máximo de pasillos
        c = [x for x in d if x[3]==maxMd[3]]

    # Media
    a = c
    c = [x for x in a if x[2]==b]

    if len(c) == 0:
        d = [x for x in a if x[2]<b]
            # Por si no hay ninguna configuración cuya media sea menor a la dada
        b_aux = b
        while len(d)==0  and  b_aux<b+10:
            b_aux += 0.5            
            d = [x for x in a if x[2]<b_aux]
        if len(d) == 0:
            raise SolutionNotFoundError()
        maxMn = max(d, key=lambda x: x[2])  # Nos quedamos con el máximo de pasillos
        c = [x for x in d if x[2]==maxMn[2]]

    return c


##########
# X ROWS #
##########

def bck_gr_getRandomBestLayout(allSolutions, b, nRows):
    # Get metricas de las soluciones
    allSolutions_st = []
    for s in allSolutions:

        corridors, corridors_row = bck_gr_getCorridorsList(s, nRows)
        
        corrMean = st.fmean(corridors)
        corrMedian = st.median(corridors)
        corrQuantiles = st.quantiles(corridors)
        corrQuantilesMean = st.mean(corrQuantiles)
        sol_st = [s,corridors, corrMean,corrMedian,corrQuantiles,corrQuantilesMean]
        
        corridors_row_stats = []
        corrQuantilesMean = [] 
        diffQ3Q1 = []
        for i in range(nRows):
            corrMean_n = st.fmean(corridors_row[i])
            corridors_row_stats.append(corrMean_n)
            
            corrMedian_n = st.median(corridors_row[i])
            corridors_row_stats.append(corrMedian_n)
            
            corrQuantiles_n = st.quantiles(corridors_row[i])
            corridors_row_stats.append(corrQuantiles_n)
            
            corrQuantilesMean_n = st.mean(corrQuantiles_n)
            corridors_row_stats.append(corrQuantilesMean_n)
            corrQuantilesMean.append(corrQuantilesMean_n)

            corrDiffQ3Q1_n = corrQuantiles_n[2]-corrQuantiles_n[0]
            diffQ3Q1.append(corrDiffQ3Q1_n)
            
        maxQuantilesMean = max(corrQuantilesMean)
        minQuantilesMean = min(corrQuantilesMean)
        diffQuantilesMean = maxQuantilesMean-minQuantilesMean
        quantiles = [maxQuantilesMean, minQuantilesMean, diffQuantilesMean]

        maxDiffQ3Q1 = max(diffQ3Q1)
        minDiffQ3Q1 = min(diffQ3Q1)
        diffDiffQ3Q1 = maxDiffQ3Q1-minDiffQ3Q1
        diffs = [maxDiffQ3Q1, minDiffQ3Q1, diffDiffQ3Q1]

        sol_st = sol_st + corridors_row_stats + quantiles + diffs
        allSolutions_st.append(sol_st)

    indDiffQMean = len(allSolutions_st[0])-3-1   # -3(diffs) -1(array empieza en 0)
    indDiffQ3Q1 = len(allSolutions_st[0])-1
    allSolutions_st_veryLimited = [x for x in allSolutions_st if x[indDiffQMean]<=1 and x[indDiffQ3Q1]<=1]
    if len(allSolutions_st_veryLimited) > 0:
        allSolutions_st = allSolutions_st_veryLimited
    else:
        allSolutions_st_limited = [x for x in allSolutions_st if x[indDiffQMean]<=1]
        if len(allSolutions_st_limited) > 0:
            allSolutions_st = allSolutions_st_limited

    allSolutions_st = sorted(allSolutions_st, key=lambda x: (x[indDiffQMean], x[5], x[2], x[3]))
    
    # Get Layouts que cumplen que sus estadisticas mas importantes son 'b'
    bestLayouts = bck_gr_getLayoutsByStatistics(allSolutions_st, b)
    
    # De todos los layouts, elegir uno aleatoriamente
    randIndex = random.randint(0,len(bestLayouts)-1)
    bestLayout = bestLayouts[randIndex][0] 

    return bestLayout
    
def bck_gr_getCorridorsList(solution, nRows):      # Es igual al 1R
    corridors = []
    corridors_row = []
    for i in range(nRows):
        corridors_row.append([])
    for i in range(len(solution)):
        row = solution[i]
        for j in range(len(row)):
            pos = row[j]
            if pos[0] in ['A', 'B', 'C', 'D']:
                corridors.append(2)
                corridors_row[i].append(2)
            elif pos[0] in ['E', 'F', 'G', 'H']:
                corridors.append(3)
                corridors_row[i].append(3)
            elif pos[0] == 'I':
                corridors.append(4)
                corridors_row[i].append(4)
            elif pos[0] == 'J':
                corridors.append(1)
                corridors_row[i].append(1)

    return corridors, corridors_row    

def bck_gr_getLayoutsByStatistics(allSolutions_st, b):      # Ídem a la versión 1R
    
    # Media de los cuartiles
    a = allSolutions_st
    c = [x for x in a if x[5]==b]
    
    if len(c) == 0:
        d = [x for x in a if x[5]<b]
            # Por si no hay ninguna configuración cuya media sea menor a la dada
        b_aux = b
        while len(d)==0  and  b_aux<b+10:
            b_aux += 0.5            
            d = [x for x in a if x[5]<b_aux]
        if len(d) == 0:
            raise SolutionNotFoundError()
        maxQC = max(d, key=lambda x: x[5])  # Nos quedamos con el máximo de pasillos
        c = [x for x in d if x[5]==maxQC[5]]

    # Mediana
    a = c
    c = [x for x in a if x[3]==b]

    if len(c) == 0:
        d = [x for x in a if x[3]<b]
            # Por si no hay ninguna configuración cuya media sea menor a la dada
        b_aux = b
        while len(d)==0  and  b_aux<b+10:
            b_aux += 0.5            
            d = [x for x in a if x[3]<b_aux]
        if len(d) == 0:
            raise SolutionNotFoundError()
        maxMd = max(d, key=lambda x: x[3])  # Nos quedamos con el máximo de pasillos
        c = [x for x in d if x[3]==maxMd[3]]

    # Media
    a = c
    c = [x for x in a if x[2]==b]

    if len(c) == 0:
        d = [x for x in a if x[2]<b]
            # Por si no hay ninguna configuración cuya media sea menor a la dada
        b_aux = b
        while len(d)==0  and  b_aux<b+10:
            b_aux += 0.5            
            d = [x for x in a if x[2]<b_aux]
        if len(d) == 0:
            raise SolutionNotFoundError()
        maxMn = max(d, key=lambda x: x[2])  # Nos quedamos con el máximo de pasillos
        c = [x for x in d if x[2]==maxMn[2]]

    return c