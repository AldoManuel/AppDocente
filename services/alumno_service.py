from config.supabase_client import supabase


def obtener_alumnos_por_grupo(grupo_id: int) -> list:
    try:
        response = (
            supabase.table("alumno")
            .select("*")
            .eq("grupo_id", grupo_id)
            .order("numero_lista")
            .execute()
        )
        return response.data if response.data else []
    except Exception as e:
        print(f"Error al obtener alumnos: {e}")
        return []


def recalcular_contadores_alumno(alumno_id: int) -> bool:
    try:
        presentes_resp = (
            supabase.table("asistencia")
            .select("*", count="exact")
            .eq("alumno_id", alumno_id)
            .eq("presente", True)
            .execute()
        )
        faltas_resp = (
            supabase.table("asistencia")
            .select("*", count="exact")
            .eq("alumno_id", alumno_id)
            .eq("presente", False)
            .execute()
        )

        total_presentes = presentes_resp.count if presentes_resp.count else 0
        total_faltas = faltas_resp.count if faltas_resp.count else 0

        supabase.table("alumno").update({
            "Asistencia": total_presentes,
            "Falta": total_faltas,
        }).eq("id", alumno_id).execute()

        return True
    except Exception as e:
        print(f"Error al recalcular contadores del alumno {alumno_id}: {e}")
        return False
