# Ejercicio: Servicio de alquiler de bicicletas públicas de Sevilla (Sevici)
**Autor**: Mariano González.      **Revisores**: Carlos G. Vallejo, José A. Troyano, Fermín Cruz, Toñi Reina.     **Última modificación:** 04/10/2023

## Requisitos previos
En este ejercicio vamos a trabajar con mapas, para lo que usaremos la librería ```folium``` . Para instalar la librería ```folium``` abre una ventana de comandos de Anaconda (Anaconda Prompt) y ejecuta el siguiente comando:
```
pip install folium
```
O si tu instalador es conda
```
conda install –c conda-forge folium
```

En este ejercicio vamos a trabajar con la red de estaciones del servicio de alquiler de bicicletas de Sevilla, Sevici. Para ello disponemos de los datos de las estaciones, obtenidos de [https://citybik.es/](https://citybik.es/).

En primer lugar leeremos los datos de las estaciones desde un fichero CSV. Realizaremos algunas operaciones con los datos, como obtener las estaciones con bicicletas libres o las estaciones más próximas a nuestra ubicación. Finalmente, dibujaremos sobre el mapa las estaciones, distinguiendo entre las que tienen bicicletas disponibles y las que no las tienen.

Como es habitual crearemos los múdulos Python **sevice.py** y **sevici_test.py** para implementar y probar las siguientes funciones a desarrollar:

1. **lee_estaciones**: lee los datos de las estaciones desde un fichero csv
2. **estaciones_bicis_libres**: crea una lista con las estaciones que tienen bicicletas libres, ordenada por el número de bicis libres
3. **calcula_distancia**: calcular la distancia a una estación desde un punto dado
4. **estaciones_cercanas**: crea una lista con las estaciones con bicis libres más cercanas a un punto dado, ordenadas de la más cercana a la más lejana
5. **media_coordenadas**: devuelve una coordenada cuya latitud es la media de las latitudes y cuya longitud es la media de las longitudes.


## 1. Carga de datos
Se dispone de los datos de las estaciones de la red de Sevici. Los datos se encuentran en un fichero CSV. Cada línea del fichero contiene seis datos:

    Nombre de la estación
    Número total de bornetas de la estación
    Número de bornetas vacías
    Número de bicicletas disponibles
    Latitud
    Longitud

Los datos dependen del instante en que se obtiene el fichero, ya que el número de bicicletas y bornetas libres varía de forma continua. Estan serían, por ejemplo, las primeras líneas del fichero en un momento dado:

        name,slots,empty_slots,free_bikes,latitude,longitude
        149_CALLE ARROYO,20,11,9,37.397829929383,-5.97567172039552
        257_TORRES ALBARRACIN,20,16,4,37.38376948792722,-5.908921914235877
        243_GLORIETA DEL PRIMERO DE MAYO,15,6,9,37.380439481169994,-5.953481197462845
        109_AVENIDA SAN FRANCISCO JAVIER,15,1,14,37.37988413609134,-5.974382770011586
        073_PLAZA SAN AGUSTIN,15,10,4,37.38951386231434,-5.984362789545622

Los principales aspectos que tendremos que resolver a la hora de procesar estos datos de entrada serán saltar la línea de encabezado del fichero, separar adecuadamente los campos mediante las comas e interpretar el formato de cada uno de los campos, que puede ser de tipo cadena, entero o real.

Para resolver estos problemas haremos uso de algunas utilidades disponibles en la librería estándar de Python. En concreto, antes de empezar, deberemos importar los siguientes elementos:


```
import csv
import math 
import folium
from typing import NamedTuple, Tuple, List, Set, Dict
```

### 1.1 Definición de tipos basados en ```NamedTuple```

 Como el trabajar con coordenadas es algo frecuente, vamos a definir una tupla con nombre llamada ```Coordenadas``` que representa una coordenada con latitud y longitud. Además, definiremos también una tupla con nombre ```Estacion``` que representa una de las estaciones de bicicletas repartidas por la ciudad, con los campos ```nombre```, ```bornetas```, ```bornetas_vacias```, ```bicis_diponibles``` y ```coordenadas```. Fíjate en que este último representa a una coordenada compuesta por latitud y longitud, es decir, será de tipo ```Coordenadas```.


```python
Coordenadas = NamedTuple('Coordenadas', [('latitud',float),('longitud',float)])
y
Estación = NamedTuple('Estación', [('nombre',str),('bornetas',int),('bornetas_vacías',int),
                      ('bicis_disponibles',int),('coordenadas',Coordenadas)])
```

### 1.2 Lectura de fichero

La siguiente función será la encargada de leer el fichero con las estaciones y construir a partir de él una estructura de datos en memoria.


```python

# Función de lectura que crea una lista de Estaciones
def lee_estaciones(ruta:str)->List[Tuple[Estación]]:
    Lee el fichero de datos (incluida la ruta) y devuelve una lista de estaciones
    
    ENTRADA: 
       :param ruta: ruta del fichero a leer 
       :type fichero: str
   
    SALIDA: 
       :return: Lista de tuplas de tipo Estación
    
    Cada estación se representa con una tupla con los siguientes valores:
    - Nombre de la estación
    - Número total de bornetas
    - Número de bornetas vacías
    - Número de bicicletas disponibles
    - Coordenadas
```

Resultados esperados:
```
Estaciones leídas 257
Las tres primeras son :
Estacion(nombre='149_CALLE ARROYO', bornetas=20, bornetas_vacias=11, bicis_disponibles=9, coordenadas=Coordenadas(latitud=37.397829929383, longitud=-5.97567172039552))
Estacion(nombre='257_TORRES ALBARRACIN', bornetas=20, bornetas_vacias=16, bicis_disponibles=4, coordenadas=Coordenadas(latitud=37.38376948792722, longitud=-5.908921914235877))
Estacion(nombre='243_GLORIETA DEL PRIMERO DE MAYO', bornetas=15, bornetas_vacias=6, bicis_disponibles=9, coordenadas=Coordenadas(latitud=37.380439481169994, longitud=-5.953481197462845))
Las tres últimas son :
Estacion(nombre='203_CALLE TESALÓNICA', bornetas=20, bornetas_vacias=7, bicis_disponibles=13, coordenadas=Coordenadas(latitud=37.396093518802566, longitud=-5.958764096016824))
Estacion(nombre='145_AVENIDA REINA MERCEDES', bornetas=20, bornetas_vacias=4, bicis_disponibles=16, coordenadas=Coordenadas(latitud=37.360233228861155, longitud=-5.986318234050904))
Estacion(nombre='048_CALLE CHURRUCA', bornetas=15, bornetas_vacias=11, bicis_disponibles=3, coordenadas=Coordenadas(latitud=37.39715651121527, longitud=-5.991066209916829))
```

## 2. Operaciones de consulta

En esta sección veremos una serie de funciones que nos permitirán filtrar y extraer informaciones de la estructura de datos que estamos manejando para representar las estaciones (una lista de tuplas). Utilizaremos estas funciones de _consulta_ en distintos puntos del resto del ejercicio.

### 2.1 Estaciones con bicicletas libres

La primera función recibirá una lista de tuplas de tipo Estación y un entero h, y devolverá una lista con datos de las estaciones que tienen un número de bicicletas disponibles igual o superior al entero dado, que por defecto será 5. La lista de salida estará formada por tuplas con dos elementos, el número de bicicletas disponibles y el nombre de la estación, y estará ordenada por el número de bicicletas disponibles


```
def estaciones_bicis_libres(estaciones:List[Estación], k:int=5)->List[Tuple[int,str]]: 
```

Cree un método `test_estaciones_bicis_libres` en un módulo sevici_test, que tome como entrada una lista de tuplas de tipo Estacion, de las leídas a partir del archivo, y muestre una salida por consola como la siguiente (note que hay que invocar al test 3 veces, una para obtener las estaciones con 5 o más bicis libres, otra para obtener las que tienen 10 o más bicis libres, y, finalmente las que tienen 1 bici libre o más):

```
Resultado esperado

El número de estaciones con 5 o más bicicletas libres es: 147
Las 5 primeras son:
(5, '024_CALLE LEÓN XIII')
(5, '043_RONDA CAPUCHINOS')
(5, '051_AVENIDA TORNEO')
(5, '064_CALLE CUESTA DE ROSARIO')
(5, '082_CALLE LUIS MONTOTO')
El número de estaciones con 10 o más bicicletas libres es: 83
Las 5 primeras son:
(10, '025_AVENIDA DE LA CRUZ ROJA')
(10, '057_PLAZA CRISTO DE BURGOS')
(10, '074_PLAZA PILATOS')
(10, '097_PASEO DE CRISTÓBAL COLÓN')
(10, '105_CALLE FRANCISCO MURILLO')
El número de estaciones con 1 o más bicicletas libres es: 225
Las 5 primeras son:
(1, '001_GLORIETA OLIMPICA')
(1, '013_CALLE FERIA')
(1, '015_CALLE DR MARAÑON')
(1, '019_PARLAMENTO')
(1, '026_AVENIDA DE MIRAFLORES')
```

### 2.2 Estaciones cercanas a una ubicación

La segunda función de consulta recibe una lista de tuplas de tipo estación, una coordenada y un número entero k y debe devolver una lista de "k" tuplas con el nombre de la estación en la que haya bicibletas disponibles, la distancia de cada estación a la coordenada dada y el número de bicicletas disponibles en dicha estación. La lista deberá estar ordenada de menor a mayor distancia.

```
def estaciones_cercanas(estaciones:List[Estación], c:Coordenadas , k:int=5)->List[Tuple[str,float,int]]: 
```
Para calcular la distancia entre dos puntos dados por su latitud y longitud utilice la misma fórmula para calcular la distancia euclidea de dos puntos en el plano. 

Cree un método ```test_estaciones_cercanas``` en el módulo sevici_test, para la coordenada (37.357659, -5.9863) y k=7:

Resultado esperado
```
Las 7 estaciones más cercanas a Coordenadas(latitud=37.357659, longitud=-5.9863) son:
('126_AVENIDA REINA MERCEDES', 0.0005378435081587429, 13)
('040_AVENIDA REINA MERCEDES', 0.0013179067450871994, 7)
('146_AVENIDA REINA MERCEDES', 0.0024416608855902374, 10)
('145_AVENIDA REINA MERCEDES', 0.0025742934390284335, 16)
('207_CALLE IFNI', 0.00473574709175822, 15)
('153_AVENIDA REINA MERCEDES', 0.005312511166942595, 25)
('105_CALLE FRANCISCO MURILLO', 0.00581606313148895, 10)
```
### 2.3 Estaciones por calle


La tercera función de consulta recibe una lista de tuplas de tipo estación y devuelve un diccionerio en que a cada nombre de calle, avenida, etc. le hace corresponder el número de estaciones que hay en ella.

```
def estaciones_por_calle(estaciones:List[Estación])->Dict[str,int]: 
```
Cree un método ```test_estaciones_por_calle``` en el módulo sevici_test

Resultado esperado
```
CALLE ARROYO --> 2
TORRES ALBARRACIN --> 1
GLORIETA DEL PRIMERO DE MAYO --> 1
AVENIDA SAN FRANCISCO JAVIER --> 2
PLAZA SAN AGUSTIN --> 1
CALLE BETIS --> 1
MIGUEL MONTORO --> 1
CALLE LUIS MONTOTO --> 4
AVENIDA DOCTOR EMILIO LEMOS --> 1
AVENIDA EDUARDO DATO --> 6
CALLE DE MANUEL VILLALOBOS --> 1
AVENIDA ALEMANIA --> 1
AVENIDA DE MIRAFLORES --> 2
AVENIDA ALCALDE LUIS URUÑUELA --> 8
VIRGEN DE LORETO --> 1
PLAZA CHAPINA --> 1
PLAZA NUEVA --> 4
CALLE SAN VICENTE --> 1
AVENIDA KANSAS CITY --> 6
CALLE LEÓN XIII --> 2
CALLE CORRAL DEL AGUA --> 1
AVENIDA RAMÓN Y CAJAL --> 2
AVENIDA DE ALEMANIA --> 1
CALLE THARSIS --> 1
CALLE ENRAMADILLA --> 2
AVENIDA DE ALVAR NUÑEZ --> 1
PRADO DE SAN SEBASTIAN --> 1
PUERTO DE LOS AZORES --> 1
RONDA TAMARGUILLO --> 4
CALLE ALFONSO LASO DE LA VEGA --> 1
AVENIDA DE LA PALMERA --> 2
CALLE PARQUE DE DOÑANA --> 1
CALLE ORFEBRE DOMINGUEZ VÁZQUEZ --> 1
PASEO CATALINA RIBERA --> 2
CALLE PAEZ DE RIVERA --> 1
AVENIDA MUJER TRABAJADORA --> 1
CALLE RAMON DE CARRANZA --> 2
PLAZA DEL PELICANO --> 1
PERO MINGO --> 1
AVENIDA DE CHILE --> 1
CAMINO DE LOS TOROS --> 1
CALLE NAVARRA --> 1
AVENIDA HYTASA --> 3
CALLE MANUEL VILLALOBOS --> 1
CALLE DE INCA GARCILASO --> 1
PLAZA DUQUESA DE ALBA --> 1
AVENIDA DE GRECIA --> 1
PLAZA DEL MUSEO --> 1
PLAZA CALDERÓN DE LA BARCA --> 1
CALLE REGINA --> 1
PLAZA DE CUBA --> 1
CALLE LEONARDO DA VINCI --> 2
CALLE IFNI --> 1
CALLE JUAN DE MATA CARRIAZO --> 1
AVENIDA SANCHEZ PIZJUAN --> 1
GLORIETA BIZCO AMATE --> 1
HOSPITAL VALME --> 1
PLAZA DE LAS MERCEDARIAS --> 1
CALLE ROMA --> 1
AVENIDA DE LAS CIENCIAS --> 3
AVDA ESPERANZA DE TRIANA --> 2
ESTADIO OLIMPICO --> 1
ESTACA DE VARES --> 1
AVENIDA TORNEO --> 1
AVDA. CRUZ CAMPO --> 1
RONDA CAPUCHINOS --> 2
CIUDAD DE CHIVA --> 4
ALBERTO JIMÉNEZ BECERRIL --> 1
CALLE ESTRELLA CANOPUS --> 1
PLAZA DE ARMAS --> 1
CALLE ANTIOQUIA --> 1
GLORIETA DE LOS FERROVIARIOS --> 1
AVENIDA ALCALDE MANUEL DEL VALLE --> 3
AVENIDA SANTA FE --> 1
CALLE DOCTOR LAFFON --> 2
AVENIDA DE ANDALUCIA --> 2
OCHO DE MARZO --> 1
AVENIDA DE LLANES --> 2
PASEO DE CRISTÓBAL COLÓN --> 1
CALLE MÉDICOS SIN FRONTERA --> 1
PASEO CRISTOBAL COLON --> 1
AVENIDA LOS GAVILANES --> 1
AVDA. RAMON Y CAJAL --> 1
CALLE FELIPE II --> 1
GLORIETA OLIMPICA --> 1
CALLE DE LA A.D.A. --> 2
AVENIDA REINA MERCEDES --> 5
NUESTRA SEÑORA DE LAS MERCEDES --> 1
CALLE DE MADRESELVA --> 1
ALAMEDA DE HERCULES --> 2
CALLE PROCURADOR --> 1
CIUDAD DE RONDA --> 1
CALLE LOPEZ DE GOMARA --> 1
GLORIETA CARLOS CANO --> 1
AVENIDA ALCALDE JUAN FERNÁNDEZ --> 1
CALLE AMERICO VESPUCIO --> 2
CALLE AMÉRICO VESPUCIO --> 3
CARRETERA DE CARMONA --> 3
CAMINO DE LOS DESCUBRIMIENTOS --> 4
AVENIDA DE LA CIUDAD JARDÍN --> 1
AVENIDA LA BUHAIRA --> 1
AVENIDA DE CORIA --> 1
AVENIDA REINIDO UNIDO --> 1
CALLE JOSE LAGUILLO --> 1
CALLE MAR DE ALBORÁN --> 1
AVENIDA DE LA BORBOLLA --> 1
CALLE JUAN ANTONIO CABESTANY --> 1
ALHAMBRA --> 1
CALLE RAMÓN CARANDE --> 1
REVOLTOSA --> 1
PLAZA CRONISTA --> 1
MAR DE ALBORÁN --> 1
PLAZA SAN MARTÍN DE PORRES --> 1
PLAZA DEL ZURRAQUE --> 1
CALLE SAMANIEGO --> 1
AVENIDA DE ROMA --> 1
PUERTA DE LA BARQUETA --> 1
PARLAMENTO --> 2
CALLE CIUDAD DE LIRIA --> 1
CALLE VICTORIA KENT --> 1
CALLE ASUNCIÓN --> 1
CALLE DR MARAÑON --> 1
RONDA URBANA NORTE --> 2
RONDA DEL TAMARGUILLO --> 1
CALLE FERIA --> 1
PLAZA ANTONIO APARICIO HERRERO --> 1
CALLE JOSÉ MARÍA MORENO GALVÁN --> 1
CALLE LAS LEANDRAS --> 1
CALLE SAN JUAN BOSCO --> 1
RONDA DE TRIANA --> 2
CALLE ALFARERIA --> 1
GLORIETA REPUBLICA DOMINICANA --> 1
CALLE SINAÍ --> 1
GLORIETA SAN DIEGO --> 1
PASEO DE EUROPA --> 1
GRAN PLAZA --> 1
ALAMEDA DE HÉRCULES --> 1
CALLE PINO MONTANO --> 1
CALLE LUIS MORALES --> 1
AVENIDA DIEGO MARTINEZ BARRIO --> 1
CALLE AGRICULTORES --> 1
PLAZA PUMAREJO --> 1
GASPAR CALDERAS --> 1
CALLE DE HERNÁN CORTÉS --> 1
AVENIDA AERONAUTICA --> 1
CALLE URQUIZA --> 1
CALLE MANUEL SIUROT --> 1
PZA FARMACÉUTICO MURILLO HERRERA --> 1
CALLE GEMA --> 1
CALLE DOCTOR PEDRO DE CASTRO --> 1
AVENIDA DE LA CRUZ ROJA --> 1
CALLE FRANCISCO MURILLO --> 1
GLORIETA PLUS ULTRA --> 1
CALLE ZORZAL --> 1
CALLE JOSÉ SARAMAGO --> 1
CALLE RAFAEL SALGADO --> 1
PLAZA CRISTO DE BURGOS --> 1
CALLE FLOR DE RETAMA --> 1
CALLE VIRGEN DE LA VICTORIA --> 1
ALCALDE MANUEL DEL VALLE --> 1
PLAZA SAN ANTONIO DE PADUA --> 1
CALLE TABLADILLA --> 1
CALLE VIRGEN DE LUJAN --> 1
CALLE AMADOR DE LOS RIOS --> 1
CALLE DOCTOR JAIME MARCOS --> 1
CALLE SAN JUAN DE RIBERA --> 1
CALLE DEL INCA GARCILASO --> 1
CALLE MUÑOZ LEÓN --> 1
AVENIDA CARDENAL BUENO MONREAL --> 3
CALLE VIRGEN DE LUJÁN --> 2
ESTACIÓN RENFE SANTA JUSTA --> 1
AVENIDA SOLEA --> 1
CALLE JOSE DIAZ --> 1
PLAZA SAN FRANCISCO --> 1
PLAZA DE LA CONCORDIA --> 1
CALLE CUESTA DE ROSARIO --> 1
PLAZA DEL ALTOZANO --> 1
CALLE SAN PABLO --> 1
PLAZA PILATOS --> 1
PLAZA SAN JUAN DE LA PALMA --> 1
CALLE ADRIANO --> 1
CALLE REYES CATÓLICOS --> 1
CALLE HINIESTA --> 1
CALLE ALHÓNDIGA --> 1
CALLE DE SALVADOR ALLENDE --> 1
CALLE TESALÓNICA --> 1
CALLE CHURRUCA --> 1 
```
### 2.4 bornetas por calle


La cuarta función de consulta recibe una lista de tuplas de tipo estación y un número entero "n", y devuelve una lista de tuplas con nombre de calle, avenida, etc. que tenga "n" o más estaciones y una tupla con la suma de las bornetas de las estaciones de dicha calle y el número de estaciones de la calle, avenida, etc. de que se trate.
La lista debe estar ordenada en orden alfabético de los nombres de las estaciónes

```
def suma_bornetas_por_calle(estaciones:List[Estación], n:int)->List[Tuple[str,Tuple[int,int]]]:
```
Cree un método ```test_suma_bornetas_por_calle``` en el módulo sevici_test

Resultado esperado

```
Para n= 3, el resultado es:
('AVENIDA ALCALDE LUIS URUÑUELA', (133, 8))
('AVENIDA ALCALDE MANUEL DEL VALLE', (60, 3))
('AVENIDA CARDENAL BUENO MONREAL', (60, 3))
('AVENIDA DE LAS CIENCIAS', (44, 3))
('AVENIDA EDUARDO DATO', (110, 6))
('AVENIDA HYTASA', (55, 3))
('AVENIDA KANSAS CITY', (113, 6))
('AVENIDA REINA MERCEDES', (122, 5))
('CALLE AMÉRICO VESPUCIO', (80, 3))
('CALLE LUIS MONTOTO', (71, 4))
('CAMINO DE LOS DESCUBRIMIENTOS', (120, 4))
('CARRETERA DE CARMONA', (45, 3))
('CIUDAD DE CHIVA', (60, 4))
('PLAZA NUEVA', (110, 4))
('RONDA TAMARGUILLO', (80, 4))
```

## 3. Visualización de estaciones

Se pretende visualizar gráficamente algunos resultados. Para ello dibujaremos un mapa y sobre él marcaremos las estaciones que cumplan determinados requisitos como, por ejemplo, tener un número mínimo de bicicletas libres.

En el proyecto se facilita un módulo ```mapa.py``` en la carpeta ```src``` con las siguientes funciones:

```
	def crea_mapa(latitud:float, longitud:float, zoom:int=15)->folium.Map:   
	def crea_marcador (latitud:int, longitud:int, etiqueta:str, color:str='red')->folium.Marker:
	def guarda_mapa_y_abre_en_navegador(mapa:folium.Map, ruta_fichero:str)->None:
```
    

Realice la función

```def visualiza_mapa_estaciones_bicis_disponibles(estaciones:List[Estación],k:int=4)->None:```

Siguiendo las siguientes pautas

    a) Calcule una coordenada promedio con los promedios de las latitudes y las longitudes.
    b) Cree un mapa centrado en dicha coordenada (vea los parámetros de crea_mapa).
    c) Recorra la lista se estaciones filtrando las que tengan al menos k biciclestas disponibles.  Para cada estación cree un marcador (vea los parámetros de crea_marcador) y añádalo al mapa con marcador.add_to(mapa).
    d) Por ultimo, guarde el mapa en la carpeta out (vea los parámetros de guarda_mapa_y_abre_en_navegador).

Cree un método ```test_visualiza_mapa_estaciones_bicis_disponibles``` en el módulo sevici_test

Resultado esperado para las estaciones con 5 o más bicis disponibles: (ver ```image.png``` que se facilita en el proyecto)
