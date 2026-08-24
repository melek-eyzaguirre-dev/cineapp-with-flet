import flet as ft


def Navbar(on_nav_change) -> ft.Control:
    """Barra superior interactiva."""
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
                        ft.ElevatedButton(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.HOME, size=18, color=ft.Colors.WHITE),
                                    ft.Text("Inicio", color=ft.Colors.WHITE),
                                ],
                                spacing=6,
                                tight=True,
                            ),
                            bgcolor=ft.Colors.BLUE_GREY_700,
                            on_click=lambda e: on_nav_change("inicio") if on_nav_change else None,
                        ),
                        ft.ElevatedButton(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.ADD_CIRCLE, size=18, color=ft.Colors.BLACK87),
                                    ft.Text("Agregar Película", color=ft.Colors.BLACK87, weight=ft.FontWeight.BOLD),
                                ],
                                spacing=6,
                                tight=True,
                            ),
                            bgcolor=ft.Colors.AMBER_500,
                            on_click=lambda e: on_nav_change("agregar") if on_nav_change else None,
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