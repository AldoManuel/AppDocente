import flet as ft
from views.login_view import LoginView
from views.docente_view import DocenteView


def main(page: ft.Page):
    page.title = "Panel Docente"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#F5F7FA"
    page.padding = 0
    page.scroll = ft.ScrollMode.AUTO

    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="#3B82F6",
            on_primary="#FFFFFF",
            secondary="#10B981",
            surface="#FFFFFF",
            on_surface="#1F2937",
        ),
        use_material3=True,
    )

    current_view = None

    def mostrar_docente_panel(docente_id: int, docente_nombre: str):
        nonlocal current_view

        page.appbar = construir_appbar(docente_nombre)
        page.controls.clear()

        docente_view = DocenteView(page, docente_id, docente_nombre)
        docente_view.load_asignaciones()

        page.add(docente_view.build())
        current_view = docente_view
        page.update()

    def mostrar_login():
        nonlocal current_view

        page.appbar = None
        page.controls.clear()

        login_view = LoginView(page, mostrar_docente_panel)
        page.add(login_view.build())
        current_view = login_view
        page.update()

    def cerrar_sesion(e):
        mostrar_login()

    def construir_appbar(docente_nombre: str) -> ft.AppBar:
        return ft.AppBar(
            title=ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.SCHOOL,
                        color="#3B82F6",
                        size=28,
                    ),
                    ft.Container(width=8),
                    ft.Column(
                        controls=[
                            ft.Text(
                                docente_nombre,
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color="#1F2937",
                            ),
                            ft.Text(
                                "Rol: Docente",
                                size=13,
                                color="#6B7280",
                            ),
                        ],
                        spacing=0,
                    ),
                ],
                spacing=0,
            ),
            actions=[
                ft.IconButton(
                    icon=ft.Icons.LOGOUT,
                    icon_color="#EF4444",
                    tooltip="Cerrar sesión",
                    on_click=cerrar_sesion,
                ),
            ],
            bgcolor="#FFFFFF",
            elevation=1,
            center_title=False,
        )

    mostrar_login()


if __name__ == "__main__":
    ft.run(main)
