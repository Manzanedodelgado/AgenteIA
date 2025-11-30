# Agente AI para Gesden G5.29 con SQL Server 2008
## Análisis Técnico Completo y Solución Propuesta

---

## 1. RESUMEN EJECUTIVO

**Viabilidad:** ✅ **SÍ, ES TOTALMENTE VIABLE**

Puedes crear un agente AI que interactúe con tu base de datos de Gesden G5.29 mediante comandos en lenguaje natural. La solución es técnicamente factible y puede implementarse con herramientas gratuitas u económicas.

**Coste estimado:** Entre 0€ y 20€/mes (dependiendo de las opciones elegidas)

**Complejidad técnica:** Media (requiere conocimientos básicos de Python y SQL)

---

## 2. ANÁLISIS DE CONTEXTO

### 2.1 Tu situación actual
- **Software:** Gesden G5.29 (software de gestión de clínicas dentales)
- **Base de datos:** SQL Server 2008
- **Acceso:** Tienes acceso directo a las tablas de la base de datos
- **Objetivo:** Crear un agente AI que ejecute comandos como:
  - "Crea una cita para Manuel López el día 19 de enero de 2026"
  - "Crea acto clínico con reconstrucción de la pieza 26"
  - "Elimina cita del día 1..."

### 2.2 Limitaciones identificadas
1. **Gesden G5 NO tiene API oficial:** El software no expone una API pública para integraciones externas
2. **SQL Server 2008:** Versión antigua pero compatible con las soluciones propuestas
3. **Estructura de base de datos desconocida:** Necesitarás hacer ingeniería inversa de las tablas

---

## 3. ARQUITECTURA PROPUESTA

### 3.1 Componentes principales

```
┌─────────────────────────────────────────────────────────┐
│                      USUARIO                            │
│            (Comandos en lenguaje natural)               │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              INTERFAZ DE USUARIO                        │
│   • Terminal/CLI                                        │
│   • Aplicación web (Streamlit/Flask)                    │
│   • Bot de Telegram/WhatsApp                            │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              AGENTE AI (Python)                         │
│   ┌──────────────────────────────────────────────┐     │
│   │  1. Procesamiento de lenguaje natural (LLM)  │     │
│   │     - Interpreta la intención del usuario    │     │
│   │     - Extrae parámetros (nombres, fechas)    │     │
│   └──────────────────────────────────────────────┘     │
│   ┌──────────────────────────────────────────────┐     │
│   │  2. Generador de SQL                         │     │
│   │     - Convierte intención en SQL             │     │
│   │     - Validación de sintaxis                 │     │
│   └──────────────────────────────────────────────┘     │
│   ┌──────────────────────────────────────────────┐     │
│   │  3. Ejecutor de consultas                    │     │
│   │     - Conexión a BD (pyodbc/pymssql)         │     │
│   │     - Ejecución segura de SQL                │     │
│   │     - Manejo de transacciones                │     │
│   └──────────────────────────────────────────────┘     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│         BASE DE DATOS SQL SERVER 2008                   │
│              (Gesden G5.29)                             │
│   • Tabla de citas                                      │
│   • Tabla de pacientes                                  │
│   • Tabla de actos clínicos                             │
│   • Tabla de tratamientos                               │
└─────────────────────────────────────────────────────────┘
```

---

## 4. SOLUCIONES TÉCNICAS DETALLADAS

### 4.1 OPCIÓN 1: Solución de coste CERO (100% gratuita)

#### Componentes:
1. **LLM Open Source:** Llama 3.2 o Mistral 7B (ejecutado localmente con Ollama)
2. **Framework:** Vanna.AI (código abierto, especializado en Text-to-SQL)
3. **Conexión a BD:** pyodbc o pymssql
4. **Interfaz:** Streamlit (aplicación web simple)

#### Ventajas:
- ✅ **100% gratuito**
- ✅ **Sin dependencias de internet** (funciona offline)
- ✅ **Control total de los datos** (privacidad máxima)
- ✅ **Sin límites de uso**

#### Desventajas:
- ❌ Requiere hardware decente (mínimo 8GB RAM, recomendado 16GB)
- ❌ Precisión ligeramente inferior a modelos comerciales
- ❌ Configuración inicial más compleja

#### Tecnologías específicas:

**A) Ollama + Llama 3.2**
```bash
# Instalación de Ollama (gratis)
curl -fsSL https://ollama.com/install.sh | sh

# Descargar modelo Llama 3.2 (3B - ligero)
ollama pull llama3.2:3b

# O modelo Mistral (mejor para SQL)
ollama pull mistral:7b
```

**B) Vanna.AI (Framework especializado)**
```python
# Instalación
pip install vanna

# Código básico
from vanna.ollama import Ollama
from vanna.chromadb import ChromaDB_VectorStore

class MyVanna(ChromaDB_VectorStore, Ollama):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        Ollama.__init__(self, config={'model': 'mistral:7b'})

vn = MyVanna(config={'model': 'mistral:7b'})

# Entrenar con el esquema de tu base de datos
vn.train(ddl="CREATE TABLE citas (...)")
vn.train(question="¿Cuántas citas hay hoy?", sql="SELECT COUNT(*) FROM citas WHERE fecha = GETDATE()")

# Usar el agente
sql = vn.generate_sql("Crea una cita para Juan el día 15 de enero")
```

**C) Conexión a SQL Server 2008**
```python
import pyodbc

# Conexión
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=tu_servidor;'
    'DATABASE=GesdenDB;'
    'UID=usuario;'
    'PWD=contraseña'
)

cursor = conn.cursor()
cursor.execute(sql)
conn.commit()
```

---

### 4.2 OPCIÓN 2: Solución de bajo coste (~5-10€/mes)

#### Componentes:
1. **LLM:** OpenAI GPT-4o-mini (API de pago, muy económico)
2. **Framework:** LangChain + SQL Database Toolkit
3. **Conexión a BD:** pyodbc
4. **Interfaz:** Streamlit o aplicación web personalizada

#### Ventajas:
- ✅ **Mayor precisión** en la comprensión del lenguaje
- ✅ **Más fácil de configurar**
- ✅ **Mejor manejo de contexto complejo**
- ✅ **No requiere hardware potente**

#### Desventajas:
- ❌ Coste mensual (pero muy bajo con GPT-4o-mini)
- ❌ Requiere conexión a internet
- ❌ Datos enviados a API externa (consideraciones de privacidad)

#### Código de ejemplo:

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_toolkits import SQLDatabaseToolkit

# Configurar conexión a BD
db = SQLDatabase.from_uri(
    "mssql+pyodbc://usuario:contraseña@servidor/GesdenDB?driver=SQL+Server"
)

# Configurar LLM (GPT-4o-mini es muy económico: ~$0.15/1M tokens)
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key="tu_api_key"
)

# Crear agente SQL
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type="openai-tools"
)

# Usar el agente
response = agent.invoke("Crea una cita para Manuel López el 19 de enero de 2026 a las 10:00")
print(response)
```

**Coste estimado de GPT-4o-mini:**
- Input: $0.150 / 1M tokens
- Output: $0.600 / 1M tokens
- **Uso típico:** ~5-10€/mes para uso moderado en una clínica

---

### 4.3 OPCIÓN 3: Solución híbrida (Recomendada)

Combina lo mejor de ambas opciones:

1. **Modelo local (Ollama + Mistral)** para tareas simples y repetitivas
2. **GPT-4o-mini** para casos complejos o cuando el modelo local falle
3. **Sistema de fallback automático**

```python
def procesar_comando(comando_usuario):
    # Intentar primero con modelo local
    try:
        resultado = agente_local.procesar(comando_usuario)
        if confianza(resultado) > 0.8:
            return resultado
    except Exception:
        pass
    
    # Si falla o baja confianza, usar GPT-4o-mini
    return agente_gpt.procesar(comando_usuario)
```

**Ventajas:**
- ✅ Coste mínimo (solo pagas cuando lo necesitas)
- ✅ Máxima fiabilidad
- ✅ Privacidad para casos simples

---

## 5. IMPLEMENTACIÓN PASO A PASO

### Fase 1: Análisis de la base de datos (1-2 días)

**Objetivo:** Entender la estructura de las tablas de Gesden

```sql
-- 1. Listar todas las tablas
SELECT TABLE_NAME 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_NAME;

-- 2. Ver estructura de una tabla específica
EXEC sp_columns 'nombre_tabla';

-- 3. Identificar tablas clave (buscar por nombre)
-- Probablemente existan tablas como:
-- - Pacientes / Clientes
-- - Citas / Agenda
-- - Tratamientos / Actos
-- - Odontograma
```

**Acción:** Documentar:
- Nombres de tablas relevantes
- Columnas y tipos de datos
- Relaciones entre tablas (claves foráneas)
- Ejemplos de datos

---

### Fase 2: Instalación del entorno (1 día)

#### Opción Gratuita (Ollama + Vanna):
```bash
# 1. Instalar Python 3.10+
python --version

# 2. Crear entorno virtual
python -m venv venv_gesden
source venv_gesden/bin/activate  # En Windows: venv_gesden\Scripts\activate

# 3. Instalar dependencias
pip install vanna
pip install pyodbc
pip install streamlit
pip install chromadb

# 4. Instalar Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama pull mistral:7b
```

#### Opción de Pago (OpenAI):
```bash
# 1-2. Igual que arriba

# 3. Instalar dependencias
pip install langchain-openai
pip install langchain-community
pip install pyodbc
pip install streamlit

# 4. Configurar API key de OpenAI
export OPENAI_API_KEY="sk-..."
```

---

### Fase 3: Desarrollo del agente (3-5 días)

#### Script básico con Vanna (gratuito):

```python
# agente_gesden.py
from vanna.ollama import Ollama
from vanna.chromadb import ChromaDB_VectorStore
import pyodbc

class AgenteGesden(ChromaDB_VectorStore, Ollama):
    def __init__(self):
        ChromaDB_VectorStore.__init__(self, config={'model': 'mistral:7b'})
        Ollama.__init__(self, config={'model': 'mistral:7b'})
        
        # Conexión a la base de datos
        self.conn = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=localhost;'  # Cambiar por tu servidor
            'DATABASE=GesdenDB;'  # Cambiar por tu BD
            'UID=usuario;'
            'PWD=contraseña'
        )
    
    def entrenar_con_esquema(self):
        """Entrena el agente con el esquema de la base de datos"""
        
        # Obtener todas las tablas y su estructura
        cursor = self.conn.cursor()
        
        # Entrenar con DDL de tablas importantes
        # EJEMPLO - Adaptar a tu esquema real:
        self.train(ddl="""
            CREATE TABLE Pacientes (
                id_paciente INT PRIMARY KEY,
                nombre VARCHAR(100),
                apellidos VARCHAR(100),
                telefono VARCHAR(20),
                email VARCHAR(100)
            )
        """)
        
        self.train(ddl="""
            CREATE TABLE Citas (
                id_cita INT PRIMARY KEY,
                id_paciente INT FOREIGN KEY REFERENCES Pacientes(id_paciente),
                fecha_cita DATETIME,
                duracion_minutos INT,
                id_doctor INT,
                estado VARCHAR(20),
                observaciones TEXT
            )
        """)
        
        # Entrenar con ejemplos de consultas
        self.train(
            question="¿Cuántas citas hay hoy?",
            sql="SELECT COUNT(*) FROM Citas WHERE CAST(fecha_cita AS DATE) = CAST(GETDATE() AS DATE)"
        )
        
        self.train(
            question="Lista todos los pacientes",
            sql="SELECT * FROM Pacientes ORDER BY apellidos, nombre"
        )
        
        self.train(
            question="Busca el paciente Juan García",
            sql="SELECT * FROM Pacientes WHERE nombre LIKE '%Juan%' AND apellidos LIKE '%García%'"
        )
    
    def procesar_comando(self, comando_natural):
        """Procesa un comando en lenguaje natural"""
        
        # Generar SQL
        sql_generado = self.generate_sql(comando_natural)
        print(f"\n🤖 SQL generado: {sql_generado}\n")
        
        # Pedir confirmación (seguridad)
        confirmacion = input("¿Ejecutar este SQL? (s/n): ")
        if confirmacion.lower() != 's':
            return "❌ Operación cancelada"
        
        # Ejecutar
        try:
            cursor = self.conn.cursor()
            
            # Detectar si es SELECT o INSERT/UPDATE/DELETE
            if sql_generado.strip().upper().startswith('SELECT'):
                cursor.execute(sql_generado)
                resultados = cursor.fetchall()
                return f"✅ Resultados: {resultados}"
            else:
                cursor.execute(sql_generado)
                self.conn.commit()
                return f"✅ Operación ejecutada correctamente"
        
        except Exception as e:
            self.conn.rollback()
            return f"❌ Error: {str(e)}"

# Uso
if __name__ == "__main__":
    agente = AgenteGesden()
    
    # Entrenar con el esquema (solo primera vez)
    agente.entrenar_con_esquema()
    
    # Interfaz de línea de comandos
    print("🦷 Agente Gesden AI iniciado")
    print("Escribe 'salir' para terminar\n")
    
    while True:
        comando = input("👤 Tú: ")
        if comando.lower() in ['salir', 'exit', 'quit']:
            break
        
        respuesta = agente.procesar_comando(comando)
        print(f"🤖 Agente: {respuesta}\n")
```

---

### Fase 4: Interfaz de usuario (2-3 días)

#### Opción A: Aplicación web con Streamlit

```python
# app_streamlit.py
import streamlit as st
from agente_gesden import AgenteGesden

st.title("🦷 Asistente AI para Gesden")

# Inicializar agente (solo una vez)
if 'agente' not in st.session_state:
    st.session_state.agente = AgenteGesden()
    st.session_state.agente.entrenar_con_esquema()

# Chat interface
comando = st.text_input("¿Qué necesitas hacer?", 
                       placeholder="Ej: Crea una cita para María el lunes a las 10:00")

if st.button("Ejecutar"):
    if comando:
        with st.spinner("Procesando..."):
            resultado = st.session_state.agente.procesar_comando(comando)
            st.success(resultado)

# Historial
if 'historial' not in st.session_state:
    st.session_state.historial = []

st.sidebar.title("Historial")
for item in st.session_state.historial:
    st.sidebar.text(item)
```

Ejecutar con: `streamlit run app_streamlit.py`

---

#### Opción B: Bot de Telegram (para uso móvil)

```python
# bot_telegram.py
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from agente_gesden import AgenteGesden

agente = AgenteGesden()
agente.entrenar_con_esquema()

async def procesar_mensaje(update: Update, context):
    comando = update.message.text
    resultado = agente.procesar_comando(comando)
    await update.message.reply_text(resultado)

def main():
    app = Application.builder().token("TU_TOKEN_DE_TELEGRAM").build()
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, procesar_mensaje))
    
    print("🤖 Bot iniciado")
    app.run_polling()

if __name__ == '__main__':
    main()
```

---

## 6. CASOS DE USO IMPLEMENTADOS

### Ejemplo 1: Crear una cita

**Usuario:** "Crea una cita para Manuel López el día 19 de enero de 2026 a las 10:00"

**Proceso del agente:**
1. Extraer información:
   - Paciente: "Manuel López"
   - Fecha: "2026-01-19"
   - Hora: "10:00"
   
2. Buscar ID del paciente:
   ```sql
   SELECT id_paciente FROM Pacientes 
   WHERE nombre LIKE '%Manuel%' AND apellidos LIKE '%López%'
   ```

3. Insertar cita:
   ```sql
   INSERT INTO Citas (id_paciente, fecha_cita, duracion_minutos, estado)
   VALUES (123, '2026-01-19 10:00:00', 30, 'Pendiente')
   ```

---

### Ejemplo 2: Crear acto clínico

**Usuario:** "Crea acto clínico con reconstrucción de la pieza 26"

**SQL generado:**
```sql
-- Asumiendo que existe una tabla ActosClinicns o Tratamientos
INSERT INTO ActosClinicns (id_paciente, id_cita, tipo_tratamiento, pieza_dental, descripcion, fecha)
VALUES (
    [id_paciente_actual],
    [id_cita_actual],
    'Reconstrucción',
    '26',
    'Reconstrucción de pieza dental 26',
    GETDATE()
)
```

---

### Ejemplo 3: Eliminar cita

**Usuario:** "Elimina la cita del día 1 de diciembre"

**SQL generado:**
```sql
DELETE FROM Citas 
WHERE CAST(fecha_cita AS DATE) = '2024-12-01'
AND id_cita = [verificar cual]
```

**⚠️ Nota de seguridad:** El agente debe pedir confirmación antes de ejecutar DELETE

---

## 7. CONSIDERACIONES IMPORTANTES

### 7.1 Seguridad

**CRÍTICO - Implementar estas medidas:**

1. **Usuario de base de datos con permisos limitados**
   ```sql
   -- Crear usuario específico para el agente
   CREATE LOGIN agente_gesden WITH PASSWORD = 'contraseña_segura';
   CREATE USER agente_gesden FOR LOGIN agente_gesden;
   
   -- Dar solo permisos necesarios (NO dar permiso de DROP o ALTER)
   GRANT SELECT, INSERT, UPDATE ON Citas TO agente_gesden;
   GRANT SELECT ON Pacientes TO agente_gesden;
   ```

2. **Validación de SQL antes de ejecutar**
   ```python
   def es_sql_seguro(sql):
       # Prohibir comandos peligrosos
       prohibidos = ['DROP', 'TRUNCATE', 'ALTER', 'EXEC', 'EXECUTE']
       sql_upper = sql.upper()
       for palabra in prohibidos:
           if palabra in sql_upper:
               return False
       return True
   ```

3. **Confirmación manual para operaciones destructivas**
   - Cualquier DELETE debe pedir confirmación
   - Mostrar siempre el SQL antes de ejecutar
   - Límite de filas afectadas

4. **Logs de auditoría**
   ```python
   import logging
   
   logging.basicConfig(
       filename='agente_gesden.log',
       level=logging.INFO,
       format='%(asctime)s - %(message)s'
   )
   
   logging.info(f"Usuario: {usuario} | Comando: {comando} | SQL: {sql}")
   ```

---

### 7.2 Privacidad y RGPD

**Consideraciones legales:**

1. **Si usas modelo local (Ollama):**
   - ✅ Los datos nunca salen del servidor
   - ✅ Cumple 100% con RGPD
   - ✅ No hay terceros procesando datos

2. **Si usas API externa (OpenAI):**
   - ⚠️ Los comandos se envían a OpenAI
   - ⚠️ **NO enviar datos personales directamente en el prompt**
   - ✅ Usar solo para generar SQL, no enviar nombres de pacientes
   
   **Solución:** Anonimizar en el prompt
   ```python
   # MAL - Envía datos personales
   prompt = "Crea cita para Manuel López DNI 12345678A"
   
   # BIEN - Usa IDs internos
   id_paciente = buscar_paciente_localmente("Manuel López")
   prompt = f"Genera SQL para insertar cita para paciente ID {id_paciente}"
   ```

3. **Consentimiento informado:**
   - Informar al personal que usa IA
   - Documento de política de uso
   - Formación en uso responsable

---

### 7.3 Integración con Gesden

**⚠️ ADVERTENCIA IMPORTANTE:**

Modificar directamente la base de datos de Gesden puede:
- Romper integridad referencial
- Causar inconsistencias en la aplicación
- Invalidar el soporte técnico de Infomed

**Recomendaciones:**

1. **Realizar backups antes de cualquier operación**
   ```sql
   BACKUP DATABASE GesdenDB 
   TO DISK = 'C:\Backups\GesdenDB_antes_agente.bak'
   WITH FORMAT, INIT, SKIP, NOREWIND, NOUNLOAD;
   ```

2. **Modo de solo lectura inicialmente**
   - Empezar solo con SELECTs
   - Validar que las consultas son correctas
   - Progresivamente añadir INSERT/UPDATE

3. **Entorno de prueba**
   - Crear copia de la BD para testing
   - Probar todas las operaciones en copia
   - Validar con Gesden que los datos se ven correctamente

4. **Contactar con Infomed**
   - Preguntar si tienen API o método recomendado
   - Verificar si invalida garantía
   - Solicitar documentación del esquema de BD

---

## 8. HOJA DE RUTA DE IMPLEMENTACIÓN

### Semana 1: Análisis y preparación
- [ ] Día 1-2: Analizar estructura de BD de Gesden
- [ ] Día 3: Documentar tablas y relaciones clave
- [ ] Día 4: Crear copia de seguridad y BD de prueba
- [ ] Día 5: Decidir entre opción gratuita o de pago

### Semana 2: Desarrollo
- [ ] Día 1: Instalar entorno (Python, Ollama/OpenAI)
- [ ] Día 2: Desarrollar conexión a BD
- [ ] Día 3: Implementar generación de SQL básica
- [ ] Día 4: Añadir validaciones de seguridad
- [ ] Día 5: Pruebas con comandos simples (SELECT)

### Semana 3: Ampliación
- [ ] Día 1-2: Implementar operaciones INSERT
- [ ] Día 3-4: Implementar UPDATE y DELETE con confirmación
- [ ] Día 5: Desarrollo de interfaz (Streamlit/Telegram)

### Semana 4: Testing y ajuste
- [ ] Día 1-3: Pruebas exhaustivas en BD de test
- [ ] Día 4: Validar con Gesden que todo funciona
- [ ] Día 5: Deployment en producción (modo lectura primero)

---

## 9. COSTES DETALLADOS

### Opción 1: 100% Gratuita (Ollama + Vanna)

| Concepto | Coste |
|----------|-------|
| Ollama (LLM local) | €0 |
| Vanna.AI framework | €0 |
| Python + librerías | €0 |
| Streamlit (self-hosted) | €0 |
| **TOTAL MENSUAL** | **€0** |

**Coste de hardware:**
- Servidor/PC con mínimo 16GB RAM (ya lo tienes)
- Almacenamiento: +5GB para modelo

---

### Opción 2: OpenAI GPT-4o-mini

| Concepto | Coste mensual |
|----------|---------------|
| API OpenAI GPT-4o-mini | €5-10 (uso moderado) |
| Python + librerías | €0 |
| Streamlit (self-hosted) | €0 |
| **TOTAL MENSUAL** | **€5-10** |

**Estimación de uso para 1 clínica:**
- 50 comandos/día = 1,500 comandos/mes
- ~1,000 tokens por comando = 1.5M tokens/mes
- Coste: ~€2.25/mes de input + ~€0 output (respuestas cortas)
- **Total real: ~€3-5/mes**

---

### Opción 3: Híbrida (Recomendada)

| Concepto | Coste mensual |
|----------|---------------|
| Ollama (80% de casos) | €0 |
| OpenAI fallback (20%) | €1-2 |
| **TOTAL MENSUAL** | **€1-2** |

---

## 10. ALTERNATIVAS COMERCIALES

Si prefieres una solución "llave en mano":

### Chat2DB (Freemium)
- ✅ Interfaz gráfica profesional
- ✅ Text-to-SQL integrado
- ✅ Compatible con SQL Server
- 💰 Plan gratuito disponible
- 💰 Plan Pro: ~$10/mes

### AI2SQL
- ✅ Especializado en generación de SQL
- 💰 ~$20/mes

**Recomendación:** Estas opciones son buenas para empezar, pero NO son agentes completos (solo generan SQL, no ejecutan ni tienen contexto de Gesden).

---

## 11. EJEMPLO DE CÓDIGO COMPLETO

```python
"""
Agente AI para Gesden G5.29
Versión: 1.0
Autor: [Tu nombre]
Descripción: Agente que procesa comandos en lenguaje natural 
             y los ejecuta en la base de datos de Gesden
"""

import pyodbc
import logging
from datetime import datetime
from typing import Optional, Dict, Any
import re

# Configuración de logging
logging.basicConfig(
    filename='agente_gesden.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ConfiguracionGesden:
    """Configuración de conexión a Gesden"""
    
    SERVIDOR = "localhost"  # Cambiar por tu servidor
    BASE_DATOS = "GesdenDB"  # Cambiar por tu BD
    USUARIO = "agente_gesden"
    CONTRASEÑA = "tu_contraseña_segura"
    
    DRIVER = "SQL Server"
    
    @classmethod
    def get_connection_string(cls):
        return (
            f'DRIVER={{{cls.DRIVER}}};'
            f'SERVER={cls.SERVIDOR};'
            f'DATABASE={cls.BASE_DATOS};'
            f'UID={cls.USUARIO};'
            f'PWD={cls.CONTRASEÑA}'
        )

class ValidadorSQL:
    """Validaciones de seguridad para SQL"""
    
    COMANDOS_PROHIBIDOS = [
        'DROP', 'TRUNCATE', 'ALTER', 'EXEC', 'EXECUTE',
        'sp_', 'xp_', 'GRANT', 'REVOKE', 'DENY'
    ]
    
    @staticmethod
    def es_seguro(sql: str) -> tuple[bool, str]:
        """
        Valida si un SQL es seguro para ejecutar
        Returns: (es_seguro: bool, mensaje: str)
        """
        sql_upper = sql.upper()
        
        # Verificar comandos prohibidos
        for cmd in ValidadorSQL.COMANDOS_PROHIBIDOS:
            if cmd in sql_upper:
                return False, f"Comando prohibido detectado: {cmd}"
        
        # Verificar SQL injection básico
        patrones_sospechosos = [
            r'--',  # Comentarios SQL
            r'/\*',  # Comentarios multilínea
            r'\bOR\s+1\s*=\s*1',  # OR 1=1
            r'\bAND\s+1\s*=\s*1',  # AND 1=1
        ]
        
        for patron in patrones_sospechosos:
            if re.search(patron, sql_upper):
                return False, f"Patrón sospechoso detectado"
        
        return True, "SQL validado"

class ConexionGesden:
    """Maneja la conexión a la base de datos de Gesden"""
    
    def __init__(self):
        self.conn: Optional[pyodbc.Connection] = None
        self.conectar()
    
    def conectar(self):
        """Establece conexión con la base de datos"""
        try:
            self.conn = pyodbc.connect(
                ConfiguracionGesden.get_connection_string()
            )
            logging.info("Conexión establecida con Gesden")
        except Exception as e:
            logging.error(f"Error al conectar: {str(e)}")
            raise
    
    def ejecutar_query(self, sql: str, es_modificacion: bool = False) -> Any:
        """
        Ejecuta una query SQL
        
        Args:
            sql: Query SQL a ejecutar
            es_modificacion: True si es INSERT/UPDATE/DELETE
        
        Returns:
            Resultados de la query o número de filas afectadas
        """
        # Validar seguridad
        es_seguro, mensaje = ValidadorSQL.es_seguro(sql)
        if not es_seguro:
            raise SecurityError(f"SQL no seguro: {mensaje}")
        
        try:
            cursor = self.conn.cursor()
            
            logging.info(f"Ejecutando SQL: {sql}")
            cursor.execute(sql)
            
            if es_modificacion:
                self.conn.commit()
                filas_afectadas = cursor.rowcount
                logging.info(f"Filas afectadas: {filas_afectadas}")
                return filas_afectadas
            else:
                resultados = cursor.fetchall()
                logging.info(f"Resultados obtenidos: {len(resultados)} filas")
                return resultados
        
        except Exception as e:
            if es_modificacion:
                self.conn.rollback()
            logging.error(f"Error al ejecutar SQL: {str(e)}")
            raise
    
    def cerrar(self):
        """Cierra la conexión"""
        if self.conn:
            self.conn.close()
            logging.info("Conexión cerrada")

class AgenteGesdenAI:
    """
    Agente AI principal para Gesden
    Procesa comandos en lenguaje natural
    """
    
    def __init__(self):
        self.db = ConexionGesden()
        self.historial = []
        
        # Aquí iría la inicialización del LLM
        # Por ahora, usaremos reglas simples como ejemplo
    
    def procesar_comando(self, comando: str) -> Dict[str, Any]:
        """
        Procesa un comando en lenguaje natural
        
        Args:
            comando: Texto del usuario
        
        Returns:
            Diccionario con resultado
        """
        comando = comando.lower().strip()
        
        # Registrar en historial
        self.historial.append({
            'timestamp': datetime.now(),
            'comando': comando,
            'usuario': 'admin'  # Aquí iría el usuario real
        })
        
        # Detectar tipo de operación (versión simplificada)
        if 'listar' in comando or 'mostrar' in comando or 'ver' in comando:
            return self._listar_datos(comando)
        
        elif 'crear' in comando and 'cita' in comando:
            return self._crear_cita(comando)
        
        elif 'eliminar' in comando or 'borrar' in comando:
            return self._eliminar_datos(comando)
        
        else:
            return {
                'exito': False,
                'mensaje': 'No entiendo el comando. Intenta reformularlo.'
            }
    
    def _listar_datos(self, comando: str) -> Dict[str, Any]:
        """Maneja comandos de listado"""
        
        # Ejemplo simple - en producción usarías el LLM
        if 'pacientes' in comando:
            sql = "SELECT TOP 10 * FROM Pacientes ORDER BY apellidos"
        elif 'citas' in comando:
            if 'hoy' in comando:
                sql = """
                    SELECT * FROM Citas 
                    WHERE CAST(fecha_cita AS DATE) = CAST(GETDATE() AS DATE)
                    ORDER BY fecha_cita
                """
            else:
                sql = "SELECT TOP 10 * FROM Citas ORDER BY fecha_cita DESC"
        else:
            return {
                'exito': False,
                'mensaje': 'No sé qué listar. Especifica pacientes, citas, etc.'
            }
        
        try:
            resultados = self.db.ejecutar_query(sql)
            return {
                'exito': True,
                'datos': resultados,
                'sql_ejecutado': sql
            }
        except Exception as e:
            return {
                'exito': False,
                'mensaje': f'Error: {str(e)}'
            }
    
    def _crear_cita(self, comando: str) -> Dict[str, Any]:
        """Maneja creación de citas"""
        
        # Aquí necesitarías el LLM para extraer:
        # - Nombre del paciente
        # - Fecha y hora
        # - Duración
        # - Doctor
        
        # Por ahora, ejemplo hardcodeado
        return {
            'exito': False,
            'mensaje': 'Creación de citas aún no implementada. Requiere integración con LLM.'
        }
    
    def _eliminar_datos(self, comando: str) -> Dict[str, Any]:
        """Maneja eliminación de datos"""
        
        # SIEMPRE pedir confirmación para deletes
        return {
            'exito': False,
            'mensaje': 'Eliminación requiere confirmación adicional',
            'requiere_confirmacion': True
        }

# Uso del agente
if __name__ == "__main__":
    print("🦷 Agente Gesden AI - Versión 1.0")
    print("=" * 50)
    
    agente = AgenteGesdenAI()
    
    print("\nEjemplos de comandos:")
    print("- Listar pacientes")
    print("- Mostrar citas de hoy")
    print("- Ver todas las citas")
    print("\nEscribe 'salir' para terminar\n")
    
    while True:
        try:
            comando = input("👤 Tú: ").strip()
            
            if comando.lower() in ['salir', 'exit', 'quit']:
                print("👋 ¡Hasta luego!")
                break
            
            if not comando:
                continue
            
            print("\n⚙️  Procesando...\n")
            resultado = agente.procesar_comando(comando)
            
            if resultado['exito']:
                print(f"✅ {resultado.get('mensaje', 'Operación exitosa')}")
                
                if 'datos' in resultado:
                    print(f"\n📊 Resultados ({len(resultado['datos'])} filas):")
                    for fila in resultado['datos'][:5]:  # Mostrar solo 5 primeras
                        print(f"   {fila}")
                    
                    if len(resultado['datos']) > 5:
                        print(f"   ... y {len(resultado['datos']) - 5} más")
                
                if 'sql_ejecutado' in resultado:
                    print(f"\n💡 SQL: {resultado['sql_ejecutado']}")
            else:
                print(f"❌ {resultado['mensaje']}")
            
            print()
        
        except KeyboardInterrupt:
            print("\n\n👋 Interrumpido por el usuario")
            break
        except Exception as e:
            print(f"\n❌ Error inesperado: {str(e)}")
            logging.error(f"Error inesperado: {str(e)}", exc_info=True)
    
    # Cerrar conexión
    agente.db.cerrar()

class SecurityError(Exception):
    """Excepción para errores de seguridad"""
    pass
```

---

## 12. PRÓXIMOS PASOS RECOMENDADOS

1. **Esta semana:**
   - [ ] Analiza tu base de datos de Gesden
   - [ ] Documenta las tablas principales
   - [ ] Decide qué opción (gratuita/pago) prefieres

2. **Próxima semana:**
   - [ ] Instala el entorno de desarrollo
   - [ ] Crea una BD de prueba (copia de Gesden)
   - [ ] Implementa conexión básica

3. **En dos semanas:**
   - [ ] Integra el LLM elegido
   - [ ] Prueba con comandos simples
   - [ ] Valida resultados

---

## 13. RECURSOS ADICIONALES

### Documentación técnica:
- **Vanna.AI:** https://vanna.ai/docs/
- **LangChain SQL:** https://python.langchain.com/docs/use_cases/sql/
- **Ollama:** https://ollama.com/
- **pyodbc:** https://github.com/mkleehammer/pyodbc

### Tutoriales:
- Text-to-SQL con Python: https://github.com/vanna-ai/vanna
- SQL Server + Python: Búsqueda "pyodbc SQL Server tutorial"

### Comunidades de ayuda:
- Discord de Vanna: https://discord.gg/qUZYKHremx
- Stack Overflow (tag: python-3.x, sql-server, nlp)

---

## 14. CONCLUSIONES

**¿Es viable?** ✅ **SÍ, totalmente viable**

**¿Es seguro?** ⚠️ Con las precauciones adecuadas, sí

**¿Vale la pena?** ✅ Sí, puede ahorrar tiempo significativo

**Mejor opción:** 
- **Para empezar:** Opción gratuita (Ollama + Vanna)
- **Para producción:** Opción híbrida (local + GPT-4o-mini fallback)
- **Coste total:** 0-5€/mes

**Tiempo de implementación:** 2-4 semanas para versión funcional

**Riesgo:** Medio-Bajo (con backups y validaciones adecuadas)

---

## 15. CONTACTO Y SOPORTE

Si necesitas ayuda durante la implementación:

1. **Foros de la comunidad:**
   - Reddit: r/MachineLearning, r/Python
   - Discord de Vanna.AI

2. **Consultoría profesional:**
   - Puedes contratar un desarrollador para acortar tiempos
   - Coste estimado: 1,000-3,000€ para implementación completa

3. **Formación:**
   - Curso de LangChain: https://www.deeplearning.ai/short-courses/
   - Tutorial de Text-to-SQL en YouTube

---

**Creado:** $(date)
**Versión:** 1.0
**Licencia:** Libre para uso personal

---

## ¿Necesitas más detalles sobre alguna sección específica?

Puedo profundizar en:
- Código específico para tu caso
- Análisis de costes más detallado
- Tutoriales paso a paso
- Solución de problemas comunes
- Integración con otras herramientas
