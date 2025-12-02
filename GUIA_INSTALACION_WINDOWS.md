# 🪟 Guía de Instalación en Windows (Recomendado)

Ejecutar el agente directamente en el PC donde está la base de datos es la **mejor opción**: más rápido, sin errores de conexión y sin necesidad de Ngrok.

## 1. Descargas Necesarias
En el PC Windows, descarga e instala:

1.  **Python 3.11+**: [python.org/downloads](https://www.python.org/downloads/)
    *   ⚠️ **IMPORTANTE:** Al instalar, marca la casilla **"Add Python to PATH"**.
2.  **Ollama para Windows**: [ollama.com/download/windows](https://ollama.com/download/windows)
3.  **Driver ODBC (Opcional)**: Normalmente Windows ya lo trae, pero si falla, instala "ODBC Driver 17 for SQL Server".

## 2. Preparar Ollama
Una vez instalado Ollama, abre una terminal (PowerShell o CMD) y ejecuta:
```powershell
ollama run llama3.2
```

## 3. Configurar el Código
Copia la carpeta del proyecto `AgenteIA` al PC Windows (ej: al Escritorio).

1.  Abre `api_server.py` con el Bloc de Notas.
2.  Busca la sección de configuración y déjala así (mucho más simple):

```python
    # SQL Server LOCAL (Windows)
    SQL_SERVER = "localhost\\INFOMED"  # O simplemente "." o "GABINETE2\INFOMED"
    SQL_DATABASE = "GELITE"
    SQL_USER = "RUBIOGARCIADENTAL"
    SQL_PASSWORD = "666666"
    
    # En Windows suele funcionar el driver genérico o el 17
    SQL_DRIVER = "SQL Server" 
```

3.  Busca el método `get_db_connection` y asegúrate de que usa `pymssql` (como lo dejamos configurado) o vuelve a `pyodbc` si prefieres.
    *   *Recomendación:* Si usas `pymssql` en Windows, funciona igual de bien.

## 4. Instalar Librerías y Ejecutar
En la carpeta del proyecto, abre una terminal:

1.  Instalar librerías:
    ```powershell
    pip install -r requirements.txt
    ```
2.  Iniciar servidor:
    ```powershell
    python api_server.py
    ```

## 5. Acceso desde Internet (Cualquier IP)
Para acceder desde tu móvil o casa sin estar en la red de la clínica:

1.  En el PC Windows, abre otra terminal.
2.  Ejecuta Ngrok apuntando al puerto del servidor (5000):
    ```powershell
    ngrok http 5000
    ```
3.  Copia la dirección que te da (ej: `https://rubio-dental.ngrok-free.app`).
4.  **¡Esa es tu Web App!** Puedes abrirla desde el móvil, tablet o cualquier PC del mundo.
    *   No hace falta Render: tu PC Windows ya actúa como servidor web seguro.

