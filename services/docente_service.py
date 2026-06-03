from config.supabase_client import supabase


def obtener_docente_por_usuario(usuario_id: int) -> dict | None:
    try:
        response = (
            supabase.table("docente")
            .select("*")
            .eq("usuario_id", usuario_id)
            .execute()
        )
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error al obtener docente: {e}")
        return None


def obtener_asignaciones_docente(docente_id: int) -> list:
    try:
        response = (
            supabase.table("docente_grupo_materia")
            .select(
                "id, "
                "grupo!inner(id, grado, nombre), "
                "materia!inner(id, nombre, codigo)"
            )
            .eq("docente_id", docente_id)
            .execute()
        )

        asignaciones = []
        for item in response.data:
            asignaciones.append({
                "docente_grupo_materia_id": item["id"],
                "grado": item["grupo"]["grado"],
                "grupo_id": item["grupo"]["id"],
                "grupo_nombre": item["grupo"]["nombre"],
                "materia_id": item["materia"]["id"],
                "materia_nombre": item["materia"]["nombre"],
                "materia_codigo": item["materia"]["codigo"],
            })

        return asignaciones
    except Exception as e:
        print(f"Error al obtener asignaciones: {e}")
        return []


def obtener_grados_disponibles(asignaciones: list) -> list:
    grados = sorted(set(a["grado"] for a in asignaciones if a.get("grado")))
    return grados


def obtener_grupos_por_grado(asignaciones: list, grado: int) -> list:
    grupos_vistos = {}
    for a in asignaciones:
        if a["grado"] == grado:
            key = a["grupo_id"]
            if key not in grupos_vistos:
                grupos_vistos[key] = {
                    "grupo_id": a["grupo_id"],
                    "grupo_nombre": a["grupo_nombre"],
                }
    return list(grupos_vistos.values())


def obtener_materias_por_grupo(asignaciones: list, grupo_id: int) -> list:
    materias_vistas = {}
    for a in asignaciones:
        if a["grupo_id"] == grupo_id:
            key = a["materia_id"]
            if key not in materias_vistas:
                materias_vistas[key] = {
                    "materia_id": a["materia_id"],
                    "materia_nombre": a["materia_nombre"],
                }
    return list(materias_vistas.values())


def obtener_docente_grupo_materia_id(
    asignaciones: list, grupo_id: int, materia_id: int
) -> int | None:
    for a in asignaciones:
        if a["grupo_id"] == grupo_id and a["materia_id"] == materia_id:
            return a["docente_grupo_materia_id"]
    return None
