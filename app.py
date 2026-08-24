import sys
import socket
from pathlib import Path

# Añadir la carpeta raíz al path de módulos
sys.path.append(str(Path(__file__).resolve().parent))

import flet as ft
from views.home_view import HomeView
from views.form_view import FormView
from components.navbar import Navbar


def get_local_ip() -> str:
    """Obtiene la IP local del equipo en la red."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # No realiza una conexión real, solo determina la interfaz de salida
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def main(page: ft.Page):
    # Configuración global de la ventana / página web
    page.title = "🎞️ Flet Películas"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.Colors.BLUE_GREY_900
    page.padding = 20

    # Alineación global centrada
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Contenedor dinámico para renderizar la vista actual
    contenedor_vistas = ft.Container(expand=True)

    # Manejador de navegación entre vistas
    def cambiar_vista(ruta: str, pelicula_id=None):
        if ruta == "inicio":
            contenedor_vistas.content = HomeView(
                page=page,
                on_editar=lambda pid: cambiar_vista("editar", pelicula_id=pid)
            )
        elif ruta == "agregar":
            contenedor_vistas.content = FormView(
                page=page,
                on_cancelar=lambda: cambiar_vista("inicio"),
                on_guardado_exitoso=lambda: cambiar_vista("inicio")
            )
        elif ruta == "editar":
            contenedor_vistas.content = FormView(
                page=page,
                pelicula_id=pelicula_id,
                on_cancelar=lambda: cambiar_vista("inicio"),
                on_guardado_exitoso=lambda: cambiar_vista("inicio")
            )
        page.update()

    # Barra de navegación
    barra_superior = Navbar(on_nav_change=cambiar_vista)

    # Cargar vista inicial
    cambiar_vista("inicio")

    # Inyección de navbar y contenido
    page.add(
        ft.Column(
            controls=[
                barra_superior,
                contenedor_vistas,
            ],
            expand=True,
        )
    )


# =====================================================================
# RECOMENDACIÓN EXTRA:
# Si planeas compartir la app en una red interna o mostrarla desde otra
# computadora, asegúrate de permitir el acceso en tu firewall al puerto 8550.
# =====================================================================

if __name__ == "__main__":
    PUERTO = 8550
    ip_local = get_local_ip()

    print("=" * 60)
    print("🚀 Servidor Flet ejecutándose...")
    print(f"👉 Dirección local:   http://localhost:{PUERTO}")
    print(f"👉 Dirección de red:  http://{ip_local}:{PUERTO}")
    print("=" * 60)

    # 1. Ejecución en Navegador Web (Accesible desde red local)
    ft.app(
        target=main,
        host="0.0.0.0",
        port=PUERTO,
        view=ft.AppView.WEB_BROWSER
    )

    # 2. Opción alternativa: Ejecutar como app de escritorio
    # ft.app(target=main, view=ft.AppView.FLET_APP)