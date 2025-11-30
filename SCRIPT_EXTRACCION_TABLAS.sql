-- =====================================================
-- SCRIPT COMPLETO DE EXTRACCIÓN DE INFORMACIÓN
-- Base de Datos: GELITE
-- Propósito: Obtener estructura de todas las tablas principales
-- Fecha: 29/11/2024
-- =====================================================

USE [GELITE];
GO

SET NOCOUNT ON;

PRINT '╔════════════════════════════════════════════════════╗';
PRINT '║  ESQUEMA COMPLETO - BASE DE DATOS GESDEN GELITE    ║';
PRINT '╚════════════════════════════════════════════════════╝';
PRINT '';

-- =====================================================
-- 1. PACIENTES
-- =====================================================
PRINT '┌────────────────────────────────────────────────────┐';
PRINT '│ 1. TABLA: Pacientes                                │';
PRINT '└────────────────────────────────────────────────────┘';
PRINT '';

SELECT 
    COLUMN_NAME AS Campo,
    DATA_TYPE AS Tipo,
    ISNULL(CAST(CHARACTER_MAXIMUM_LENGTH AS VARCHAR), '-') AS Tamaño,
    CASE WHEN IS_NULLABLE = 'YES' THEN 'SÍ' ELSE 'NO' END AS Acepta_Nulo
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'Pacientes'
ORDER BY ORDINAL_POSITION;

PRINT '';
PRINT 'Ejemplo de datos:';
SELECT TOP 3 
    IdPac, NumPac, Nombre, Apellidos, FecNacim, TelMovil, Email
FROM Pacientes 
ORDER BY IdPac DESC;

PRINT '';
PRINT '';

-- =====================================================
-- 2. CITAS
-- =====================================================
PRINT '┌────────────────────────────────────────────────────┐';
PRINT '│ 2. TABLA: DCitas                                   │';
PRINT '└────────────────────────────────────────────────────┘';
PRINT '';

SELECT 
    COLUMN_NAME AS Campo,
    DATA_TYPE AS Tipo,
    ISNULL(CAST(CHARACTER_MAXIMUM_LENGTH AS VARCHAR), '-') AS Tamaño,
    CASE WHEN IS_NULLABLE = 'YES' THEN 'SÍ' ELSE 'NO' END AS Acepta_Nulo
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'DCitas'
ORDER BY ORDINAL_POSITION;

PRINT '';
PRINT 'Ejemplo de datos:';
SELECT TOP 3 
    IdCita, IdPac, Fecha, Hora, Duracion, Texto, NUMPAC
FROM DCitas 
ORDER BY IdCita DESC;

PRINT '';
PRINT '';

-- =====================================================
-- 3. TRATAMIENTOS
-- =====================================================
PRINT '┌────────────────────────────────────────────────────┐';
PRINT '│ 3. TABLA: TtosMed                                  │';
PRINT '└────────────────────────────────────────────────────┘';
PRINT '';

SELECT 
    COLUMN_NAME AS Campo,
    DATA_TYPE AS Tipo,
    ISNULL(CAST(CHARACTER_MAXIMUM_LENGTH AS VARCHAR), '-') AS Tamaño,
    CASE WHEN IS_NULLABLE = 'YES' THEN 'SÍ' ELSE 'NO' END AS Acepta_Nulo
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'TtosMed'
ORDER BY ORDINAL_POSITION;

PRINT '';
PRINT 'Ejemplo de datos:';
SELECT TOP 3 
    IdPac, NumTto, IdTto, FecIni, Notas, Importe, StaTto
FROM TtosMed 
ORDER BY IdPac DESC, NumTto DESC;

PRINT '';
PRINT '';

-- =====================================================
-- 4. PRESUPUESTOS - CABECERA
-- =====================================================
PRINT '┌────────────────────────────────────────────────────┐';
PRINT '│ 4. TABLA: Presu                                    │';
PRINT '└────────────────────────────────────────────────────┘';
PRINT '';

SELECT 
    COLUMN_NAME AS Campo,
    DATA_TYPE AS Tipo,
    ISNULL(CAST(CHARACTER_MAXIMUM_LENGTH AS VARCHAR), '-') AS Tamaño,
    CASE WHEN IS_NULLABLE = 'YES' THEN 'SÍ' ELSE 'NO' END AS Acepta_Nulo
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'Presu'
ORDER BY ORDINAL_POSITION;

PRINT '';
PRINT 'Ejemplo de datos:';
SELECT TOP 3 * FROM Presu ORDER BY IdPac DESC;

PRINT '';
PRINT '';

-- =====================================================
-- 5. PRESUPUESTOS - DETALLE
-- =====================================================
PRINT '┌────────────────────────────────────────────────────┐';
PRINT '│ 5. TABLA: PresuTto                                 │';
PRINT '└────────────────────────────────────────────────────┘';
PRINT '';

SELECT 
    COLUMN_NAME AS Campo,
    DATA_TYPE AS Tipo,
    ISNULL(CAST(CHARACTER_MAXIMUM_LENGTH AS VARCHAR), '-') AS Tamaño,
    CASE WHEN IS_NULLABLE = 'YES' THEN 'SÍ' ELSE 'NO' END AS Acepta_Nulo
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'PresuTto'
ORDER BY ORDINAL_POSITION;

PRINT '';
PRINT 'Ejemplo de datos:';
SELECT TOP 3 
    Id_Presu, IdPac, NumSerie, NumPre, LinPre, IdTto, Unidades, ImportePre
FROM PresuTto 
ORDER BY Id_Presu DESC;

PRINT '';
PRINT '';

-- =====================================================
-- 6. PAGOS
-- =====================================================
PRINT '┌────────────────────────────────────────────────────┐';
PRINT '│ 6. TABLA: PagoCli                                  │';
PRINT '└────────────────────────────────────────────────────┘';
PRINT '';

SELECT 
    COLUMN_NAME AS Campo,
    DATA_TYPE AS Tipo,
    ISNULL(CAST(CHARACTER_MAXIMUM_LENGTH AS VARCHAR), '-') AS Tamaño,
    CASE WHEN IS_NULLABLE = 'YES' THEN 'SÍ' ELSE 'NO' END AS Acepta_Nulo
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'PagoCli'
ORDER BY ORDINAL_POSITION;

PRINT '';
PRINT 'Ejemplo de datos:';
SELECT TOP 3 
    IdPagoCli, IdCli, Pagado, FecPago, IdForPago, NFactura
FROM PagoCli 
ORDER BY IdPagoCli DESC;

PRINT '';
PRINT '';

-- =====================================================
-- 7. DEUDA
-- =====================================================
PRINT '┌────────────────────────────────────────────────────┐';
PRINT '│ 7. TABLA: DeudaCli                                 │';
PRINT '└────────────────────────────────────────────────────┘';
PRINT '';

SELECT 
    COLUMN_NAME AS Campo,
    DATA_TYPE AS Tipo,
    ISNULL(CAST(CHARACTER_MAXIMUM_LENGTH AS VARCHAR), '-') AS Tamaño,
    CASE WHEN IS_NULLABLE = 'YES' THEN 'SÍ' ELSE 'NO' END AS Acepta_Nulo
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'DeudaCli'
ORDER BY ORDINAL_POSITION;

PRINT '';
PRINT 'Ejemplo de datos:';
SELECT TOP 3 
    IdDeudaCli, IdCli, IdPac, Adeudo, Pendiente, Liquidado, NFactura
FROM DeudaCli 
ORDER BY IdDeudaCli DESC;

PRINT '';
PRINT '';

-- =====================================================
-- 8. ANTECEDENTES
-- =====================================================
PRINT '┌────────────────────────────────────────────────────┐';
PRINT '│ 8. TABLA: TAntecedentes                            │';
PRINT '└────────────────────────────────────────────────────┘';
PRINT '';

SELECT 
    COLUMN_NAME AS Campo,
    DATA_TYPE AS Tipo,
    ISNULL(CAST(CHARACTER_MAXIMUM_LENGTH AS VARCHAR), '-') AS Tamaño,
    CASE WHEN IS_NULLABLE = 'YES' THEN 'SÍ' ELSE 'NO' END AS Acepta_Nulo
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'TAntecedentes'
ORDER BY ORDINAL_POSITION;

PRINT '';
PRINT 'Ejemplo de datos:';
SELECT TOP 3 
    IdPac, IdAntecedente, TipoAntecedente, Descripcion, Status
FROM TAntecedentes 
ORDER BY IdPac DESC;

PRINT '';
PRINT '';

-- =====================================================
-- 9. ALERTAS
-- =====================================================
PRINT '┌────────────────────────────────────────────────────┐';
PRINT '│ 9. TABLA: AlertPac                                 │';
PRINT '└────────────────────────────────────────────────────┘';
PRINT '';

SELECT 
    COLUMN_NAME AS Campo,
    DATA_TYPE AS Tipo,
    ISNULL(CAST(CHARACTER_MAXIMUM_LENGTH AS VARCHAR), '-') AS Tamaño,
    CASE WHEN IS_NULLABLE = 'YES' THEN 'SÍ' ELSE 'NO' END AS Acepta_Nulo
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'AlertPac'
ORDER BY ORDINAL_POSITION;

PRINT '';
PRINT 'Ejemplo de datos:';
SELECT TOP 3 * FROM AlertPac ORDER BY Id DESC;

PRINT '';
PRINT '';

-- =====================================================
-- 10. CATÁLOGO DE TRATAMIENTOS
-- =====================================================
PRINT '┌────────────────────────────────────────────────────┐';
PRINT '│ 10. TABLA: TTratamientos                           │';
PRINT '└────────────────────────────────────────────────────┘';
PRINT '';

SELECT 
    COLUMN_NAME AS Campo,
    DATA_TYPE AS Tipo,
    ISNULL(CAST(CHARACTER_MAXIMUM_LENGTH AS VARCHAR), '-') AS Tamaño,
    CASE WHEN IS_NULLABLE = 'YES' THEN 'SÍ' ELSE 'NO' END AS Acepta_Nulo
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'TTratamientos'
ORDER BY ORDINAL_POSITION;

PRINT '';
PRINT 'Ejemplo de tratamientos más usados:';
SELECT TOP 10 
    tt.IdTto, 
    tt.Descripcio, 
    COUNT(*) AS Veces_Usado
FROM TTratamientos tt
LEFT JOIN TtosMed tm ON tt.IdTto = tm.IdTto
GROUP BY tt.IdTto, tt.Descripcio
ORDER BY Veces_Usado DESC;

PRINT '';
PRINT '';

-- =====================================================
-- ESTADÍSTICAS GENERALES
-- =====================================================
PRINT '╔════════════════════════════════════════════════════╗';
PRINT '║  ESTADÍSTICAS GENERALES                            ║';
PRINT '╚════════════════════════════════════════════════════╝';
PRINT '';

SELECT 
    'Pacientes' AS Tabla,
    COUNT(*) AS Total_Registros
FROM Pacientes

UNION ALL

SELECT 
    'Citas',
    COUNT(*)
FROM DCitas

UNION ALL

SELECT 
    'Tratamientos Realizados',
    COUNT(*)
FROM TtosMed

UNION ALL

SELECT 
    'Presupuestos',
    COUNT(*)
FROM Presu

UNION ALL

SELECT 
    'Pagos',
    COUNT(*)
FROM PagoCli

UNION ALL

SELECT 
    'Deudas Pendientes',
    COUNT(*)
FROM DeudaCli
WHERE Liquidado = 0;

PRINT '';
PRINT '';

-- =====================================================
-- CONTADORES
-- =====================================================
PRINT '┌────────────────────────────────────────────────────┐';
PRINT '│ CONTADORES DEL SISTEMA                             │';
PRINT '└────────────────────────────────────────────────────┘';
PRINT '';

SELECT 
    Tabla,
    Contador,
    Descripcion
FROM Contadores
WHERE Tabla IN ('Pacientes', 'Citas', 'Tratamientos')
ORDER BY Tabla;

PRINT '';
PRINT '';

PRINT '╔════════════════════════════════════════════════════╗';
PRINT '║  FIN DEL ANÁLISIS                                  ║';
PRINT '╚════════════════════════════════════════════════════╝';

SET NOCOUNT OFF;
