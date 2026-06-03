import flet as ft
from services.docente_service import (
    obtener_grados_disponibles,
    obtener_grupos_por_grado,
    obtener_materias_por_grupo,
)


class FiltersSection:
    def __init__(self, page: ft.Page, on_consultar):
        self.page = page
        self.on_consultar = on_consultar
        self.asignaciones = []
        self.grados_disponibles = []

        self.grado_dropdown = ft.Dropdown(
            label="Grado",
            hint_text="Selecciona un grado",
            options=[],
            width=None,
            expand=True,
            on_select=self._on_grado_change,
            color="#1F2937",
            bgcolor="#FFFFFF",
            border_color="#D1D5DB",
            border_radius=8,
        )

        self.grupo_dropdown = ft.Dropdown(
            label="Grupo",
            hint_text="Selecciona un grupo",
            options=[],
            width=None,
            expand=True,
            on_select=self._on_grupo_change,
            color="#1F2937",
            bgcolor="#FFFFFF",
            border_color="#D1D5DB",
            border_radius=8,
        )

        self.materia_dropdown = ft.Dropdown(
            label="Materia",
            hint_text="Selecciona una materia",
            options=[],
            width=None,
            expand=True,
            color="#1F2937",
            bgcolor="#FFFFFF",
            border_color="#D1D5DB",
            border_radius=8,
        )

        self.fecha_picker = ft.DatePicker(
            on_change=self._on_fecha_change,
        )

        self.fecha_text = ft.Text(
            value="Selecciona una fecha",
            color="#6B7280",
            size=14,
        )

        self.fecha_button = ft.Button(
            "Seleccionar fecha",
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=self._abrir_fecha_picker,
            style=ft.ButtonStyle(
                color="#1F2937",
                bgcolor="#FFFFFF",
                side=ft.BorderSide(1, "#D1D5DB"),
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
        )

        self.consultar_button = ft.Button(
            "Consultar",
            icon=ft.Icons.SEARCH,
            on_click=self._on_consultar,
            style=ft.ButtonStyle(
                color="#FFFFFF",
                bgcolor="#3B82F6",
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
        )

        self.selected_fecha = None

    def _abrir_fecha_picker(self, e):
        if self.fecha_picker not in self.page.overlay:
            self.page.overlay.append(self.fecha_picker)
        self.fecha_picker.open = True
        self.page.update()

    def _on_fecha_change(self, e):
        fecha = e.control.value
        self.selected_fecha = fecha.strftime("%Y-%m-%d")
        self.fecha_text.value = fecha.strftime("%d/%m/%Y")
        self.fecha_text.color = "#1F2937"
        self.page.update()

    def set_asignaciones(self, asignaciones: list):
        self.asignaciones = asignaciones
        self.grados_disponibles = obtener_grados_disponibles(asignaciones)

        self.grado_dropdown.options = [
            ft.DropdownOption(key=str(g), text=f"{g}°")
            for g in self.grados_disponibles
        ]
        self.grado_dropdown.value = None
        self.grupo_dropdown.options = []
        self.grupo_dropdown.value = None
        self.materia_dropdown.options = []
        self.materia_dropdown.value = None
        self.selected_fecha = None
        self.fecha_text.value = "Selecciona una fecha"
        self.fecha_text.color = "#6B7280"

    def _on_grado_change(self, e):
        grado = int(e.control.value)
        grupos = obtener_grupos_por_grado(self.asignaciones, grado)
        self.grupo_dropdown.options = [
            ft.DropdownOption(key=str(g["grupo_id"]), text=g["grupo_nombre"])
            for g in grupos
        ]
        self.grupo_dropdown.value = None
        self.materia_dropdown.options = []
        self.materia_dropdown.value = None

    def _on_grupo_change(self, e):
        grupo_id = int(e.control.value)
        materias = obtener_materias_por_grupo(self.asignaciones, grupo_id)
        self.materia_dropdown.options = [
            ft.DropdownOption(key=str(m["materia_id"]), text=m["materia_nombre"])
            for m in materias
        ]
        self.materia_dropdown.value = None

    def _on_consultar(self, e):
        if self.on_consultar:
            self.on_consultar(self.get_filtros())

    def get_filtros(self) -> dict:
        return {
            "grado": int(self.grado_dropdown.value) if self.grado_dropdown.value else None,
            "grupo_id": int(self.grupo_dropdown.value) if self.grupo_dropdown.value else None,
            "materia_id": int(self.materia_dropdown.value) if self.materia_dropdown.value else None,
            "fecha": self.selected_fecha,
        }

    def build(self) -> ft.Container:
        side = ft.BorderSide(1, "#E5E7EB")
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.ResponsiveRow(
                        controls=[
                            ft.Container(
                                content=self.grado_dropdown,
                                col={"xs": 12, "sm": 6, "md": 3},
                            ),
                            ft.Container(
                                content=self.grupo_dropdown,
                                col={"xs": 12, "sm": 6, "md": 3},
                            ),
                            ft.Container(
                                content=self.materia_dropdown,
                                col={"xs": 12, "sm": 6, "md": 3},
                            ),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        self.fecha_button,
                                        self.fecha_text,
                                    ],
                                    spacing=4,
                                ),
                                col={"xs": 12, "sm": 6, "md": 3},
                            ),
                        ],
                        spacing=12,
                    ),
                    ft.Container(height=8),
                    ft.Row(
                        controls=[
                            self.consultar_button,
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ],
                spacing=8,
            ),
            padding=20,
            border_radius=12,
            bgcolor="#FFFFFF",
            border=ft.Border(left=side, top=side, right=side, bottom=side),
        )
