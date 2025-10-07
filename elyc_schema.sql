CREATE TABLE usuarios (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT,
  correo TEXT,
  rol TEXT
);

CREATE TABLE noticias (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  titulo TEXT,
  contenido TEXT,
  fecha TEXT
);

CREATE TABLE imagenes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ruta TEXT,
  descripcion TEXT
);

CREATE TABLE contacto (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT,
  mensaje TEXT,
  fecha TEXT
);
