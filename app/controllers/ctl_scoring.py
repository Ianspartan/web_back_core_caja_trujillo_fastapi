from sqlalchemy.orm import Session
from app.repositories import rep_clientes, rep_creditos

# ==========================================================
# TARIFARIO DE CRÉDITOS
# ==========================================================
# La TEA (Tasa Efectiva Anual) se obtiene del tarifario del
# producto financiero.
#
# Conversión utilizada por el sistema:
#
# TEM = (1 + TEA/100) ** (1/12) - 1
#
# La TEM es utilizada para calcular:
# - Cuota mensual
# - Cronograma de pagos
#
# Crédito Microempresa:
#   Con seguro    : 40.92%
#   Sin seguro    : 43.92%
# ==========================================================

TEA_POR_TIPO = {
    "ME": {
        "min": 31.90,
        "mid": 72.53,
        "max": 113.16,
        "producto": "Crédito Mype - Microemprendedor",
    },
    "PE": {"min": 31.90, "mid": 72.53, "max": 113.16},
    "CO": {"min": 31.90, "mid": 72.53, "max": 113.16},
    "HI": {"min": 31.90, "mid": 72.53, "max": 113.16},
    "GE": {"min": 31.90, "mid": 72.53, "max": 113.16},
}


SECTORES_RIESGO = {
    # Riesgo bajo
    "4711": 20,
    "4721": 20,
    "4731": 18,
    "5610": 18,
    "6810": 15,
    "8511": 15,

    # Riesgo medio
    "4921": 12,
    "4923": 12,
    "0111": 10,
    "0112": 10,

    # Riesgo alto
    "6201": 8,
    "5510": 8,
}


def calcular_score(
    codcliente: str,
    montosolicitud: float,
    plazo: int,
    codtipocredito: str,
    montoingresoneto: float,
    codactividadeconomica: str,
    db: Session,
) -> dict:

    observaciones = []
    detalle = {}

    # ======================================================
    # 1. CAPACIDAD DE PAGO (40 puntos)
    # ======================================================

    tea_tipo = TEA_POR_TIPO.get(
        codtipocredito,
        {"min": 40.92, "mid": 43.92, "max": 43.92},
    )

    tea_ref = tea_tipo["mid"]

    # Conversión TEA -> TEM
    tem = (1 + tea_ref / 100) ** (1 / 12) - 1

    cuota = (
        montosolicitud
        * tem
        * (1 + tem) ** plazo
        / ((1 + tem) ** plazo - 1)
    )

    ratio_cuota_ingreso = (
        cuota / montoingresoneto if montoingresoneto > 0 else 1
    )

    if ratio_cuota_ingreso <= 0.30:
        score_capacidad = 40

    elif ratio_cuota_ingreso <= 0.40:
        score_capacidad = 30

    elif ratio_cuota_ingreso <= 0.50:
        score_capacidad = 18
        observaciones.append(
            "La cuota representa más del 40% del ingreso neto."
        )

    else:
        score_capacidad = 5
        observaciones.append(
            "La cuota supera el 50% del ingreso neto. Riesgo alto."
        )

    detalle["capacidad_pago"] = {
        "cuota_estimada": round(cuota, 2),
        "ratio_cuota_ingreso": round(ratio_cuota_ingreso * 100, 2),
        "puntaje": score_capacidad,
    }

    # ======================================================
    # 2. HISTORIAL CREDITICIO (30 puntos)
    # ======================================================

    cliente = rep_clientes.get_by_cod(db, codcliente)

    if not cliente:

        score_historial = 10

        observaciones.append(
            "Cliente no registrado en la institución."
        )

    else:

        tiene_vencido = rep_creditos.tiene_mala_calificacion(
            db,
            cliente.pkcliente,
        )

        if tiene_vencido:

            score_historial = 5

            observaciones.append(
                "Cliente registra créditos con calificación Deficiente, Dudoso o Pérdida."
            )

        else:

            score_historial = 30

    detalle["historial"] = {
        "puntaje": score_historial
    }

    # ======================================================
    # 3. SECTOR ECONÓMICO (20 puntos)
    # ======================================================

    score_sector = SECTORES_RIESGO.get(
        codactividadeconomica,
        10,
    )

    detalle["sector_economico"] = {
        "codactividad": codactividadeconomica,
        "puntaje": score_sector,
    }

    # ======================================================
    # 4. PLAZO (10 puntos)
    # ======================================================

    if plazo <= 24:

        score_plazo = 10

    elif plazo <= 48:

        score_plazo = 7

    elif plazo <= 120:

        score_plazo = 4

    else:

        score_plazo = 2

        observaciones.append(
            "Plazo mayor a 10 años incrementa el riesgo."
        )

    detalle["plazo"] = {
        "meses": plazo,
        "puntaje": score_plazo,
    }

    # ======================================================
    # SCORE TOTAL
    # ======================================================

    score_total = (
        score_capacidad
        + score_historial
        + score_sector
        + score_plazo
    )

    detalle["score_total"] = score_total

    # ======================================================
    # DECISIÓN
    # ======================================================

    if score_total >= 70:

        decision = "APROBADO"

        tea_sugerida = tea_tipo["min"]

    elif score_total >= 50:

        decision = "OBSERVADO"

        tea_sugerida = tea_tipo["mid"]

        observaciones.append(
            "Requiere aprobación del jefe de agencia."
        )

    else:

        decision = "RECHAZADO"

        tea_sugerida = tea_tipo["max"]

        observaciones.append(
            "Score insuficiente para aprobación automática."
        )

    # ======================================================
    # CÁLCULO FINAL DEL CRONOGRAMA
    # ======================================================

    tem_real = (1 + tea_sugerida / 100) ** (1 / 12) - 1

    cuota_final = (
        montosolicitud
        * tem_real
        * (1 + tem_real) ** plazo
        / ((1 + tem_real) ** plazo - 1)
    )

    return {
        "codcliente": codcliente,
        "score": round(score_total, 2),
        "decision": decision,
        "tea_sugerida": tea_sugerida,
        "cuota_estimada": round(cuota_final, 2),
        "observaciones": observaciones,
        "detalle_score": detalle,
    }