import folium
import webbrowser
import os
from typing import NamedTuple, Tuple, List, Set, Dict

def crea_mapa(latitud:float, longitud:float, zoom:int=15)->folium.Map:
    '''    
    Función que crea un mapa folium que está centrado en la latitud y longitud
    dados como parámetro y mostrado con el nivel de zoom dado.
    ENTRADA:
        :param latitud: promedio de las latitudes de todas las estaciones 
        :param longitud: promedio de las longitudes del todas las estaciones
        :param zoom: nivel del zoom con el que se visualiza el mapa en la pantalla
    SALIDA:
        :return: objeto mapa creado
    '''    
    mapa = folium.Map(location=[latitud, longitud], zoom_start=zoom)
    return mapa

def crea_marcador (latitud:int, longitud:int, etiqueta:str, color:str='red')->folium.Marker:
    '''
    Función que crea un marcador del color que se indica en el cuarto parámetro, en el punto de
    coordenada de la latitud y la longitud que se pasen en los dos primeros parámetro y con el texto
    que se pase en la etiqueta.
    
    ENTRADA:
        :param latitud: latitud del marcador
        :param longitud: longitud del marcador
        :param etiqueta: texto de la etiqueta que se asociará al marcador
        :param color: nombre del color del marcador en inglés 

    SALIDA:
        :return: objeto marcador creado
    '''
    marcador = folium.Marker([latitud,longitud], popup=etiqueta, 
                            icon=folium.Icon(color=color, icon='info-sign')) 
    return marcador     

def guarda_mapa_y_abre_en_navegador(mapa:folium.Map, ruta_fichero:str)->None:
    '''Guarda un mapa como archivo en formato html e intenta abrirlo
       directamente con un navegador web
    ENTRADA:
        :param mapa: Objeto mapa a guardar
        :param ruta_fichero: Nombre con la ruta del fichero

    SALIDA:
        ninguna
    '''
    mapa.save(ruta_fichero)
    webbrowser.open("file://" + os.path.realpath(ruta_fichero))