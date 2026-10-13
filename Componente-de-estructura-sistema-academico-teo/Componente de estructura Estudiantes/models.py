
from datetime import date


# --- Clase ModeloBase ---

class ModeloBase:

    def __init__(self, id_registro):
        self.id = id_registro

    @classmethod
    def desde_diccionario(cls, datos):
        datos = datos.copy()
        id_registro = datos.pop("id")
        return cls(id_registro, **datos)

    def a_diccionario(self):
        return {"id": self.id}

    def etiqueta(self):
        return f"Registro #{self.id}"

    def __str__(self):
        return self.etiqueta()


# --- Clase Persona ---

class Persona(ModeloBase):

    def __init__(self, id_registro, nombre, apellido, email):
        super().__init__(id_registro)
        self.nombre = nombre
        self.apellido = apellido
        self.email = email

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["nombre"] = self.nombre
        datos["apellido"] = self.apellido
        datos["email"] = self.email
        return datos

    def etiqueta(self):
        return self.nombre_completo()


# --- Clase Estudiante ---

class Estudiante(Persona):

    def __init__(self, id_registro, nombre, apellido, email,
                 carnet="", carrera=""):
        super().__init__(id_registro, nombre, apellido, email)
        self.carnet = carnet
        self.carrera = carrera

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["carnet"] = self.carnet
        datos["carrera"] = self.carrera
        return datos

    def etiqueta(self):
        return (
            f"{self.nombre_completo()} · "
            f"{self.carnet} · {self.carrera}"
        )


# --- Clase Materia ---

class Materia(ModeloBase):

    CUPOS_MAXIMOS = 30
    NOTA_APROBACION = 14

    def __init__(self, id_registro, nombre, codigo,
                 creditos, cupos=30):
        super().__init__(id_registro)
        self.nombre = nombre
        self.codigo = codigo
        self.creditos = int(creditos)
        self.cupos = int(cupos)

    @staticmethod
    def es_nota_valida(valor):
        try:
            nota = float(valor)
            return 0 <= nota <= 20
        except (ValueError, TypeError):
            return False

    def hay_cupo(self):
        return self.cupos > 0

    def ocupar_cupo(self):
        if self.hay_cupo():
            self.cupos -= 1
            return True
        return False

    def liberar_cupo(self):
        if self.cupos < Materia.CUPOS_MAXIMOS:
            self.cupos += 1
            return True
        return False

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["nombre"] = self.nombre
        datos["codigo"] = self.codigo
        datos["creditos"] = self.creditos
        datos["cupos"] = self.cupos
        return datos

    def etiqueta(self):
        return (
            f"{self.nombre} · {self.codigo} · "
            f"{self.creditos} créditos · {self.cupos} cupos"
        )


# --- Clase Matricula ---

class Matricula(ModeloBase):

    def __init__(self, id_registro, estudiante_id, materia_id,
                 periodo, nota=0, fecha=None):
        super().__init__(id_registro)
        self.estudiante_id = int(estudiante_id)
        self.materia_id = int(materia_id)
        self.periodo = periodo
        self.nota = float(nota)

        if fecha is None:
            self.fecha = date.today()
        else:
            self.fecha = fecha

    def esta_aprobada(self):
        return self.nota >= Materia.NOTA_APROBACION

    def estado(self):
        if self.esta_aprobada():
            return "Aprobado"
        return "Reprobado"

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["estudiante_id"] = self.estudiante_id
        datos["materia_id"] = self.materia_id
        datos["periodo"] = self.periodo
        datos["nota"] = self.nota

        if hasattr(self.fecha, "isoformat"):
            datos["fecha"] = self.fecha.isoformat()
        else:
            datos["fecha"] = self.fecha

        return datos

    def etiqueta(self):
        return (
            f"Matrícula #{self.id} · "
            f"Estudiante {self.estudiante_id} · "
            f"Materia {self.materia_id} · "
            f"{self.periodo} · Nota: {self.nota} · "
            f"{self.estado()}"
        )
