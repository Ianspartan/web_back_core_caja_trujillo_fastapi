# Estado Global del Ecosistema + Roadmap (Recuperaciones / Mora)

## 1. Mapa del ecosistema (4 proyectos + Base de Datos compartida)

```text
                         ┌────────────────────────────────┐
                         │ PostgreSQL: bd_core_financiero │
                         │ Base de datos compartida       │
                         └──────────────┬─────────────────┘
              ┌────────────────────────┼────────────────────────┐
              │                        │                        │
   ┌──────────▼──────────┐   ┌─────────▼───────────┐
   │ BACKEND CORE :8001  │   │ BACKEND HB :8002    │
   │ FastAPI             │   │ FastAPI             │
   │ Core Financiero     │   │ Homebanking         │
   └──────────┬──────────┘   └─────────┬───────────┘
              │                        │
   ┌──────────▼──────────┐   ┌─────────▼───────────┐
   │ FRONT CORE :5173    │   │ FRONT HB :5174      │
   │ Personal Caja       │   │ Portal Cliente      │
   │ Trujillo            │   │ Caja Trujillo       │
   └─────────────────────┘   └─────────────────────┘
```

---

# 2. Estado por proyecto

| Proyecto                        | Estado           | Detalle                                                                                  |
| ------------------------------- | ---------------- | ---------------------------------------------------------------------------------------- |
| **Backend Core (8001)**         | ✅ Operativo      | Flujo de otorgamiento de créditos, dashboard, bandeja, desembolso y productos dinámicos. |
| **Frontend Core (5173)**        | ✅ Operativo      | Consume los endpoints del Core Financiero.                                               |
| **Backend Homebanking (8002)**  | 🟡 En desarrollo | API para clientes del portal Homebanking.                                                |
| **Frontend Homebanking (5174)** | 🟡 En desarrollo | Portal del cliente.                                                                      |
| **Base de Datos**               | ✅ Operativa      | PostgreSQL compartida entre Core y Homebanking.                                          |

---

# 3. Funcionalidades implementadas

## Core Financiero

* Solicitud de crédito.
* Pre-scoring.
* Evaluación.
* Ruta de aprobación.
* Comité.
* Resolución.
* Desembolso.
* Cronograma de pagos.

## Homebanking

* Login del cliente.
* Consulta de movimientos.
* Solicitud de créditos.
* Pago de cuotas.

## Dashboard

* KPIs.
* Mora.
* Productividad.
* Desembolsos.

## Seguridad

* JWT.
* Roles.
* Control de acceso.

---

# 4. Recuperaciones y Mora

## Soporte actual de la Base de Datos

Existe información para:

* días de atraso
* saldo vencido
* intereses moratorios
* créditos judiciales
* créditos castigados

Falta implementar:

* Gestión de cobranzas.
* Historial de acciones.
* Agenda de compromisos.

---

## Bandas de mora

| Banda      | Estado     |
| ---------- | ---------- |
| Preventiva | Disponible |
| Temprana   | Disponible |
| Tardía     | Disponible |
| Judicial   | Disponible |
| Castigada  | Disponible |

---

## Roadmap

### Fase R1

Consulta de mora.

* Dashboard.
* Indicadores.
* Bandas.

### Fase R2

Gestión de cobranzas.

* Registrar llamadas.
* Registrar SMS.
* Registrar visitas.

### Fase R3

Transiciones.

* Judicial.
* Castigo.
* Validaciones.

---

# 5. Roles

* Asesor
* Gestor de cobranza
* Administrador
* Funcionario de recuperaciones
* Comité
* Gerencia

---

## Conclusión

El ecosistema implementado para **Caja Trujillo** utiliza una única base de datos PostgreSQL compartida entre el Core Financiero y el Homebanking, permitiendo integrar los procesos de evaluación, aprobación, desembolso y recuperación de créditos dentro de una misma arquitectura.
