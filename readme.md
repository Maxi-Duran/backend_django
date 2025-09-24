Instalación

Clonar el repositorio:

git clone <TU_REPOSITORIO_BACKEND>
cd backend

Crear y activar el entorno virtual:

python -m venv venv

# Windows

venv\Scripts\activate

# Mac / Linux

source venv/bin/activate

Instalar dependencias:

pip install -r requirements.txt

Configurar base de datos (por defecto SQLite):

python manage.py migrate

Configurar correo electrónico en settings.py:

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "TU_CORREO@gmail.com"
EMAIL_HOST_PASSWORD = "TU_CONTRASEÑA_DE_APLICACIÓN"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

🔹 Nota: Para Gmail necesitas generar una contraseña de aplicación
https://support.google.com/accounts/answer/185833?hl=es
Opcional si desea usar su correo por defecto en el codigo esta el mio.

Ejecutar el servidor:

python manage.py runserver

Por defecto, el backend estará en http://localhost:8000.

agrega en el backend que use locust para test de rendimientos, hice un par de test unitarios.

para correr los test unitarios:

python manage.py test

para correr los test de rendimiento:

locust -f locustfile.py

# Decisiones Tecnicas

Django REST Framework para API REST, con ViewSets y routers para endpoints limpios y escalables.

JWT (SimpleJWT) para autenticación de usuarios y admins.

CORS headers para permitir que Nuxt 3 consuma la API localmente.

Correo con Gmail SMTP para verificación de usuarios y notificación de ganadores.

Uso de Celery para enviar correos de forma asíncrona.

# Endpoints

Usuarios (/api/users/)
Método URL Descripción
POST /users/ Registrar usuario. Envía correo de verificación.
GET /users/ Listar usuarios (solo admin).
GET /users/verify/<uuid:code>/ Verificar correo de usuario.
POST /admin-login/ Login de administrador. Devuelve JWT.

Ejemplo: Crear usuario

POST /api/users/
Content-Type: application/json

{
"name": "Maximiliano",
"email": "max@example.com",
"password": "12345678",
"phone": "123456789"
}

Response:

{
"message": "Usuario creado. Revisa tu correo para verificar tu cuenta."
}

Concurso (/api/contest/)

Participantes (participants)

Método URL Descripción
GET /participants/ Lista participantes. Admin ve todos.
POST /participants/ Crear participación (requiere usuario verificado).

Ejemplo: Crear participación

POST /api/contest/participants/
Authorization: Bearer <TOKEN>

Response:

{
"message": "Participación confirmada. Revisa tu correo."
}

Selección de ganadores (winner)

Método URL Descripción
POST /winner/select/ Seleccionar un ganador aleatorio (solo admin).
GET /winner/history/ Historial de ganadores.

Ejemplo: Seleccionar ganador

POST /api/contest/winner/select/
Authorization: Bearer <TOKEN>

Response:

{
"id": 5,
"user": {
"id": 2,
"name": "Juan Perez",
"email": "juan@example.com",
"phone": "987654321"
},
"participation_code": "uuid-participacion",
"won_at": "2025-09-24T12:00:00Z",
"is_winner": true
}

Ejemplo: Historial de ganadores

GET /api/contest/winner/history/
Authorization: Bearer <TOKEN>

Response:

[
{
"id": 5,
"user": {
"id": 2,
"name": "Juan Perez",
"email": "juan@example.com",
"phone": "987654321"
},
"participation_code": "uuid-participacion",
"won_at": "2025-09-24T12:00:00Z"
}
]
