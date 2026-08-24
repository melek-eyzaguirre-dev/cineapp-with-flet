import flet as ft
from services.pelicula_service import crear, obtener_por_id, actualizar


def FormView(page: ft.Page, pelicula_id: int = None, on_cancelar=None, on_guardado_exitoso=None) -> ft.Control:
    """Componente vista de formulario reactivo con validación visual en tiempo real."""

    es_edicion = pelicula_id is not None
    pelicula_actual = None

    if es_edicion:
        pelicula_actual = obtener_por_id(pelicula_id)

    icono_formulario = ft.Icon(
        ft.Icons.EDIT_DOCUMENT if es_edicion else ft.Icons.ADD_TO_QUEUE,
        size=50,
        color=ft.Colors.AMBER_400
    )

    titulo_formulario = ft.Text(
        value="Editar Película" if es_edicion else "Agregar Nueva Película",
        size=24,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE,
        text_align=ft.TextAlign.CENTER
    )

    subtitulo = ft.Text(
        value=f"Modificando registro ID #{pelicula_id}" if es_edicion else "Ingresa los datos correspondientes en el formulario",
        size=14,
        color=ft.Colors.BLUE_GREY_200,
        text_align=ft.TextAlign.CENTER
    )

    # Declaración previa del botón para poder alternar su estado  # [NUEVO]
    btn_guardar = ft.ElevatedButton(  # [NUEVO]
        content=ft.Text("Guardar cambios" if es_edicion else "Guardar", color=ft.Colors.BLACK87),  # [NUEVO]
        icon=ft.Icons.SAVE,  # [NUEVO]
        bgcolor=ft.Colors.AMBER_600,  # [NUEVO]
        disabled=not es_edicion,  # Inicia deshabilitado si es nuevo  # [NUEVO]
        expand=True,  # [NUEVO]
    )  # [NUEVO]

    # Validador reactivo conforme el usuario escribe o borra  # [NUEVO]
    def validar_formulario(e=None):  # [NUEVO]
        titulo = campo_titulo.value.strip() if campo_titulo.value else ""  # [NUEVO]
        director = campo_director.value.strip() if campo_director.value else ""  # [NUEVO]
        puntuacion_str = campo_puntuacion.value.strip() if campo_puntuacion.value else ""  # [NUEVO]

        formulario_valido = True  # [NUEVO]

        # Validación visual del campo Puntuación sin bloquear borrado  # [NUEVO]
        if not puntuacion_str:  # [NUEVO]
            campo_puntuacion.error_text = None  # Si está vacío mientras escribe, no muestra error brusco  # [NUEVO]
            formulario_valido = False  # [NUEVO]
        else:  # [NUEVO]
            try:  # [NUEVO]
                puntuacion_val = int(puntuacion_str)  # [NUEVO]
                if puntuacion_val < 1 or puntuacion_val > 10:  # [NUEVO]
                    campo_puntuacion.error_text = "Debe ser un número entero entre 1 y 10"  # [NUEVO]
                    formulario_valido = False  # [NUEVO]
                else:  # [NUEVO]
                    campo_puntuacion.error_text = None  # [NUEVO]
            except ValueError:  # [NUEVO]
                campo_puntuacion.error_text = "Solo números enteros permitidos (1-10)"  # [NUEVO]
                formulario_valido = False  # [NUEVO]

        # Requerimiento de campos de texto  # [NUEVO]
        if not titulo or not director:  # [NUEVO]
            formulario_valido = False  # [NUEVO]

        # Actualizar dinámicamente el estado del botón Guardar  # [NUEVO]
        btn_guardar.disabled = not formulario_valido  # [NUEVO]
        page.update()  # [NUEVO]

    # Campos de entrada con escucha on_change para reactividad  # [MODIFICADO]
    campo_titulo = ft.TextField(
        label="Título de la Película",
        value=pelicula_actual["titulo"] if pelicula_actual else "",
        prefix_icon=ft.Icons.MOVIE_CREATION,
        focused_border_color=ft.Colors.AMBER_400,
        cursor_color=ft.Colors.AMBER_400,
        text_style=ft.TextStyle(color=ft.Colors.WHITE),
        on_change=validar_formulario,  # [NUEVO]
        expand=True,
    )

    campo_director = ft.TextField(
        label="Director",
        value=pelicula_actual["director"] if pelicula_actual else "",
        prefix_icon=ft.Icons.PERSON,
        focused_border_color=ft.Colors.AMBER_400,
        cursor_color=ft.Colors.AMBER_400,
        text_style=ft.TextStyle(color=ft.Colors.WHITE),
        on_change=validar_formulario,  # [NUEVO]
        expand=True,
    )

    campo_puntuacion = ft.TextField(
        label="Puntuación (Entero: 1 - 10)",  # [MODIFICADO]
        value=str(int(pelicula_actual["puntuacion"])) if pelicula_actual else "",  # [MODIFICADO]
        prefix_icon=ft.Icons.STAR,
        focused_border_color=ft.Colors.AMBER_400,
        cursor_color=ft.Colors.AMBER_400,
        text_style=ft.TextStyle(color=ft.Colors.WHITE),
        keyboard_type=ft.KeyboardType.NUMBER,
        on_change=validar_formulario,  # [NUEVO]
        expand=True,
    )

    def guardar_pelicula(e):
        titulo = campo_titulo.value.strip()
        director = campo_director.value.strip()
        puntuacion_val = int(campo_puntuacion.value.strip())

        datos_pelicula = {
            "titulo": titulo,
            "director": director,
            "puntuacion": puntuacion_val
        }

        if es_edicion:
            exito, mensaje = actualizar(pelicula_id, datos_pelicula)  # [MODIFICADO]
        else:
            exito, mensaje = crear(datos_pelicula)  # [MODIFICADO]

        if exito:
            # SnackBar de éxito en color verde suave  # [MODIFICADO]
            snackbar = ft.SnackBar(
                content=ft.Text(f"¡Éxito! {mensaje}", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.GREEN_800  # [MODIFICADO]
            )
            if hasattr(page, "open"):
                page.open(snackbar)
            else:
                page.snack_bar = snackbar
                page.snack_bar.open = True
            page.update()

            if on_guardado_exitoso:
                on_guardado_exitoso()
        else:
            # SnackBar de error en color rojo suave  # [MODIFICADO]
            snackbar_err = ft.SnackBar(
                content=ft.Text(f"Error: {mensaje}", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_800  # [MODIFICADO]
            )
            if hasattr(page, "open"):
                page.open(snackbar_err)
            else:
                page.snack_bar = snackbar_err
                page.snack_bar.open = True
            page.update()

    # Asignar acción al botón guardar  # [MODIFICADO]
    btn_guardar.on_click = guardar_pelicula  # [MODIFICADO]

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
                ft.Divider(color=ft.Colors.TRANSPARENT, height=10),
                ft.Row(controls=[campo_titulo]),
                ft.Row(controls=[campo_director]),
                ft.Row(controls=[campo_puntuacion]),
                ft.Divider(color=ft.Colors.TRANSPARENT, height=10),
                ft.Row(
                    controls=[btn_cancelar, btn_guardar],
                    spacing=15
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            tight=True
        ),
        bgcolor=ft.Colors.BLUE_GREY_800,
        padding=30,
        border_radius=12,
        width=500,
    )

    return ft.Column(
        controls=[formulario_card],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
        scroll=ft.ScrollMode.AUTO
    )