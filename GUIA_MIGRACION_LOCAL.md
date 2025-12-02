# Guía de Migración a Agente Local (Ollama)

Para ejecutar el agente de forma 100% local y privada, sigue estos pasos:

## 1. Instalar Ollama
Ollama es el motor que ejecutará el modelo de IA en tu Mac.

1. Descarga Ollama desde [ollama.com](https://ollama.com/download/mac).
2. Instala la aplicación.
3. Abre la terminal y ejecuta el siguiente comando para descargar el modelo:
   ```bash
   ollama run llama3.1
   ```
   *Esto descargará unos 4.7GB. Espera a que termine y te deje en un prompt `>>>`. Puedes escribir `/bye` para salir.*

## 2. Instalar Driver SQL Server (ODBC)
Para conectar con el PC Windows, necesitas el driver oficial de Microsoft.

1. Abre la terminal y ejecuta estos comandos uno por uno:
   ```bash
   # 1. Añadir el catálogo de Microsoft
   brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
   
   # 2. Actualizar Homebrew
   brew update
   
   # 3. Instalar el driver (ACEPTA la licencia si te pregunta con 'YES')
   brew install msodbcsql17 mssql-tools
   ```

## 3. Actualizar Dependencias Python
Hemos cambiado las librerías de Google por LangChain.

1. En tu terminal, dentro de la carpeta del proyecto:
   ```bash
   pip install -r requirements.txt
   ```

## 3. Ejecutar el Servidor
¡Todo listo! Para iniciar el servidor usa este comando (asegúrate de usar `./venv/bin/python`):

```bash
./venv/bin/python api_server.py
```

## Verificación
- El servidor debería mostrar: `✅ Ollama configurado: llama3.1`
- Base de datos: `conectada` (usando pymssql)
