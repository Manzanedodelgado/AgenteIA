"""
=====================================================
AGENTE GESDEN IA - API SERVER
Acceso remoto vía Ngrok Tunnel
=====================================================

Este servidor corre en tu PC de la clínica
y es accesible desde internet via Ngrok.

Base de datos: LOCAL (SQL Server GELITE)
Acceso: Desde cualquier sitio via Ngrok tunnel
IA: Claude API
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import pymssql
import os
from datetime import datetime, timedelta
import logging
import secrets
import secrets
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage

# =====================================================
# CONFIGURACIÓN
# =====================================================

class Config:
    """Configuración del servidor"""
    
    # SQL Server REMOTO (Vía Ngrok)
    SQL_SERVER = "5.tcp.eu.ngrok.io"
    SQL_PORT = 19317
    SQL_DATABASE = "GELITE"
    SQL_USER = "RUBIOGARCIADENTAL"
    SQL_PASSWORD = "666666"
    
    ID_CENTRO = 2
    
    # Ollama Configuration
    OLLAMA_BASE_URL = "http://localhost:11434"
    OLLAMA_MODEL = "llama3.2" # Modelo mucho más rápido (3B params)
    
    # Seguridad
    SECRET_KEY = secrets.token_hex(16)
    
    @classmethod
    def get_db_connection(cls):
        return pymssql.connect(
            server=cls.SQL_SERVER,
            port=cls.SQL_PORT,
            user=cls.SQL_USER,
            password=cls.SQL_PASSWORD,
            database=cls.SQL_DATABASE,
            as_dict=True
        )

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_server.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# =====================================================
# INICIALIZAR FLASK
# =====================================================

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = Config.SECRET_KEY

# CORS RESTRINGIDO - Solo localhost y ngrok
ALLOWED_ORIGINS = [
    'http://localhost:5000',
    'http://127.0.0.1:5000',
    'https://*.ngrok-free.app',
    'https://*.ngrok.io',
]
CORS(app, origins=ALLOWED_ORIGINS, supports_credentials=True)

# Cliente Ollama
try:
    llm = ChatOllama(
        model=Config.OLLAMA_MODEL,
        temperature=0,
        base_url=Config.OLLAMA_BASE_URL
    )
    logging.info(f"✅ Ollama configurado: {Config.OLLAMA_MODEL}")
except Exception as e:
    llm = None
    logging.error(f"❌ Error configurando Ollama: {e}")

# =====================================================
# UTILIDADES BASE DE DATOS
# =====================================================

class GesdenDB:
    """Manejador de base de datos Gesden"""
    
    @staticmethod
    def ejecutar_query(sql, params=None):
        """Ejecuta query SELECT y retorna resultados"""
        try:
            conn = Config.get_db_connection()
            cursor = conn.cursor(as_dict=True)
            
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            
            results = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return results
        
        except Exception as e:
            logging.error(f"Error en query: {e}")
            raise
    
    @staticmethod
    def ejecutar_insert(sql, params):
        """Ejecuta INSERT y retorna ID generado"""
        try:
            conn = Config.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(sql, params)
            conn.commit()
            
            cursor.execute("SELECT @@IDENTITY AS id")
            row = cursor.fetchone()
            id_generado = row['id'] if row else 0
            
            cursor.close()
            conn.close()
            
            return int(id_generado)
        
        except Exception as e:
            logging.error(f"Error en insert: {e}")
            raise
    
    @staticmethod
    def fecha_gesden_a_iso(fecha_int):
        """Convierte fecha Gesden a ISO"""
        if not fecha_int:
            return None
        base_date = datetime(1899, 12, 30)
        fecha = base_date + timedelta(days=fecha_int)
        return fecha.strftime('%Y-%m-%d')
    
    @staticmethod
    def fecha_iso_a_gesden(fecha_iso):
        """Convierte fecha ISO a Gesden"""
        fecha = datetime.strptime(fecha_iso, '%Y-%m-%d')
        base_date = datetime(1899, 12, 30)
        return (fecha - base_date).days
    
    @staticmethod
    def hora_gesden_a_string(hora_int):
        """Convierte hora Gesden a HH:MM"""
        if not hora_int:
            return "00:00"
        horas = hora_int // 10000
        minutos = (hora_int % 10000) // 100
        return f"{horas:02d}:{minutos:02d}"
    
    @staticmethod
    def hora_string_a_gesden(hora_str):
        """Convierte HH:MM a formato Gesden"""
        partes = hora_str.split(':')
        return (int(partes[0]) * 10000) + (int(partes[1]) * 100)

# =====================================================
# MOTOR IA CON CLAUDE
# =====================================================

# =====================================================
# HERRAMIENTAS LANGCHAIN
# =====================================================

@tool
def buscar_paciente_db(busqueda: str) -> dict:
    """Busca pacientes en la base de datos por nombre, apellidos o número de paciente.
    Args:
        busqueda: El nombre, apellido o número del paciente a buscar.
    """
    return ejecutar_buscar_paciente(busqueda)

@tool
def listar_citas_db(fecha: str) -> dict:
    """Lista las citas médicas de una fecha específica.
    Args:
        fecha: La fecha a consultar. Puede ser 'hoy', 'mañana' o una fecha en formato 'YYYY-MM-DD'.
    """
    return ejecutar_listar_citas(fecha)

@tool
def crear_cita_db(id_paciente: int, fecha: str, hora: str, motivo: str = "") -> dict:
    """Crea una nueva cita médica en la agenda.
    Args:
        id_paciente: El ID único del paciente (IdPac).
        fecha: La fecha de la cita en formato 'YYYY-MM-DD'.
        hora: La hora de la cita en formato 'HH:MM'.
        motivo: (Opcional) El motivo o descripción de la cita.
    """
    return ejecutar_crear_cita(id_paciente, fecha, hora, motivo)

# Lista de herramientas disponibles para el modelo
tools = [buscar_paciente_db, listar_citas_db, crear_cita_db]

# =====================================================
# MOTOR IA CON LANGCHAIN + OLLAMA
# =====================================================

def procesar_con_ia(comando):
    """Procesa comando con Ollama usando LangChain y Tools"""
    
    if not llm:
        return {"accion": "error", "mensaje": "⚠️ Ollama no configurado"}
    
    try:
        # Vincular herramientas al modelo
        llm_with_tools = llm.bind_tools(tools)
        
        # Contexto del sistema
        system_msg = f"""Eres Rubito, asistente virtual de Rubio Garcia Dental.
Fecha actual: {datetime.now().strftime('%d/%m/%Y %A')}

Instrucciones:
1. Eres un asistente útil y amable.
2. Tienes acceso a la base de datos de la clínica mediante herramientas.
3. Cuando el usuario pida crear una cita:
    a. Busca primero al paciente por nombre para obtener su ID.
    b. Si encuentras al paciente, usa su ID para crear la cita.
    c. Calcula las fechas automáticamente (ej: "próximo lunes").
    d. Confirma la acción al usuario.
4. Si te preguntan algo que requiere datos, USA LAS HERRAMIENTAS.
"""

        # Invocar al modelo
        messages = [
            SystemMessage(content=system_msg),
            HumanMessage(content=comando)
        ]
        
        logging.info(f"📤 Enviando a Ollama: {comando}")
        response = llm_with_tools.invoke(messages)
        logging.info(f"📥 Respuesta Ollama (Raw): {response}")
        
        # Procesar llamadas a herramientas (Tool Calls)
        if response.tool_calls:
            messages.append(response) # Añadir respuesta del asistente con tool_calls
            
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"].lower()
                tool_args = tool_call["args"]
                
                logging.info(f"🛠️ Ejecutando herramienta: {tool_name} con args: {tool_args}")
                
                tool_result = None
                if tool_name == "buscar_paciente_db":
                    tool_result = buscar_paciente_db.invoke(tool_args)
                elif tool_name == "listar_citas_db":
                    tool_result = listar_citas_db.invoke(tool_args)
                elif tool_name == "crear_cita_db":
                    tool_result = crear_cita_db.invoke(tool_args)
                
                logging.info(f"✅ Resultado herramienta: {str(tool_result)[:100]}...")
                
                # Añadir resultado de la herramienta
                from langchain_core.messages import ToolMessage
                messages.append(ToolMessage(tool_call_id=tool_call["id"], content=str(tool_result)))
            
            # Invocar de nuevo para obtener respuesta final
            final_response = llm_with_tools.invoke(messages)
            logging.info(f"📥 Respuesta Final: {final_response.content}")
            
            return {
                "accion": "respuesta_tool",
                "mensaje": final_response.content
            }
        
        return {
            "accion": "respuesta_libre",
            "mensaje": response.content
        }
    
    except Exception as e:
        logging.error(f"Error Ollama: {e}")
        return {"accion": "error", "mensaje": f"Error procesando con IA: {str(e)}"}


# Funciones ejecutoras de herramientas
def ejecutar_buscar_paciente(busqueda):
    """Ejecuta búsqueda de paciente"""
    try:
        import re
        busqueda = re.sub(r'[;\'"\\]', '', busqueda).strip()
        
        if busqueda.isdigit():
            sql = """
                SELECT TOP 20 IdPac, NumPac, Nombre, Apellidos, TelMovil, Email, FecNacim
                FROM Pacientes
                WHERE NumPac = %s AND IdCentro = %s
            """
            params = (int(busqueda), Config.ID_CENTRO)
        else:
            sql = """
                SELECT TOP 20 IdPac, NumPac, Nombre, Apellidos, TelMovil, Email, FecNacim
                FROM Pacientes
                WHERE (Nombre LIKE %s OR Apellidos LIKE %s) AND IdCentro = %s
                ORDER BY Apellidos, Nombre
            """
            params = (f'%{busqueda}%', f'%{busqueda}%', Config.ID_CENTRO)
        
        pacientes = GesdenDB.ejecutar_query(sql, params)
        
        for p in pacientes:
            if p.get('FecNacim'):
                try:
                    p['FecNacim'] = GesdenDB.fecha_gesden_a_iso(p['FecNacim'])
                except:
                    p['FecNacim'] = None
        
        return {"pacientes": pacientes, "total": len(pacientes)}
    except Exception as e:
        return {"error": str(e)}


def ejecutar_listar_citas(fecha_str):
    """Ejecuta listado de citas"""
    try:
        if fecha_str == 'hoy':
            fecha = datetime.now()
        elif fecha_str == 'mañana':
            fecha = datetime.now() + timedelta(days=1)
        else:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
        
        fecha_gesden = GesdenDB.fecha_iso_a_gesden(fecha.strftime('%Y-%m-%d'))
        
        sql = """
            SELECT c.IdCita, c.Fecha, c.Hora, c.Duracion, c.Texto,
                   p.NumPac, p.Nombre, p.Apellidos, p.TelMovil
            FROM DCitas c
            LEFT JOIN Pacientes p ON c.IdPac = p.IdPac
            WHERE c.Fecha = %s AND c.IdCentro = %s
            ORDER BY c.Hora
        """
        
        citas = GesdenDB.ejecutar_query(sql, (fecha_gesden, Config.ID_CENTRO))
        
        for cita in citas:
            if cita.get('Fecha'):
                cita['Fecha'] = GesdenDB.fecha_gesden_a_iso(cita['Fecha'])
            if cita.get('Hora'):
                cita['HoraFormato'] = GesdenDB.hora_gesden_a_string(cita['Hora'])
        
        return {"citas": citas, "fecha": fecha.strftime('%Y-%m-%d'), "total": len(citas)}
    except Exception as e:
        return {"error": str(e)}


def ejecutar_crear_cita(id_pac, fecha_iso, hora_str, texto=""):
    """Ejecuta creación de cita"""
    try:
        fecha_gesden = GesdenDB.fecha_iso_a_gesden(fecha_iso)
        hora_gesden = GesdenDB.hora_string_a_gesden(hora_str)
        
        sql_orden = "SELECT ISNULL(MAX(IdOrden), 0) + 1 AS siguiente FROM DCitas WHERE Fecha = %s"
        resultado = GesdenDB.ejecutar_query(sql_orden, (fecha_gesden,))
        id_orden = resultado[0]['siguiente'] if resultado else 1
        
        sql = """
            INSERT INTO DCitas (IdPac, Fecha, Hora, Duracion, Texto, IdOrden, IdCentro)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        id_cita = GesdenDB.ejecutar_insert(sql, (
            id_pac,
            fecha_gesden,
            hora_gesden,
            30,  # 30 minutos por defecto
            texto,
            id_orden,
            Config.ID_CENTRO
        ))
        
        return {
            "success": True,
            "id_cita": id_cita,
            "fecha": fecha_iso,
            "hora": hora_str,
            "paciente_id": id_pac
        }
    except Exception as e:
        return {"error": str(e)}

# =====================================================
# RUTAS WEB - INTERFAZ
# =====================================================

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check para Cloudflare"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'database': 'connected'
    })

@app.route('/api/estado')
def estado():
    """Estado del sistema - Health check extendido"""
    try:
        # Verificar conexión BD
        conn = Config.get_db_connection()
        conn.close()
        bd_status = "conectada"
    except:
        bd_status = "desconectada"
    
    # Verificar MiniMax
    minimax_status = "configurada" if minimax_client else "no configurada"
    
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'base_datos': bd_status,
        'minimax_api': minimax_status,
        'version': '5.0-minimax'
    })

# =====================================================
# API - PACIENTES
# =====================================================

@app.route('/api/pacientes/buscar', methods=['POST'])
def buscar_pacientes():
    """Buscar pacientes"""
    try:
        data = request.json
        busqueda = data.get('busqueda', '').strip()
        
        # SANITIZACIÓN: Limitar longitud y caracteres peligrosos
        if len(busqueda) > 100:
            return jsonify({
                'success': False,
                'error': 'Búsqueda demasiado larga (máx 100 caracteres)'
            }), 400
        
        # Remover caracteres peligrosos
        import re
        busqueda = re.sub(r'[;\'"\\]', '', busqueda)
        
        if not busqueda:
            return jsonify({
                'success': True,
                'pacientes': []
            })
        
        # Si es número, buscar por NumPac
        if busqueda.isdigit():
            sql = """
                SELECT TOP 20 IdPac, NumPac, Nombre, Apellidos, TelMovil, Email, FecNacim
                FROM Pacientes
                WHERE NumPac = %s AND IdCentro = %s
            """
            params = (int(busqueda), Config.ID_CENTRO)
        else:
            # Buscar por nombre/apellidos
            sql = """
                SELECT TOP 20 IdPac, NumPac, Nombre, Apellidos, TelMovil, Email, FecNacim
                FROM Pacientes
                WHERE (Nombre LIKE %s OR Apellidos LIKE %s) AND IdCentro = %s
                ORDER BY Apellidos, Nombre
            """
            params = (f'%{busqueda}%', f'%{busqueda}%', Config.ID_CENTRO)
        
        pacientes = GesdenDB.ejecutar_query(sql, params)
        
        # Convertir fechas con manejo de errores
        for p in pacientes:
            if p.get('FecNacim'):
                try:
                    p['FecNacim'] = GesdenDB.fecha_gesden_a_iso(p['FecNacim'])
                except:
                    p['FecNacim'] = None  # Si falla, poner null
        
        logging.info(f"Búsqueda pacientes: [REDACTED] - {len(pacientes)} resultados")
        
        return jsonify({
            'success': True,
            'pacientes': pacientes
        })
    
    except Exception as e:
        logging.error(f"Error buscando pacientes: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# =====================================================
# API - CITAS
# =====================================================

@app.route('/api/citas/listar', methods=['POST'])
def listar_citas():
    """Listar citas de una fecha"""
    try:
        data = request.json
        fecha_str = data.get('fecha', 'hoy')
        
        # Parsear fecha
        if fecha_str == 'hoy':
            fecha = datetime.now()
        elif fecha_str == 'mañana':
            fecha = datetime.now() + timedelta(days=1)
        else:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
        
        fecha_gesden = GesdenDB.fecha_iso_a_gesden(fecha.strftime('%Y-%m-%d'))
        
        sql = """
            SELECT c.IdCita, c.Fecha, c.Hora, c.Duracion, c.Texto,
                   p.NumPac, p.Nombre, p.Apellidos, p.TelMovil
            FROM DCitas c
            LEFT JOIN Pacientes p ON c.IdPac = p.IdPac
            WHERE c.Fecha = %s
            ORDER BY c.Hora
        """
        
        citas = GesdenDB.ejecutar_query(sql, (fecha_gesden,))
        
        # Convertir formato
        for c in citas:
            c['Fecha'] = GesdenDB.fecha_gesden_a_iso(c['Fecha'])
            c['Hora'] = GesdenDB.hora_gesden_a_string(c['Hora'])
            c['Paciente'] = f"{c['Nombre']} {c['Apellidos']}" if c.get('Nombre') else "Sin paciente"
        
        logging.info(f"Listar citas: {fecha.strftime('%d/%m/%Y')} - {len(citas)} citas")
        
        return jsonify({
            'success': True,
            'citas': citas,
            'fecha': fecha.strftime('%Y-%m-%d')
        })
    
    except Exception as e:
        logging.error(f"Error listando citas: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/citas/crear', methods=['POST'])
def crear_cita():
    """Crear nueva cita"""
    try:
        data = request.json
        
        id_pac = data.get('id_pac')
        fecha_iso = data.get('fecha')
        hora_str = data.get('hora')
        duracion = data.get('duracion', 30)
        texto = data.get('texto', '')
        
        # Convertir formatos
        fecha_gesden = GesdenDB.fecha_iso_a_gesden(fecha_iso)
        hora_gesden = GesdenDB.hora_string_a_gesden(hora_str)
        
        # Obtener siguiente IdOrden para esa fecha
        sql_orden = "SELECT ISNULL(MAX(IdOrden), 0) + 1 FROM DCitas WHERE Fecha = %s"
        resultado = GesdenDB.ejecutar_query(sql_orden, (fecha_gesden,))
        id_orden = resultado[0][''] if resultado else 1
        
        # Insertar cita
        sql = """
            INSERT INTO DCitas (IdPac, Fecha, Hora, Duracion, Texto, IdOrden, IdCentro)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        id_cita = GesdenDB.ejecutar_insert(sql, (
            id_pac,
            fecha_gesden,
            hora_gesden,
            duracion,
            texto,
            id_orden,
            Config.ID_CENTRO
        ))
        
        logging.info(f"Listar citas: {fecha.strftime('%d/%m/%Y')} - {len(citas)} citas")
        
        return jsonify({
            'success': True,
            'id_cita': id_cita,
            'mensaje': f'Cita creada para el {fecha_iso} a las {hora_str}'
        })
    
    except Exception as e:
        logging.error(f"Error creando cita: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# =====================================================
# API - COLABORADORES
# =====================================================

@app.route('/api/colaboradores', methods=['GET'])
def listar_colaboradores():
    """Listar colaboradores activos"""
    try:
        sql = """
            SELECT IdCol, Codigo, Nombre, Apellidos
            FROM TColabos
            WHERE Activo = 'S'
            ORDER BY Apellidos, Nombre
        """
        
        colaboradores = GesdenDB.ejecutar_query(sql)
        
        return jsonify({
            'success': True,
            'colaboradores': colaboradores
        })
    
    except Exception as e:
        logging.error(f"Error listando colaboradores: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# =====================================================
# API - COMANDOS IA
# =====================================================

@app.route('/api/comando', methods=['POST'])
def procesar_comando():
    """Procesar comando con IA"""
    try:
        data = request.json
        comando = data.get('comando', '')
        
        logging.info(f"Comando recibido: {comando}")
        
        # Procesar con Claude (con herramientas)
        respuesta_ia = procesar_con_ia(comando)
        
        # Devolver respuesta directa de Claude
        return jsonify({
            'success': True,
            'mensaje': respuesta_ia.get('mensaje', 'Sin respuesta')
        })
    
    except Exception as e:
        logging.error(f"Error procesando comando: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# =====================================================
# INICIAR SERVIDOR
# =====================================================

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 AGENTE GESDEN IA - API SERVER")
    print("=" * 60)
    print()
    print("🗄️  Base de datos: LOCAL (SQL Server)")
    print("🌐 Acceso remoto: Vía Ngrok")
    print("🤖 IA: Ollama (Llama 3.2) - 100% LOCAL & RÁPIDO")
    print()
    print("📍 Servidor: http://localhost:5000")
    print()
    print("=" * 60)
    print()
    
    # Detectar si estamos en desarrollo o producción
    is_dev = os.getenv('FLASK_ENV') == 'development'
    
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=is_dev  # Solo debug en desarrollo
    )
