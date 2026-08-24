import sys
import os
import socket
from pathlib import Path

# Añadir la carpeta raíz al path de módulos
sys.path.append(str(Path(__file__).resolve().parent))

# Asegurar directorios
os.makedirs("assets/posters", exist_ok=True)

import flet as ft
from views.home_view import HomeView
from views.form_view import FormView
from components.navbar import Navbar


def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def main(page: ft.Page):
    page.title = "🎞️ CineApp - Catálogo de Películas"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.Colors.BLUE_GREY_900
    page.padding = 20

    # Contenedores de ambas vistas
    contenedor_home = ft.Container(expand=True, visible=True)
    contenedor_form = ft.Container(expand=True, visible=False)

    def ir_a_inicio():
        contenedor_home.content = HomeView(page=page, on_editar=ir_a_editar)
        contenedor_home.visible = True
        contenedor_form.visible = False
        page.update()

    def ir_a_agregar():
        contenedor_form.content = FormView(
            page=page,
            pelicula_id=None,
            on_cancelar=ir_a_inicio,
            on_guardado_exitoso=ir_a_inicio
        )
        contenedor_home.visible = False
        contenedor_form.visible = True
        page.update()

    def ir_a_editar(pid: int):
        contenedor_form.content = FormView(
            page=page,
            pelicula_id=pid,
            on_cancelar=ir_a_inicio,
            on_guardado_exitoso=ir_a_inicio
        )
        contenedor_home.visible = False
        contenedor_form.visible = True
        page.update()

    def manejar_nav(ruta: str):
        if ruta == "inicio":
            ir_a_inicio()
        elif ruta == "agregar":
            ir_a_agregar()

    # Barra superior
    barra_superior = Navbar(on_nav_change=manejar_nav)

    # Inyección inicial
    page.add(
        ft.Column(
            controls=[
                barra_superior,
                contenedor_home,
                contenedor_form,
            ],
            expand=True,
            spacing=15,
        )
    )

    # Cargar datos iniciales
    ir_a_inicio()


if __name__ == "__main__":
    PUERTO = 8550
    ip_local = get_local_ip()

    print("=" * 60)
    print("🚀 Servidor CineApp ejecutándose...")
    print(f"👉 Dirección local:   http://localhost:{PUERTO}")
    print(f"👉 Dirección de red:  http://{ip_local}:{PUERTO}")
    print("=" * 60)

    if hasattr(ft, "run"):
        ft.run(main, host="0.0.0.0", port=PUERTO, assets_dir="assets", view=ft.AppView.WEB_BROWSER)
    else:
        ft.app(target=main, host="0.0.0.0", port=PUERTO, assets_dir="assets", view=ft.AppView.WEB_BROWSER)