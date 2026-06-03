import flet as ft
from services.auth_service import login
from services.docente_service import obtener_docente_por_usuario


class LoginView:
    def __init__(self, page: ft.Page, on_login_exitoso):
        self.page = page
        self.on_login_exitoso = on_login_exitoso

        self.correo_field = ft.TextField(
            label="Correo electrónico",
            hint_text="tu@correo.com",
            prefix_icon=ft.Icons.EMAIL_OUTLINED,
            border_radius=8,
            border_color="#D1D5DB",
            focused_border_color="#3B82F6",
            color="#1F2937",
            bgcolor="#FFFFFF",
            filled=True,
            fill_color="#F9FAFB",
            width=360,
            on_submit=self._iniciar_sesion,
        )

        self.contrasena_field = ft.TextField(
            label="Contraseña",
            hint_text="••••••••",
            prefix_icon=ft.Icons.LOCK_OUTLINED,
            password=True,
            can_reveal_password=True,
            border_radius=8,
            border_color="#D1D5DB",
            focused_border_color="#3B82F6",
            color="#1F2937",
            bgcolor="#FFFFFF",
            filled=True,
            fill_color="#F9FAFB",
            width=360,
            on_submit=self._iniciar_sesion,
        )

        self.login_button = ft.Button(
            "Iniciar sesión",
            icon=ft.Icons.LOGIN,
            on_click=self._iniciar_sesion,
            style=ft.ButtonStyle(
                color="#FFFFFF",
                bgcolor="#3B82F6",
                shape=ft.RoundedRectangleBorder(radius=8),
                elevation=2,
            ),
            width=360,
            height=44,
        )

        self.error_text = ft.Text(
            value="",
            color="#EF4444",
            size=13,
            text_align=ft.TextAlign.CENTER,
            visible=False,
        )

        self.cargando = ft.ProgressBar(
            width=360,
            color="#3B82F6",
            bgcolor="#E5E7EB",
            visible=False,
        )

        self.container = self._build()

    def _build(self):
        side = ft.BorderSide(1, "#E5E7EB")

        login_card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(
                        ft.Icons.SCHOOL,
                        color="#3B82F6",
                        size=56,
                    ),
                    ft.Container(height=8),
                    ft.Text(
                        "Panel Docente",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color="#1F2937",
                    ),
                    ft.Text(
                        "Inicia sesión para continuar",
                        size=14,
                        color="#6B7280",
                    ),
                    ft.Container(height=16),
                    self.correo_field,
                    ft.Container(height=8),
                    self.contrasena_field,
                    ft.Container(height=4),
                    self.error_text,
                    ft.Container(height=4),
                    self.cargando,
                    ft.Container(height=8),
                    self.login_button,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            padding=32,
            border_radius=16,
            bgcolor="#FFFFFF",
            border=ft.Border(left=side, top=side, right=side, bottom=side),
            shadow=ft.BoxShadow(
                blur_radius=20,
                color="rgba(0,0,0,0.05)",
            ),
        )

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=login_card,
                        alignment=ft.Alignment(0, 0),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=24,
            expand=True,
        )

    def _iniciar_sesion(self, e=None):
        correo = self.correo_field.value.strip()
        contrasena = self.contrasena_field.value.strip()

        if not correo or not contrasena:
            self._mostrar_error("Todos los campos son obligatorios.")
            return

        self._mostrar_cargando(True)
        self._limpiar_error()

        usuario = login(correo, contrasena)

        self._mostrar_cargando(False)

        if not usuario:
            self._mostrar_error(
                "Credenciales incorrectas o no tienes permisos de docente."
            )
            self.contrasena_field.value = ""
            self.page.update()
            return

        docente = obtener_docente_por_usuario(usuario["id"])
        if not docente:
            self._mostrar_error(
                "No se encontró un docente asociado a esta cuenta."
            )
            self.contrasena_field.value = ""
            self.page.update()
            return

        self.on_login_exitoso(
            docente_id=docente["id"],
            docente_nombre=(
                f"{docente.get('nombre', '')} {docente.get('apellido', '')}".strip()
            ),
        )

    def _mostrar_error(self, mensaje: str):
        self.error_text.value = mensaje
        self.error_text.visible = True
        self.page.update()

    def _limpiar_error(self):
        self.error_text.value = ""
        self.error_text.visible = False

    def _mostrar_cargando(self, activo: bool):
        self.cargando.visible = activo
        self.login_button.disabled = activo
        self.correo_field.disabled = activo
        self.contrasena_field.disabled = activo
        self.page.update()

    def build(self) -> ft.Container:
        return self.container
