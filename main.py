import json
import csv
import chardet
import os


def detectar_codificacion(archivo):
    with open(archivo, "rb") as f:
        resultado = chardet.detect(f.read(100000))  # Leer una parte del archivo
    return resultado["encoding"]


def read_csv(path) -> list[dict]:
    codificacion = detectar_codificacion(path)
    with open(path, "r", encoding=codificacion) as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        header = next(reader)
        data = []
        for row in reader:
            iterable = zip(header, row)
            registro = {key: value for key, value in iterable}
            data.append(registro)

    return data


def update_csv(path: str, data: dict):
    with open(path, "a", encoding="utf-8-sig", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(data.values())

    return


def write_csv(data: list[dict], nombre: str) -> csv:
    with open(f"{nombre}.csv", "w", encoding="utf-8-sig", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(list(data[0].keys()))
        for item in data:
            writer.writerow(list(item.values()))


def obtener_datos_json(nombre: str):
    with open(f"{nombre}.json", "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    return datos


def generar_estructura_json_contactos(bd_telefonos: list[dict]) -> json:
    contactos = [
        {"number": f"549{registro["Celular"]}", "message": generar_mensaje(registro)}
        for registro in bd_telefonos
    ]
    # print(len(contactos))
    exportar_json(contactos, "contacts")


def exportar_json(datos: list[dict], nombre: str) -> json:
    # vemos = {}
    # for vemo in datos:
    #     vemos.update(vemo)

    with open(f"{nombre}.json", "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)

    return


def generar_mensaje(registro: dict):
    return f"""
{registro['value2']}. {registro['value1']}
"""


def run():
    # paths
    nombre_archivo = "enviar.csv"
    bd_telefonos_mensajes = os.path.join(os.getcwd(), nombre_archivo)

    bd_envios = read_csv(bd_telefonos_mensajes)

    print("Generando estructura JSON de los contactos")
    # print(len(bd_nomivac_telefono))
    generar_estructura_json_contactos(bd_envios)

    # registro = {
    #     "Nro. de documento": "26804916",
    #     "Apellido": "MOYA",
    #     "Nombre": "ROXANA DEL VALLE",
    #     "Departamento residencia actual": "Valle Viejo",
    #     "Cobertura social": "OBRA SOCIAL DEL PERSONAL DE LA INDUSTRIA TEXTIL",
    #     "Código de establecimiento": "5,01E+13",
    #     "Departamento establecimiento": "Valle Viejo",
    #     "Establecimiento": "HOSPITAL DE VILLA DOLORES DR. DERMIDIO HERRERA",
    #     "Vacuna": "Tetravalente contra el Dengue",
    #     "Dósis": "1ra Dosis",
    #     "Lote": "557223",
    #     "Fecha de aplicación": "14/11/2024",
    #     "Edad de aplicación": "46",
    #     "Fecha de registro": "15/11/2024",
    #     "Usuario": "sggonzalez",
    #     "Comentarios": "TURNO - Dengue (Personal de Salud y Brigadas)",
    #     "Telefono": "3834522761",
    # }
    # print(generar_mensaje(registro))
    # logs = obtener_datos_json("log")
    # enviados = [registro for registro in logs if registro["status"] == "Enviado"]
    # print(len(enviados))


if __name__ == "__main__":
    run()
