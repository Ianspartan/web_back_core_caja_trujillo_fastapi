# Historias de Usuario y Requisitos Funcionales — Core Caja Trujillo

> Convención: **HU** = Historia de Usuario, **RF** = Requisito Funcional.
> Estado: ✅ implementado · 🟡 parcial · ⬜ pendiente.

---

## ÉPICA 1 — Otorgamiento de Créditos (MPR-003-CRE) [✅]

### HU-01 — Solicitar crédito (cliente vía Homebanking) ✅

> Como **cliente**, quiero solicitar un crédito desde el portal para evitar acudir presencialmente a una agencia.

* RF-01.1 El cliente autenticado envía monto, plazo, tipo (ME/PE/CO), actividad e ingreso. ✅
* RF-01.2 El sistema crea la solicitud en estado **"En Evaluación"**. ✅
* RF-01.3 Si el cliente no es sujeto de crédito, la solicitud se rechaza indicando el motivo (HTTP 422). ✅

### HU-02 — Pre-scoring y evaluación de riesgo ✅

> Como **asesor**, quiero obtener un pre-scoring automático para priorizar la evaluación crediticia.

* RF-02.1 Calcular el score (capacidad, historial, sector y plazo) y emitir una decisión. ✅
* RF-02.2 Calcular el RDS (3 ratios según Art. 13) con semáforo de apetito y tolerancia al riesgo. ✅
* RF-02.3 Validar la elegibilidad del cliente (sujeto de crédito, Política 2.3.A). ✅

### HU-03 — Registrar ingresos y evaluación ✅

> Como **asesor**, quiero registrar la fuente de ingresos y la evaluación del cliente.

* RF-03.1 Registrar la fuente de ingreso (negocio, boleta o recibo por honorarios) en **fclientefuenteingreso**. ✅
* RF-03.2 Registrar la evaluación ME (activos) o CO (capacidad de pago). ✅

### HU-04 — Ruta de aprobación por monto ✅

> Como **sistema**, debo derivar automáticamente la solicitud al nivel de aprobación correspondiente.

* RF-04.1 Determinar el nivel de aprobación según el monto (dnivelaprobacion, 7 niveles). ✅
* RF-04.2 Determinar si requiere opinión de Administrador, Jefe Regional o Riesgos. ✅

### HU-05 — Comité y resolución ✅

> Como **comité**, quiero aprobar o denegar solicitudes dejando evidencia de la decisión.

* RF-05.1 Enviar la solicitud al comité (estado **En Comité**). ✅
* RF-05.2 Resolver: **Aprobado**, **Denegado temporal** o **Denegado definitivo**. ✅
* RF-05.3 Regla obligatoria: una opinión desfavorable de Riesgos impide la aprobación por cualquier comité. ✅

### HU-06 — Desembolso ✅

> Como **comité u operaciones**, quiero desembolsar el crédito para que el cliente lo visualice en su portal.

* RF-06.1 Crear la cuenta de crédito y registrar el movimiento de desembolso. ✅
* RF-06.2 Mostrar el desembolso en los movimientos del Homebanking. ✅
* RF-06.3 Generar un cronograma referencial de pagos. ✅

---

## ÉPICA 2 — Homebanking [🟡]

### HU-07 — Login del cliente ✅

* RF-07.1 Autenticación mediante usuario y contraseña (bcrypt), generando un token de tipo **cliente**. ✅
* RF-07.2 Bloqueo tras múltiples intentos fallidos. 🟡

### HU-08 — Consultar cuentas y movimientos 🟡

> Como **cliente**, quiero visualizar mis cuentas y movimientos financieros.

* RF-08.1 Consultar cuentas de ahorro con su saldo. 🟡
* RF-08.2 Consultar créditos con saldo y cuotas pendientes. ✅
* RF-08.3 Visualizar movimientos (desembolsos y pagos). ✅

### HU-09 — Pagar cuota desde el portal ✅

* RF-09.1 Permitir el pago de la siguiente cuota pendiente. ✅
* RF-09.2 Registrar el pago como movimiento del canal App. ✅

### HU-10 — Transferencias propias ⬜

---

## ÉPICA 3 — Gestión y Dashboard [✅]

### HU-11 — Dashboard institucional ✅

* RF-11.1 Mostrar KPIs de cartera (total, vigente, vencida y ratio de mora). ✅
* RF-11.2 Mostrar productividad de asesores respecto a sus metas. ✅
* RF-11.3 Mostrar desembolsos por mes, año, oficina y zona. ✅

### HU-12 — Bandeja de solicitudes ✅

* RF-12.1 Listar solicitudes con filtros por estado, búsqueda y rango de fechas. ✅
* RF-12.2 Mostrar contadores por estado. ✅

### HU-13 — Mi cartera (asesor) ✅

* RF-13.1 El asesor visualiza automáticamente únicamente su cartera mediante el **pkasesor** almacenado en el token JWT. ✅

---

## ÉPICA 4 — Recuperaciones y Mora [⬜]

### HU-14 — Consultar cartera en mora ⬜

> Como **gestor o administrador**, quiero consultar los créditos en mora por bandas.

* RF-14.1 Mostrar cartera por bandas: preventiva, temprana, tardía, judicial y castigada. ⬜
* RF-14.2 Mostrar KPIs de mora por agencia y asesor. ⬜

### HU-15 — Registrar gestión de cobranza ⬜

> Como **gestor de cobranza**, quiero registrar las acciones realizadas sobre un crédito.

* RF-15.1 Registrar tipo de gestión, fecha, gestor, resultado y compromiso de pago. ⬜
* RF-15.2 Consultar el historial de gestiones de un crédito. ⬜
* RF-15.3 Mostrar la agenda de gestiones pendientes. ⬜

### HU-16 — Transiciones de estado de cobranza ⬜

> Como **funcionario de recuperaciones**, quiero escalar el crédito según las políticas institucionales.

* RF-16.1 Pasar un crédito a Cobranza Judicial. ⬜
* RF-16.2 Castigar créditos con más de 180 días de atraso. ⬜
* RF-16.3 Validar reglas de negocio y permisos según el rol. ⬜

### HU-17 — Mora preventiva automática ⬜

> Como **sistema**, quiero generar recordatorios automáticos antes y durante el inicio del atraso.

* RF-17.1 Identificar créditos entre -1 y 2 días de atraso y generar notificaciones. ⬜

---

## Matriz de permisos por rol

| Acción            | Roles                                     |
| ----------------- | ----------------------------------------- |
| Consultar mora    | asesor, administrador, riesgos, gerencia  |
| Registrar gestión | asesor, gestor_cobranza                   |
| Registrar visita  | gestor_cobranza, administrador            |
| Pasar a judicial  | funcionario_recuperaciones, administrador |
| Castigar crédito  | comité, gerencia                          |

---

## Definición de Hecho (Definition of Done)

1. Endpoint implementado con validación de permisos por rol.
2. Funcionalidad verificada con datos reales de la base de datos.
3. Integridad referencial preservada.
4. Frontend consume correctamente el endpoint y presenta la información.
5. Evidencia alineada al proceso y normativa correspondiente.
