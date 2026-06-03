-- ============================================================
-- QUERIES PARA INICIO DE SESIÓN Y CONSULTAS DEL DOCENTE
-- ============================================================
-- Base de datos: Supabase (PostgreSQL)
-- ============================================================

-- ============================================================
-- 1. INICIO DE SESIÓN
-- ============================================================

-- 1.1 Verificar credenciales del usuario
-- Busca un usuario por correo, contraseña y rol 'docente'
SELECT
    id,
    correo,
    rol
FROM public.usuario
WHERE
    correo = 'correo_del_docente@ejemplo.com'
    AND contrasena = 'contraseña_del_docente'
    AND rol = 'docente';

-- 1.2 Obtener datos del docente a partir del usuario_id
SELECT
    id,
    usuario_id,
    nombre,
    apellido,
    numero_empleado
FROM public.docente
WHERE usuario_id = 1;  -- Reemplazar 1 con el id del usuario obtenido

-- ============================================================
-- 2. ASIGNACIONES DEL DOCENTE
-- ============================================================

-- 2.1 Obtener todas las asignaciones (grupo-materia) de un docente
-- Incluye grado, nombre del grupo y nombre de la materia
SELECT
    dgm.id AS docente_grupo_materia_id,
    g.grado,
    g.id AS grupo_id,
    g.nombre AS grupo_nombre,
    m.id AS materia_id,
    m.nombre AS materia_nombre,
    m.codigo AS materia_codigo
FROM public.docente_grupo_materia dgm
INNER JOIN public.grupo g ON g.id = dgm.grupo_id
INNER JOIN public.materia m ON m.id = dgm.materia_id
WHERE dgm.docente_id = 1;  -- Reemplazar 1 con el id del docente

-- ============================================================
-- 3. ALUMNOS
-- ============================================================

-- 3.1 Obtener alumnos de un grupo específico
SELECT
    id,
    tutor_id,
    grupo_id,
    nombre,
    apellido,
    numero_lista,
    estatus,
    "Asistencia",
    "Falta"
FROM public.alumno
WHERE grupo_id = 1  -- Reemplazar 1 con el id del grupo
ORDER BY numero_lista ASC;

-- ============================================================
-- 4. ASISTENCIAS
-- ============================================================

-- 4.1 Obtener asistencias de una fecha y materia específicas
SELECT
    id,
    alumno_id,
    docente_grupo_materia_id,
    fecha,
    presente
FROM public.asistencia
WHERE
    docente_grupo_materia_id = 1  -- Reemplazar 1 con el id de docente_grupo_materia
    AND fecha = '2026-06-02';     -- Reemplazar con la fecha deseada

-- 4.2 Verificar si ya existe un registro de asistencia
-- (para upsert: insertar o actualizar)
SELECT id, presente
FROM public.asistencia
WHERE
    alumno_id = 1
    AND docente_grupo_materia_id = 1
    AND fecha = '2026-06-02';

-- 4.3 Insertar un nuevo registro de asistencia
INSERT INTO public.asistencia (alumno_id, docente_grupo_materia_id, fecha, presente)
VALUES (1, 1, '2026-06-02', true);

-- 4.4 Actualizar un registro existente de asistencia
UPDATE public.asistencia
SET presente = false
WHERE id = 1;  -- Reemplazar 1 con el id del registro

-- 4.5 Contar asistencias (presente = true) de un alumno
SELECT COUNT(*) AS total_asistencias
FROM public.asistencia
WHERE alumno_id = 1 AND presente = true;

-- 4.6 Contar faltas (presente = false) de un alumno
SELECT COUNT(*) AS total_faltas
FROM public.asistencia
WHERE alumno_id = 1 AND presente = false;

-- ============================================================
-- 5. RECALCULAR CONTADORES DEL ALUMNO
-- ============================================================

-- 5.1 Actualizar los campos "Asistencia" y "Falta" en la tabla alumno
-- basado en los registros de la tabla asistencia
UPDATE public.alumno
SET
    "Asistencia" = (
        SELECT COUNT(*)
        FROM public.asistencia
        WHERE alumno_id = 1 AND presente = true
    ),
    "Falta" = (
        SELECT COUNT(*)
        FROM public.asistencia
        WHERE alumno_id = 1 AND presente = false
    )
WHERE id = 1;  -- Reemplazar 1 con el id del alumno

-- ============================================================
-- 6. FUNCIÓN PARA INICIO DE SESIÓN (OPCIONAL)
-- ============================================================
-- Función reutilizable que autentica al usuario y devuelve
-- sus datos junto con los del docente en una sola llamada.

-- CREATE OR REPLACE FUNCTION public.login_docente(
--     p_correo TEXT,
--     p_contrasena TEXT
-- )
-- RETURNS TABLE(
--     usuario_id INT,
--     correo TEXT,
--     docente_id INT,
--     nombre TEXT,
--     apellido TEXT,
--     numero_empleado TEXT
-- )
-- LANGUAGE plpgsql
-- SECURITY DEFINER
-- AS $$
-- BEGIN
--     RETURN QUERY
--     SELECT
--         u.id,
--         u.correo,
--         d.id,
--         d.nombre,
--         d.apellido,
--         d.numero_empleado
--     FROM public.usuario u
--     INNER JOIN public.docente d ON d.usuario_id = u.id
--     WHERE
--         u.correo = p_correo
--         AND u.contrasena = p_contrasena
--         AND u.rol = 'docente';
-- END;
-- $$;
