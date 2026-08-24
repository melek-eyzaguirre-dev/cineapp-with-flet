import flet as ft
from services.pelicula_service import obtener_todos, eliminar  # <-- Quita 'peliculas_flet.'
from components.dialogs import mostrar_dialogo_confirmacion


def HomeView(page: ft.Page, on_editar=None) -> ft.Control:
    """Componente vista principal con catálogo y tabla centrada."""

    icono_principal = ft.Icon(
        ft.Icons.MOVIE,
        size=60,
        color=ft.Colors.AMBER_400
    )

    titulo_principal = ft.Text(
        value="Catálogo de Películas",
        size=26,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE,
        text_align=ft.TextAlign.CENTER
    )

    subtitulo = ft.Text(
        value="Lectura en tiempo real desde MySQL",
        size=14,
        color=ft.Colors.BLUE_GREY_200,
        text_align=ft.TextAlign.CENTER
    )

    # DataTable sin border.all ni border_radius.all problemáticos
    tabla_peliculas = ft.DataTable(
        border_radius=8,
        heading_row_color=ft.Colors.BLUE_GREY_800,
        heading_row_height=48,
        data_row_min_height=45,
        column_spacing=24,
        columns=[
            ft.DataColumn(label=ft.Text("ID", weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_400)),
            ft.DataColumn(label=ft.Text("Título", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)),
            ft.DataColumn(label=ft.Text("Director", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)),
            ft.DataColumn(label=ft.Text("Puntuación", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE), numeric=True),
            ft.DataColumn(label=ft.Text("Acciones", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)),
        ],
        rows=[]
    )

    def confirmar_eliminar(pelicula_id: int, titulo: str):
        if eliminar(pelicula_id):
            snackbar = ft.SnackBar(
                content=ft.Text(f"Película '{titulo}' eliminada correctamente", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.GREEN_700
            )
            if hasattr(page, "open"):
                page.open(snackbar)
            else:
                page.snack_bar = snackbar
                page.snack_bar.open = True
            cargar_datos()
        else:
            snackbar_err = ft.SnackBar(
                content=ft.Text("Error al eliminar el registro", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_700
            )
            if hasattr(page, "open"):
                page.open(snackbar_err)
            else:
                page.snack_bar = snackbar_err
                page.snack_bar.open = True
        page.update()

    def cargar_datos():
        tabla_peliculas.rows.clear()
        lista_peliculas = obtener_todos()

        for pelicula in lista_peliculas:
            pelicula_id = pelicula["id"]
            pelicula_titulo = pelicula["titulo"]

            fila = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(pelicula_id), color=ft.Colors.AMBER_200)),
                    ft.DataCell(ft.Text(pelicula_titulo, color=ft.Colors.WHITE)),
                    ft.DataCell(ft.Text(pelicula["director"], color=ft.Colors.BLUE_GREY_100)),
                    ft.DataCell(
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.STAR, size=16, color=ft.Colors.AMBER_400),
                                ft.Text(f"{pelicula['puntuacion']:.1f}", color=ft.Colors.WHITE)
                            ],
                            alignment=ft.MainAxisAlignment.END,
                            tight=True
                        )
                    ),
                    ft.DataCell(
                        ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    icon_color=ft.Colors.BLUE_300,
                                    tooltip="Editar",
                                    icon_size=18,
                                    on_click=lambda e, pid=pelicula_id: on_editar(pid) if on_editar else None
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_color=ft.Colors.RED_400,
                                    tooltip="Eliminar",
                                    icon_size=18,
                                    on_click=lambda e, pid=pelicula_id, tit=pelicula_titulo: mostrar_dialogo_confirmacion(
                                        page=page,
                                        titulo="Confirmar Eliminación",
                                        mensaje=f"¿Estás seguro de que deseas eliminar '{tit}'?",
                                        on_confirmar=lambda: confirmar_eliminar(pid, tit)
                                    )
                                ),
                            ],
                            spacing=0,
                            tight=True
                        )
                    ),
                ]
            )
            tabla_peliculas.rows.append(fila)
        page.update()

    cargar_datos()

    contenedor_tabla = ft.Row(
        controls=[tabla_peliculas],
        alignment=ft.MainAxisAlignment.CENTER,
        scroll=ft.ScrollMode.ADAPTIVE
    )

    vista = ft.Column(
        controls=[
            icono_principal,
            titulo_principal,
            subtitulo,
            ft.Divider(color=ft.Colors.TRANSPARENT, height=10),
            contenedor_tabla
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
        scroll=ft.ScrollMode.AUTO
    )

    return vista