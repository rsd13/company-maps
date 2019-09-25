# company-maps



# Estructura del projecto

## Get Offices

El directorio ./functions/get_offices se corresponde a la primera mitad del proyecto.
En esta parte se llama a la base de datos companies y se hace un filtro especifico. El
filtro utilizado por mi va derivado de las condiciones derivado del problema: empresas
que hayan ganado mas de 1 millon y que tenga como máximo 10 años de antiguedad. Una vez
efectuado el filtro se limpia las columnas y me quedo con un total de 80 empresas. 
Ficheros que conforman esta parte:

- **mongodb.py**: fichero que se encarga de las operaciones de MongoDB, en esta parte 
se llama al código, y hace los distintos filtrados.
- **foreignExchange.py**: funcion que llama a una api de cambio de divisas, en este fichero
traspasa todas las ganancias a euros.
- **clear.py**: fichero que se encarga de hacer distintas funciones de limpieza.


## Analityc offices

El directorio  ./functions/get_offices se encarga de haceer una comparación entre 
las distintas coordenadas obtenido del filtro de la parte de Get offices. Para obtener
el mejor punto he ido punto por punto y viendo los distintos locales cercanos. Los ficheros
que conforman esta parte es:

- **mongo.py**: fichero que se encarga en realizar operaciones reacionas con mongo, además
de hacer la operación $near.
- **analitcy**: fichero que se encarga de distintas operaciones de conteo de puntuaciones.
- **foursquare**: fichero que se encarga de llamar a la api de foursquare para obtener los 
distintos locales

# Trabajo Futuro

- Optimizar la parte de analityc offices
- Realizar el mapa con la liberia folium
