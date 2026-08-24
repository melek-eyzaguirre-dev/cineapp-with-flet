import flet as ft
from services.pelicula_service import crear, obtener_por_id, actualizar

GENEROS_DISPONIBLES = [
    "Acción", "Aventura", "Ciencia Ficción", "Comedia",
    "Drama", "Fantasía", "Terror", "Suspenso", "Animación", "Documental"
]

POSTER_PLACEHOLDER = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=500&q=80"


def FormView(page: ft.Page, pelicula_id: int = None, on_cancelar=None, on_guardado_exitoso=None) -> ft.Control:
    """Formulario reactivo sin colisiones en overlay."""

    es_edicion = pelicula_id is not None
    pelicula_actual = None

    if es_edicion:
        pelicula_actual = obtener_por_id(pelicula_id)

    icono_formulario = ft.Icon(
        ft.Icons.EDIT_DOCUMENT if es_edicion else ft.Icons.ADD_TO_QUEUE,
        size=44,
        color=ft.Colors.AMBER_400
    )

    titulo_formulario = ft.Text(
        value="Editar Película" if es_edicion else "Agregar Nueva Película",
        size=22,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE,
        text_align=ft.TextAlign.CENTER
    )

    subtitulo = ft.Text(
        value=f"Modificando registro ID #{pelicula_id}" if es_edicion else "Completa los campos para registrar la película",
        size=13,
        color=ft.Colors.BLUE_GREY_200,
        text_align=ft.TextAlign.CENTER
    )

    indicador_escala = ft.Text(
        value="Escala: Ingrese valor (1.0 - 10.0)",
        size=12,
        color=ft.Colors.BLUE_GREY_300,
        weight=ft.FontWeight.W_500,
    )

    poster_inicial = pelicula_actual["poster_url"] if (
                pelicula_actual and pelicula_actual.get("poster_url")) else POSTER_PLACEHOLDER

    img_preview = ft.Image(
        src=poster_inicial,
        width=120,
        height=150,
        fit="cover",
        border_radius=8,
        error_content=ft.Container(
            content=ft.Icon(ft.Icons.BROKEN_IMAGE, size=35, color=ft.Colors.RED_400),
            alignment=ft.Alignment(0, 0),
            bgcolor=ft.Colors.BLUE_GREY_900,
            width=120,
            height=150,
            border_radius=8,
        )
    )

    def actualizar_texto_escala(valor: float):
        if valor >= 9.5:
            indicador_escala.value = "Escala: 🏆 Obra Maestra (9.5 - 10.0)"
            indicador_escala.color = ft.Colors.AMBER_300
        elif valor >= 8.5:
            indicador_escala.value = "Escala: 🔵 Muy Buena (8.5 - 9.4)"
            indicador_escala.color = ft.Colors.BLUE_300
        elif valor >= 7.0:
            indicador_escala.value = "Escala: 🟢 Buena (7.0 - 8.4)"
            indicador_escala.color = ft.Colors.GREEN_400
        elif valor >= 5.0:
            indicador_escala.value = "Escala: 🟡 Regular / Pasable (5.0 - 6.9)"
            indicador_escala.color = ft.Colors.YELLOW_400
        elif valor >= 3.0:
            indicador_escala.value = "Escala: 🟠 Mala (3.0 - 4.9)"
            indicador_escala.color = ft.Colors.ORANGE_400
        else:
            indicador_escala.value = "Escala: 🔴 Desastrosa (1.0 - 2.9)"
            indicador_escala.color = ft.Colors.RED_400

    def on_poster_url_change(e):
        url = campo_poster.value.strip()
        img_preview.src = url if url else POSTER_PLACEHOLDER
        page.update()

    def on_puntuacion_change(e):
        puntuacion_str = campo_puntuacion.value.strip() if campo_puntuacion.value else ""
        if puntuacion_str:
            try:
                p_val = float(puntuacion_str.replace(",", "."))
                if 1.0 <= p_val <= 10.0:
                    campo_puntuacion.error_text = None
                    actualizar_texto_escala(p_val)
                else:
                    campo_puntuacion.error_text = "Entre 1.0 y 10.0"
            except ValueError:
                campo_puntuacion.error_text = "Número decimal inválido"
        page.update()

    campo_titulo = ft.TextField(
        label="Título de la Película",
        value=pelicula_actual["titulo"] if pelicula_actual else "",
        prefix_icon=ft.Icons.MOVIE_CREATION,
        focused_border_color=ft.Colors.AMBER_400,
        text_style=ft.TextStyle(color=ft.Colors.WHITE),
        expand=True,
    )

    campo_director = ft.TextField(
        label="Director",
        value=pelicula_actual["director"] if pelicula_actual else "",
        prefix_icon=ft.Icons.PERSON,
        focused_border_color=ft.Colors.AMBER_400,
        text_style=ft.TextStyle(color=ft.Colors.WHITE),
        expand=True,
    )

    genero_actual = pelicula_actual["genero"] if (
                pelicula_actual and pelicula_actual.get("genero")) else "Ciencia Ficción"
    campo_genero = ft.Dropdown(
        label="Género",
        value=genero_actual,
        options=[ft.dropdown.Option(g) for g in GENEROS_DISPONIBLES],
        focused_border_color=ft.Colors.AMBER_400,
        text_style=ft.TextStyle(color=ft.Colors.WHITE),
        expand=True,
    )

    puntuacion_inicial = f"{float(pelicula_actual['puntuacion']):.1f}" if pelicula_actual else "8.0"
    if pelicula_actual:
        actualizar_texto_escala(float(pelicula_actual["puntuacion"]))
    else:
        actualizar_texto_escala(8.0)

    campo_puntuacion = ft.TextField(
        label="Puntuación (1.0 - 10.0)",
        value=puntuacion_inicial,
        prefix_icon=ft.Icons.STAR,
        focused_border_color=ft.Colors.AMBER_400,
        text_style=ft.TextStyle(color=ft.Colors.WHITE),
        keyboard_type=ft.KeyboardType.NUMBER,
        on_change=on_puntuacion_change,
        expand=True,
    )

    campo_anio = ft.TextField(
        label="Año de Estreno",
        value=str(pelicula_actual["anio_estreno"]) if (
                    pelicula_actual and pelicula_actual.get("anio_estreno")) else "2024",
        prefix_icon=ft.Icons.CALENDAR_MONTH,
        focused_border_color=ft.Colors.AMBER_400,
        text_style=ft.TextStyle(color=ft.Colors.WHITE),
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True,
    )

    campo_duracion = ft.TextField(
        label="Duración (minutos)",
        value=str(pelicula_actual["duracion_min"]) if (
                    pelicula_actual and pelicula_actual.get("duracion_min")) else "120",
        prefix_icon=ft.Icons.TIMER_OUTLINED,
        focused_border_color=ft.Colors.AMBER_400,
        text_style=ft.TextStyle(color=ft.Colors.WHITE),
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True,
    )

    campo_poster = ft.TextField(
        label="Ruta o URL del Póster",
        value=pelicula_actual["poster_url"] if (pelicula_actual and pelicula_actual.get("poster_url")) else "",
        prefix_icon=ft.Icons.IMAGE_OUTLINED,
        focused_border_color=ft.Colors.AMBER_400,
        cursor_color=ft.Colors.AMBER_400,
        text_style=ft.TextStyle(color=ft.Colors.WHITE),
        hint_text="https://ejemplo.com/poster.jpg o /posters/foto.jpg",
        on_change=on_poster_url_change,
        expand=True,
    )

    campo_comentario = ft.TextField(
        label="Crítica / Reseña personal (Opcional)",
        value=pelicula_actual["comentario"] if (pelicula_actual and pelicula_actual.get("comentario")) else "",
        prefix_icon=ft.Icons.RATE_REVIEW_OUTLINED,
        focused_border_color=ft.Colors.AMBER_400,
        text_style=ft.TextStyle(color=ft.Colors.WHITE),
        multiline=True,
        min_lines=3,
        max_lines=4,
        hint_text="Escribe aquí tu opinión...",
        expand=True,
    )

    def ejecutar_guardado(e):
        titulo = campo_titulo.value.strip() if campo_titulo.value else ""
        director = campo_director.value.strip() if campo_director.value else ""
        genero = campo_genero.value if campo_genero.value else "General"
        puntuacion_str = campo_puntuacion.value.strip() if campo_puntuacion.value else ""
        anio_str = campo_anio.value.strip() if campo_anio.value else "2024"
        duracion_str = campo_duracion.value.strip() if campo_duracion.value else "120"

        if not titulo:
            campo_titulo.error_text = "El título es obligatorio"
            page.update()
            return

        if not director:
            campo_director.error_text = "El director es obligatorio"
            page.update()
            return

        try:
            p_val = float(puntuacion_str.replace(",", "."))
            if not (1.0 <= p_val <= 10.0):
                campo_puntuacion.error_text = "Debe estar entre 1.0 y 10.0"
                page.update()
                return
        except ValueError:
            campo_puntuacion.error_text = "Puntuación no válida"
            page.update()
            return

        try:
            a_val = int(anio_str)
        except ValueError:
            campo_anio.error_text = "Año no válido"
            page.update()
            return

        try:
            d_val = int(duracion_str)
        except ValueError:
            campo_duracion.error_text = "Duración no válida"
            page.update()
            return

        datos_pelicula = {
            "titulo": titulo,
            "director": director,
            "genero": genero,
            "anio_estreno": a_val,
            "duracion_min": d_val,
            "poster_url": campo_poster.value.strip() if campo_poster.value else "",
            "comentario": campo_comentario.value.strip() if campo_comentario.value else "",
            "puntuacion": p_val,
        }

        if es_edicion:
            exito, mensaje = actualizar(pelicula_id, datos_pelicula)
        else:
            exito, mensaje = crear(datos_pelicula)

        if exito:
            snackbar = ft.SnackBar(
                content=ft.Text(f"¡Éxito! {mensaje}", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.GREEN_800
            )
            page.overlay.append(snackbar)
            snackbar.open = True
            page.update()

            if on_guardado_exitoso:
                on_guardado_exitoso()
        else:
            snackbar_err = ft.SnackBar(
                content=ft.Text(f"Error: {mensaje}", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_800
            )
            page.overlay.append(snackbar_err)
            snackbar_err.open = True
            page.update()

    btn_guardar = ft.ElevatedButton(
        content=ft.Text("Guardar cambios" if es_edicion else "Guardar", color=ft.Colors.BLACK87,
                        weight=ft.FontWeight.BOLD),
        icon=ft.Icons.SAVE,
        bgcolor=ft.Colors.AMBER_500,
        on_click=ejecutar_guardado,
        expand=True,
    )

    btn_cancelar = ft.OutlinedButton(
        content=ft.Text("Cancelar", color=ft.Colors.BLUE_GREY_200),
        icon=ft.Icons.CANCEL_OUTLINED,
        on_click=lambda e: on_cancelar() if on_cancelar else None,
        expand=True,
    )

    formulario_card = ft.Container(
        content=ft.Column(
            controls=[
                icono_formulario,
                titulo_formulario,
                subtitulo,
                ft.Divider(color=ft.Colors.TRANSPARENT, height=8),
                ft.Row(controls=[campo_titulo, campo_director], spacing=15),
                ft.Row(controls=[campo_genero, campo_puntuacion], spacing=15),
                indicador_escala,
                ft.Row(controls=[campo_anio, campo_duracion], spacing=15),
                ft.Row(controls=[campo_poster, img_preview], spacing=15,
                       vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Row(controls=[campo_comentario]),
                ft.Divider(color=ft.Colors.TRANSPARENT, height=8),
                ft.Row(controls=[btn_cancelar, btn_guardar], spacing=15),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            tight=True
        ),
        bgcolor=ft.Colors.BLUE_GREY_800,
        padding=25,
        border_radius=12,
        width=680,
    )

    return ft.Column(
        controls=[formulario_card],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
        scroll=ft.ScrollMode.AUTO
    )