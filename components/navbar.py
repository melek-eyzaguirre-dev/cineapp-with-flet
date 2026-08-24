import flet as ft


def Navbar(on_nav_change) -> ft.Control:
    """Barra de navegación adaptable para cambiar entre vistas."""
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.LOCAL_MOVIES, color=ft.Colors.AMBER_400, size=28),
                        ft.Text(
                            "CineApp",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE
                        ),
                    ],
                    spacing=10,
                ),
                ft.Row(
                    controls=[
                        ft.TextButton(
                            content=ft.Text("Inicio"),
                            icon=ft.Icons.HOME,
                            on_click=lambda e: on_nav_change("inicio"),
                        ),
                        ft.TextButton(
                            content=ft.Text("Agregar Película"),
                            icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                            on_click=lambda e: on_nav_change("agregar"),
                        ),
                    ],
                    spacing=10,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=15,
        bgcolor=ft.Colors.BLUE_GREY_800,
        border_radius=10,
    )