import flet as ft


def create_dashboard_card(
    titulo: str,
    valor: str,
    icono: ft.IconData,
    color_icono: str = "#3B82F6",
) -> ft.Container:
    side = ft.BorderSide(1, "#E5E7EB")
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(
                            icono,
                            color=color_icono,
                            size=28,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Container(height=8),
                ft.Text(
                    value=valor,
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color="#1F2937",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    value=titulo,
                    size=13,
                    color="#6B7280",
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        ),
        padding=16,
        border_radius=12,
        bgcolor="#FFFFFF",
        border=ft.Border(left=side, top=side, right=side, bottom=side),
        expand=True,
        animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
        ink=True,
    )
