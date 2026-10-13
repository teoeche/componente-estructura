from models import Estudiante, Materia, Matricula
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido


# ============================================================
# ARCHIVOS JSON
# ============================================================

gestor_estudiantes = GestorJSON("data/estudiantes.json")
gestor_materias = GestorJSON("data/materias.json")
gestor_matriculas = GestorJSON("data/matriculas.json")


# ============================================================
# FUNCIONES GENERICAS
# Se utilizan con cualquier modelo.
# ============================================================

def leer_objetos(gestor, modelo):
    """Convierte los diccionarios JSON en objetos."""
    objetos = []

    for datos in gestor.leer():
        objetos.append(modelo.desde_diccionario(datos))

    return objetos


def obtener_por_id(objetos, id_registro):
    """Busca un objeto por su identificador."""
    for objeto in objetos:
        if objeto.id == id_registro:
            return objeto

    return None


def buscar(objetos, termino, campos):
    # TUPLA: los campos buscables son fijos y no necesitan modificarse.
    termino = str(termino).strip().lower()
    encontrados = []

    if termino == "":
        return encontrados

    for objeto in objetos:
        for campo in campos:
            valor = str(getattr(objeto, campo, "")).lower()

            if termino in valor:
                encontrados.append(objeto)
                break

    return encontrados


def siguiente_id(gestor):
    mayor = 0

    for registro in gestor.leer():
        identificador = int(registro["id"])

        if identificador > mayor:
            mayor = identificador

    return mayor + 1


def guardar_nuevo(gestor, objeto):
    registros = gestor.leer()
    registros.append(objeto.a_diccionario())
    gestor.guardar(registros)


def reemplazar(gestor, objeto):
    registros = gestor.leer()

    for i in range(len(registros)):
        if int(registros[i]["id"]) == objeto.id:
            registros[i] = objeto.a_diccionario()
            gestor.guardar(registros)
            return True

    return False


def eliminar(gestor, id_registro):
    registros = gestor.leer()
    nuevos = []

    for registro in registros:
        if int(registro["id"]) != int(id_registro):
            nuevos.append(registro)

    if len(nuevos) == len(registros):
        return False

    gestor.guardar(nuevos)
    return True


def ids_registrados(gestor):
    # CONJUNTO: permite comprobar rápidamente si un ID ya existe.
    return {int(registro["id"]) for registro in gestor.leer()}


def indice_por_id(objetos):
    # DICCIONARIO: permite encontrar un objeto directamente usando su ID.
    return {objeto.id: objeto for objeto in objetos}


# ============================================================
# ESTUDIANTES
# ============================================================

CAMPOS_ESTUDIANTE = ("nombre", "apellido", "email", "carnet")
CAMPOS_BUSCABLES_ESTUDIANTE = (
    "nombre", "apellido", "email", "carnet", "carrera"
)


def carnets_registrados(excepto_id=None):
    # CONJUNTO: evita carnets repetidos y permite buscarlos rápidamente.
    return {
        str(r["carnet"]).strip().upper()
        for r in gestor_estudiantes.leer()
        if int(r["id"]) != excepto_id
    }


def emails_registrados(excepto_id=None):
    # CONJUNTO: evita que dos estudiantes compartan el mismo email.
    return {
        str(r["email"]).strip().lower()
        for r in gestor_estudiantes.leer()
        if int(r["id"]) != excepto_id
    }


def validar_estudiante(datos, id_actual=None):
    if id_actual is None:
        for campo in CAMPOS_ESTUDIANTE:
            if str(datos.get(campo, "")).strip() == "":
                return f"El campo {campo} es obligatorio"

    # Comprueba que los campos enviados no queden vacíos.
    for campo in CAMPOS_ESTUDIANTE:
        if campo in datos and str(datos[campo]).strip() == "":
            return f"El campo {campo} es obligatorio"

    if "email" in datos:
        email = str(datos["email"]).strip().lower()

        if not es_email_valido(email):
            return f"Email inválido: '{email}'"

        if email in emails_registrados(id_actual):
            return "Ese email ya está registrado"

    if "carnet" in datos:
        carnet = str(datos["carnet"]).strip().upper()

        if carnet in carnets_registrados(id_actual):
            return "Ese carnet ya está registrado"

    return None


def crear_estudiante(datos):
    error = validar_estudiante(datos)

    if error:
        return False, error

    estudiante = Estudiante(
        siguiente_id(gestor_estudiantes),
        str(datos["nombre"]).strip().title(),
        str(datos["apellido"]).strip().title(),
        str(datos["email"]).strip().lower(),
        str(datos["carnet"]).strip().upper(),
        str(datos.get("carrera", "")).strip().title()
    )

    guardar_nuevo(gestor_estudiantes, estudiante)

    return True, f"Estudiante creado: {estudiante.etiqueta()}"


def obtener_estudiantes():
    return leer_objetos(gestor_estudiantes, Estudiante)


def obtener_estudiante(id_registro):
    return obtener_por_id(
        obtener_estudiantes(), int(id_registro)
    )


def buscar_estudiantes(termino):
    return buscar(
        obtener_estudiantes(),
        termino,
        CAMPOS_BUSCABLES_ESTUDIANTE
    )


def actualizar_estudiante(id_registro, cambios):
    estudiante = obtener_estudiante(id_registro)

    if estudiante is None:
        return False, f"No existe el estudiante {id_registro}"

    if not cambios:
        return False, "No se indicó ningún cambio"

    permitidos = set(CAMPOS_ESTUDIANTE) | {"carrera"}
    desconocidos = set(cambios) - permitidos

    if desconocidos:
        return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

    error = validar_estudiante(cambios, estudiante.id)

    if error:
        return False, error

    datos = estudiante.a_diccionario()
    datos.update(cambios)

    datos["nombre"] = str(datos["nombre"]).strip().title()
    datos["apellido"] = str(datos["apellido"]).strip().title()
    datos["email"] = str(datos["email"]).strip().lower()
    datos["carnet"] = str(datos["carnet"]).strip().upper()
    datos["carrera"] = str(datos.get("carrera", "")).strip().title()

    actualizado = Estudiante.desde_diccionario(datos)

    if not reemplazar(gestor_estudiantes, actualizado):
        return False, "No se pudo actualizar el estudiante"

    return True, f"Estudiante {id_registro} actualizado"


def eliminar_estudiante(id_registro):
    estudiante = obtener_estudiante(id_registro)

    if estudiante is None:
        return False, f"No existe el estudiante {id_registro}"

    # Evita dejar matrículas asociadas a un estudiante inexistente.
    for matricula in obtener_matriculas():
        if matricula.estudiante_id == estudiante.id:
            return False, "No se puede eliminar: el estudiante tiene matrículas"

    if eliminar(gestor_estudiantes, estudiante.id):
        return True, f"Estudiante {id_registro} eliminado"

    return False, "No se pudo eliminar el estudiante"


# ============================================================
# MATERIAS
# ============================================================

CAMPOS_MATERIA = ("nombre", "codigo", "creditos", "cupos")
CAMPOS_BUSCABLES_MATERIA = ("nombre", "codigo")


def codigos_registrados(excepto_id=None):
    # CONJUNTO: permite comprobar que el código de una materia sea único.
    return {
        str(r["codigo"]).strip().upper()
        for r in gestor_materias.leer()
        if int(r["id"]) != excepto_id
    }


def validar_materia(datos, id_actual=None):
    if id_actual is None:
        for campo in ("nombre", "codigo", "creditos"):
            if str(datos.get(campo, "")).strip() == "":
                return f"El campo {campo} es obligatorio"

    for campo in ("nombre", "codigo"):
        if campo in datos and str(datos[campo]).strip() == "":
            return f"El campo {campo} es obligatorio"

    if "codigo" in datos:
        codigo = str(datos["codigo"]).strip().upper()

        if codigo in codigos_registrados(id_actual):
            return "Ese código de materia ya está registrado"

    if "creditos" in datos:
        try:
            creditos = int(datos["creditos"])
        except (ValueError, TypeError):
            return "Los créditos deben ser un número entero"

        if creditos < 1 or creditos > 10:
            return "Los créditos deben estar entre 1 y 10"

    if "cupos" in datos:
        try:
            cupos = int(datos["cupos"])
        except (ValueError, TypeError):
            return "Los cupos deben ser un número entero"

        if cupos < 0 or cupos > Materia.CUPOS_MAXIMOS:
            return f"Los cupos deben estar entre 0 y {Materia.CUPOS_MAXIMOS}"

    return None


def crear_materia(datos):
    error = validar_materia(datos)

    if error:
        return False, error

    cupos = int(datos.get("cupos", Materia.CUPOS_MAXIMOS))

    materia = Materia(
        siguiente_id(gestor_materias),
        str(datos["nombre"]).strip().title(),
        str(datos["codigo"]).strip().upper(),
        int(datos["creditos"]),
        cupos
    )

    guardar_nuevo(gestor_materias, materia)

    return True, f"Materia creada: {materia.etiqueta()}"


def obtener_materias():
    return leer_objetos(gestor_materias, Materia)


def obtener_materia(id_registro):
    return obtener_por_id(
        obtener_materias(), int(id_registro)
    )


def buscar_materias(termino):
    return buscar(
        obtener_materias(),
        termino,
        CAMPOS_BUSCABLES_MATERIA
    )


def actualizar_materia(id_registro, cambios):
    materia = obtener_materia(id_registro)

    if materia is None:
        return False, f"No existe la materia {id_registro}"

    if not cambios:
        return False, "No se indicó ningún cambio"

    permitidos = set(CAMPOS_MATERIA)
    desconocidos = set(cambios) - permitidos

    if desconocidos:
        return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

    # No se permite cambiar cupos manualmente si hay matrículas activas.
    if "cupos" in cambios:
        matriculas = obtener_matriculas()
        usadas = sum(
            1 for m in matriculas if m.materia_id == materia.id
        )
        try:
            nuevos_cupos = int(cambios["cupos"])
        except (ValueError, TypeError):
            return False, "Los cupos deben ser un número entero"

        if nuevos_cupos + usadas > Materia.CUPOS_MAXIMOS:
            return False, "Los cupos más las matrículas superan el máximo permitido"

    error = validar_materia(cambios, materia.id)

    if error:
        return False, error

    datos = materia.a_diccionario()
    datos.update(cambios)

    datos["nombre"] = str(datos["nombre"]).strip().title()
    datos["codigo"] = str(datos["codigo"]).strip().upper()
    datos["creditos"] = int(datos["creditos"])
    datos["cupos"] = int(datos["cupos"])

    actualizada = Materia.desde_diccionario(datos)

    if not reemplazar(gestor_materias, actualizada):
        return False, "No se pudo actualizar la materia"

    return True, f"Materia {id_registro} actualizada"


def eliminar_materia(id_registro):
    materia = obtener_materia(id_registro)

    if materia is None:
        return False, f"No existe la materia {id_registro}"

    for matricula in obtener_matriculas():
        if matricula.materia_id == materia.id:
            return False, "No se puede eliminar: la materia tiene matrículas"

    if eliminar(gestor_materias, materia.id):
        return True, f"Materia {id_registro} eliminada"

    return False, "No se pudo eliminar la materia"


def materias_sin_cupo():
    return [
        materia for materia in obtener_materias()
        if not materia.hay_cupo()
    ]


# ============================================================
# MATRICULAS
# ============================================================

def crear_matricula(datos):
    try:
        estudiante_id = int(datos["estudiante_id"])
        materia_id = int(datos["materia_id"])
    except (KeyError, ValueError, TypeError):
        return False, "Debe indicar un estudiante y una materia válidos"

    periodo = str(datos.get("periodo", "")).strip()

    if periodo == "":
        return False, "El periodo es obligatorio"

    try:
        nota = float(datos.get("nota", 0))
    except (ValueError, TypeError):
        return False, "La nota debe ser numérica"

    if not Materia.es_nota_valida(nota):
        return False, "La nota debe estar entre 0 y 20"

    estudiante = obtener_estudiante(estudiante_id)

    if estudiante is None:
        return False, f"No existe el estudiante {estudiante_id}"

    materia = obtener_materia(materia_id)

    if materia is None:
        return False, f"No existe la materia {materia_id}"

    # Comprueba que no se repita estudiante + materia + periodo.
    for matricula in obtener_matriculas():
        if (
            matricula.estudiante_id == estudiante_id
            and matricula.materia_id == materia_id
            and matricula.periodo == periodo
        ):
            return False, "El estudiante ya está matriculado en esa materia y periodo"

    if not materia.hay_cupo():
        return False, f"La materia {materia.nombre} no tiene cupos"

    matricula = Matricula(
        siguiente_id(gestor_matriculas),
        estudiante_id,
        materia_id,
        periodo,
        nota
    )

    # Primero ocupa un cupo y guarda el cambio de la materia.
    materia.ocupar_cupo()
    reemplazar(gestor_materias, materia)

    guardar_nuevo(gestor_matriculas, matricula)

    return True, f"Matrícula creada: {matricula.etiqueta()}"


def obtener_matriculas():
    return leer_objetos(gestor_matriculas, Matricula)


def obtener_matricula(id_registro):
    return obtener_por_id(
        obtener_matriculas(), int(id_registro)
    )


def registrar_nota(id_registro, nota):
    matricula = obtener_matricula(id_registro)

    if matricula is None:
        return False, f"No existe la matrícula {id_registro}"

    if not Materia.es_nota_valida(nota):
        return False, "La nota debe ser numérica y estar entre 0 y 20"

    matricula.nota = float(nota)

    if not reemplazar(gestor_matriculas, matricula):
        return False, "No se pudo registrar la nota"

    return True, f"Nota registrada. Estado: {matricula.estado()}"


def retirar_matricula(id_registro):
    matricula = obtener_matricula(id_registro)

    if matricula is None:
        return False, f"No existe la matrícula {id_registro}"

    materia = obtener_materia(matricula.materia_id)

    # Se elimina la matrícula y se libera su cupo.
    if not eliminar(gestor_matriculas, matricula.id):
        return False, "No se pudo retirar la matrícula"

    if materia is not None:
        materia.liberar_cupo()
        reemplazar(gestor_materias, materia)

    return True, f"Matrícula {id_registro} retirada"


def certificado(id_registro):
    matricula = obtener_matricula(id_registro)

    if matricula is None:
        return None

    # DICCIONARIO ÍNDICE: permite buscar estudiante y materia por ID.
    estudiantes = indice_por_id(obtener_estudiantes())
    materias = indice_por_id(obtener_materias())

    estudiante = estudiantes.get(matricula.estudiante_id)
    materia = materias.get(matricula.materia_id)

    if estudiante is None or materia is None:
        return "No se puede generar el certificado: faltan datos relacionados"

    texto = f"CERTIFICADO #{matricula.id}   periodo: {matricula.periodo}\n"
    texto += (
        f"Estudiante: {estudiante.nombre_completo()} "
        f"({estudiante.carnet})\n"
    )
    texto += (
        f"Materia   : {materia.nombre} ({materia.codigo}) "
        f"· {materia.creditos} créditos\n"
    )
    texto += "-" * 42 + "\n"
    texto += f"Nota      : {matricula.nota}\n"
    texto += f"Estado    : {matricula.estado()}"

    return texto


def matriculas_por_estudiante():
    # DICCIONARIO DE LISTAS: agrupa las matrículas usando setdefault.
    agrupadas = {}

    for matricula in obtener_matriculas():
        agrupadas.setdefault(matricula.estudiante_id, []).append(matricula)

    return agrupadas


def promedio_de_estudiante(id_registro):
    matriculas = obtener_matriculas()
    notas = []

    for matricula in matriculas:
        if matricula.estudiante_id == int(id_registro):
            notas.append(matricula.nota)

    if not notas:
        return None

    return round(sum(notas) / len(notas), 2)