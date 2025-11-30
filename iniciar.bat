@echo off
REM =====================================================
REM AGENTE GESDEN IA - SCRIPT DE INICIO
REM =====================================================

title Agente Gesden IA

echo.
echo ============================================================
echo       AGENTE GESDEN IA - INICIANDO SISTEMA
echo ============================================================
echo.

REM Verificar que estamos en la carpeta correcta
if not exist "api_server.py" (
    echo ERROR: No se encuentra api_server.py
    echo Asegurate de ejecutar este script desde la carpeta correcta
    pause
    exit /b 1
)

echo [1/3] Iniciando servidor Flask...
start "Servidor Flask - Agente Gesden" /MIN python api_server.py

echo [2/3] Esperando 5 segundos...
timeout /t 5 /nobreak > nul

echo [3/3] Iniciando Ngrok tunnel...
start "Ngrok Tunnel" ngrok http 5000

echo.
echo ============================================================
echo       SISTEMA INICIADO CORRECTAMENTE
echo ============================================================
echo.
echo   Servidor local:  http://localhost:5000
echo   Ngrok:          Consulta la ventana de Ngrok para la URL
echo.
echo   Presiona cualquier tecla para cerrar esta ventana
echo   (Las otras ventanas seguiran abiertas)
echo ============================================================
echo.

pause > nul
