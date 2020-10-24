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

import config as cf
from App import model
import datetime
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________
def init():
    """
    Llama la funcion de inicializacion del modelo.
    """
    analyzer = model.newAnalyzer()
    return analyzer
# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________
def loadData(analyzer, accidents_file):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    accidents_file = cf.data_dir + accidents_file
    input_file = csv.DictReader(open(accidents_file, encoding="utf-8"),
                                delimiter=",")
    for accidente in input_file:
        model.addaccidente(analyzer, accidente)
    return analyzer
# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________
def accidentesSize(analyzer):
    """
    Numero de accidentes leidos
    """
    return model.accidentesSize(analyzer)

def indexHeight(analyzer):
    """
    Altura del indice (arbol)
    """
    return model.indexHeight(analyzer)

def minKey(analyzer):

    return model.minKey(analyzer)

def getaccidentesByRangeCode(analyzer, StartDate, severity):
    """
    Retorna el total de accidentes de un tipo especifico en una
    fecha determinada
    """
    StartDate = datetime.datetime.strptime(StartDate, '%Y-%m-%d')
    return model.getaccidentesByRangeCode(analyzer, StartDate.date(), severity)
    
def getAccidentsByRange(analyzer, initialDate, finalDate):
    """
    Retorna el total de crimenes en un rango de fechas
    """
    initialDate= datetime.datetime.strptime(initialDate, "%Y-%m-%d")
    finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
    return model.getAccidentsByRange(analyzer, initialDate.date(),finalDate.date())

def getAccidentsByRangeHour(analyzer, initialDate, finalDate):
    """
    Retorna el total de crimenes en un rango de fechas
    """
    initialDate= datetime.time(hour=int(initialDate[0]),minute=int(initialDate[1]),second=59)
    finalDate = datetime.time(hour=int(finalDate[0]),minute=int(finalDate[1]),second=59)
    return model.getAccidentsByRangeHour(analyzer, initialDate,finalDate)

def getAccidentsByRangeState(analyzer, initialDate, finalDate):
    """
    Retorna el total de crimenes en un rango de fechas
    """
    initialDate= datetime.datetime.strptime(initialDate, "%Y-%m-%d")
    finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
    return model.getAccidentsByState(analyzer, initialDate.date(),finalDate.date())

def getAccidentsBeforeDate (analyzer, finalDate):
    final = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
    finalDate = final.date()
    model.getAccidentsBeforeDate(analyzer, finalDate)

def getaccidentesByDistance(analyzer,lon,lat,R):
    
    model.getAccidentsByDistance(analyzer,lon,lat,R)

def getsizeaccidentes(analyzer):
    return model.accidentesSize(analyzer)

def getInitialDate(analyzer):
    initialDate=model.minKey(analyzer)
    initialDate=str(initialDate.strftime("%Y-%m-%d"))
    return initialDate