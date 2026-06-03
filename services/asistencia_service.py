from config.supabase_client import supabase
from services.alumno_service import recalcular_contadores_alumno


def obtener_asistencia_por_fecha(
    docente_grupo_materia_id: int, fecha: str
) -> dict:
    try:
        response = (
            supabase.table("asistencia")
            .select("*")
            .eq("docente_grupo_materia_id", docente_grupo_materia_id)
            .eq("fecha", fecha)
            .execute()
        )
        result = {}
        if response.data:
            for registro in response.data:
                result[registro["alumno_id"]] = registro
        return result
    except Exception as e:
        print(f"Error al obtener asistencias por fecha: {e}")
        return {}


def registrar_asistencia(
    alumno_id: int,
    docente_grupo_materia_id: int,
    fecha: str,
    presente: bool,
) -> bool:
    try:
        existente = (
            supabase.table("asistencia")
            .select("*")
            .eq("alumno_id", alumno_id)
            .eq("docente_grupo_materia_id", docente_grupo_materia_id)
            .eq("fecha", fecha)
            .execute()
        )

        if existente.data:
            supabase.table("asistencia").update({
                "presente": presente,
            }).eq("id", existente.data[0]["id"]).execute()
        else:
            supabase.table("asistencia").insert({
                "alumno_id": alumno_id,
                "docente_grupo_materia_id": docente_grupo_materia_id,
                "fecha": fecha,
                "presente": presente,
            }).execute()

        recalcular_contadores_alumno(alumno_id)
        return True
    except Exception as e:
        print(f"Error al registrar asistencia: {e}")
        return False


def obtener_resumen_asistencia(
    docente_grupo_materia_id: int, fecha: str
) -> dict:
    try:
        response = (
            supabase.table("asistencia")
            .select("*")
            .eq("docente_grupo_materia_id", docente_grupo_materia_id)
            .eq("fecha", fecha)
            .execute()
        )

        total_asistencias = 0
        total_faltas = 0
        if response.data:
            for reg in response.data:
                if reg["presente"]:
                    total_asistencias += 1
                else:
                    total_faltas += 1

        return {
            "total_asistencias": total_asistencias,
            "total_faltas": total_faltas,
        }
    except Exception as e:
        print(f"Error al obtener resumen de asistencia: {e}")
        return {"total_asistencias": 0, "total_faltas": 0}
