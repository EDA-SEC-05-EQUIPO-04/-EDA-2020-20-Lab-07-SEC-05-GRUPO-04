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
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
from DISClib.DataStructures import listiterator as it
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
                'dateIndex': None
                }

    analyzer['accidentes'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer['dateIndex'] = om.newMap(omaptype='BST',
                                      comparefunction=compareDates)
    return analyzer

# Funciones para agregar informacion al catalogo

def addaccidente(analyzer, accidente):

    lt.addLast(analyzer['accidentes'], accidente)
    updateDateIndex(analyzer['dateIndex'], accidente)
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
    return datentry

def newDataEntry(accidente):


    entry = {'severityIndex': None, 'lstaccidentes': None}
    entry['severityIndex'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareseverity)
    entry['lstaccidentes'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry


def newseverityEntry(severity, accidente):


    severityentry = {'severity': None, 'lstseverity': None}
    severityentry['severity'] = severity
    severityentry['lstseverity'] = lt.newList('SINGLELINKED', compareseverity)
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


def getAccidentsByRange2(analyzer, initialDate, fecha_final):
    lst = om.values(analyzer['dateIndex'], initialDate, fecha_final)
    lstiterator = it.newIterator(lst)
    tot_accidents = 0
    serv_1 = 0
    serv_2 = 0
    serv_3 = 0
    serv_4 = 0
    while (it.hasNext(lstiterator)):
        lstdate  = it.next(lstiterator)
        i = 1
        while i <= 4:
            if i == 1:
                serv_1 += getaccidentesByRangeCode(analyzer,lstdate,str(i))
            elif i == 2:
                serv_2 += getaccidentesByRangeCode(analyzer,lstdate,str(i))
            elif i == 3:
                serv_3 += getaccidentesByRangeCode(analyzer,lstdate,str(i))
            else:
                serv_4 += getaccidentesByRangeCode(analyzer,lstdate,str(i))
            tot_accidents += getaccidentesByRangeCode(analyzer,lstdate,str(i))
            i += 1
    severidad_repetida = serv_2,2
    if serv_1 > severidad_repetida[0]:
        severidad_repetida = serv_1,1
    elif serv_3 > severidad_repetida[0]:
        severidad_repetida = serv_3,3
    elif serv_4 > severidad_repetida[0]:
        severidad_repetida = serv_4,4
    return tot_accidents,severidad_repetida


def getAccidentsByRange(analyzer, initialDate, fecha_final):
    lst = om.values(analyzer['dateIndex'], initialDate, fecha_final)
    lstiterator = it.newIterator(lst)
    tot_accidents = 0
    
    mayor = 0
    while (it.hasNext(lstiterator)):
        lstdate  = it.next(lstiterator)
        accidents_fecha = 0
        i = 1
        while i <= 4:
            accidents_fecha += getaccidentesByRangeCode(analyzer,lstdate,str(i))
            tot_accidents += getaccidentesByRangeCode(analyzer,lstdate,str(i))
            i += 1
        if accidents_fecha > mayor:
            mayor = accidents_fecha
            fecha_mas_acc = lstdate
    return tot_accidents,mayor,fecha_mas_acc

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