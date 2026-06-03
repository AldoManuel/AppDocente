from config.supabase_client import supabase


def login(correo: str, contrasena: str) -> dict | None:
    try:
        response = (
            supabase.table("usuario")
            .select("id, correo, rol")
            .eq("correo", correo)
            .eq("contrasena", contrasena)
            .eq("rol", "docente")
            .execute()
        )

        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error al iniciar sesión: {e}")
        return None
