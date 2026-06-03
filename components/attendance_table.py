import flet as ft


class AttendanceTable:
    def __init__(
        self,
        page: ft.Page,
        on_presente,
        on_falta,
        docente_grupo_materia_id: int = None,
        fecha: str = None,
    ):
        self.page = page
        self.on_presente = on_presente
        self.on_falta = on_falta
        self.docente_grupo_materia_id = docente_grupo_materia_id
        self.fecha = fecha
        self.data_table = self._build_table()
        self.container = self._build_container()

    def _build_table(self) -> ft.DataTable:
        side = ft.BorderSide(1, "#E5E7EB")
        return ft.DataTable(
            columns=[
                ft.DataColumn(
                    ft.Text(
                        "Alumno",
                        weight=ft.FontWeight.BOLD,
                        color="#1F2937",
                        size=14,
                    ),
                ),
                ft.DataColumn(
                    ft.Text(
                        "Asistencia",
                        weight=ft.FontWeight.BOLD,
                        color="#1F2937",
                        size=14,
                    ),
                    numeric=False,
                ),
                ft.DataColumn(
                    ft.Text(
                        "Falta",
                        weight=ft.FontWeight.BOLD,
                        color="#1F2937",
                        size=14,
                    ),
                    numeric=False,
                ),
            ],
            rows=[],
            border_radius=8,
            border=ft.Border(left=side, top=side, right=side, bottom=side),
            heading_row_color="#F9FAFB",
            heading_row_height=48,
            data_row_min_height=56,
            data_row_max_height=64,
            column_spacing=24,
            horizontal_margin=16,
        )

    def _build_container(self) -> ft.Container:
        side = ft.BorderSide(1, "#E5E7EB")
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Registro de Asistencia",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color="#1F2937",
                    ),
                    ft.Container(height=8),
                    ft.Column(
                        controls=[self.data_table],
                        scroll=ft.ScrollMode.AUTO,
                        height=400,
                    ),
                ],
                spacing=0,
            ),
            padding=20,
            border_radius=12,
            bgcolor="#FFFFFF",
            border=ft.Border(left=side, top=side, right=side, bottom=side),
        )

    def _build_alumno_cell(self, alumno: dict) -> ft.Column:
        nombre = f"{alumno.get('nombre', '')} {alumno.get('apellido', '')}"
        lista = alumno.get("numero_lista")
        controls = [
            ft.Text(
                nombre.strip(),
                size=14,
                weight=ft.FontWeight.MEDIUM,
                color="#1F2937",
            ),
        ]
        if lista:
            controls.append(
                ft.Text(
                    f"# Lista: {lista}",
                    size=12,
                    color="#6B7280",
                ),
            )
        return ft.Column(controls=controls, spacing=2)

    def update_rows(
        self,
        alumnos: list,
        asistencias: dict,
        docente_grupo_materia_id: int,
        fecha: str,
    ):
        self.docente_grupo_materia_id = docente_grupo_materia_id
        self.fecha = fecha

        rows = []
        for alumno in alumnos:
            alumno_id = alumno["id"]
            registro = asistencias.get(alumno_id)
            presente = registro["presente"] if registro else None

            presente_btn = ft.Button(
                "Presente",
                icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
                on_click=lambda e, a=alumno: self.on_presente(a),
                style=ft.ButtonStyle(
                    color="#FFFFFF",
                    bgcolor="#10B981",
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
                disabled=presente is True,
            )

            falta_btn = ft.Button(
                "Falta",
                icon=ft.Icons.CANCEL_OUTLINED,
                on_click=lambda e, a=alumno: self.on_falta(a),
                style=ft.ButtonStyle(
                    color="#FFFFFF",
                    bgcolor="#EF4444",
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
                disabled=presente is False,
            )

            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(self._build_alumno_cell(alumno)),
                        ft.DataCell(presente_btn),
                        ft.DataCell(falta_btn),
                    ],
                )
            )

        self.data_table.rows = rows
        self.page.update()

    def build(self) -> ft.Container:
        return self.container
