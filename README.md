
# CorpEx Logistics - Demo (Flask)

Demo mínima para registrar **Ventas**, **Gastos** y consultar **Reportes**.

## Usuario de prueba
- Usuario: `agencia1`
- Contraseña: `demo123`

## Deploy en Render
1. Crea una cuenta en https://render.com
2. Sube estos archivos a un **repositorio de GitHub** (nuevo repo).
3. En Render, elige **New +** → **Web Service** → **Connect** tu repo.
4. Configura:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment**: `Python 3`
5. Variables de entorno (opcionalmente en **Environment**):
   - `SECRET_KEY` = una cadena aleatoria segura
   - `DATABASE_URL` = (opcional) por defecto usa SQLite local `sqlite:///corpex_demo.db`.
     Para producción puedes usar un PostgreSQL de Render y pegar aquí su URL.
6. Click en **Create Web Service** y espera a que haga el deploy. Te dará una **URL pública**.

## Ejecutar localmente
```bash
pip install -r requirements.txt
python app.py
# abre http://localhost:5000
```
