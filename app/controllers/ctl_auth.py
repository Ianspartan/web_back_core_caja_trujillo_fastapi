from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.cfg_security import create_access_token
from app.core.cfg_roles import rol_desde_cargo


MAX_INTENTOS = 5
INTENTOS_FALLIDOS = {}
USUARIOS_BLOQUEADOS = set()


def login(db: Session, numerodni: str, password: str):
    dni = numerodni.strip()

    if dni in USUARIOS_BLOQUEADOS:
        return None

    sql = text("""
        SELECT p.pkpersonal, p.codpersonal, p.nombre,
               cp.codcargopersonal,
               cp.descargopersonal,
               a.pkasesor, a.codasesor
        FROM dpersonal p
        LEFT JOIN dpersonalcargo pc  ON pc.pkpersonal = p.pkpersonal
        LEFT JOIN dcargopersonal cp  ON cp.pkcargopersonal = pc.pkcargopersonal
        LEFT JOIN dpersonalasesor pa ON pa.pkpersonal = p.pkpersonal
        LEFT JOIN dasesor a          ON a.pkasesor = pa.pkasesor
        WHERE p.numerodni = :dni
        LIMIT 1
    """)

    row = db.execute(sql, {"dni": dni}).fetchone()

    if not row or password != dni:
        INTENTOS_FALLIDOS[dni] = INTENTOS_FALLIDOS.get(dni, 0) + 1

        if INTENTOS_FALLIDOS[dni] >= MAX_INTENTOS:
            USUARIOS_BLOQUEADOS.add(dni)

        return None

    INTENTOS_FALLIDOS.pop(dni, None)

    rol = rol_desde_cargo(row.codcargopersonal)
    codagencia = "0001"
    codasesor = row.codasesor.strip() if row.codasesor else None

    token = create_access_token({
        "sub": row.codpersonal,
        "pkpersonal": row.pkpersonal,
        "pkasesor": row.pkasesor,
        "codasesor": codasesor,
        "nombre": row.nombre,
        "rol": rol,
        "cargo": row.descargopersonal or "Asesor de Negocios",
        "codagencia": codagencia,
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "codpersonal": row.codpersonal,
        "pkasesor": row.pkasesor,
        "codasesor": codasesor,
        "nombre": row.nombre,
        "rol": rol,
        "codagencia": codagencia,
    }