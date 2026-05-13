# Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

## Descripción
Proyecto funcional en Python que desarrolla un sistema orientado a objetos, sin uso de base de datos, para gestionar clientes, servicios y reservas.

## Requisitos cumplidos
- Clase abstracta general: `EntidadSistema`.
- Clase `Cliente` con encapsulación y validaciones.
- Clase abstracta `Servicio`.
- Tres servicios especializados:
  - `ReservaSala`
  - `AlquilerEquipo`
  - `AsesoriaEspecializada`
- Clase `Reserva` con confirmación, cancelación y procesamiento.
- Herencia, abstracción, polimorfismo y encapsulación.
- Métodos con parámetros opcionales que simulan sobrecarga para el cálculo de costos.
- Excepciones personalizadas.
- Uso de `try/except`, `try/except/else/finally` y encadenamiento de excepciones con `raise ... from`.
- Registro de eventos y errores en `logs/sistema_fj.log`.
- Simulación de 12 operaciones completas, válidas e inválidas.
- No utiliza motor de base de datos; toda la información se maneja con objetos y listas internas.

## Cómo ejecutar
1. Descomprimir el archivo ZIP.
2. Abrir una terminal en la carpeta del proyecto.
3. Ejecutar:

```bash
python main.py
```

## Archivos incluidos
- `main.py`: código fuente completo.
- `README.md`: explicación del proyecto.
- `resultado_ejecucion.txt`: salida de ejemplo de la simulación.
- `logs/sistema_fj.log`: archivo de eventos y errores generado durante la ejecución.

## Nota
El programa está diseñado para continuar funcionando aunque ocurran errores, registrando cada evento relevante en el archivo de logs.
