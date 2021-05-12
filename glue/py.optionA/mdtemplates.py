mdfiles = """
## Archivos de medición

Los archivos de medición se incluyen en formato Rinex 2.11, como

- Base permanente RAMSAC: `{BASE}`
- Punto base del vector: `{PIE}`
- Punto de azimut del vector: `{AZIMUT}`

## Datos de Sesion.

Los datos de la sesión, extraidos de los archivos de medición,
se proveen en los anexos 4.1 que se adjuntan.

Se incluye también el anexo 4 con datos generales del trabajo.
"""

mdpdop = """
## Filtrado por PDOP

Con la herramienta PRSolve, parte de GPSTk, se calculó el PDOP para cada época de los archivos de medición.

Luego, con la herramienta RinEdit se eliminaron las epocas con PDOP > 2.5, resultando en:

- {base}: {nbase} epocas eliminadas, {nbasehs:.2f} horas efectivas de medición
- {az}: {naz} epocas eliminadas, {nazhs:.2f} horas efectivas de medición
"""

mdsessions = """
## Archivos de Sesiones

Se generaron los archivos de sesión para el cálculo individual, utilizando RinEdit para realizar el corte de los mismos.

- Vector {nbase}->{npie}:
  - Sesion 1: {fbase}; {fpie1}
  - Sesion 2: {fbase}; {fpie2}
  - Sesion completa: {fbase}; {fpie}

- Vector {npie}->{naz}:
  - Sesion 1: {fpie}; {faz1}
  - Sesion 2: {fpie}; {faz2}
  - Sesion completa: {fbase}; {faz1}
"""

mdpdopgraphs = """
## PDOP de cada sesión

Para cada sesión se buscó el PDOP máximo, y a continuación se presentan las gráficas
de PDOP en función del tiempo para cada una.
"""

mdconfigs = """
## Opciones de Procesamiento (RTKLIB)

### General

| Opción | valor |
|--------|:-----:|
|Modo de Procesamiento | {pos1-posmode} |
|Frecuencias | {pos1-frequency} |
|Modo del filtro Kallman | {pos1-soltype} |
|Mascara de Elevación | {pos1-elmask} |
|Mascara de SNR | {pos1-snrmask} |
|Aceleración/velocidad en el filtro Kallman | {pos1-dynamics} |
|Corrección por marea terrestre | {pos1-tidecorr} |
|Modo de Corrección de ionosfera | {pos1-ionoopt} |
|Modo de Corrección de troposfera | {pos1-tropopt} |
|Tipo de efemérides | {pos1-sateph} |
|Excluir satelites | {pos1-exclsats} |
|Sistemas utilizados | {pos1-navsys} |
|Modo resolución de ambiguedad | {pos2-armode} |
|Resolver Ambiguedad Glonass (si corresponde) | {pos2-gloarmode} |
|Umbral resolución de ambiguedad | {pos2-arthres} |
|Minimo segmento para fijar ambiguedad | {pos2-arlockcnt} |
|Mascara de elevación para resolver ambiguedad | {pos2-arelmask} |
|Ciclos faltantes para resetear ambiguedad | {pos2-aroutcnt} |
|Minimo segmento para mantener ambiguedad | {pos2-arminfix} |
|Mascara de elevación para mantener ambiguedad | {pos2-elmaskhold} |
|Umbral para salto de ciclo | {pos2-slipthres} |
|Tipo de altura | {out-height} |

### Parámetros del filtro Kallman

| Opción | valor |
|--------|:-----:|
| Varianza relativa Codigo/fase | {stats-errratio} |
| Varianza fase [m] | {stats-errphase} |
| Varianza de fase segun elevación [m/seno(el)] | {stats-errphaseel} |
| Desvio a-priori Ambiguedades | {stats-stdbias} |
| Desvio a-priori Ambiguedades retardo iono | {stats-stdiono} |
| Desvio a-priori Ambiguedades retardo tropo | {stats-stdtrop} |
| Ruido de proceso aceleración H | {stats-prnaccelh} |
| Ruido de proceso aceleración V | {stats-prnaccelv} |
| Ruido de proceso ambiguedades | {stats-prnbias} |
| Ruido de proceso retardo ionosferico | {stats-prniono} |
| Ruido de proceso retardo troposferico | {stats-prntrop} |
| Estabilidad de reloj | {stats-clkstab} |
"""

mdpos = """
## Resultados de procesamiento

La posición calculada para punto de llegada del vector, punto {npto}, fue:

{tablaLL}

En coordenadas proyectadas, Gauss Krugger faja 5:

{tablaGK}

A continuación se grafica un resumen de los resultados de procesamiento.

La posición horizontal se grafica, centrada en la posición final de la sesión
completa, con dos curvas. Una curva llena que indica
un desvío de 2$\sigma$ --es decir que el 66% de las épocas resueltas fijas
quedan dentro de ese perimetro-- y una punteada que indica un intervalo del
95%.

La altura se grafica con un histogramas correspondientes a cada sesión, donde
también se grafica con un gráfico de caja y bigote la media y los cuartiles
(que encierran el %50 de las soluciones).

La posición final se puede
[Ver en Google Maps](https://maps.google.com/maps?t=k&q=loc:{ptlat}+{ptlon})
para mayor comodidad
"""
