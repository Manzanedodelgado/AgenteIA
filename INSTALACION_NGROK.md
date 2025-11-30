# 🚀 INSTALACIÓN AGENTE GESDEN IA - VERSIÓN NGROK

## 📋 REQUISITOS PREVIOS

- Windows 10/11
- Python 3.8+
- SQL Server con base de datos GELITE (Gesden)
- Cuenta Anthropic (API Key de Claude)
- Cuenta Ngrok (gratis)

---

## ⚡ INSTALACIÓN RÁPIDA (15 MINUTOS)

### PASO 1: Preparar carpeta (2 min)

```powershell
# Crear estructura
cd C:\Users\BOX2\Desktop
mkdir AGENTE-IA_GESDEN
cd AGENTE-IA_GESDEN
mkdir templates
mkdir static
```

---

### PASO 2: Copiar archivos

Descargar y copiar estos archivos:

```
C:\Users\BOX2\Desktop\AGENTE-IA_GESDEN\
├── api_server.py          ← Servidor Flask
├── templates\
│   └── index.html         ← Interfaz web
└── static\
    ├── logo.png           ← Logo Rubio García
    └── avatar.png         ← Avatar dental
```

---

### PASO 3: Instalar dependencias Python (3 min)

```powershell
pip install flask flask-cors pyodbc anthropic
```

---

### PASO 4: Configurar Claude API Key (2 min)

```powershell
# Abrir PowerShell como ADMINISTRADOR
setx ANTHROPIC_API_KEY "sk-ant-api03-TU-KEY-AQUI"
```

**⚠️ IMPORTANTE:** Cierra y abre PowerShell de nuevo para que cargue la variable.

**Verificar:**
```powershell
echo $env:ANTHROPIC_API_KEY
```

Debe mostrar tu API key.

---

### PASO 5: Instalar Ngrok (3 min)

**Opción A: Con winget (recomendado)**
```powershell
winget install ngrok
```

**Opción B: Descarga manual**
1. Ve a: https://ngrok.com/download
2. Descarga `ngrok-v3-stable-windows-amd64.zip`
3. Extrae `ngrok.exe` a `C:\Windows\System32\`

**Verificar instalación:**
```powershell
ngrok version
```

---

### PASO 6: Configurar Ngrok (2 min)

1. **Crear cuenta gratis:** https://dashboard.ngrok.com/signup

2. **Obtener authtoken:** https://dashboard.ngrok.com/get-started/your-authtoken

3. **Configurar token:**
```powershell
ngrok config add-authtoken TU_TOKEN_AQUI
```

---

### PASO 7: Iniciar el servidor (1 min)

**Terminal 1 - Servidor Flask:**
```powershell
cd C:\Users\BOX2\Desktop\AGENTE-IA_GESDEN
python api_server.py
```

Deberías ver:
```
============================================================
🚀 AGENTE GESDEN IA - API SERVER
============================================================

🗄️  Base de datos: LOCAL (SQL Server)
🌐 Acceso remoto: Vía Ngrok Tunnel
🤖 IA: Claude API

📍 Servidor corriendo en: http://localhost:5000

🌍 ACCESO DESDE INTERNET:
   1. Abre otra terminal
   2. Ejecuta: ngrok http 5000
   3. Copia la URL: https://xxx.ngrok-free.app
   4. Esa URL es accesible desde cualquier sitio

============================================================
```

**Terminal 2 - Ngrok Tunnel:**
```powershell
ngrok http 5000
```

Deberías ver:
```
ngrok

Session Status                online
Forwarding                    https://abc-123.ngrok-free.app -> http://localhost:5000

Connections                   ttl     opn     rt1
                              0       0       0.00
```

---

### PASO 8: Probar (2 min)

1. **Local:** Abre `http://localhost:5000` en navegador
   - ✅ Deberías ver la interfaz del agente

2. **Remoto:** Abre la URL de ngrok `https://abc-123.ngrok-free.app`
   - ⚠️ Puede aparecer advertencia de ngrok → Click "Visit Site"
   - ✅ Deberías ver la misma interfaz

3. **Probar comando:**
   - Escribe: "hola"
   - Click ENVIAR
   - ✅ Debe responder el asistente

---

## 🔄 USO DIARIO

### Iniciar el sistema:

**Terminal 1:**
```powershell
cd C:\Users\BOX2\Desktop\AGENTE-IA_GESDEN
python api_server.py
```

**Terminal 2:**
```powershell
ngrok http 5000
```

**Anota la URL de ngrok** y úsala para acceder desde cualquier sitio.

---

## 🤖 INICIO AUTOMÁTICO (OPCIONAL)

### Opción 1: Script BAT

**Crear:** `C:\Users\BOX2\Desktop\AGENTE-IA_GESDEN\iniciar.bat`

```batch
@echo off
echo Iniciando Agente Gesden IA...

start "Servidor Flask" /MIN python api_server.py

timeout /t 5 /nobreak

start "Ngrok Tunnel" ngrok http 5000

echo.
echo ============================================================
echo Agente iniciado correctamente
echo ============================================================
echo.
echo Servidor Flask: http://localhost:5000
echo Ngrok: Consulta la terminal de Ngrok para ver la URL publica
echo.
pause
```

**Usar:** Doble click en `iniciar.bat`

---

### Opción 2: Añadir al inicio de Windows

1. `Win + R` → `shell:startup`
2. Copiar acceso directo de `iniciar.bat` ahí
3. Reiniciar PC para probar

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### ❌ Error: "ANTHROPIC_API_KEY no configurada"

```powershell
# Configurar de nuevo
setx ANTHROPIC_API_KEY "sk-ant-api03-TU-KEY-AQUI"

# Cerrar TODO PowerShell y abrir nuevo
```

---

### ❌ Error: "Can't connect to SQL Server"

1. Verificar que Gesden esté corriendo
2. Verificar nombre del servidor en `api_server.py`:
   ```python
   SQL_SERVER = "GABINETE2\\INFOMED"  # ← Cambiar si es diferente
   ```

---

### ❌ Error: "ngrok not found"

```powershell
# Reinstalar ngrok
winget install ngrok

# O descargar manualmente y poner en C:\Windows\System32\
```

---

### ❌ Error 404 en ngrok

- El servidor Flask NO está corriendo
- Reinicia `python api_server.py` en Terminal 1

---

### ❌ La URL de ngrok cambia cada vez

**Versión gratis:** La URL cambia cada reinicio

**Solución 1 (gratis):** Apuntar la nueva URL cada vez

**Solución 2 (pago $8/mes):**
```powershell
# Ngrok Pro - URL fija
ngrok http --domain=tu-dominio.ngrok.io 5000
```

---

### ❌ Ngrok muestra pantalla de advertencia

**Normal en versión gratis.**

Click en **"Visit Site"** para continuar.

---

## 📊 COMANDOS DE EJEMPLO

```
✅ "busca paciente 4134"
✅ "busca a Juan García"
✅ "citas de hoy"
✅ "citas de mañana"
✅ "citas del lunes"
✅ "crear cita para María el martes 10:00"
✅ "lista de doctores"
✅ "ayuda"
```

---

## 💰 COSTES

| Componente | Coste |
|------------|-------|
| Servidor (tu PC) | Gratis |
| Base de datos Gesden | Gratis |
| Ngrok (versión free) | Gratis |
| Ngrok Pro (URL fija) | $8/mes |
| Claude API | ~$6/mes |
| **TOTAL GRATIS** | **$6/mes** |
| **TOTAL PRO** | **$14/mes** |

---

## 🔒 SEGURIDAD

✅ Implementado:
- Sanitización SQL injection
- Validación de inputs
- CORS restringido
- Logs sin datos sensibles
- Manejo de errores seguro

⚠️ Pendiente (producción):
- Autenticación de usuarios
- HTTPS end-to-end
- Rate limiting avanzado
- Audit logging

---

## 📞 SOPORTE

**Errores comunes:** Ver sección "Solución de problemas"

**Logs del servidor:** `C:\Users\BOX2\Desktop\AGENTE-IA_GESDEN\api_server.log`

**Ver logs en tiempo real:**
```powershell
Get-Content api_server.log -Wait
```

---

## ✅ CHECKLIST DE INSTALACIÓN

- [ ] Python instalado
- [ ] Dependencias instaladas (flask, pyodbc, etc.)
- [ ] ANTHROPIC_API_KEY configurada
- [ ] Ngrok instalado
- [ ] Ngrok authtoken configurado
- [ ] Archivos copiados (api_server.py, index.html, imágenes)
- [ ] Servidor inicia sin errores
- [ ] Funciona en localhost:5000
- [ ] Ngrok crea túnel correctamente
- [ ] Funciona desde URL de ngrok
- [ ] Claude responde a comandos

---

**¡LISTO! El sistema está funcionando.** 🎉
