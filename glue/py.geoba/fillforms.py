from re import match,findall
from string import Template
from IPython import get_ipython

ipy = get_ipython()

def get_rx_data(base,s1,s2):
    """
    Carga los archivos rinex de la base y las sesiones
    independientes (archivos cortados).
    devuelve un diccionario para poder cargar en el anexo 4.1
    """

    datos_gen = {}
    datos_gen['S1'] = {}
    datos_gen['S1']['_B'] = {}
    datos_gen['S1']['_R'] = {}
    datos_gen['S2'] = {}
    datos_gen['S2']['_B'] = {}
    datos_gen['S2']['_R'] = {}

    datos_gen['S1']['_B']['_rinex'] = base
    datos_gen['S1']['_R']['_rinex'] = s1
    datos_gen['S2']['_B']['_rinex'] = base
    datos_gen['S2']['_R']['_rinex'] = s2

    # Itera sobre archivos rinex, cargando los datos del encabezado
    # en un diccionario.
    for s,r in [['S1','_B'],['S1','_R'],['S2','_B'],['S2','_R']]:
        file = datos_gen[s][r]['_rinex']
        with open(file,'r') as f:
            ini = 0
            header = True
            datos = {}
            for line in f:
                if 'MARKER NAME' in line:
                    datos['_punto'] = line.split()[0]
                if 'REC # / TYPE' in line:
                    datos['R_serie'], datos['R_marca'], datos['R_modelo'] = line.split()[:3]
                if 'ANT # / TYPE' in line:
                    datos['A_serie'], datos['A_modelo'] = line.split()[:2]
                if 'ANTENNA: DELTA H/E/N' in line:
                    datos['_altura'] = line.split()[0]
                if 'END OF HEADER' in line:
                    header = False
                if match(r'(\s+\d+){6}\.\d+',line) and not header:
                    if ini == 0:
                        datos_gen[s]['_fecha_inicio']='20{:02d}-{:02d}-{:02d}'.format(*[int(i) for i in line.strip().split()[:3]])
                        datos_gen[s]['_hora_inicio']='{:02.0f}:{:02.0f}:{:02.0f}-UTC'.format(*[float(i) for i in line.strip().split()[3:6]])
                        ini += 1
                    else:
                        tmp = line
                        ini += 1
        datos_gen[s]['_fecha_fin']='20{:02d}-{:02d}-{:02d}'.format(*[int(i) for i in tmp.strip().split()[:3]])
        datos_gen[s]['_hora_fin']='{:02.0f}:{:02.0f}:{:02.0f}-UTC'.format(*[float(i) for i in tmp.strip().split()[3:6]])
        datos_gen[s][r] = datos
        datos_gen[s][r]['_rinex'] = file

    tmp = datos_gen

    while True:
        # Aplanar el diccionario a un solo nivel.
        flag = False
        for k in list(tmp.keys()):
            if isinstance(tmp[k],dict):
                for l in tmp[k]:
                    tmp['{}{}'.format(k,l)] = tmp[k][l]
                tmp[k] = None
                flag = True
        if not flag:
            break

    return {i:j for i,j in tmp.items() if j is not None}

# Datos extra para cargar
extra_data = {
    'S2_PDOP':'',
    'S1_RA_marca':'Ashtech',
    'S2_mascara':'10',
    'S2_intervalo':'1 segundo',
    'S1_B_archivo':'',
    'S1_otros':'',
    'S1_R_archivo':'',
    'S1_intervalo':'1 segundo',
    'S2_R_antena':'',
    'S1_mascara':'10',
    'S2_R_archivo':'',
    'S2_otros':'',
    'S1_PDOP':'',
    'S1_BA_marca':'Ashtech',
    'S2_BA_marca':'Ashtech',
    'S2_B_archivo':'',
    'S2_RA_marca':'Ashtech'}

def make_template(data,out='./4.1.tmp.fdf',template_file='/vinculacion/data/Anexo4.1.fdf',extra_data=extra_data):
    #Cargar Template
    filein = open( template_file,encoding='latin1' )
    #Leerlo
    src = Template( filein.read() )

    # Hacer la primera sustitución con los datos que provistos
    #print(*findall('\(([$].*)\)',src.safe_substitute(data)), sep='\n')

    intermedio = Template(src.safe_substitute(data))

    with open( out, 'w', encoding='latin1' ) as f:
        print(intermedio.safe_substitute(extra_data),file=f)

    return

def apply_template(**kwargs):
    data = (\
        kwargs.get('pdf_file','/vinculacion/data/Anexo4.1.pdf'),
        kwargs.get('fdf_file','4.1.tmp.pdf'),
        kwargs.get('out',f"Anexo4.1-{kwargs.get('base','____')}-{kwargs.get('punto','____')}.pdf")
           )

    ipy.run_cell(\
    """%%script bash
    pdftk {} \
          fill_form {} output {}
    """.format(*data)\
            )
