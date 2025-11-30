# 🦷 AGENTE AI PARA GESDEN G5.29

Sistema de Inteligencia Artificial para gestión automatizada de clínica dental mediante comandos en lenguaje natural.

---

## 📋 INFORMACIÓN DEL PROYECTO

- **Cliente:** Clínica Dental (GABINETE2)
- **Sistema:** Gesden G5.29 
- **Base de Datos:** SQL Server 2008 - GELITE
- **Versión Actual:** 2.0
- **Fecha Inicio:** 29/11/2024
- **Estado:** ✅ En desarrollo activo

---

## 🎯 FUNCIONALIDADES IMPLEMENTADAS

### ✅ VERSIÓN 2.0 (ACTUAL)

#### 1. Gestión de Pacientes
- ✅ **Crear paciente nuevo**
  - Validación de duplicados (nombre + apellidos)
  - Validación de teléfono duplicado
  - Advertencia de similitudes
  - Nombres/apellidos en MAYÚSCULAS automático
  - Generación automática de NumPac
  
- ✅ **Buscar paciente**
  - Por nombre
  - Por apellidos
  - Por número de paciente
  - Por teléfono

#### 2. Gestión de Citas
- ✅ **Crear cita**
  - Asignación automática a paciente
  - Conversión de fechas automática
  - Duración configurable
  
- ✅ **Listar citas**
  - Por fecha (hoy, mañana, fecha específica)
  - Con datos del paciente
  - Ordenadas por hora

#### 3. Sistema de Comandos en Lenguaje Natural
- ✅ Procesamiento de comandos en español
- ✅ Extracción automática de fechas
- ✅ Detección de intenciones
- ✅ Confirmaciones interactivas

---

## 📂 ESTRUCTURA DEL PROYECTO

```
AGENTE_AI_GESDEN/
├── codigo/
│   └── agente_gesden.py          # Código principal (VERSIÓN ACTIVA)
│
├── documentacion/
│   ├── GUIA_INSTALACION.md       # Guía de instalación paso a paso
│   ├── ANALISIS_TECNICO.md       # Análisis completo del sistema
│   └── REGISTRO_CAMBIOS.md       # Historial de versiones
│
└── versiones/
    └── (versiones anteriores archivadas)
```

---

## 🚀 INSTALACIÓN RÁPIDA

### Requisitos:
- Python 3.8+
- SQL Server 2008+
- Acceso a base de datos GELITE

### Pasos:
1. Instalar Python: https://www.python.org/downloads/
2. Instalar dependencias:
   ```bash
   pip install pyodbc
   ```
3. Ejecutar:
   ```bash
   python codigo/agente_gesden.py
   ```

📖 **Documentación completa:** Ver `documentacion/GUIA_INSTALACION.md`

---

## 💬 EJEMPLOS DE USO

```
👤 Tú: crear paciente
[El sistema pedirá los datos interactivamente]

👤 Tú: buscar paciente Juan García

👤 Tú: crear cita para María López el 15/12/2025 a las 10:30

👤 Tú: listar citas de hoy
```

---

## 🛡️ VALIDACIONES Y SEGURIDAD

### Protección contra duplicados:
1. ✅ Bloqueo si nombre + apellidos exactos existen
2. ✅ Bloqueo si teléfono ya está registrado
3. ✅ Advertencia si hay nombres similares
4. ✅ Confirmación manual requerida en casos dudosos

### Logging:
- ✅ Todas las operaciones se registran en `agente_gesden.log`
- ✅ Trazabilidad completa de acciones

---

## 📊 MAPEO DE BASE DE DATOS

### Tablas Principales:
- **Pacientes** → Datos de pacientes
- **DCitas** → Citas/agenda
- **TtosMed** → Tratamientos realizados
- **Presu / PresuTto** → Presupuestos
- **PagoCli / DeudaCli** → Pagos y deuda
- **AlertPac** → Alertas del paciente
- **TAntecedentes** → Antecedentes médicos

📖 **Mapeo completo:** Ver `documentacion/ANALISIS_TECNICO.md`

---

## 🔄 PRÓXIMAS FUNCIONALIDADES

### En Desarrollo:
- [ ] Gestión de presupuestos
- [ ] Registro de pagos
- [ ] Consulta de deuda
- [ ] Historial clínico completo
- [ ] Antecedentes y alergias
- [ ] Tratamientos/actos clínicos
- [ ] Integración con LLM avanzado (Ollama/GPT-4)

---

## 📝 REGISTRO DE CAMBIOS

### v2.0 (29/11/2024)
- ✅ Añadida función crear paciente
- ✅ Validación completa de duplicados
- ✅ Validación de teléfono duplicado
- ✅ Advertencias de similitud
- ✅ Mejoras en procesamiento de lenguaje natural

### v1.0 (29/11/2024)
- ✅ Conexión a base de datos GELITE
- ✅ Búsqueda de pacientes
- ✅ Creación de citas
- ✅ Listado de citas
- ✅ Sistema básico de comandos

📖 **Historial completo:** Ver `documentacion/REGISTRO_CAMBIOS.md`

---

## 🔧 CONFIGURACIÓN

### Parámetros principales (en el código):

```python
class ConfigGesden:
    SERVIDOR = "GABINETE2\\INFOMED"
    BASE_DATOS = "GELITE"
    ID_CENTRO = 2  # Tu centro
```

---

## 📞 SOPORTE Y MANTENIMIENTO

### Archivos de log:
- `agente_gesden.log` → Registro de todas las operaciones

### En caso de error:
1. Revisar el log
2. Verificar conexión SQL Server
3. Verificar permisos de usuario

---

## ⚠️ ADVERTENCIAS IMPORTANTES

1. **Backup:** Hacer backup de la BD antes de usar en producción
2. **Pruebas:** Probar primero en copia de la BD
3. **Permisos:** Usuario necesita permisos INSERT/UPDATE/DELETE
4. **Gesden:** Validar que los datos creados se ven correctamente en Gesden

---

## 📄 LICENCIA

Código propietario desarrollado para uso exclusivo de la clínica.

---

**Última actualización:** 29/11/2024  
**Versión:** 2.0  
**Estado:** ✅ Operativo con validaciones completas
