from sqlalchemy import Column, Integer, String
from ..database import Base

class Pelicula(Base):
    __tablename__ = "peliculas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    titulo = Column(String(150), nullable=False)
    director = Column(String(100), nullable=False)
    puntuacion = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Pelicula(id={self.id}, titulo='{self.titulo}', director='{self.director}', puntuacion={self.puntuacion})>"


# Bloque de prueba para validar la creación del objeto en memoria
if __name__ == "__main__":
    pelicula_prueba = Pelicula(
        titulo="Inception",
        director="Christopher Nolan",
        puntuacion=9
    )
    print("==================================================")
    print("✅ Objeto Pelicula creado en memoria correctamente:")
    print(pelicula_prueba)
    print(f"🎬 Título: {pelicula_prueba.titulo}")
    print(f"👤 Director: {pelicula_prueba.director}")
    print(f"⭐ Puntuación: {pelicula_prueba.puntuacion}/10")
    print("==================================================")