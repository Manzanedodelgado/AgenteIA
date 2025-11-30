"""
=====================================================
AGENTE GESDEN IA - SUITE DE TESTS AUTOMÁTICOS
50 Casos de Prueba
=====================================================
"""

import requests
import time
import json
from datetime import datetime
from colorama import init, Fore, Style

# Inicializar colorama para colores en terminal
init(autoreset=True)

# =====================================================
# CONFIGURACIÓN
# =====================================================

BASE_URL = "http://localhost:5000"  # Cambiar si usas ngrok
TIMEOUT = 30  # segundos

# =====================================================
# UTILIDADES
# =====================================================

def print_header(text):
    """Imprimir cabecera"""
    print("\n" + "="*80)
    print(f"{Fore.CYAN}{Style.BRIGHT}{text}")
    print("="*80)

def print_test(num, name):
    """Imprimir nombre de test"""
    print(f"\n{Fore.YELLOW}[TEST {num:02d}] {name}")

def print_result(success, message="", response_time=0):
    """Imprimir resultado"""
    if success:
        print(f"{Fore.GREEN}✅ PASS {message} ({response_time:.2f}s)")
    else:
        print(f"{Fore.RED}❌ FAIL {message}")

def test_endpoint(method, endpoint, data=None, expected_status=200, test_name=""):
    """Test genérico de endpoint"""
    start_time = time.time()
    try:
        url = f"{BASE_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, timeout=TIMEOUT)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=TIMEOUT)
        else:
            return False, "Método no soportado", 0
        
        elapsed = time.time() - start_time
        
        if response.status_code == expected_status:
            return True, f"Status {response.status_code}", elapsed
        else:
            return False, f"Expected {expected_status}, got {response.status_code}", elapsed
    
    except requests.exceptions.Timeout:
        return False, "Timeout", time.time() - start_time
    except requests.exceptions.ConnectionError:
        return False, "Connection error - ¿Servidor corriendo?", 0
    except Exception as e:
        return False, str(e), time.time() - start_time

# =====================================================
# SUITE DE TESTS
# =====================================================

def run_tests():
    """Ejecutar todos los tests"""
    
    results = {
        'total': 50,
        'passed': 0,
        'failed': 0,
        'errors': [],
        'times': []
    }
    
    print_header("🧪 INICIANDO SUITE DE TESTS - 50 CASOS")
    print(f"URL Base: {BASE_URL}")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # =====================================================
    # CATEGORÍA 1: TESTS DE INFRAESTRUCTURA (1-5)
    # =====================================================
    
    print_header("🏗️ CATEGORÍA 1: INFRAESTRUCTURA")
    
    # TEST 1
    print_test(1, "Servidor responde en /")
    success, msg, elapsed = test_endpoint("GET", "/")
    print_result(success, msg, elapsed)
    if success:
        results['passed'] += 1
        results['times'].append(elapsed)
    else:
        results['failed'] += 1
        results['errors'].append(f"TEST 1: {msg}")
    
    # TEST 2
    print_test(2, "Health check endpoint")
    success, msg, elapsed = test_endpoint("GET", "/health")
    print_result(success, msg, elapsed)
    if success:
        results['passed'] += 1
        results['times'].append(elapsed)
    else:
        results['failed'] += 1
        results['errors'].append(f"TEST 2: {msg}")
    
    # TEST 3
    print_test(3, "Archivos estáticos - logo.png")
    success, msg, elapsed = test_endpoint("GET", "/static/logo.png")
    print_result(success, msg, elapsed)
    if success:
        results['passed'] += 1
        results['times'].append(elapsed)
    else:
        results['failed'] += 1
        results['errors'].append(f"TEST 3: {msg}")
    
    # TEST 4
    print_test(4, "Archivos estáticos - avatar.png")
    success, msg, elapsed = test_endpoint("GET", "/static/avatar.png")
    print_result(success, msg, elapsed)
    if success:
        results['passed'] += 1
        results['times'].append(elapsed)
    else:
        results['failed'] += 1
        results['errors'].append(f"TEST 4: {msg}")
    
    # TEST 5
    print_test(5, "404 en ruta inexistente")
    success, msg, elapsed = test_endpoint("GET", "/ruta/que/no/existe", expected_status=404)
    print_result(success, msg, elapsed)
    if success:
        results['passed'] += 1
        results['times'].append(elapsed)
    else:
        results['failed'] += 1
        results['errors'].append(f"TEST 5: {msg}")
    
    # =====================================================
    # CATEGORÍA 2: TESTS DE COMANDOS BÁSICOS (6-15)
    # =====================================================
    
    print_header("💬 CATEGORÍA 2: COMANDOS BÁSICOS")
    
    comandos_basicos = [
        ("Saludo simple", "hola"),
        ("Ayuda", "ayuda"),
        ("Comando vacío", ""),
        ("Comando con espacios", "   "),
        ("Comando largo (100 chars)", "a" * 100),
        ("Números aleatorios", "123456"),
        ("Caracteres especiales", "¿Cómo estás? ¡Bien!"),
        ("Emojis", "😀 🦷 💊"),
        ("HTML tags", "<script>alert('test')</script>"),
        ("SQL injection attempt", "'; DROP TABLE Pacientes; --"),
    ]
    
    test_num = 6
    for nombre, comando in comandos_basicos:
        print_test(test_num, f"Comando: {nombre}")
        success, msg, elapsed = test_endpoint("POST", "/api/comando", {"comando": comando})
        print_result(success, msg, elapsed)
        if success:
            results['passed'] += 1
            results['times'].append(elapsed)
        else:
            results['failed'] += 1
            results['errors'].append(f"TEST {test_num}: {msg}")
        test_num += 1
    
    # =====================================================
    # CATEGORÍA 3: BÚSQUEDA DE PACIENTES (16-25)
    # =====================================================
    
    print_header("👤 CATEGORÍA 3: BÚSQUEDA DE PACIENTES")
    
    busquedas = [
        ("Buscar por nombre común", "busca a María"),
        ("Buscar por apellido", "busca García"),
        ("Buscar nombre compuesto", "busca Juan Antonio"),
        ("Buscar con acentos", "busca José María"),
        ("Buscar con Ñ", "busca Muñoz"),
        ("Buscar paciente inexistente", "busca ZZZZZZ999999"),
        ("Buscar con números", "busca paciente 12345"),
        ("Buscar nombre muy largo", "busca " + "a" * 50),
        ("Buscar con caracteres raros", "busca @#$%"),
        ("Comando ambiguo", "encuentra maría garcía lópez"),
    ]
    
    test_num = 16
    for nombre, comando in busquedas:
        print_test(test_num, nombre)
        success, msg, elapsed = test_endpoint("POST", "/api/comando", {"comando": comando})
        print_result(success, msg, elapsed)
        if success:
            results['passed'] += 1
            results['times'].append(elapsed)
        else:
            results['failed'] += 1
            results['errors'].append(f"TEST {test_num}: {msg}")
        test_num += 1
    
    # =====================================================
    # CATEGORÍA 4: GESTIÓN DE CITAS (26-35)
    # =====================================================
    
    print_header("📅 CATEGORÍA 4: GESTIÓN DE CITAS")
    
    citas = [
        ("Citas de hoy", "citas de hoy"),
        ("Citas de mañana", "citas de mañana"),
        ("Citas de ayer", "citas de ayer"),
        ("Citas fecha específica", "citas del 15 de diciembre"),
        ("Citas próxima semana", "citas de la próxima semana"),
        ("Crear cita básica", "crear cita para Juan el lunes a las 10"),
        ("Crear cita compleja", "agendar cita para María López el próximo martes 15:30 para limpieza"),
        ("Crear cita sin hora", "cita para Pedro mañana"),
        ("Crear cita sin fecha", "cita para Ana a las 11"),
        ("Listar todas las citas", "muéstrame todas las citas"),
    ]
    
    test_num = 26
    for nombre, comando in citas:
        print_test(test_num, nombre)
        success, msg, elapsed = test_endpoint("POST", "/api/comando", {"comando": comando})
        print_result(success, msg, elapsed)
        if success:
            results['passed'] += 1
            results['times'].append(elapsed)
        else:
            results['failed'] += 1
            results['errors'].append(f"TEST {test_num}: {msg}")
        test_num += 1
    
    # =====================================================
    # CATEGORÍA 5: EDGE CASES Y SEGURIDAD (36-45)
    # =====================================================
    
    print_header("🔒 CATEGORÍA 5: EDGE CASES Y SEGURIDAD")
    
    edge_cases = [
        ("Comando muy largo (1000 chars)", "a" * 1000),
        ("JSON malformado", "}{}{}{"),
        ("Unicode extremo", "🦷💉🩺🏥👨‍⚕️👩‍⚕️💊"),
        ("XSS intento", "<img src=x onerror=alert(1)>"),
        ("Path traversal", "../../etc/passwd"),
        ("Command injection", "; ls -la"),
        ("CRLF injection", "test\r\nInjected-Header: value"),
        ("Null bytes", "test\x00admin"),
        ("Formato fecha inválido", "citas del 32/13/2025"),
        ("Hora inválida", "cita a las 25:99"),
    ]
    
    test_num = 36
    for nombre, comando in edge_cases:
        print_test(test_num, nombre)
        success, msg, elapsed = test_endpoint("POST", "/api/comando", {"comando": comando})
        print_result(success, msg, elapsed)
        if success:
            results['passed'] += 1
            results['times'].append(elapsed)
        else:
            results['failed'] += 1
            results['errors'].append(f"TEST {test_num}: {msg}")
        test_num += 1
    
    # =====================================================
    # CATEGORÍA 6: RENDIMIENTO Y STRESS (46-50)
    # =====================================================
    
    print_header("⚡ CATEGORÍA 6: RENDIMIENTO")
    
    # TEST 46: Respuesta rápida
    print_test(46, "Respuesta < 5 segundos")
    success, msg, elapsed = test_endpoint("POST", "/api/comando", {"comando": "hola"})
    if elapsed < 5.0:
        print_result(True, f"Respondió en {elapsed:.2f}s", elapsed)
        results['passed'] += 1
        results['times'].append(elapsed)
    else:
        print_result(False, f"Tardó {elapsed:.2f}s (>5s)")
        results['failed'] += 1
        results['errors'].append(f"TEST 46: Timeout ({elapsed:.2f}s)")
    
    # TEST 47: Múltiples requests rápidas
    print_test(47, "5 requests consecutivas rápidas")
    start = time.time()
    all_ok = True
    for i in range(5):
        success, msg, elapsed = test_endpoint("POST", "/api/comando", {"comando": f"test {i}"})
        if not success:
            all_ok = False
            break
    total_time = time.time() - start
    if all_ok:
        print_result(True, f"5 requests completadas en {total_time:.2f}s", total_time)
        results['passed'] += 1
        results['times'].append(total_time)
    else:
        print_result(False, "Falló alguna request")
        results['failed'] += 1
        results['errors'].append("TEST 47: Request falló en serie")
    
    # TEST 48: Request muy compleja
    print_test(48, "Comando muy complejo")
    comando_complejo = """
    Necesito buscar al paciente Juan Antonio Manzanedo García,
    verificar sus citas del mes de diciembre, crear una nueva cita
    para el próximo lunes a las 11:00 para reconstrucción dental,
    y enviarle un recordatorio por SMS.
    """
    success, msg, elapsed = test_endpoint("POST", "/api/comando", {"comando": comando_complejo})
    print_result(success, msg, elapsed)
    if success:
        results['passed'] += 1
        results['times'].append(elapsed)
    else:
        results['failed'] += 1
        results['errors'].append(f"TEST 48: {msg}")
    
    # TEST 49: Búsqueda directa pacientes
    print_test(49, "Endpoint directo /api/pacientes/buscar")
    success, msg, elapsed = test_endpoint("POST", "/api/pacientes/buscar", {"busqueda": "Juan"})
    print_result(success, msg, elapsed)
    if success:
        results['passed'] += 1
        results['times'].append(elapsed)
    else:
        results['failed'] += 1
        results['errors'].append(f"TEST 49: {msg}")
    
    # TEST 50: Endpoint directo citas
    print_test(50, "Endpoint directo /api/citas/listar")
    success, msg, elapsed = test_endpoint("POST", "/api/citas/listar", {"fecha": "hoy"})
    print_result(success, msg, elapsed)
    if success:
        results['passed'] += 1
        results['times'].append(elapsed)
    else:
        results['failed'] += 1
        results['errors'].append(f"TEST 50: {msg}")
    
    # =====================================================
    # RESUMEN FINAL
    # =====================================================
    
    print_header("📊 RESUMEN DE RESULTADOS")
    
    print(f"\n{Fore.CYAN}Total Tests: {results['total']}")
    print(f"{Fore.GREEN}✅ Passed: {results['passed']} ({results['passed']/results['total']*100:.1f}%)")
    print(f"{Fore.RED}❌ Failed: {results['failed']} ({results['failed']/results['total']*100:.1f}%)")
    
    if results['times']:
        avg_time = sum(results['times']) / len(results['times'])
        min_time = min(results['times'])
        max_time = max(results['times'])
        
        print(f"\n{Fore.YELLOW}⏱️  TIEMPOS DE RESPUESTA:")
        print(f"   Promedio: {avg_time:.2f}s")
        print(f"   Mínimo: {min_time:.2f}s")
        print(f"   Máximo: {max_time:.2f}s")
    
    if results['errors']:
        print(f"\n{Fore.RED}❌ ERRORES ENCONTRADOS:")
        for error in results['errors']:
            print(f"   • {error}")
    
    # Calcular score
    score = (results['passed'] / results['total']) * 100
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*80}")
    if score >= 90:
        print(f"{Fore.GREEN}{Style.BRIGHT}🏆 EXCELENTE - Score: {score:.1f}%")
    elif score >= 70:
        print(f"{Fore.YELLOW}{Style.BRIGHT}⚠️  ACEPTABLE - Score: {score:.1f}%")
    else:
        print(f"{Fore.RED}{Style.BRIGHT}❌ CRÍTICO - Score: {score:.1f}%")
    print(f"{Fore.CYAN}{Style.BRIGHT}{'='*80}\n")
    
    # Guardar resultados en archivo
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = f"test_report_{timestamp}.json"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total': results['total'],
            'passed': results['passed'],
            'failed': results['failed'],
            'score': score,
            'avg_time': avg_time if results['times'] else 0,
            'errors': results['errors']
        }, f, indent=2, ensure_ascii=False)
    
    print(f"{Fore.CYAN}📄 Reporte guardado en: {report_file}\n")
    
    return results

# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":
    try:
        results = run_tests()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️  Tests interrumpidos por el usuario")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Error fatal: {e}")
