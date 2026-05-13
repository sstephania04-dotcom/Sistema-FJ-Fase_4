
"""
Proyecto: Sistema Integral de Gestión de Clientes, Servicios y Reservas
Empresa: Software FJ
Curso: Programación - UNAD

Este programa desarrolla un sistema orientado a objetos, sin base de datos,
con abstracción, herencia, polimorfismo, encapsulación, métodos con parámetros
opcionales tipo sobrecarga y manejo robusto de excepciones.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
import logging
import os
import re
from typing import Any, Dict, List, Optional


# ==========================================================
# CONFIGURACIÓN DE LOGS
# ==========================================================

def configurar_logger() -> logging.Logger:
    """Configura el archivo de logs para eventos y errores."""
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("SoftwareFJ")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        archivo_log = logging.FileHandler("logs/sistema_fj.log", encoding="utf-8")
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        archivo_log.setFormatter(formato)
        logger.addHandler(archivo_log)

    return logger


logger = configurar_logger()


# ==========================================================
# EXCEPCIONES PERSONALIZADAS
# ==========================================================

class SistemaFJException(Exception):
    """Excepción base del sistema Software FJ."""


class ValidacionException(SistemaFJException):
    """Error generado por datos inválidos."""


class ParametroFaltanteException(SistemaFJException):
    """Error generado cuando faltan parámetros obligatorios."""


class ServicioNoDisponibleException(SistemaFJException):
    """Error generado cuando un servicio no está disponible."""


class ReservaException(SistemaFJException):
    """Error generado en operaciones de reservas."""


class CalculoInconsistenteException(SistemaFJException):
    """Error generado por cálculos incorrectos o inconsistentes."""


# ==========================================================
# CLASE ABSTRACTA GENERAL
# ==========================================================

class EntidadSistema(ABC):
    """Clase abstracta general para entidades del sistema."""

    def __init__(self, codigo: str, nombre: str) -> None:
        self._codigo = self._validar_codigo(codigo)
        self._nombre = self._validar_nombre(nombre)

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, nuevo_nombre: str) -> None:
        self._nombre = self._validar_nombre(nuevo_nombre)

    def _validar_codigo(self, codigo: str) -> str:
        if not isinstance(codigo, str) or not codigo.strip():
            raise ValidacionException("El código no puede estar vacío.")
        if len(codigo.strip()) < 3:
            raise ValidacionException("El código debe tener mínimo 3 caracteres.")
        return codigo.strip().upper()

    def _validar_nombre(self, nombre: str) -> str:
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValidacionException("El nombre no puede estar vacío.")
        if len(nombre.strip()) < 3:
            raise ValidacionException("El nombre debe tener mínimo 3 caracteres.")
        return nombre.strip()

    @abstractmethod
    def resumen(self) -> str:
        """Devuelve un resumen textual de la entidad."""
        pass


# ==========================================================
# CLASE CLIENTE
# ==========================================================

class Cliente(EntidadSistema):
    """Cliente con encapsulación y validación de datos personales."""

    def __init__(
        self,
        codigo: str,
        nombre: str,
        documento: str,
        correo: str,
        telefono: str
    ) -> None:
        super().__init__(codigo, nombre)
        self.__documento = self.__validar_documento(documento)
        self.__correo = self.__validar_correo(correo)
        self.__telefono = self.__validar_telefono(telefono)

    @property
    def documento(self) -> str:
        return self.__documento

    @property
    def correo(self) -> str:
        return self.__correo

    @property
    def telefono(self) -> str:
        return self.__telefono

    @correo.setter
    def correo(self, nuevo_correo: str) -> None:
        self.__correo = self.__validar_correo(nuevo_correo)

    @telefono.setter
    def telefono(self, nuevo_telefono: str) -> None:
        self.__telefono = self.__validar_telefono(nuevo_telefono)

    def __validar_documento(self, documento: str) -> str:
        if not isinstance(documento, str) or not documento.isdigit():
            raise ValidacionException("El documento debe contener solo números.")
        if not (6 <= len(documento) <= 12):
            raise ValidacionException("El documento debe tener entre 6 y 12 dígitos.")
        return documento

    def __validar_correo(self, correo: str) -> str:
        patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not isinstance(correo, str) or not re.match(patron, correo):
            raise ValidacionException("El correo electrónico no tiene un formato válido.")
        return correo.lower().strip()

    def __validar_telefono(self, telefono: str) -> str:
        if not isinstance(telefono, str) or not telefono.isdigit():
            raise ValidacionException("El teléfono debe contener solo números.")
        if not (7 <= len(telefono) <= 10):
            raise ValidacionException("El teléfono debe tener entre 7 y 10 dígitos.")
        return telefono

    def resumen(self) -> str:
        return (
            f"Cliente[{self.codigo}] {self.nombre} | "
            f"Documento: {self.documento} | Correo: {self.correo}"
        )


# ==========================================================
# CLASE ABSTRACTA SERVICIO
# ==========================================================

class Servicio(EntidadSistema, ABC):
    """Clase abstracta para los servicios de Software FJ."""

    def __init__(
        self,
        codigo: str,
        nombre: str,
        tarifa_base: float,
        disponible: bool = True
    ) -> None:
        super().__init__(codigo, nombre)
        self._tarifa_base = self._validar_tarifa(tarifa_base)
        self._disponible = bool(disponible)

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        self._disponible = bool(valor)

    def _validar_tarifa(self, tarifa: float) -> float:
        if not isinstance(tarifa, (int, float)):
            raise ValidacionException("La tarifa debe ser numérica.")
        if tarifa <= 0:
            raise ValidacionException("La tarifa debe ser mayor que cero.")
        return float(tarifa)

    @abstractmethod
    def describir(self) -> str:
        """Describe el servicio especializado."""
        pass

    @abstractmethod
    def validar_parametros(self, duracion_horas: int) -> None:
        """Valida parámetros particulares del servicio."""
        pass

    @abstractmethod
    def _calcular_base(self, duracion_horas: int) -> float:
        """Calcula el valor base según el tipo de servicio."""
        pass

    def calcular_costo(
        self,
        duracion_horas: int,
        descuento: float = 0.0,
        incluir_iva: bool = False,
        codigo_promocional: Optional[str] = None
    ) -> float:
        """
        Método con parámetros opcionales que simula sobrecarga:
        - calcular_costo(duracion)
        - calcular_costo(duracion, descuento)
        - calcular_costo(duracion, descuento, incluir_iva)
        - calcular_costo(duracion, descuento, incluir_iva, codigo_promocional)
        """
        try:
            self.validar_parametros(duracion_horas)

            if not isinstance(descuento, (int, float)):
                raise ValidacionException("El descuento debe ser numérico.")
            if descuento < 0 or descuento > 0.80:
                raise ValidacionException("El descuento debe estar entre 0 y 0.80.")

            costo = self._calcular_base(duracion_horas)

            if codigo_promocional:
                if codigo_promocional.upper() == "FJ10":
                    descuento += 0.10
                else:
                    raise ValidacionException("El código promocional no es válido.")

            costo = costo * (1 - descuento)

            if incluir_iva:
                costo = costo * 1.19

            if costo <= 0:
                raise CalculoInconsistenteException("El costo calculado no puede ser menor o igual a cero.")

            return round(costo, 2)

        except SistemaFJException as error:
            # Encadenamiento de excepciones: se conserva el error original.
            raise CalculoInconsistenteException(
                f"No fue posible calcular el costo del servicio {self.codigo}."
            ) from error

    def resumen(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        return f"Servicio[{self.codigo}] {self.nombre} | Tarifa: ${self.tarifa_base:,.0f} | {estado}"


class ReservaSala(Servicio):
    """Servicio especializado para reserva de salas."""

    def __init__(
        self,
        codigo: str,
        nombre: str,
        tarifa_base: float,
        capacidad: int,
        incluye_video_beam: bool = False,
        disponible: bool = True
    ) -> None:
        super().__init__(codigo, nombre, tarifa_base, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ValidacionException("La capacidad de la sala debe ser un entero positivo.")
        self.capacidad = capacidad
        self.incluye_video_beam = incluye_video_beam

    def describir(self) -> str:
        video = "con video beam" if self.incluye_video_beam else "sin video beam"
        return f"Reserva de sala para {self.capacidad} personas, {video}."

    def validar_parametros(self, duracion_horas: int) -> None:
        if not self.disponible:
            raise ServicioNoDisponibleException("La sala no está disponible.")
        if not isinstance(duracion_horas, int) or duracion_horas <= 0:
            raise ValidacionException("La duración debe ser un entero positivo.")
        if duracion_horas > 12:
            raise ValidacionException("La sala solo se puede reservar máximo por 12 horas.")

    def _calcular_base(self, duracion_horas: int) -> float:
        costo = self.tarifa_base * duracion_horas
        if self.capacidad > 20:
            costo *= 1.20
        if self.incluye_video_beam:
            costo += 30000
        return costo


class AlquilerEquipo(Servicio):
    """Servicio especializado para alquiler de equipos."""

    def __init__(
        self,
        codigo: str,
        nombre: str,
        tarifa_base: float,
        tipo_equipo: str,
        requiere_seguro: bool = True,
        disponible: bool = True
    ) -> None:
        super().__init__(codigo, nombre, tarifa_base, disponible)
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise ValidacionException("El tipo de equipo es obligatorio.")
        self.tipo_equipo = tipo_equipo.strip()
        self.requiere_seguro = requiere_seguro

    def describir(self) -> str:
        seguro = "incluye seguro" if self.requiere_seguro else "sin seguro"
        return f"Alquiler de equipo: {self.tipo_equipo}, {seguro}."

    def validar_parametros(self, duracion_horas: int) -> None:
        if not self.disponible:
            raise ServicioNoDisponibleException("El equipo no está disponible.")
        if not isinstance(duracion_horas, int) or duracion_horas <= 0:
            raise ValidacionException("La duración del alquiler debe ser un entero positivo.")
        if duracion_horas > 24:
            raise ValidacionException("El alquiler de equipo no puede superar 24 horas continuas.")

    def _calcular_base(self, duracion_horas: int) -> float:
        costo = self.tarifa_base * duracion_horas
        if duracion_horas >= 8:
            costo *= 0.90
        if self.requiere_seguro:
            costo += 20000
        return costo


class AsesoriaEspecializada(Servicio):
    """Servicio especializado para asesorías profesionales."""

    def __init__(
        self,
        codigo: str,
        nombre: str,
        tarifa_base: float,
        area: str,
        nivel_especialista: str,
        disponible: bool = True
    ) -> None:
        super().__init__(codigo, nombre, tarifa_base, disponible)
        if not isinstance(area, str) or not area.strip():
            raise ValidacionException("El área de asesoría es obligatoria.")

        niveles_validos = {"junior", "semi senior", "senior"}
        if nivel_especialista.lower() not in niveles_validos:
            raise ValidacionException("El nivel debe ser junior, semi senior o senior.")

        self.area = area.strip()
        self.nivel_especialista = nivel_especialista.lower()

    def describir(self) -> str:
        return (
            f"Asesoría especializada en {self.area}, "
            f"nivel {self.nivel_especialista}."
        )

    def validar_parametros(self, duracion_horas: int) -> None:
        if not self.disponible:
            raise ServicioNoDisponibleException("La asesoría no está disponible.")
        if not isinstance(duracion_horas, int) or duracion_horas <= 0:
            raise ValidacionException("La duración de la asesoría debe ser un entero positivo.")
        if duracion_horas > 6:
            raise ValidacionException("La asesoría no puede superar 6 horas por sesión.")

    def _calcular_base(self, duracion_horas: int) -> float:
        multiplicadores = {
            "junior": 1.0,
            "semi senior": 1.30,
            "senior": 1.60
        }
        return self.tarifa_base * duracion_horas * multiplicadores[self.nivel_especialista]


# ==========================================================
# CLASE RESERVA
# ==========================================================

class EstadoReserva(Enum):
    CREADA = "Creada"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
    PROCESADA = "Procesada"


class Reserva(EntidadSistema):
    """Integra cliente, servicio, duración y estado de la reserva."""

    def __init__(
        self,
        codigo: str,
        cliente: Cliente,
        servicio: Servicio,
        duracion_horas: int
    ) -> None:
        super().__init__(codigo, f"Reserva {codigo}")
        if not isinstance(cliente, Cliente):
            raise ValidacionException("La reserva debe tener un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ValidacionException("La reserva debe tener un servicio válido.")
        if not isinstance(duracion_horas, int) or duracion_horas <= 0:
            raise ValidacionException("La duración de la reserva debe ser un entero positivo.")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion_horas = duracion_horas
        self.estado = EstadoReserva.CREADA
        self.fecha_creacion = datetime.now()

    def confirmar(self) -> None:
        try:
            if self.estado != EstadoReserva.CREADA:
                raise ReservaException("Solo se pueden confirmar reservas en estado CREADA.")
            self.servicio.validar_parametros(self.duracion_horas)
            self.estado = EstadoReserva.CONFIRMADA
            logger.info("Reserva confirmada: %s", self.codigo)
        except SistemaFJException as error:
            raise ReservaException(f"No se pudo confirmar la reserva {self.codigo}.") from error

    def cancelar(self) -> None:
        if self.estado == EstadoReserva.PROCESADA:
            raise ReservaException("No se puede cancelar una reserva ya procesada.")
        if self.estado == EstadoReserva.CANCELADA:
            raise ReservaException("La reserva ya se encuentra cancelada.")
        self.estado = EstadoReserva.CANCELADA
        logger.info("Reserva cancelada: %s", self.codigo)

    def procesar(
        self,
        descuento: float = 0.0,
        incluir_iva: bool = True,
        codigo_promocional: Optional[str] = None
    ) -> float:
        try:
            if self.estado != EstadoReserva.CONFIRMADA:
                raise ReservaException("Solo se pueden procesar reservas confirmadas.")

            costo = self.servicio.calcular_costo(
                self.duracion_horas,
                descuento=descuento,
                incluir_iva=incluir_iva,
                codigo_promocional=codigo_promocional
            )
            self.estado = EstadoReserva.PROCESADA
            logger.info("Reserva procesada: %s | Costo final: %.2f", self.codigo, costo)
            return costo

        except SistemaFJException as error:
            raise ReservaException(f"No se pudo procesar la reserva {self.codigo}.") from error

    def resumen(self) -> str:
        return (
            f"Reserva[{self.codigo}] Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | Duración: {self.duracion_horas} horas | "
            f"Estado: {self.estado.value}"
        )


# ==========================================================
# SISTEMA GESTOR
# ==========================================================

class SistemaGestion:
    """Sistema principal con listas internas, sin base de datos."""

    def __init__(self) -> None:
        self.clientes: List[Cliente] = []
        self.servicios: List[Servicio] = []
        self.reservas: List[Reserva] = []

    def registrar_cliente(self, cliente: Cliente) -> None:
        if not isinstance(cliente, Cliente):
            raise ValidacionException("Solo se pueden registrar objetos de tipo Cliente.")
        if self.buscar_cliente(cliente.codigo):
            raise ValidacionException(f"Ya existe un cliente con código {cliente.codigo}.")
        self.clientes.append(cliente)
        logger.info("Cliente registrado: %s", cliente.codigo)

    def crear_cliente_desde_diccionario(self, datos: Dict[str, Any]) -> Cliente:
        """Demuestra encadenamiento de excepciones por parámetros faltantes."""
        try:
            return Cliente(
                datos["codigo"],
                datos["nombre"],
                datos["documento"],
                datos["correo"],
                datos["telefono"]
            )
        except KeyError as error:
            raise ParametroFaltanteException(
                f"Falta el parámetro obligatorio: {error}."
            ) from error

    def registrar_servicio(self, servicio: Servicio) -> None:
        if not isinstance(servicio, Servicio):
            raise ValidacionException("Solo se pueden registrar objetos derivados de Servicio.")
        if self.buscar_servicio(servicio.codigo):
            raise ValidacionException(f"Ya existe un servicio con código {servicio.codigo}.")
        self.servicios.append(servicio)
        logger.info("Servicio registrado: %s", servicio.codigo)

    def crear_reserva(
        self,
        codigo: str,
        codigo_cliente: str,
        codigo_servicio: str,
        duracion_horas: int
    ) -> Reserva:
        cliente = self.buscar_cliente(codigo_cliente)
        servicio = self.buscar_servicio(codigo_servicio)

        if cliente is None:
            raise ReservaException(f"No existe el cliente {codigo_cliente}.")
        if servicio is None:
            raise ReservaException(f"No existe el servicio {codigo_servicio}.")
        if self.buscar_reserva(codigo):
            raise ReservaException(f"Ya existe una reserva con código {codigo}.")

        reserva = Reserva(codigo, cliente, servicio, duracion_horas)
        self.reservas.append(reserva)
        logger.info("Reserva creada: %s", reserva.codigo)
        return reserva

    def buscar_cliente(self, codigo: str) -> Optional[Cliente]:
        return next((c for c in self.clientes if c.codigo == codigo.upper()), None)

    def buscar_servicio(self, codigo: str) -> Optional[Servicio]:
        return next((s for s in self.servicios if s.codigo == codigo.upper()), None)

    def buscar_reserva(self, codigo: str) -> Optional[Reserva]:
        return next((r for r in self.reservas if r.codigo == codigo.upper()), None)

    def reporte_general(self) -> str:
        return (
            f"Clientes registrados: {len(self.clientes)} | "
            f"Servicios registrados: {len(self.servicios)} | "
            f"Reservas registradas: {len(self.reservas)}"
        )


# ==========================================================
# SIMULACIÓN DE OPERACIONES
# ==========================================================

def ejecutar_operacion(numero: int, descripcion: str, accion) -> None:
    """
    Ejecuta una operación demostrando try/except/else/finally.
    Si ocurre un error, se registra en logs y la aplicación continúa.
    """
    print(f"\nOPERACIÓN {numero}: {descripcion}")

    try:
        resultado = accion()
    except SistemaFJException as error:
        logger.exception("Error controlado en operación %s: %s", numero, error)
        print(f"ERROR CONTROLADO: {error}")
        causa = error.__cause__
        if causa:
            print(f"Causa original: {causa}")
    except Exception as error:
        logger.exception("Error general en operación %s: %s", numero, error)
        print(f"ERROR GENERAL CONTROLADO: {error}")
    else:
        logger.info("Operación %s ejecutada correctamente: %s", numero, descripcion)
        if resultado is not None:
            print(resultado)
    finally:
        print("Estado: la aplicación continúa funcionando.")


def main() -> None:
    print("=" * 70)
    print("SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS")
    print("Empresa: Software FJ")
    print("=" * 70)

    sistema = SistemaGestion()

    ejecutar_operacion(
        1,
        "Registro válido de cliente",
        lambda: (
            sistema.registrar_cliente(
                Cliente("CLI001", "Laura Gómez", "1020304050", "laura.gomez@mail.com", "3104567890")
            ),
            sistema.buscar_cliente("CLI001").resumen()
        )[1]
    )

    ejecutar_operacion(
        2,
        "Registro inválido de cliente por correo incorrecto",
        lambda: sistema.registrar_cliente(
            Cliente("CLI002", "Carlos Pérez", "100200300", "correo_invalido", "3123456789")
        )
    )

    ejecutar_operacion(
        3,
        "Creación de cliente con parámetro faltante",
        lambda: sistema.registrar_cliente(
            sistema.crear_cliente_desde_diccionario(
                {
                    "codigo": "CLI003",
                    "nombre": "María Torres",
                    "documento": "99887766",
                    # Falta el correo para generar excepción encadenada.
                    "telefono": "3209876543"
                }
            )
        )
    )

    ejecutar_operacion(
        4,
        "Registro de tres servicios válidos con herencia y polimorfismo",
        lambda: registrar_servicios_validos(sistema)
    )

    ejecutar_operacion(
        5,
        "Creación incorrecta de servicio por tarifa negativa",
        lambda: sistema.registrar_servicio(
            ReservaSala("SAL002", "Sala defectuosa", -50000, capacidad=10)
        )
    )

    ejecutar_operacion(
        6,
        "Reserva exitosa de sala, confirmación y procesamiento con IVA y descuento",
        lambda: procesar_reserva_exitosa(sistema)
    )

    ejecutar_operacion(
        7,
        "Reserva fallida por servicio no disponible",
        lambda: reserva_con_servicio_no_disponible(sistema)
    )

    ejecutar_operacion(
        8,
        "Cancelación correcta de reserva creada",
        lambda: cancelar_reserva_creada(sistema)
    )

    ejecutar_operacion(
        9,
        "Intento incorrecto de procesar una reserva cancelada",
        lambda: procesar_reserva_cancelada(sistema)
    )

    ejecutar_operacion(
        10,
        "Métodos tipo sobrecarga para calcular costos",
        lambda: demostrar_sobrecarga_costos(sistema)
    )

    ejecutar_operacion(
        11,
        "Reserva inválida por duración igual a cero",
        lambda: sistema.crear_reserva("RES004", "CLI001", "ASE001", 0)
    )

    ejecutar_operacion(
        12,
        "Reserva fallida por servicio inexistente",
        lambda: sistema.crear_reserva("RES005", "CLI001", "SER999", 2)
    )

    print("\n" + "=" * 70)
    print("REPORTE FINAL")
    print(sistema.reporte_general())
    print("Revise el archivo logs/sistema_fj.log para ver eventos y errores.")
    print("=" * 70)


def registrar_servicios_validos(sistema: SistemaGestion) -> str:
    servicios: List[Servicio] = [
        ReservaSala("SAL001", "Sala de reuniones premium", 80000, capacidad=25, incluye_video_beam=True),
        AlquilerEquipo("EQP001", "Alquiler de portátil empresarial", 35000, tipo_equipo="Portátil", requiere_seguro=True),
        AsesoriaEspecializada("ASE001", "Asesoría en arquitectura de software", 120000, area="Sistemas", nivel_especialista="senior")
    ]

    descripciones = []
    for servicio in servicios:
        sistema.registrar_servicio(servicio)
        descripciones.append(servicio.describir())

    return "\n".join(descripciones)


def procesar_reserva_exitosa(sistema: SistemaGestion) -> str:
    reserva = sistema.crear_reserva("RES001", "CLI001", "SAL001", 3)
    reserva.confirmar()
    costo = reserva.procesar(descuento=0.10, incluir_iva=True)
    return f"{reserva.resumen()} | Costo final: ${costo:,.2f}"


def reserva_con_servicio_no_disponible(sistema: SistemaGestion) -> str:
    servicio = sistema.buscar_servicio("EQP001")
    if servicio is None:
        raise ServicioNoDisponibleException("No se encontró el servicio EQP001.")

    servicio.disponible = False
    reserva = sistema.crear_reserva("RES002", "CLI001", "EQP001", 5)
    reserva.confirmar()
    return reserva.resumen()


def cancelar_reserva_creada(sistema: SistemaGestion) -> str:
    reserva = sistema.crear_reserva("RES003", "CLI001", "ASE001", 2)
    reserva.cancelar()
    return reserva.resumen()


def procesar_reserva_cancelada(sistema: SistemaGestion) -> str:
    reserva = sistema.buscar_reserva("RES003")
    if reserva is None:
        raise ReservaException("No se encontró la reserva RES003.")
    costo = reserva.procesar()
    return f"Costo procesado: ${costo:,.2f}"


def demostrar_sobrecarga_costos(sistema: SistemaGestion) -> str:
    servicio = sistema.buscar_servicio("ASE001")
    if servicio is None:
        raise ValidacionException("No se encontró el servicio ASE001.")

    costo_basico = servicio.calcular_costo(2)
    costo_con_descuento = servicio.calcular_costo(2, descuento=0.15)
    costo_con_descuento_iva = servicio.calcular_costo(2, descuento=0.15, incluir_iva=True)
    costo_con_codigo = servicio.calcular_costo(2, descuento=0.05, incluir_iva=True, codigo_promocional="FJ10")

    return (
        f"Costo básico: ${costo_basico:,.2f}\n"
        f"Costo con descuento: ${costo_con_descuento:,.2f}\n"
        f"Costo con descuento e IVA: ${costo_con_descuento_iva:,.2f}\n"
        f"Costo con código promocional FJ10: ${costo_con_codigo:,.2f}"
    )


if __name__ == "__main__":
    main()
