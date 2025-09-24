
## Backend (Django)

### Requisitos

* Python 3.12+
* pip
* Virtualenv

### Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/Maxi-Duran/backend_django.git
cd backend_django
```

2. Crear y activar el entorno virtual:

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Configurar base de datos (por defecto SQLite):

```bash
python manage.py migrate
```

5. Configurar correo electrónico en `settings.py`:

```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "TU_CORREO@gmail.com"
EMAIL_HOST_PASSWORD = "TU_CONTRASEÑA_DE_APLICACIÓN"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

> 🔹 Nota: Para Gmail necesitas generar una [contraseña de aplicación](https://support.google.com/accounts/answer/185833?hl=es).
> Puedes usar mi correo por defecto.

6. Iniciar Redis con Docker:
Abrir docker desktop
```bash
docker run -p 6379:6379 redis
```

7. Iniciar Celery:

```bash
python -m celery -A backend worker -l info --pool=solo
```

8. Ejecutar el servidor Django:

```bash
python manage.py runserver
```

El backend estará disponible en: `http://localhost:8000`


### Testeo

* Ejecutar test unitarios:

```bash
python manage.py test
```

* Ejecutar test de rendimiento con Locust:

```bash
locust -f locustfile.py
```

---

### Decisiones Técnicas

* **Django REST Framework** para API REST, con ViewSets y routers para endpoints limpios y escalables.
* **JWT (SimpleJWT)** para autenticación de usuarios y admins.
* **CORS headers** para permitir que Nuxt 3 consuma la API localmente.
* **Correo con Gmail SMTP** para verificación de usuarios y notificación de ganadores.
* **Celery** para enviar correos de forma asíncrona.

---

## Endpoints principales

### Usuarios (`/api/users/`)

| Método | URL                                    | Descripción                                      |
| ------ | -------------------------------------- | ------------------------------------------------ |
| POST   | /users/                                | Registrar usuario. Envía correo de verificación. |
| GET    | /users/                                | Listar usuarios (solo admin).                    |
| GET    | /users/verify/[uuid\:code](uuid:code)/ | Verificar correo de usuario.                     |
| POST   | /admin-login/                          | Login de administrador. Devuelve JWT.            |

**Ejemplo: Crear usuario**

```http
POST /api/users/
Content-Type: application/json

{
  "name": "Maximiliano",
  "email": "max@example.com",
  "password": "12345678",
  "phone": "123456789"
}
```

**Response:**

```json
{
  "message": "Usuario creado. Revisa tu correo para verificar tu cuenta."
}
```

---

### Concurso (`/api/contest/`)

#### Participantes (`participants`)

| Método | URL            | Descripción                                        |
| ------ | -------------- | -------------------------------------------------- |
| GET    | /participants/ | Lista participantes. Admin ve todos.               |
| POST   | /participants/ | Crear participación (requiere usuario verificado). |

**Ejemplo: Crear participación**

```http
POST /api/contest/participants/
Authorization: Bearer <TOKEN>
```

**Response:**

```json
{
  "message": "Participación confirmada. Revisa tu correo."
}
```

#### Selección de ganadores (`winner`)

| Método | URL              | Descripción                                    |
| ------ | ---------------- | ---------------------------------------------- |
| POST   | /winner/select/  | Seleccionar un ganador aleatorio (solo admin). |
| GET    | /winner/history/ | Historial de ganadores.                        |

**Ejemplo: Seleccionar ganador**

```http
POST /api/contest/winner/select/
Authorization: Bearer <TOKEN>
```

**Response:**

```json
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
```

**Ejemplo: Historial de ganadores**

```http
GET /api/contest/winner/history/
Authorization: Bearer <TOKEN>
```

**Response:**

```json
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
```

---

## Frontend (Nuxt 3)

### Instalación

1. Entrar al directorio del frontend:

```bash
git clone https://github.com/Maxi-Duran/front-django.git
cd front-django
```

2. Instalar dependencias:

```bash
npm install
# o
yarn install
```

3. Ejecutar servidor de desarrollo:

```bash
npm run dev
# o
yarn dev
```

El frontend estará disponible en: `http://localhost:3000`
