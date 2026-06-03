import flet as ft

from services.docente_service import (
    obtener_asignaciones_docente,
    obtener_docente_grupo_materia_id,
)
from services.alumno_service import obtener_alumnos_por_grupo
from services.asistencia_service import (
    obtener_asistencia_por_fecha,
    registrar_asistencia,
    obtener_resumen_asistencia,
)
from components.filters_section import FiltersSection
from components.dashboard_card import create_dashboard_card
from components.attendance_table import AttendanceTable


class DocenteView:
    def __init__(self, page: ft.Page, docente_id: int = None, docente_nombre: str = "Docente"):
        self.page = page
        self.docente_id = docente_id
        self.docente_nombre = docente_nombre
        self.asignaciones = []
        self.alumnos = []
        self.filtros_actuales = {}

        self.filters_section = FiltersSection(page, self._on_consultar)
        self.attendance_table = AttendanceTable(
            page, self._on_presente, self._on_falta
        )

        self.dashboard_row = ft.ResponsiveRow(spacing=12)

        self.mensaje_inicial = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(
                        ft.Icons.INFO_OUTLINE,
                        size=48,
                        color="#9CA3AF",
                    ),
                    ft.Container(height=12),
                    ft.Text(
                        "Selecciona un grado, grupo, materia y fecha para consultar los alumnos.",
                        size=16,
                        color="#6B7280",
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=40,
            alignment=ft.Alignment(0, 0),
        )

        self.body_container = ft.Container(
            content=self.mensaje_inicial,
            padding=0,
        )

        self.content_column = ft.Column(
            controls=[
                self._build_header(),
                self.filters_section.build(),
                self.dashboard_row,
                self.body_container,
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
        )

        self.main_container = ft.Container(
            content=self.content_column,
            padding=ft.Padding(left=24, top=24, right=24, bottom=24),
            expand=True,
        )

    def _build_header(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Panel Docente",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color="#1F2937",
                    ),
                    ft.Text(
                        "Gestiona la asistencia de tus grupos y materias asignadas.",
                        size=15,
                        color="#6B7280",
                    ),
                ],
                spacing=4,
            ),
        )

    def load_asignaciones(self):
        if not self.docente_id:
            return
        self.asignaciones = obtener_asignaciones_docente(self.docente_id)
        self.filters_section.set_asignaciones(self.asignaciones)

    def _on_consultar(self, filtros: dict):
        self.filtros_actuales = filtros
        grado = filtros.get("grado")
        grupo_id = filtros.get("grupo_id")
        materia_id = filtros.get("materia_id")
        fecha = filtros.get("fecha")

        if not all([grado, grupo_id, materia_id, fecha]):
            self._mostrar_error("Todos los filtros son obligatorios.")
            return

        dgmi = obtener_docente_grupo_materia_id(
            self.asignaciones, grupo_id, materia_id
        )
        if not dgmi:
            self._mostrar_error("No se encontró la asignación del docente.")
            return

        self.alumnos = obtener_alumnos_por_grupo(grupo_id)
        if not self.alumnos:
            self._mostrar_error(
                "No hay alumnos registrados en este grupo."
            )
            self._mostrar_sin_datos()
            return

        asistencias = obtener_asistencia_por_fecha(dgmi, fecha)
        resumen = obtener_resumen_asistencia(dgmi, fecha)

        self._actualizar_dashboard(
            total_alumnos=len(self.alumnos),
            total_asistencias=resumen["total_asistencias"],
            total_faltas=resumen["total_faltas"],
            materia_nombre=self._get_materia_nombre(materia_id),
        )

        self._mostrar_tabla(dgmi, fecha, asistencias)

    def _get_materia_nombre(self, materia_id: int) -> str:
        for a in self.asignaciones:
            if a["materia_id"] == materia_id:
                return a["materia_nombre"]
        return "---"

    def _mostrar_tabla(self, dgmi: int, fecha: str, asistencias: dict):
        self.body_container.content = self.attendance_table.build()
        self.attendance_table.update_rows(
            self.alumnos, asistencias, dgmi, fecha
        )
        self.page.update()

    def _mostrar_sin_datos(self):
        self.body_container.content = self.mensaje_inicial
        self.dashboard_row.controls.clear()
        self.page.update()

    def _actualizar_dashboard(
        self,
        total_alumnos: int,
        total_asistencias: int,
        total_faltas: int,
        materia_nombre: str,
    ):
        self.dashboard_row.controls = [
            ft.Container(
                content=create_dashboard_card(
                    titulo="Total Alumnos",
                    valor=str(total_alumnos),
                    icono=ft.Icons.PEOPLE_ALT,
                    color_icono="#3B82F6",
                ),
                col={"xs": 6, "sm": 6, "md": 3},
            ),
            ft.Container(
                content=create_dashboard_card(
                    titulo="Asistencias",
                    valor=str(total_asistencias),
                    icono=ft.Icons.CHECK_CIRCLE,
                    color_icono="#10B981",
                ),
                col={"xs": 6, "sm": 6, "md": 3},
            ),
            ft.Container(
                content=create_dashboard_card(
                    titulo="Faltas",
                    valor=str(total_faltas),
                    icono=ft.Icons.CANCEL,
                    color_icono="#EF4444",
                ),
                col={"xs": 6, "sm": 6, "md": 3},
            ),
            ft.Container(
                content=create_dashboard_card(
                    titulo="Materia",
                    valor=materia_nombre,
                    icono=ft.Icons.BOOK,
                    color_icono="#8B5CF6",
                ),
                col={"xs": 6, "sm": 6, "md": 3},
            ),
        ]
        self.page.update()

    def _on_presente(self, alumno: dict):
        self._registrar_y_actualizar(alumno, presente=True)

    def _on_falta(self, alumno: dict):
        self._registrar_y_actualizar(alumno, presente=False)

    def _registrar_y_actualizar(self, alumno: dict, presente: bool):
        filtros = self.filtros_actuales
        grupo_id = filtros.get("grupo_id")
        materia_id = filtros.get("materia_id")
        fecha = filtros.get("fecha")

        dgmi = obtener_docente_grupo_materia_id(
            self.asignaciones, grupo_id, materia_id
        )
        if not dgmi:
            self._mostrar_error("Error al obtener la asignación.")
            return

        exito = registrar_asistencia(
            alumno_id=alumno["id"],
            docente_grupo_materia_id=dgmi,
            fecha=fecha,
            presente=presente,
        )

        if exito:
            tipo = "Asistencia" if presente else "Falta"
            self._mostrar_exito(f"{tipo} registrada correctamente")
            self._refrescar(dgmi, fecha)
        else:
            self._mostrar_error("Ocurrió un error al registrar.")

    def _refrescar(self, dgmi: int, fecha: str):
        asistencias = obtener_asistencia_por_fecha(dgmi, fecha)
        resumen = obtener_resumen_asistencia(dgmi, fecha)

        self._actualizar_dashboard(
            total_alumnos=len(self.alumnos),
            total_asistencias=resumen["total_asistencias"],
            total_faltas=resumen["total_faltas"],
            materia_nombre=self._get_materia_nombre(
                self.filtros_actuales.get("materia_id")
            ),
        )

        self.attendance_table.update_rows(
            self.alumnos, asistencias, dgmi, fecha
        )

    def _mostrar_exito(self, mensaje: str):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(mensaje, color="#FFFFFF"),
            bgcolor="#10B981",
            duration=2500,
        )
        self.page.snack_bar.open = True
        self.page.update()

    def _mostrar_error(self, mensaje: str):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(mensaje, color="#FFFFFF"),
            bgcolor="#EF4444",
            duration=3500,
        )
        self.page.snack_bar.open = True
        self.page.update()

    def build(self) -> ft.Container:
        return self.main_container
