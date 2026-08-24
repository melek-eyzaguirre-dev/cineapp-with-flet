import csv
import os
from datetime import datetime
import flet as ft
from services.pelicula_service import obtener_todos, eliminar
from components.dialogs import mostrar_dialogo_confirmacion

GENEROS_FILTRO = [
    "Todos",
    "Ciencia Ficción",
    "Acción",
    "Drama",
    "Aventura",
    "Suspenso",
    "Comedia",
    "Animación",
    "Terror",
    "Documental",
]

POSTER_PLACEHOLDER = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=500&q=80"


def obtener_etiqueta_ranking(puntuacion: float) -> tuple[str, str]:
    """Retorna la etiqueta descriptiva y el color según la escala 1.0 - 10.0."""
    if puntuacion >= 9.5:
        return "🏆 Obra Maestra", ft.Colors.AMBER_300
    elif puntuacion >= 8.5:
        return "🔵 Muy Buena", ft.Colors.BLUE_300
    elif puntuacion >= 7.0:
        return "🟢 Buena", ft.Colors.GREEN_400
    elif puntuacion >= 5.0:
        return "🟡 Regular", ft.Colors.YELLOW_400
    elif puntuacion >= 3.0:
        return "🟠 Mala", ft.Colors.ORANGE_400
    else:
        return "🔴 Desastrosa", ft.Colors.RED_400


def HomeView(page: ft.Page, on_editar=None) -> ft.Control:
    """Vista principal con KPIs, escala de ranking, alternador de vista y filtros."""

    filtro_genero_actual = ["Todos"]
    texto_busqueda_actual = [""]
    modo_vista_actual = ["grid"]
    todas_las_peliculas = []

    # 1. KPIs
    kpi_total = ft.Text("0", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_400)
    kpi_promedio = ft.Text("0.0", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_300)
    kpi_top = ft.Text("-", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, no_wrap=True, max_lines=1)

    def crear_tarjeta_kpi(titulo: str, control_valor: ft.Control, icono, color_icono):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(icono, color=color_icono, size=32),
                    ft.Column(
                        controls=[
                            ft.Text(titulo, size=11, color=ft.Colors.BLUE_GREY_200, weight=ft.FontWeight.W_500),
                            control_valor,
                        ],
                        spacing=2,
                        tight=True,
                    ),
                ],
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=ft.Colors.BLUE_GREY_800,
            padding=12,
            border_radius=10,
            width=210,
        )

    fila_kpis = ft.Row(
        controls=[
            crear_tarjeta_kpi("TOTAL PELÍCULAS", kpi_total, ft.Icons.LOCAL_MOVIES_ROUNDED, ft.Colors.AMBER_400),
            crear_tarjeta_kpi("PROMEDIO CALIFICACIÓN", kpi_promedio, ft.Icons.STAR_HALF_ROUNDED, ft.Colors.CYAN_300),
            crear_tarjeta_kpi("MEJOR VALORADA", kpi_top, ft.Icons.EMOJI_EVENTS_ROUNDED, ft.Colors.AMBER_300),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        wrap=True,
        spacing=15,
    )

    # 2. Exportación a CSV
    def exportar_csv(e):
        peliculas = obtener_todos()
        if not peliculas:
            snackbar = ft.SnackBar(
                content=ft.Text("No hay películas registradas para exportar", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.AMBER_800,
            )
            page.overlay.append(snackbar)
            snackbar.open = True
            page.update()
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"catalogo_peliculas_{timestamp}.csv"
        ruta_guardado = os.path.abspath(nombre_archivo)

        try:
            with open(ruta_guardado, mode="w", newline="", encoding="utf-8-sig") as f:
                escritor = csv.writer(f, delimiter=";", quoting=csv.QUOTE_MINIMAL)
                escritor.writerow(["ID", "Título", "Director", "Género", "Año", "Duración (min)", "Puntuación", "Escala Ranking", "Crítica/Reseña", "URL Póster"])
                for p in peliculas:
                    score = float(p.get("puntuacion", 0.0))
                    ranking_txt, _ = obtener_etiqueta_ranking(score)
                    escritor.writerow([
                        p.get("id", ""),
                        p.get("titulo", ""),
                        p.get("director", ""),
                        p.get("genero", "General"),
                        p.get("anio_estreno", 2024),
                        p.get("duracion_min", 120),
                        f"{score:.1f}",
                        ranking_txt,
                        p.get("comentario", ""),
                        p.get("poster_url", "")
                    ])

            snackbar = ft.SnackBar(
                content=ft.Text(f"✅ Catálogo exportado ({len(peliculas)} películas): {nombre_archivo}", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.GREEN_700,
            )
        except Exception as err:
            snackbar = ft.SnackBar(
                content=ft.Text(f"❌ Error al exportar: {err}", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_700,
            )

        page.overlay.append(snackbar)
        snackbar.open = True
        page.update()

    # 3. Modal de Crítica y Ficha
    def ver_critica(titulo: str, comentario: str, puntuacion: float):
        ranking_txt, ranking_col = obtener_etiqueta_ranking(puntuacion)
        dialogo_critica = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.RATE_REVIEW, color=ft.Colors.AMBER_400, size=24),
                    ft.Text(f"Crítica: {titulo}", color=ft.Colors.WHITE, size=16),
                ],
                spacing=10,
            ),
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Text(f"Calificación: {puntuacion:.1f}/10 • {ranking_txt}", color=ranking_col, weight=ft.FontWeight.BOLD, size=13),
                        bgcolor=ft.Colors.BLUE_GREY_900,
                        padding=6,
                        border_radius=6,
                    ),
                    ft.Divider(color=ft.Colors.TRANSPARENT, height=6),
                    ft.Text(
                        comentario if comentario else "Esta película aún no tiene una reseña registrada.",
                        color=ft.Colors.BLUE_GREY_100,
                        size=14,
                    ),
                ],
                tight=True,
                spacing=6,
            ),
            bgcolor=ft.Colors.BLUE_GREY_800,
            actions=[
                ft.TextButton(
                    content=ft.Text("Cerrar", color=ft.Colors.AMBER_400),
                    on_click=lambda e: (setattr(dialogo_critica, "open", False), page.update()),
                )
            ],
        )
        page.overlay.append(dialogo_critica)
        dialogo_critica.open = True
        page.update()

    # 4. Tabla y Cuadrícula
    tabla_peliculas = ft.DataTable(
        border_radius=8,
        heading_row_color=ft.Colors.BLUE_GREY_800,
        heading_row_height=46,
        data_row_min_height=48,
        column_spacing=16,
        columns=[
            ft.DataColumn(label=ft.Text("ID", weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_400)),
            ft.DataColumn(label=ft.Text("Título", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)),
            ft.DataColumn(label=ft.Text("Género", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)),
            ft.DataColumn(label=ft.Text("Director", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)),
            ft.DataColumn(label=ft.Text("Año", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE), numeric=True),
            ft.DataColumn(label=ft.Text("Duración", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE), numeric=True),
            ft.DataColumn(label=ft.Text("Puntuación & Escala", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)),
            ft.DataColumn(label=ft.Text("Acciones", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)),
        ],
        rows=[],
    )

    grid_peliculas = ft.GridView(
        expand=True,
        runs_count=5,
        max_extent=240,
        child_aspect_ratio=0.55,
        spacing=18,
        run_spacing=18,
    )

    def confirmar_eliminar(pelicula_id: int, titulo: str):
        if eliminar(pelicula_id):
            snackbar = ft.SnackBar(
                content=ft.Text(f"Película '{titulo}' eliminada correctamente", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.GREEN_700,
            )
            page.overlay.append(snackbar)
            snackbar.open = True
            recargar_todo()
        else:
            snackbar_err = ft.SnackBar(
                content=ft.Text("Error al eliminar el registro", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_700,
            )
            page.overlay.append(snackbar_err)
            snackbar_err.open = True
        page.update()

    def actualizar_kpis(lista):
        total = len(lista)
        kpi_total.value = str(total)

        if total > 0:
            promedio = sum(float(p["puntuacion"]) for p in lista) / total
            ranking_prom, _ = obtener_etiqueta_ranking(promedio)
            kpi_promedio.value = f"{promedio:.1f} ({ranking_prom.split()[0]})"
            mejor = max(lista, key=lambda p: float(p["puntuacion"]))
            kpi_top.value = f"{mejor['titulo']} ({float(mejor['puntuacion']):.1f}★)"
        else:
            kpi_promedio.value = "0.0"
            kpi_top.value = "N/A"

    def crear_card_pelicula(pelicula):
        pid = pelicula["id"]
        ptitulo = pelicula["titulo"]
        pcomentario = pelicula.get("comentario", "")
        pgenero = pelicula.get("genero") or "General"
        panio = pelicula.get("anio_estreno") or 2024
        pduracion = pelicula.get("duracion_min") or 120
        ppuntuacion = float(pelicula["puntuacion"])
        poster_src = pelicula.get("poster_url") if pelicula.get("poster_url") else POSTER_PLACEHOLDER
        ranking_txt, ranking_col = obtener_etiqueta_ranking(ppuntuacion)

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Stack(
                        controls=[
                            ft.Image(
                                src=poster_src,
                                width=240,
                                height=210,
                                fit="cover",  # String directo compatible con Flet
                                border_radius=ft.BorderRadius(top_left=10, top_right=10, bottom_left=0, bottom_right=0),
                                error_content=ft.Container(
                                    content=ft.Icon(ft.Icons.MOVIE, size=50, color=ft.Colors.AMBER_400),
                                    alignment=ft.Alignment(0, 0),
                                    bgcolor=ft.Colors.BLUE_GREY_900,
                                    height=210,
                                ),
                            ),
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.STAR, size=13, color=ft.Colors.AMBER_400),
                                        ft.Text(f"{ppuntuacion:.1f}", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                    ],
                                    spacing=3,
                                    tight=True,
                                ),
                                bgcolor=ft.Colors.with_opacity(0.85, ft.Colors.BLACK),
                                padding=5,
                                border_radius=6,
                                top=8,
                                right=8,
                            ),
                            ft.Container(
                                content=ft.Text(ranking_txt, size=10, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                bgcolor=ft.Colors.with_opacity(0.85, ft.Colors.BLUE_GREY_900),
                                padding=4,
                                border_radius=4,
                                bottom=8,
                                left=8,
                            ),
                        ]
                    ),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(ptitulo, size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, no_wrap=True, max_lines=1),
                                ft.Text(f"{pelicula['director']} • {panio}", size=11, color=ft.Colors.BLUE_GREY_200, no_wrap=True, max_lines=1),
                                ft.Row(
                                    controls=[
                                        ft.Container(
                                            content=ft.Text(pgenero, size=10, color=ft.Colors.CYAN_200),
                                            bgcolor=ft.Colors.BLUE_GREY_900,
                                            padding=3,
                                            border_radius=4,
                                        ),
                                        ft.Text(f"{pduracion} min", size=10, color=ft.Colors.BLUE_GREY_300),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                ft.Divider(color=ft.Colors.BLUE_GREY_700, height=8),
                                ft.Row(
                                    controls=[
                                        ft.IconButton(
                                            icon=ft.Icons.CHAT_BUBBLE_OUTLINE,
                                            icon_color=ft.Colors.AMBER_300,
                                            tooltip="Ver Crítica",
                                            icon_size=16,
                                            on_click=lambda e, t=ptitulo, c=pcomentario, s=ppuntuacion: ver_critica(t, c, s),
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.EDIT,
                                            icon_color=ft.Colors.BLUE_300,
                                            tooltip="Editar",
                                            icon_size=16,
                                            on_click=lambda e, p=pid: on_editar(p) if on_editar else None,
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE,
                                            icon_color=ft.Colors.RED_400,
                                            tooltip="Eliminar",
                                            icon_size=16,
                                            on_click=lambda e, p=pid, t=ptitulo: mostrar_dialogo_confirmacion(
                                                page=page,
                                                titulo="Confirmar Eliminación",
                                                mensaje=f"¿Estás seguro de que deseas eliminar '{t}'?",
                                                on_confirmar=lambda: confirmar_eliminar(p, t),
                                            ),
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.END,
                                    spacing=0,
                                    tight=True,
                                ),
                            ],
                            spacing=4,
                            tight=True,
                        ),
                        padding=10,
                    ),
                ],
                spacing=0,
                tight=True,
            ),
            bgcolor=ft.Colors.BLUE_GREY_800,
            border_radius=10,
        )

    def renderizar_elementos():
        texto = texto_busqueda_actual[0].lower().strip()
        genero_sel = filtro_genero_actual[0]

        peliculas_filtradas = []
        for p in todas_las_peliculas:
            coincide_texto = texto in p["titulo"].lower() or texto in p["director"].lower()
            coincide_genero = genero_sel == "Todos" or p.get("genero", "") == genero_sel

            if coincide_texto and coincide_genero:
                peliculas_filtradas.append(p)

        tabla_peliculas.rows.clear()
        for pelicula in peliculas_filtradas:
            pid = pelicula["id"]
            ptitulo = pelicula["titulo"]
            pcomentario = pelicula.get("comentario", "")
            pgenero = pelicula.get("genero") or "General"
            panio = pelicula.get("anio_estreno") or 2024
            pduracion = pelicula.get("duracion_min") or 120
            ppuntuacion = float(pelicula["puntuacion"])
            ranking_txt, ranking_col = obtener_etiqueta_ranking(ppuntuacion)

            fila = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(pid), color=ft.Colors.AMBER_200)),
                    ft.DataCell(ft.Text(ptitulo, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500)),
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(pgenero, size=11, color=ft.Colors.CYAN_200),
                            bgcolor=ft.Colors.BLUE_GREY_900,
                            padding=4,
                            border_radius=6,
                        )
                    ),
                    ft.DataCell(ft.Text(pelicula["director"], color=ft.Colors.BLUE_GREY_100)),
                    ft.DataCell(ft.Text(str(panio), color=ft.Colors.BLUE_GREY_200)),
                    ft.DataCell(ft.Text(f"{pduracion} min", color=ft.Colors.BLUE_GREY_200)),
                    ft.DataCell(
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.STAR, size=15, color=ft.Colors.AMBER_400),
                                ft.Text(f"{ppuntuacion:.1f}", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                                ft.Text(f"({ranking_txt})", size=11, color=ranking_col),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            tight=True,
                            spacing=4,
                        )
                    ),
                    ft.DataCell(
                        ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.Icons.CHAT_BUBBLE_OUTLINE,
                                    icon_color=ft.Colors.AMBER_300,
                                    tooltip="Ver Crítica",
                                    icon_size=18,
                                    on_click=lambda e, t=ptitulo, c=pcomentario, s=ppuntuacion: ver_critica(t, c, s),
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    icon_color=ft.Colors.BLUE_300,
                                    tooltip="Editar",
                                    icon_size=18,
                                    on_click=lambda e, p=pid: on_editar(p) if on_editar else None,
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_color=ft.Colors.RED_400,
                                    tooltip="Eliminar",
                                    icon_size=18,
                                    on_click=lambda e, p=pid, t=ptitulo: mostrar_dialogo_confirmacion(
                                        page=page,
                                        titulo="Confirmar Eliminación",
                                        mensaje=f"¿Estás seguro de que deseas eliminar '{t}'?",
                                        on_confirmar=lambda: confirmar_eliminar(p, t),
                                    ),
                                ),
                            ],
                            spacing=0,
                            tight=True,
                        )
                    ),
                ]
            )
            tabla_peliculas.rows.append(fila)

        grid_peliculas.controls.clear()
        for pelicula in peliculas_filtradas:
            grid_peliculas.controls.append(crear_card_pelicula(pelicula))

        if modo_vista_actual[0] == "grid":
            contenedor_principal_datos.content = grid_peliculas
        else:
            contenedor_principal_datos.content = ft.Row(
                controls=[tabla_peliculas],
                alignment=ft.MainAxisAlignment.CENTER,
                scroll=ft.ScrollMode.ADAPTIVE,
            )

        page.update()

    def recargar_todo():
        nonlocal todas_las_peliculas
        todas_las_peliculas = obtener_todos()
        actualizar_kpis(todas_las_peliculas)
        renderizar_elementos()

    # 5. Buscador y Filtros
    def on_buscar_change(e):
        texto_busqueda_actual[0] = e.control.value
        renderizar_elementos()

    campo_buscador = ft.TextField(
        hint_text="Buscar por título o director...",
        prefix_icon=ft.Icons.SEARCH,
        focused_border_color=ft.Colors.AMBER_400,
        text_style=ft.TextStyle(color=ft.Colors.WHITE),
        dense=True,
        width=300,
        on_change=on_buscar_change,
    )

    def cambiar_modo_vista(e, modo):
        modo_vista_actual[0] = modo
        btn_vista_grid.style = ft.ButtonStyle(bgcolor=ft.Colors.AMBER_600 if modo == "grid" else ft.Colors.TRANSPARENT)
        btn_vista_tabla.style = ft.ButtonStyle(bgcolor=ft.Colors.AMBER_600 if modo == "tabla" else ft.Colors.TRANSPARENT)
        renderizar_elementos()

    btn_vista_grid = ft.IconButton(
        icon=ft.Icons.GRID_VIEW_ROUNDED,
        icon_color=ft.Colors.WHITE,
        tooltip="Vista Tarjetas (Pósters)",
        style=ft.ButtonStyle(bgcolor=ft.Colors.AMBER_600),
        on_click=lambda e: cambiar_modo_vista(e, "grid"),
    )

    btn_vista_tabla = ft.IconButton(
        icon=ft.Icons.TABLE_ROWS_ROUNDED,
        icon_color=ft.Colors.WHITE,
        tooltip="Vista Tabla",
        style=ft.ButtonStyle(bgcolor=ft.Colors.TRANSPARENT),
        on_click=lambda e: cambiar_modo_vista(e, "tabla"),
    )

    btn_exportar = ft.ElevatedButton(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.DOWNLOAD_ROUNDED, color=ft.Colors.WHITE, size=18),
                ft.Text("Exportar CSV", color=ft.Colors.WHITE, size=13),
            ],
            spacing=6,
            tight=True,
        ),
        bgcolor=ft.Colors.GREEN_800,
        on_click=exportar_csv,
    )

    def seleccionar_genero(e, genero):
        filtro_genero_actual[0] = genero
        for chip in fila_chips.controls:
            chip.selected = (chip.label.value == genero)
        renderizar_elementos()

    chips_controles = []
    for g in GENEROS_FILTRO:
        chip = ft.Chip(
            label=ft.Text(g),
            selected=(g == "Todos"),
            selected_color=ft.Colors.AMBER_600,
            on_select=lambda e, genero=g: seleccionar_genero(e, genero),
        )
        chips_controles.append(chip)

    fila_chips = ft.Row(
        controls=chips_controles,
        alignment=ft.MainAxisAlignment.CENTER,
        scroll=ft.ScrollMode.ADAPTIVE,
        spacing=8,
    )

    contenedor_principal_datos = ft.Container(
        expand=True,
        padding=10,
    )

    recargar_todo()

    vista = ft.Column(
        controls=[
            ft.Divider(color=ft.Colors.TRANSPARENT, height=5),
            fila_kpis,
            ft.Divider(color=ft.Colors.TRANSPARENT, height=10),
            ft.Row(
                controls=[
                    campo_buscador,
                    ft.Row(controls=[btn_vista_grid, btn_vista_tabla], spacing=4),
                    btn_exportar,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=12,
                wrap=True,
            ),
            fila_chips,
            ft.Divider(color=ft.Colors.TRANSPARENT, height=5),
            contenedor_principal_datos,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.START,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    return vista