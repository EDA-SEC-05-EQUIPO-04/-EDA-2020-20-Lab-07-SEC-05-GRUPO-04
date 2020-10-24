"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """
import config
from DISClib.ADT import list as lt
import numpy as np
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
from DISClib.DataStructures import listiterator as it
import numpy as np
import datetime
assert config


"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria


"""


# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------
def newAnalyzer():
    """ Inicializa el analizador
    Crea una lista vacia para guardar todos los accidentes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas
    Retorna el analizador inicializado.
    """
    analyzer = {'accidentes': None,
                'dateIndex': None,
                'hourIndex':None }

    analyzer['accidentes'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer['dateIndex'] = om.newMap(omaptype='BST',
                                      comparefunction=compareDates)
    analyzer['hourIndex'] = om.newMap(omaptype='BST',
                                      comparefunction=compareDates)
    analyzer['distanceIndex'] = om.newMap(omaptype='BST',
                                      comparefunction=compareDates)

    return analyzer
# Funciones para agregar informacion al catalogo
def addaccidente(analyzer, accidente):
    lt.addLast(analyzer['accidentes'], accidente)
    updateDateIndex(analyzer['dateIndex'], accidente)
    updateHourIndex(analyzer['hourIndex'], accidente)
    return analyzer

def addaccidenteDistance(analyzer, accidente,R):
    lt.addLast(analyzer['accidentes'], accidente)
    updateDateIndex(analyzer['dateIndex'], accidente)
    updateHourIndex(analyzer['hourIndex'], accidente)
    updateDistanceIndex(analyzer['distanceIndex'], accidente,R)
    return analyzer

def updateDateIndex(map, accidente):
    occurreddate = accidente['Start_Time']
    accidentedate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, accidentedate.date())
    if entry is None:
        datentry = newDataEntry(accidente)
        om.put(map, accidentedate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, accidente)
    return map

def updateHourIndex(map, accidente):
    occurreddate = roundingtime(accidente['Start_Time'])    
    accidentedate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, accidentedate.time())
    if entry is None:
        datentry = newDataEntry(accidente)
        om.put(map, accidentedate.time(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, accidente)
    return map

def updateDistanceIndex(map, accidente, R):  
    entry = om.get(map,R)
    if entry is None:
        datentry = newDataEntry(accidente)
        om.put(map, R, datentry)
    else:
        datentry = me.getValue(entry)
    addDistanceIndex(datentry, accidente)
    return map

def updateHourIndex(map, accidente):
    occurreddate = roundingtime(accidente['Start_Time']).split(" ")[1]
    accidentedate = datetime.datetime.strptime(occurreddate, '%H:%M:%S')
    entry = om.get(map, accidentedate.time())
    if entry is None:
        datentry = newDataEntry(accidente)
        om.put(map, accidentedate.time(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, accidente)
    return map

def addDateIndex(datentry, accidente):
    lst = datentry['lstaccidentes']
    lt.addLast(lst, accidente)

    severityIndex = datentry['severityIndex']
    severityentry = m.get(severityIndex, accidente['Severity'])
    if (severityentry is None):
        entry = newseverityEntry(accidente['Severity'], accidente)
        lt.addLast(entry['lstseverity'], accidente)
        m.put(severityIndex, accidente['Severity'], entry)
    else:
        entry = me.getValue(severityentry)
        lt.addLast(entry['lstseverity'], accidente)

    stateIndex = datentry['stateIndex']
    stateentry = m.get(stateIndex, accidente['State'])
    if (stateentry is None):
        entry = newstateEntry(accidente['State'], accidente)
        lt.addLast(entry['lststate'], accidente)
        m.put(stateIndex, accidente['State'], entry)
    else:
        entry = me.getValue(stateentry)
        lt.addLast(entry['lststate'], accidente)
    return datentry

def addDistanceIndex(datentry, accidente):
    lst = datentry['lstaccidentes']
    lt.addLast(lst, accidente)

    severityIndex = datentry['severityIndex']
    severityentry = m.get(severityIndex, accidente['Start_Time'])
    if (severityentry is None):
        entry = newseverityEntry(accidente['Start_Time'], accidente)
        lt.addLast(entry['lstseverity'], accidente)
        m.put(severityIndex, accidente['Start_Time'], entry)
    else:
        entry = me.getValue(severityentry)
        lt.addLast(entry['lstseverity'], accidente)

def addTimeIndex(datentry, accidente):
    lst = datentry['lstaccidentes']
    lt.addLast(lst, accidente)

    severityIndex = datentry['severityIndex']
    severityentry = m.get(severityIndex, accidente['Severity'])
    if (severityentry is None):
        entry = newseverityEntry(accidente['Severity'], accidente)
        lt.addLast(entry['lstseverity'], accidente)
        m.put(severityIndex, accidente['Severity'], entry)
    else:
        entry = me.getValue(severityentry)
        lt.addLast(entry['lstseverity'], accidente)

    stateIndex = datentry['stateIndex']
    stateentry = m.get(stateIndex, accidente['State'])
    if (stateentry is None):
        entry = newstateEntry(accidente['State'], accidente)
        lt.addLast(entry['lststate'], accidente)
        m.put(stateIndex, accidente['State'], entry)
    else:
        entry = me.getValue(stateentry)
        lt.addLast(entry['lststate'], accidente)
    return datentry

def newDataEntry(accidente):
    entry = {'severityIndex': None, 'lstaccidentes': None,'stateIndex':None}
    entry['severityIndex'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareseverity)
    entry['lstaccidentes'] = lt.newList('SINGLE_LINKED', compareDates)
    entry['stateIndex'] =m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareseverity)
    return entry

def newseverityEntry(severity, accidente):
    severityentry = {'severity': None, 'lstseverity': None}
    severityentry['severity'] = severity
    severityentry['lstseverity'] = lt.newList('SINGLELINKED', compareseverity)
    return severityentry

def newstateEntry(severity, accidente):
    severityentry = {'state': None, 'lststate': None}
    severityentry['state'] = severity
    severityentry['lststate'] = lt.newList('SINGLELINKED', compareseverity)
    return severityentry
# ==============================
# Funciones de consulta
# ==============================
def accidentesSize(analyzer):
    """
    Número de accidentes leidos
    """
    return lt.size(analyzer['accidentes'])

def indexHeight(analyzer):
    """
    Altura del indice (arbol)
    """
    return om.height(analyzer['dateIndex'])

def getaccidentesByRangeCode(analyzer, StartDate, severity):
    """
    Para una fecha determinada, retorna el numero de accidentes
    de un tipo especifico.
    """
    accidentedate = om.get(analyzer['dateIndex'], StartDate)
    if accidentedate['key'] is not None:
        severitymap = me.getValue(accidentedate)['severityIndex']
        numaccidentes = m.get(severitymap, severity)
        if numaccidentes is not None:
            return m.size(me.getValue(numaccidentes)['lstseverity'])
        return 0

def getaccidentesByRangeCodeHour(analyzer, StartDate, severity):
    """
    Para una fecha determinada, retorna el numero de accidentes
    de un tipo especifico.
    """
    accidentedate = om.get(analyzer['hourIndex'], StartDate)
    if accidentedate['key'] is not None:
        severitymap = me.getValue(accidentedate)['severityIndex']
        numaccidentes = m.get(severitymap, severity)
        if numaccidentes is not None:
            return m.size(me.getValue(numaccidentes)['lstseverity'])
        return 0

def getaccidentesByRangeState(analyzer, StartDate):
    """
    Para una fecha determinada, retorna el numero de accidentes
    de un tipo especifico.
    """
    accidentedate = om.get(analyzer['dateIndex'], StartDate)
    if accidentedate['key'] is not None:
        statemap = me.getValue(accidentedate)['stateIndex']
        return statemap

def getAccidentsByRange(analyzer, initialDate, fecha_final):
    lst = om.values(analyzer['dateIndex'], initialDate, fecha_final)
    lstiterator = it.newIterator(lst)
    tot_accidents = 0
    mapa=om.newMap(comparefunction=compareIds)
    mapa2=om.newMap(comparefunction=compareIds)
    while (it.hasNext(lstiterator)):
        lstdate  = it.next(lstiterator)
        accidentes_max=0
        i = 1
        while i <= 4:
            num=getaccidentesByRangeCode(analyzer,lstdate,str(i))
            tot_accidents += num
            accidentes_max+=num
            i += 1
            if om.contains(mapa2,i):
                om.put(mapa2,i,int(om.get(mapa2,i)['value'])+num)
            else:
                om.put(mapa2,i,num)
        om.put(mapa,accidentes_max,str(lstdate))
    resu=om.newMap(comparefunction=compareIds)
    max_sev=0
    sev=0
    for i in range (1,5):
        if om.contains(mapa2,i):
            val=om.get(mapa2,i)
            if val['value']>max_sev:
                max_sev=val['value']
                sev=i
    om.put(resu,sev,max_sev)
    return tot_accidents,om.get(mapa,om.maxKey(mapa)),om.get(resu,sev)

def getAccidentsByRangeHour(analyzer, initialDate, fecha_final):
    lst = om.values(analyzer['hourIndex'], initialDate, fecha_final)
    lstiterator = it.newIterator(lst)
    tot_accidents = 0
    mapa=om.newMap(comparefunction=compareIds)
    mapa2=om.newMap(comparefunction=compareIds)
    while (it.hasNext(lstiterator)):
        lstdate  = it.next(lstiterator)
        accidentes_max=0
        i = 1
        while i <= 4:
            num=getaccidentesByRangeCodeHour(analyzer,lstdate,str(i))
            tot_accidents += num
            accidentes_max+=num
            i += 1
            if om.contains(mapa2,i):
                om.put(mapa2,i,int(om.get(mapa2,i)['value'])+num)
            else:
                om.put(mapa2,i,num)
        om.put(mapa,accidentes_max,str(lstdate))
    resu=om.newMap(comparefunction=compareIds)
    max_sev=0
    sev=0
    for i in range (1,6):
        if om.contains(mapa2,i):
            val=om.get(mapa2,i)
            if val['value']>max_sev:
                max_sev=val['value']
                sev=i
            om.put(resu,i,val['value'])
        else:
            om.put(resu,i,0)
    om.put(resu,sev,max_sev)

    return tot_accidents,om.get(mapa,om.maxKey(mapa)),resu

def updateAccidentsByDistance(analyzer,lon1,lat1,R):
    accidentes=analyzer['accidentes']
    iterator= it.newIterator(accidentes)
    while it.hasNext(iterator):
        accidente=it.next(iterator)
        lat2 = accidente['Start_Lat']
        lon2 = accidente['Start_Lng']
        
        dist=dinstancefunction(float(lat1),float(lon1),np.radians(float(lat2)),np.radians(float(lon2)))
        updateDistanceIndex(analyzer['distanceIndex'],accidente,dist)
    mapasemana=om.newMap(comparefunction=compareIds)
    lst = om.values(analyzer['distanceIndex'],0, R)
    lstiterator = it.newIterator(lst)
    while it.hasNext(lstiterator):
        element=it.next(lstiterator)
        mapa=om.get(analyzer['distanceIndex'],element)['value']['severityIndex']
        listafechas=m.keySet(mapa)
        listaiterator=it.newIterator(listafechas)
        while it.hasNext(listaiterator):
            fecha=it.next(listaiterator)
            dia=datetime.datetime.strptime(fecha.split(" ")[0], '%Y-%m-%d').weekday()
            if om.contains(mapasemana,int(dia)):
                om.put(mapasemana,dia,int(om.get(mapasemana,dia)['value'])+1)
            else:
                om.put(mapasemana,dia,1)
    tot_accidents = 0
    
    
    return mapasemana
    
def getAccidentsByDistance(analyzer,lon1,lat1,R):
    return updateAccidentsByDistance(analyzer,lon1,lat1,R)

def getAccidentsByState(analyzer, initialDate, fecha_final):
    lst = om.values(analyzer['dateIndex'], initialDate, fecha_final)
    lstiterator = it.newIterator(lst)
    tot_accidents = 0
    mapaState=om.newMap(comparefunction=compareState)
    mapallaves=m.newMap(comparefunction=compareState)
    while (it.hasNext(lstiterator)):
        lstdate  = it.next(lstiterator)
        states=getaccidentesByRangeState(analyzer,lstdate)
        llaves=m.keySet(states)
        iterator=it.newIterator(llaves)
        while it.hasNext(iterator):
            state=it.next(iterator)
            m.put(mapallaves,state,state)
            numstate=lt.size(m.get(states,state)['value']['lststate'])  
            if om.contains(mapaState,state):
                om.put(mapaState,state,int(om.get(mapaState,state)['value'])+numstate)
            else:
                om.put(mapaState,state,int(numstate))
    statemax=""
    nummax=0
    llaves=m.keySet(mapallaves)
    iterator=it.newIterator(llaves)
    while it.hasNext(iterator):
       state=it.next(iterator)
       if int(om.get(mapaState,state)['value'])>nummax:
           statemax=state
           nummax=om.get(mapaState,state)['value']
    return statemax,nummax

def getAccidentsBeforeDate(analyzer, fecha_final):

    inicio = datetime.datetime.strptime(str(om.minKey(analyzer['dateIndex'])), '%Y-%m-%d')
    iniciodate = inicio.date()
    lst = getAccidentsByRange(analyzer, iniciodate, fecha_final)
    return lst
# ==============================
# Funciones de Comparacion
# ==============================
def compareIds(id1, id2):
    """
    Compara dos accidentes
    """
    if type(id2)==type("a"):
        id2=int(id2)
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

def compareDates(date1, date2):

    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def compareState(date1, date2):
    if type(date2) == type({'a':1}):
        date2=date2['key'] 
    if (date1 == date2):
        return 0
    elif (date1> date2):
        return 1
    else:
        return -1

def compareseverity(severity1, severity2):
    """
    Compara dos ids , id es un identificador
    y entry una pareja llave-valor
    """
    severity = me.getKey(severity2)
    if (severity1 == severity):
        return 0
    elif (severity1 > severity):
        return 1
    else:
        return -1
    
def minKey(analyzer):
    """
    Llave mas pequeña
    """
    return om.minKey(analyzer['dateIndex'])

def roundingtime(x,base=30):
    x=x.split(" ")
    var=x[1].split(":")
    if round(int(var[1])/30)==0 :
        x[1]="{:02d}".format(int(var[0]))+":"+"00"+":"+var[2]
    elif round(int(var[1])/30)==1:
        x[1]="{:02d}".format(int(var[0]))+":"+str(30)+":"+var[2]
    else:
        if int(var[0]) <=22:
            x[1]="{:02d}".format(int(var[0])+1)+":"+"00"+":"+var[2]
        else:
            var2=x[0].split("-")
            x[0]=var2[0]+"-"+var2[1]+"-"+"{:02d}".format(int(var2[2])+1)
    return x[0]+" "+x[1]

def dinstancefunction(lat1,lon1,lat2,lon2):
    R=3958.8
    return np.arccos(np.sin(lat1)*np.sin(lat2)+np.cos(lat1)*np.cos(lat2)*np.cos(lon1-lon2))*R