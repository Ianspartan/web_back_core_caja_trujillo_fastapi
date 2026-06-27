# Análisis — Simulación del flujo Homebanking ⇄ Core (Otorgamiento de Créditos)

> **Objetivo:** El cliente solicita un crédito desde el Homebanking → el asesor realiza la evaluación en el Core (registrando ingresos, estados financieros o boletas según el tipo de crédito) → se determina la ruta de aprobación → comité → aprobación → desembolso al Homebanking → el cliente realiza el pago desde el Homebanking.
>
> **Alcance:** únicamente créditos **Microempresa (ME)** y **Consumo (CO)**.

---

# 1. Hallazgo principal: NO es necesario poblar las 77 tablas

Las 77 tablas de la base de datos pueden dividirse en tres grupos:

### A. Catálogos (ya existentes)

No requieren modificaciones.

* dtipocredito
* dproducto
* dcalificacioncrediticia
* dnivelaprobacion
* dagencia
* dasesor
* dmoneda
* dsectoreconomico
* dactividadeconomica
* destadocredito
* dsolicitudestado
* etc.

**≈45 tablas ya se encuentran correctamente pobladas.**

---

### B. Datos transaccionales existentes

Se reutilizan sin necesidad de recrearlos.

* dcliente
* dcuentacredito
* fagcuentacredito
* dcuentaahorro
* entre otras.

Los datos fueron revisados y mantienen consistencia.

---

### C. Tablas necesarias para el flujo de negocio

Estas tablas requieren generación de información.

* usuarios_homebanking
* foperaciones
* fclientefuenteingreso
* devaluacion
* fevalconsumo
* fevalmicroactivo
* fevalempresarial (opcional)

**Conclusión:** el verdadero trabajo consiste aproximadamente en poblar seis tablas, no las 77 existentes.

---

# 2. La base de datos ya contiene la estructura necesaria

## Homebanking

**usuarios_homebanking**

Permite el acceso del cliente al portal mediante usuario y contraseña.

**foperaciones**

Registra:

* pagos
* transferencias
* desembolsos

Además permite diferenciar el canal utilizado (Homebanking o Ventanilla).

---

## Evaluación crediticia

**fclientefuenteingreso**

Registra las fuentes de ingreso del cliente.

**devaluacion**

Representa la cabecera de la evaluación crediticia asociada a una solicitud.

**fevalconsumo**

Contiene el detalle para créditos de Consumo.

**fevalmicroactivo**

Contiene la evaluación financiera simplificada para Microempresa.

La estructura existente permite implementar completamente el flujo definido para el proceso MPR-003-CRE.

---

# 3. Relación entre el flujo y las tablas

| Paso | Acción                    | Tabla                                            |
| ---- | ------------------------- | ------------------------------------------------ |
| 0    | Crear usuario Homebanking | usuarios_homebanking                             |
| 1    | Consultar movimientos     | foperaciones                                     |
| 2    | Registrar solicitud       | dsolicitud                                       |
| 3    | Registrar ingresos        | fclientefuenteingreso                            |
| 4    | Registrar evaluación      | devaluacion + fevalconsumo / fevalmicroactivo    |
| 5    | Ruta de aprobación        | determinar_ruta                                  |
| 6    | Comité                    | dsolicitud                                       |
| 7    | Desembolso                | dcuentacredito + fagcuentacredito + foperaciones |
| 8    | Pago de cuota             | foperaciones                                     |

---

# 4. Estrategia recomendada

En lugar de generar miles de sentencias INSERT manuales, se propone desarrollar dos generadores en Python.

## seed_homebanking.py

Genera:

* usuarios del portal
* historial de operaciones
* pagos
* transferencias

---

## seed_evaluaciones.py

Genera automáticamente:

* fuentes de ingreso
* evaluación crediticia
* evaluación ME
* evaluación CO

Cada generador:

* utiliza los catálogos reales
* respeta las relaciones entre tablas
* evita registros duplicados
* puede ejecutarse múltiples veces sin inconsistencias

---

# 5. Aspectos pendientes

1. Definir la cantidad de clientes con acceso al Homebanking.

2. Definir si se utilizarán solicitudes existentes o se crearán nuevas solicitudes de demostración.

3. Implementar los endpoints faltantes para completar el flujo de negocio.

---

# 6. Endpoints pendientes

| Funcionalidad         | Estado         |
| --------------------- | -------------- |
| Login Homebanking     | ❌ Pendiente    |
| Consultar movimientos | ❌ Pendiente    |
| Solicitar crédito     | ✅ Implementado |
| Registrar ingresos    | ❌ Pendiente    |
| Registrar evaluación  | ❌ Pendiente    |
| Comité                | ✅ Implementado |
| Desembolso            | ❌ Pendiente    |
| Pago de cuota         | ❌ Pendiente    |

---

## Conclusión

La base de datos ya dispone de la estructura necesaria para soportar el flujo completo de otorgamiento de créditos entre el Homebanking y el Core Financiero de **Caja Trujillo**. El principal trabajo pendiente consiste en poblar las tablas transaccionales e implementar los endpoints faltantes para completar el proceso de extremo a extremo.
