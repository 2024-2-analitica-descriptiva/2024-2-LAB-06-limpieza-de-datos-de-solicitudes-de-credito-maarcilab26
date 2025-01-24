"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"
    """
    import pandas as pd
    import os
    import re

    # Función para normalizar la columna 'barrio'
    def normalize_barrio(value):
        value = str(value)
        value = value.replace('_', ' ').replace('-', ' ')
        value = value.lower()
        value = re.sub(r'no\.\s*(\d+)', r'no\1', value)
        return value

    # Función para organizar las fechas de forma coherente
    def format_fecha(date):
        try:
            return pd.to_datetime(date, format='%Y/%m/%d')
        except ValueError:
            try:
                return pd.to_datetime(date, format='%d/%m/%Y')
            except ValueError:
                print(f"Fecha inválida: {date}")
                return pd.NaT  # Devuelve Not a Time si la fecha es inválida

    # Intentar cargar los datos y verificar si el archivo existe
    try:
        df = pd.read_csv('files/input/solicitudes_de_credito.csv', delimiter=';', encoding='utf-8', index_col=0)
        print("Archivo cargado correctamente.")
    except FileNotFoundError:
        print("El archivo 'solicitudes_de_credito.csv' no se encuentra en la ruta especificada.")
        return  # Sale de la función si el archivo no se encuentra

    # Verificar si hay columnas faltantes
    required_columns = ['sexo', 'tipo_de_emprendimiento', 'idea_negocio', 'barrio', 'estrato', 'comuna_ciudadano', 'monto_del_credito', 'fecha_de_beneficio', 'línea_credito']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Faltan las siguientes columnas en los datos: {', '.join(missing_columns)}")
        return  # Sale de la función si faltan columnas esenciales
    else:
        print("Todas las columnas necesarias están presentes.")

    # Eliminar registros con valores faltantes
    df_before_drop = df.shape[0]
    df = df.dropna()
    df_after_drop = df.shape[0]
    print(f"Registros antes de eliminar los valores faltantes: {df_before_drop}. Registros después: {df_after_drop}. Registros eliminados: {df_before_drop - df_after_drop}.")

    # Verificar si hay valores duplicados antes de eliminarlos
    df_before_duplicates = df.shape[0]
    df = df.drop_duplicates()
    df_after_duplicates = df.shape[0]
    print(f"Registros antes de eliminar duplicados: {df_before_duplicates}. Registros después: {df_after_duplicates}. Registros eliminados: {df_before_duplicates - df_after_duplicates}.")

    # Normalización de las columnas

    # Normalizar la columna 'sexo'
    df['sexo'] = df['sexo'].str.lower().str.strip()
    print("Normalización de la columna 'sexo' completada.")

    # Verificar si hay valores inesperados en 'sexo' después de la normalización
    if df['sexo'].isnull().any():
        print("Advertencia: Existen valores nulos en la columna 'sexo'. Se procederá a eliminarlos.")
        df = df.dropna(subset=['sexo'])

    # Normalizar la columna 'tipo_de_emprendimiento'
    df['tipo_de_emprendimiento'] = df['tipo_de_emprendimiento'].str.lower().str.strip()
    print("Normalización de la columna 'tipo_de_emprendimiento' completada.")

    # Verificar si 'tipo_de_emprendimiento' contiene valores inesperados
    if df['tipo_de_emprendimiento'].isnull().any():
        print("Advertencia: Existen valores nulos en la columna 'tipo_de_emprendimiento'. Se procederá a eliminarlos.")
        df = df.dropna(subset=['tipo_de_emprendimiento'])

    # Normalizar la columna 'idea_negocio'
    df['idea_negocio'] = df['idea_negocio'].str.replace('_', ' ').str.replace('-', ' ')
    df['idea_negocio'] = df['idea_negocio'].str.lower().str.strip()
    print("Normalización de la columna 'idea_negocio' completada.")

    # Verificar si 'idea_negocio' tiene valores nulos
    if df['idea_negocio'].isnull().any():
        print("Advertencia: Existen valores nulos en la columna 'idea_negocio'. Se procederá a eliminarlos.")
        df = df.dropna(subset=['idea_negocio'])

    # Normalizar la columna 'barrio'
    df['barrio'] = df['barrio'].astype(str)
    df['barrio'] = df['barrio'].apply(normalize_barrio)
    print("Normalización de la columna 'barrio' completada.")

    # Verificar si 'barrio' tiene valores nulos
    if df['barrio'].isnull().any():
        print("Advertencia: Existen valores nulos en la columna 'barrio'. Se procederá a eliminarlos.")
        df = df.dropna(subset=['barrio'])

    # Normalizar la columna 'estrato'
    df['estrato'] = df['estrato'].astype(int)
    print("Normalización de la columna 'estrato' completada.")

    # Verificar si 'estrato' tiene valores nulos
    if df['estrato'].isnull().any():
        print("Advertencia: Existen valores nulos en la columna 'estrato'. Se procederá a eliminarlos.")
        df = df.dropna(subset=['estrato'])

    # Normalizar la columna 'comuna_ciudadano'
    df['comuna_ciudadano'] = df['comuna_ciudadano'].astype(int)
    print("Normalización de la columna 'comuna_ciudadano' completada.")

    # Verificar si 'comuna_ciudadano' tiene valores nulos
    if df['comuna_ciudadano'].isnull().any():
        print("Advertencia: Existen valores nulos en la columna 'comuna_ciudadano'. Se procederá a eliminarlos.")
        df = df.dropna(subset=['comuna_ciudadano'])

    # Limpiar la columna 'monto_del_credito'
    df['monto_del_credito'] = df['monto_del_credito'].replace({'\$': '', ',': '', ' ': ''}, regex=True)
    df['monto_del_credito'] = df['monto_del_credito'].astype(float)
    print("Normalización de la columna 'monto_del_credito' completada.")

    # Verificar si 'monto_del_credito' tiene valores nulos
    if df['monto_del_credito'].isnull().any():
        print("Advertencia: Existen valores nulos en la columna 'monto_del_credito'. Se procederá a eliminarlos.")
        df = df.dropna(subset=['monto_del_credito'])

    # Aplicar la nueva función 'format_fecha' para la columna 'fecha_de_beneficio'
    df['fecha_de_beneficio'] = df['fecha_de_beneficio'].apply(format_fecha)
    print("Normalización de la columna 'fecha_de_beneficio' completada.")

    # Verificar si 'fecha_de_beneficio' tiene valores nulos
    if df['fecha_de_beneficio'].isnull().any():
        print("Advertencia: Existen valores nulos en la columna 'fecha_de_beneficio'. Se procederá a eliminarlos.")
        df = df.dropna(subset=['fecha_de_beneficio'])

    # Normalizar la columna 'línea_credito'
    df['línea_credito'] = df['línea_credito'].str.replace('-', ' ').str.replace('_', ' ')
    df['línea_credito'] = df['línea_credito'].str.lower().str.strip()
    print("Normalización de la columna 'línea_credito' completada.")

    # Verificar si 'línea_credito' tiene valores nulos
    if df['línea_credito'].isnull().any():
        print("Advertencia: Existen valores nulos en la columna 'línea_credito'. Se procederá a eliminarlos.")
        df = df.dropna(subset=['línea_credito'])

    # Eliminar registros duplicados nuevamente (en caso de que aparezcan después de limpiar otras columnas)
    df_before_duplicates = df.shape[0]
    df = df.drop_duplicates()
    df_after_duplicates = df.shape[0]
    print(f"Registros antes de eliminar duplicados: {df_before_duplicates}. Registros después: {df_after_duplicates}. Registros eliminados: {df_before_duplicates - df_after_duplicates}.")

    # Validar si la carpeta de salida existe, si no, la crea
    if not os.path.exists('files/output/'):
        print("La carpeta de salida no existe. Se creará.")
        os.makedirs('files/output/')

    # Guardar el archivo limpio
    df.to_csv('files/output/solicitudes_de_credito.csv', index=False, sep=';')
    print("El archivo limpio ha sido guardado correctamente en 'files/output/solicitudes_de_credito.csv'.")