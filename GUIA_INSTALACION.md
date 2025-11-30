# 🚀 GUÍA DE INSTALACIÓN Y USO
## Agente IA para Gesden G5.29

---

## 📋 REQUISITOS PREVIOS

### 1. Python instalado
- Versión: Python 3.8 o superior
- Verificar: Abre PowerShell y ejecuta `python --version`
- Si no está instalado, descarga de: https://www.python.org/downloads/

### 2. Acceso a SQL Server
- ✅ Ya tienes: `GABINETE2\INFOMED`
- ✅ Base de datos: `GELITE`
- ✅ Usuario: `GABINETE2\BOX2` (Windows Authentication)

---

## 🔧 INSTALACIÓN PASO A PASO

### Paso 1: Crear carpeta del proyecto

```powershell
# Crear carpeta
New-Item -Path "C:\AgenteGesden" -ItemType Directory -Force

# Ir a la carpeta
cd C:\AgenteGesden
```

### Paso 2: Copiar el archivo Python

Copia el archivo `agente_gesden_ai.py` a la carpeta `C:\AgenteGesden\`

### Paso 3: Instalar dependencias

```powershell
# Instalar pyodbc
pip install pyodbc

# Verificar instalación
pip list | Select-String pyodbc
```

---

## ▶️ CÓMO USAR EL AGENTE

### Opción 1: Desde PowerShell

```powershell
# Ir a la carpeta
cd C:\AgenteGesden

# Ejecutar el agente
python agente_gesden_ai.py
```

### Opción 2: Doble clic

1. Abre el Bloc de notas
2. Escribe esto:

```batch
@echo off
cd C:\AgenteGesden
python agente_gesden_ai.py
pause
```

3. Guarda como `IniciarAgente.bat` en `C:\AgenteGesden\`
4. Haz doble clic en `IniciarAgente.bat` para ejecutar

---

## 💬 EJEMPLOS DE COMANDOS

### 1️⃣ Crear una cita

```
Crear cita para Manuel López el 19 de enero de 2026 a las 10:30
```

```
Nueva cita para ALICIA el día de mañana a las 15:00
```

### 2️⃣ Listar citas

```
Listar citas de hoy
```

```
Mostrar citas de mañana
```

### 3️⃣ Buscar paciente

```
Buscar paciente Manuel López
```

```
Encontrar paciente ALICIA
```

---

## 🔍 SOLUCIÓN DE PROBLEMAS

### ❌ Error: "No se reconoce python"

**Solución:**
1. Instala Python desde https://www.python.org/downloads/
2. Durante la instalación, marca "Add Python to PATH"
3. Reinicia PowerShell

### ❌ Error: "No module named pyodbc"

**Solución:**
```powershell
pip install pyodbc
```

### ❌ Error: "No se pudo conectar a Gesden"

**Verificaciones:**
1. SQL Server está corriendo
2. El servicio SQL Server está activo
3. Tienes permisos de Windows Authentication

**Comando de verificación:**
```powershell
# Abrir servicios
services.msc

# Buscar: SQL Server (INFOMED)
# Estado debe ser: En ejecución
```

### ❌ Error: "Paciente no encontrado"

**Causa:** El nombre no coincide exactamente

**Solución:**
1. Primero busca el paciente: `Buscar paciente [nombre aproximado]`
2. Verifica el nombre exacto
3. Usa ese nombre para crear la cita

---

## 🎯 FUNCIONALIDADES ACTUALES

### ✅ Implementado:
- [x] Buscar pacientes por nombre
- [x] Listar citas de una fecha
- [x] Crear citas para pacientes existentes
- [x] Conversión automática de fechas
- [x] Registro de operaciones (log)

### 🚧 Próximamente (requiere más desarrollo):
- [ ] Eliminar/modificar citas
- [ ] Crear actos clínicos/tratamientos
- [ ] Integración con LLM avanzado (Ollama/GPT-4)
- [ ] Búsqueda más inteligente con IA
- [ ] Interfaz gráfica

---

## 📊 ESTRUCTURA DE ARCHIVOS

```
C:\AgenteGesden\
├── agente_gesden_ai.py      # Código principal
├── IniciarAgente.bat         # Acceso directo (opcional)
└── agente_gesden.log         # Registro de operaciones
```

---

## 🔐 SEGURIDAD

### ⚠️ IMPORTANTE:

1. **Hacer backup antes de usar:**
   ```sql
   BACKUP DATABASE GELITE 
   TO DISK = 'C:\Backups\GELITE_backup.bak'
   ```

2. **El agente actualmente usa:**
   - Usuario con permisos completos
   - Sin confirmación para operaciones críticas

3. **Recomendaciones:**
   - Probar primero en copia de la BD
   - Revisar el log: `agente_gesden.log`
   - Validar datos antes de insertar

---

## 📝 REGISTRO DE OPERACIONES

Todas las operaciones se guardan en: `C:\AgenteGesden\agente_gesden.log`

**Ver últimas 20 líneas:**
```powershell
Get-Content C:\AgenteGesden\agente_gesden.log -Tail 20
```

---

## 🆘 SOPORTE

### Si algo no funciona:

1. **Revisa el log:**
   ```powershell
   notepad C:\AgenteGesden\agente_gesden.log
   ```

2. **Verifica la conexión a SQL:**
   ```sql
   USE GELITE;
   SELECT DB_NAME() AS BaseDatos;
   ```

3. **Copia el error exacto** y consulta

---

## 🎓 PRÓXIMOS PASOS

### Para mejorar el agente:

1. **Instalar Ollama (IA local, gratis):**
   - Descargar de: https://ollama.com/download
   - Instalar modelo: `ollama pull mistral`
   - Integrar en el código para mejor comprensión

2. **Añadir más funcionalidades:**
   - Modificar citas existentes
   - Eliminar citas con confirmación
   - Crear tratamientos/actos clínicos
   - Enviar recordatorios SMS

3. **Crear interfaz gráfica:**
   - Con Streamlit (web simple)
   - Con PyQt (aplicación Windows)

---

## 📞 CONTACTO

Para mejoras o problemas, revisa:
- El archivo de log
- La documentación de Gesden
- Los comentarios en el código Python

---

**Versión:** 1.0  
**Fecha:** 29/11/2024  
**Estado:** Beta - Funcional para operaciones básicas
