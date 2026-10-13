
from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error,
    imprimir_info, confirmar
)

from views import (
    crear_estudiante, obtener_estudiantes, obtener_estudiante,
    buscar_estudiantes, actualizar_estudiante, eliminar_estudiante,
    crear_materia, obtener_materias, obtener_materia,
    buscar_materias, actualizar_materia, eliminar_materia,
    materias_sin_cupo, crear_matricula, obtener_matriculas,
    obtener_matricula, registrar_nota, retirar_matricula,
    certificado, promedio_de_estudiante
)


# ============================================================
# AYUDAS DE PANTALLA
# ============================================================

def pausa():
    input("\nPresione Enter para continuar...")


def pedir_entero(etiqueta):
    try:
        return int(input(etiqueta))
    except ValueError:
        return None


def pedir_decimal(etiqueta):
    try:
        return float(input(etiqueta))
    except ValueError:
        return None


def mostrar_resultado(exito, mensaje):
    # TUPLA: recibe el resultado y el mensaje de cada operación.
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)


def mostrar_lista(objetos, vacio="No hay registros todavía."):
    # POLIMORFISMO: cada objeto sabe cómo representarse.
    if not objetos:
        imprimir_info(vacio)
        return

    for objeto in objetos:
        print(f"  {objeto}")

    imprimir_info(f"Total: {len(objetos)}")


def mostrar_detalle(objeto):
    # DICCIONARIO: recorre las claves y valores del objeto.
    for clave, valor in objeto.a_diccionario().items():
        print(
            f"  {str(clave).replace('_', ' ').capitalize():<16}: "
            f"{valor}"
        )


# ============================================================
# MENÚ DE ESTUDIANTES
# ============================================================

def crear_estudiante_menu():
    imprimir_titulo("CREAR ESTUDIANTE")

    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "carnet": input("Carnet: "),
        "carrera": input("Carrera: ")
    }

    mostrar_resultado(*crear_estudiante(datos))
    pausa()


def listar_estudiantes():
    imprimir_titulo("ESTUDIANTES")
    mostrar_lista(
        obtener_estudiantes(),
        "Todavía no hay estudiantes."
    )
    pausa()


def buscar_estudiante_menu():
    imprimir_titulo("BUSCAR ESTUDIANTE")

    termino = input(
        "Nombre, apellido, email, carnet o carrera: "
    )

    mostrar_lista(
        buscar_estudiantes(termino),
        f"No hay coincidencias con '{termino}'."
    )
    pausa()


def ver_estudiante():
    imprimir_titulo("VER ESTUDIANTE POR ID")

    id_estudiante = pedir_entero("ID del estudiante: ")

    if id_estudiante is None:
        imprimir_error("El ID debe ser un número entero.")
        return pausa()

    estudiante = obtener_estudiante(id_estudiante)

    if estudiante is None:
        imprimir_error("No existe ese estudiante.")
    else:
        mostrar_detalle(estudiante)

        promedio = promedio_de_estudiante(id_estudiante)

        if promedio is None:
            imprimir_info("El estudiante todavía no tiene notas.")
        else:
            imprimir_info(f"Promedio de notas: {promedio}")

    pausa()


def actualizar_estudiante_menu():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")

    id_estudiante = pedir_entero("ID del estudiante: ")

    if id_estudiante is None:
        imprimir_error("El ID debe ser un número entero.")
        return pausa()

    estudiante = obtener_estudiante(id_estudiante)

    if estudiante is None:
        imprimir_error("No existe ese estudiante.")
        return pausa()

    imprimir_info(f"Editando: {estudiante.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")

    cambios = {}

    for campo in (
        "nombre", "apellido", "email", "carnet", "carrera"
    ):
        actual = getattr(estudiante, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()

        if nuevo:
            cambios[campo] = nuevo

    mostrar_resultado(
        *actualizar_estudiante(id_estudiante, cambios)
    )
    pausa()


def eliminar_estudiante_menu():
    imprimir_titulo("ELIMINAR ESTUDIANTE")

    id_estudiante = pedir_entero("ID del estudiante: ")

    if id_estudiante is None:
        imprimir_error("El ID debe ser un número entero.")
        return pausa()

    estudiante = obtener_estudiante(id_estudiante)

    if estudiante is None:
        imprimir_error("No existe ese estudiante.")
        return pausa()

    imprimir_info(f"Se eliminará: {estudiante.etiqueta()}")

    if confirmar("¿Confirma la eliminación?"):
        mostrar_resultado(eliminar_estudiante(id_estudiante))
    else:
        imprimir_info("Operación cancelada.")

    pausa()


# ============================================================
# MENÚ DE MATERIAS
# ============================================================

def crear_materia_menu():
    imprimir_titulo("CREAR MATERIA")

    datos = {
        "nombre": input("Nombre de la materia: "),
        "codigo": input("Código: "),
        "creditos": input("Créditos (1 a 10): "),
        "cupos": input(
            f"Cupos (0 a {30}; Enter para usar el máximo): "
        )
    }

    # Si no se escribe un número de cupos, se usa el máximo.
    if datos["cupos"].strip() == "":
        datos["cupos"] = 30

    mostrar_resultado(*crear_materia(datos))
    pausa()


def listar_materias():
    imprimir_titulo("MATERIAS")

    mostrar_lista(
        obtener_materias(),
        "Todavía no hay materias."
    )
    pausa()


def buscar_materia_menu():
    imprimir_titulo("BUSCAR MATERIA")

    termino = input("Nombre o código: ")

    mostrar_lista(
        buscar_materias(termino),
        "No hay materias que coincidan."
    )
    pausa()


def ver_materia():
    imprimir_titulo("VER MATERIA POR ID")

    id_materia = pedir_entero("ID de la materia: ")

    if id_materia is None:
        imprimir_error("El ID debe ser un número entero.")
        return pausa()

    materia = obtener_materia(id_materia)

    if materia is None:
        imprimir_error("No existe esa materia.")
    else:
        mostrar_detalle(materia)

    pausa()


def actualizar_materia_menu():
    imprimir_titulo("ACTUALIZAR MATERIA")

    id_materia = pedir_entero("ID de la materia: ")

    if id_materia is None:
        imprimir_error("El ID debe ser un número entero.")
        return pausa()

    materia = obtener_materia(id_materia)

    if materia is None:
        imprimir_error("No existe esa materia.")
        return pausa()

    imprimir_info(f"Editando: {materia.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")

    cambios = {}

    for campo in ("nombre", "codigo", "creditos", "cupos"):
        actual = getattr(materia, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()

        if nuevo:
            cambios[campo] = nuevo

    mostrar_resultado(
        *actualizar_materia(id_materia, cambios)
    )
    pausa()


def eliminar_materia_menu():
    imprimir_titulo("ELIMINAR MATERIA")

    id_materia = pedir_entero("ID de la materia: ")

    if id_materia is None:
        imprimir_error("El ID debe ser un número entero.")
        return pausa()

    materia = obtener_materia(id_materia)

    if materia is None:
        imprimir_error("No existe esa materia.")
        return pausa()

    imprimir_info(f"Se eliminará: {materia.etiqueta()}")

    if confirmar("¿Confirma la eliminación?"):
        mostrar_resultado(eliminar_materia(id_materia))
    else:
        imprimir_info("Operación cancelada.")

    pausa()


# ============================================================
# MENÚ DE MATRÍCULAS
# ============================================================

def matricular_estudiante():
    imprimir_titulo("REGISTRAR MATRÍCULA")

    imprimir_info("Estudiantes disponibles:")
    mostrar_lista(obtener_estudiantes())

    imprimir_info("Materias disponibles:")
    mostrar_lista(obtener_materias())

    estudiante_id = pedir_entero("\nID del estudiante: ")
    materia_id = pedir_entero("ID de la materia: ")
    periodo = input("Periodo académico (ej. 2026-1): ").strip()

    if estudiante_id is None or materia_id is None:
        imprimir_error("Los ID deben ser números enteros.")
        return pausa()

    datos = {
        "estudiante_id": estudiante_id,
        "materia_id": materia_id,
        "periodo": periodo
    }

    mostrar_resultado(*crear_matricula(datos))
    pausa()


def listar_matriculas():
    imprimir_titulo("MATRÍCULAS")

    mostrar_lista(
        obtener_matriculas(),
        "Todavía no hay matrículas."
    )
    pausa()


def registrar_nota_menu():
    imprimir_titulo("REGISTRAR NOTA")

    mostrar_lista(obtener_matriculas())

    id_matricula = pedir_entero("\nID de la matrícula: ")

    if id_matricula is None:
        imprimir_error("El ID debe ser un número entero.")
        return pausa()

    matricula = obtener_matricula(id_matricula)

    if matricula is None:
        imprimir_error("No existe esa matrícula.")
        return pausa()

    nota = pedir_decimal("Nota (0 a 20): ")

    if nota is None:
        imprimir_error("La nota debe ser numérica.")
        return pausa()

    mostrar_resultado(
        *registrar_nota(id_matricula, nota)
    )
    pausa()


def ver_certificado():
    imprimir_titulo("CERTIFICADO ACADÉMICO")

    id_matricula = pedir_entero("ID de la matrícula: ")

    if id_matricula is None:
        imprimir_error("El ID debe ser un número entero.")
        return pausa()

    texto = certificado(id_matricula)

    if texto is None:
        imprimir_error("No existe esa matrícula.")
    else:
        print()
        print(texto)

    pausa()


def retirar_matricula_menu():
    imprimir_titulo("RETIRAR MATRÍCULA")

    mostrar_lista(obtener_matriculas())

    id_matricula = pedir_entero("\nID de la matrícula: ")

    if id_matricula is None:
        imprimir_error("El ID debe ser un número entero.")
        return pausa()

    matricula = obtener_matricula(id_matricula)

    if matricula is None:
        imprimir_error("No existe esa matrícula.")
        return pausa()

    imprimir_info(f"Se retirará: {matricula.etiqueta()}")

    if confirmar("¿Confirma el retiro de la matrícula?"):
        mostrar_resultado(retirar_matricula(id_matricula))
    else:
        imprimir_info("Operación cancelada.")

    pausa()


# ============================================================
# RESUMEN ACADÉMICO
# ============================================================

def resumen():
    imprimir_titulo("RESUMEN ACADÉMICO")

    estudiantes = obtener_estudiantes()
    materias = obtener_materias()
    matriculas = obtener_matriculas()

    # CONJUNTO: reúne las carreras sin repetirlas.
    carreras = sorted({
        estudiante.carrera
        for estudiante in estudiantes
        if estudiante.carrera.strip() != ""
    })

    # Cuenta las matrículas cuya nota alcanza el mínimo de aprobación.
    aprobadas = sum(
        1 for matricula in matriculas
        if matricula.esta_aprobada()
    )

    sin_cupo = materias_sin_cupo()

    print(f"  Estudiantes             : {len(estudiantes)}")
    print(f"  Carreras distintas      : {', '.join(carreras) or '-'}")
    print(f"  Materias registradas    : {len(materias)}")
    print(f"  Materias sin cupo       : {len(sin_cupo)}")
    print(f"  Matrículas registradas  : {len(matriculas)}")
    print(f"  Matrículas aprobadas    : {aprobadas}")

    if sin_cupo:
        print("\nMaterias sin cupo disponible:")

        for materia in sin_cupo:
            print(f"  - {materia.nombre} ({materia.codigo})")

    pausa()


# ============================================================
# MENÚS
# DICCIONARIO: relaciona cada opción con su texto y función.
# ============================================================

MENU_ESTUDIANTES = {
    "1": ("Crear estudiante", crear_estudiante_menu),
    "2": ("Ver todos", listar_estudiantes),
    "3": ("Buscar", buscar_estudiante_menu),
    "4": ("Ver por ID", ver_estudiante),
    "5": ("Actualizar", actualizar_estudiante_menu),
    "6": ("Eliminar", eliminar_estudiante_menu),
    "0": ("Volver", None)
}

MENU_MATERIAS = {
    "1": ("Crear materia", crear_materia_menu),
    "2": ("Ver todas", listar_materias),
    "3": ("Buscar", buscar_materia_menu),
    "4": ("Ver por ID", ver_materia),
    "5": ("Actualizar", actualizar_materia_menu),
    "6": ("Eliminar", eliminar_materia_menu),
    "0": ("Volver", None)
}

MENU_MATRICULAS = {
    "1": ("Matricular", matricular_estudiante),
    "2": ("Ver todas", listar_matriculas),
    "3": ("Registrar nota", registrar_nota_menu),
    "4": ("Ver certificado", ver_certificado),
    "5": ("Retirar matrícula", retirar_matricula_menu),
    "0": ("Volver", None)
}


def ejecutar_menu(titulo, opciones):
    while True:
        imprimir_titulo(titulo)

        for tecla, (texto, funcion) in opciones.items():
            print(f"  {tecla}. {texto}")

        print()
        tecla = input("Opción: ").strip()

        if tecla not in opciones:
            imprimir_error("Opción no válida.")
            pausa()
            continue

        texto, funcion = opciones[tecla]

        if funcion is None:
            break

        funcion()


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():
    while True:
        imprimir_titulo("SISTEMA DE GESTIÓN ACADÉMICA")

        print("  1. Estudiantes")
        print("  2. Materias")
        print("  3. Matrículas")
        print("  4. Resumen")
        print("  0. Salir\n")

        tecla = input("Opción: ").strip()

        if tecla == "1":
            ejecutar_menu("ESTUDIANTES", MENU_ESTUDIANTES)

        elif tecla == "2":
            ejecutar_menu("MATERIAS", MENU_MATERIAS)

        elif tecla == "3":
            ejecutar_menu("MATRÍCULAS", MENU_MATRICULAS)

        elif tecla == "4":
            resumen()

        elif tecla == "0":
            imprimir_info("¡Hasta luego!")
            break

        else:
            imprimir_error("Opción no válida.")
            pausa()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")
