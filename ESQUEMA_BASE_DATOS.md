# 📊 ESQUEMA COMPLETO DE BASE DE DATOS - GESDEN GELITE

Mapeo completo de todas las tablas necesarias para que la IA comprenda el funcionamiento del sistema Gesden.

---

## 🗄️ INFORMACIÓN GENERAL

- **Base de Datos:** GELITE
- **Motor:** SQL Server 2008
- **Servidor:** GABINETE2\INFOMED
- **Total de Tablas:** 628
- **Tablas Principales Mapeadas:** 40+
- **Fecha de Análisis:** 29/11/2024

---

## 📋 ÍNDICE DE TABLAS

### 1. GESTIÓN DE PACIENTES
- [Pacientes](#1-pacientes) - Datos principales del paciente
- [PacCli](#pacientes-relacionadas) - Relación paciente-cliente
- [AlertPac](#9-alertpac) - Alertas del paciente
- [TAntecedentes](#8-tantecedentes) - Antecedentes médicos

### 2. GESTIÓN DE CITAS Y AGENDA
- [DCitas](#2-dcitas) - Citas/Agenda principal
- [Sch_Appointments](#sistema-scheduler) - Sistema de citas nuevo
- [TUsuAgd](#usuarios-agenda) - Usuarios de agenda

### 3. TRATAMIENTOS Y ACTOS CLÍNICOS
- [TtosMed](#3-ttosmed) - Tratamientos realizados
- [TTratamientos](#10-ttratamientos) - Catálogo de tratamientos
- [TtosMedSes](#tratamientos-relacionadas) - Sesiones de tratamientos

### 4. PRESUPUESTOS
- [Presu](#4-presu) - Cabecera de presupuestos
- [PresuTto](#5-presutto) - Líneas de tratamientos del presupuesto
- [PresuTipo](#presupuestos-relacionadas) - Tipos de presupuesto

### 5. PAGOS Y FACTURACIÓN
- [PagoCli](#6-pagocli) - Pagos realizados
- [DeudaCli](#7-deudacli) - Deuda pendiente
- [FormasPago](#12-formaspago) - Formas de pago

### 6. DOCUMENTOS E IMÁGENES
- [DocPac](#11-docpac) - Documentos del paciente
- [ItemImg](#documentos-relacionadas) - Imágenes

### 7. CONFIGURACIÓN
- [Centros](#centros) - Centros/Clínicas
- [TColabos](#colaboradores) - Colaboradores/Doctores
- [Contadores](#contadores) - Contadores del sistema

---

## 📊 TABLAS PRINCIPALES - DETALLE COMPLETO

---

### 1. **Pacientes**

**Descripción:** Tabla principal con todos los datos de los pacientes.

**Uso:** Almacena información personal, contacto y datos administrativos.

#### Campos Principales:

| Campo | Tipo | Tamaño | Nulo | Descripción |
|-------|------|--------|------|-------------|
| **IdPac** | int | - | NO | 🔑 ID único del paciente (PK) |
| **NumPac** | varchar | 20 | NO | Número de paciente (visible) |
| **Nombre** | varchar | 80 | SÍ | Nombre (MAYÚSCULAS) |
| **Apellidos** | varchar | 100 | SÍ | Apellidos (MAYÚSCULAS) |
| **NIF** | char | 20 | SÍ | DNI/NIE/Pasaporte |
| **FecNacim** | smalldatetime | - | SÍ | Fecha de nacimiento |
| **Sexo** | varchar | 1 | SÍ | 'M' o 'F' |
| **Direccion** | varchar | 80 | SÍ | Dirección postal |
| **CP** | varchar | 20 | SÍ | Código postal |
| **IdPoblacio** | smallint | - | SÍ | FK → Población |
| **Tel1** | varchar | 15 | SÍ | Teléfono fijo |
| **TelMovil** | varchar | 15 | SÍ | Teléfono móvil |
| **Email** | varchar | 255 | SÍ | Email |
| **FecAlta** | datetime | - | SÍ | Fecha de alta en sistema |
| **IdCentro** | int | - | SÍ | FK → Centro/Clínica |
| **Notas** | text | - | SÍ | Observaciones generales |
| **IdCli** | int | - | SÍ | FK → Cliente (si es distinto del paciente) |
| **Mailing** | bit | - | NO | Acepta publicidad |
| **AceptaLOPD** | bit | - | SÍ | Acepta LOPD/RGPD |
| **Inactivo** | smalldatetime | - | SÍ | Fecha de baja |

#### Relaciones:
- **1 → N** con `DCitas` (Un paciente tiene muchas citas)
- **1 → N** con `TtosMed` (Un paciente tiene muchos tratamientos)
- **1 → N** con `Presu` (Un paciente tiene muchos presupuestos)
- **1 → N** con `AlertPac` (Un paciente tiene muchas alertas)
- **1 → N** con `TAntecedentes` (Un paciente tiene muchos antecedentes)

#### Índices Importantes:
- PRIMARY KEY: `IdPac`
- UNIQUE: `NumPac`
- INDEX: `Nombre`, `Apellidos`, `TelMovil`

#### Ejemplo de Registro:
```sql
IdPac: 6843
NumPac: 6213
Nombre: GINA
Apellidos: ROSALES ALVIARES
FecNacim: 2015-03-06
TelMovil: 699522682
Email: NULL
IdCentro: 2
FecAlta: 2025-11-28
```

---

### 2. **DCitas**

**Descripción:** Tabla de citas/agenda del sistema.

**Uso:** Gestiona todas las citas programadas de los pacientes.

#### Campos Principales:

| Campo | Tipo | Tamaño | Nulo | Descripción |
|-------|------|--------|------|-------------|
| **IdCita** | bigint | - | NO | 🔑 ID único de la cita (PK) |
| **IdUsu** | int | - | NO | FK → Usuario/Doctor que atiende |
| **IdOrden** | int | - | NO | Orden de la cita en el día |
| **IdPac** | int | - | SÍ | FK → Paciente |
| **Fecha** | int | - | SÍ | Fecha en formato Gesden (días desde 1899-12-30) |
| **Hora** | int | - | SÍ | Hora en formato Gesden (HHMMSS * 100) |
| **Duracion** | int | - | SÍ | Duración en minutos |
| **IdSitC** | int | - | SÍ | FK → Estado de la cita (1=Pendiente, 2=Realizada, etc.) |
| **Texto** | varchar | 1000 | SÍ | Descripción/motivo de la cita |
| **NUMPAC** | varchar | 20 | SÍ | Número del paciente (denormalizado) |
| **Contacto** | varchar | 50 | SÍ | Teléfono de contacto |
| **Movil** | varchar | 50 | SÍ | Móvil de contacto |
| **NOTAS** | text | - | SÍ | Notas adicionales |
| **IdBox** | int | - | SÍ | FK → Box/Gabinete |
| **Recordada** | tinyint | - | NO | ¿Se envió recordatorio? |
| **Confirmada** | tinyint | - | NO | ¿Está confirmada? |
| **FecAlta** | smalldatetime | - | SÍ | Fecha de creación de la cita |

#### Relaciones:
- **N → 1** con `Pacientes` (Muchas citas de un paciente)
- **N → 1** con `TUsuAgd` (Muchas citas de un doctor)

#### Conversión de Fechas:
```python
# Gesden guarda fechas como días desde 1899-12-30
fecha_python = datetime(1899, 12, 30) + timedelta(days=fecha_gesden)

# Ejemplo: 
# 41456 → 2013-06-15
```

#### Conversión de Horas:
```python
# Gesden guarda horas como HHMMSS * 100
horas = hora_gesden // 10000
minutos = (hora_gesden % 10000) // 100

# Ejemplo:
# 143000 → 14:30
```

#### Ejemplo de Registro:
```sql
IdCita: 13259
IdUsu: 5
IdPac: 3
Fecha: 41456 (= 2013-06-15)
Hora: 41400 (= 11:30)
Duracion: 30
Texto: "empieza tratamiento .empastes"
IdSitC: 1
```

---

### 3. **TtosMed**

**Descripción:** Tratamientos médicos/dentales realizados.

**Uso:** Registra todos los actos clínicos efectivamente realizados al paciente.

#### Campos Principales:

| Campo | Tipo | Tamaño | Nulo | Descripción |
|-------|------|--------|------|-------------|
| **IdPac** | int | - | NO | 🔑 FK → Paciente |
| **NumTto** | smallint | - | NO | 🔑 Número de tratamiento (secuencial por paciente) |
| **IdTto** | int | - | SÍ | FK → TTratamientos (tipo de tratamiento) |
| **ZonasBoca** | tinyint | - | SÍ | Zonas de la boca afectadas |
| **PiezasNum** | numeric | - | SÍ | Número de piezas dentales |
| **ZonasPieza** | numeric | - | SÍ | Zona específica de la pieza |
| **StaTto** | tinyint | - | SÍ | Estado (0=Pendiente, 7=Realizado) |
| **FecIni** | smalldatetime | - | SÍ | Fecha de inicio |
| **FecFin** | smalldatetime | - | SÍ | Fecha de finalización |
| **IdCol** | int | - | SÍ | FK → Colaborador/Doctor que realizó |
| **Notas** | text | - | SÍ | Observaciones del tratamiento |
| **Importe** | numeric | - | SÍ | Importe del tratamiento |
| **Dto** | smallint | - | SÍ | Descuento (%) |
| **Pendiente** | float | - | SÍ | Importe pendiente de pago |
| **Tiempo** | int | - | SÍ | Tiempo empleado (minutos) |
| **Actos** | tinyint | - | SÍ | Número de actos/sesiones |
| **UniqueID** | int | - | SÍ | ID único global |

#### Relaciones:
- **N → 1** con `Pacientes` (Muchos tratamientos de un paciente)
- **N → 1** con `TTratamientos` (Muchos usos de un tipo de tratamiento)
- **1 → N** con `TtosMedSes` (Un tratamiento tiene muchas sesiones)

#### Ejemplo de Registro:
```sql
IdPac: 3
NumTto: 1
IdTto: 570
StaTto: 7  (Realizado)
FecIni: 2014-06-25
Notas: "empieza tratamiento .empastes"
Importe: 50.00
Pendiente: 0.00
```

---

### 4. **Presu** (Presupuestos - Cabecera)

**Descripción:** Cabecera de los presupuestos.

**Uso:** Almacena el encabezado de cada presupuesto generado.

#### Campos Principales:

| Campo | Tipo | Tamaño | Nulo | Descripción |
|-------|------|--------|------|-------------|
| **IdPac** | int | - | NO | 🔑 FK → Paciente |
| **NumSerie** | smallint | - | NO | 🔑 Número de serie |
| **NumPre** | smallint | - | NO | 🔑 Número de presupuesto |
| **Descripcio** | varchar | 255 | SÍ | Descripción del presupuesto |
| **Direccion** | varchar | 80 | SÍ | Dirección (del momento) |
| **CP** | varchar | 20 | SÍ | Código postal |
| **IdPoblacio** | smallint | - | SÍ | FK → Población |
| **FecPre** | smalldatetime | - | SÍ | Fecha del presupuesto |
| **FecAcepta** | smalldatetime | - | SÍ | Fecha de aceptación |
| **IdCol** | int | - | SÍ | FK → Colaborador que lo emite |
| **IdCli** | int | - | SÍ | FK → Cliente (compañía de seguros) |
| **ImportePre** | float | - | SÍ | Importe total del presupuesto |
| **Dto** | smallint | - | SÍ | Descuento general (%) |
| **StaPre** | tinyint | - | SÍ | Estado (0=Pendiente, 1=Aceptado, 2=Rechazado) |

#### Relaciones:
- **N → 1** con `Pacientes` (Un paciente tiene muchos presupuestos)
- **1 → N** con `PresuTto` (Un presupuesto tiene muchas líneas)

#### Ejemplo de Registro:
```sql
IdPac: 743
NumSerie: 0
NumPre: 1
Descripcio: "Traspasado de EURODENT"
FecPre: 2005-12-31
ImportePre: 887
StaPre: 0
```

---

### 5. **PresuTto** (Presupuestos - Detalle)

**Descripción:** Líneas de tratamientos dentro de cada presupuesto.

**Uso:** Cada línea es un tratamiento incluido en el presupuesto.

#### Campos Principales:

| Campo | Tipo | Tamaño | Nulo | Descripción |
|-------|------|--------|------|-------------|
| **Id_Presu** | int | - | NO | 🔑 ID único de la línea (PK) |
| **IdPac** | int | - | NO | FK → Paciente |
| **NumSerie** | smallint | - | NO | FK → Presu (NumSerie) |
| **NumPre** | smallint | - | NO | FK → Presu (NumPre) |
| **LinPre** | smallint | - | NO | Número de línea en el presupuesto |
| **IdTto** | int | - | SÍ | FK → TTratamientos |
| **PiezasNum** | numeric | - | SÍ | Número de piezas |
| **ZonasPieza** | numeric | - | SÍ | Zonas de piezas dentales |
| **Unidades** | int | - | SÍ | Cantidad de unidades |
| **ImportePre** | float | - | SÍ | Importe de la línea |
| **Dto** | smallint | - | SÍ | Descuento (%) |
| **Notas** | text | - | SÍ | Notas del tratamiento |
| **FecAcepta** | smalldatetime | - | SÍ | Fecha de aceptación específica |
| **ImporteIVA** | float | - | SÍ | Importe del IVA |
| **BaseImponible** | float | - | SÍ | Base imponible |

#### Relaciones:
- **N → 1** con `Presu` (Muchas líneas de un presupuesto)
- **N → 1** con `TTratamientos` (Muchos usos de un tratamiento)

#### Ejemplo de Registro:
```sql
Id_Presu: 1
IdPac: 18
NumSerie: 0
NumPre: 1
LinPre: 1
IdTto: 570
Unidades: 1
ImportePre: 50
Dto: 0
```

---

### 6. **PagoCli** (Pagos de Cliente)

**Descripción:** Registro de todos los pagos realizados.

**Uso:** Cada vez que un cliente/paciente paga, se crea un registro aquí.

#### Campos Principales:

| Campo | Tipo | Tamaño | Nulo | Descripción |
|-------|------|--------|------|-------------|
| **IdPagoCli** | int | - | NO | 🔑 ID único del pago (PK) |
| **IdCli** | int | - | NO | FK → Cliente que paga |
| **Pagado** | float | - | NO | Importe pagado |
| **FecPago** | smalldatetime | - | NO | Fecha del pago |
| **IdForPago** | int | - | NO | FK → Forma de pago |
| **IdBanco** | smallint | - | SÍ | FK → Banco (si es transferencia/tarjeta) |
| **NumIngre** | varchar | 100 | SÍ | Número de ingreso/operación |
| **IdUser** | smallint | - | SÍ | FK → Usuario que registró |
| **NFactura** | varchar | 20 | SÍ | Número de factura asociada |
| **IdAnulado** | int | - | SÍ | Si está anulado, ID del pago que lo anula |
| **IdCentro** | int | - | SÍ | FK → Centro donde se realizó |

#### Relaciones:
- **N → 1** con `Clientes` (Muchos pagos de un cliente)
- **N → 1** con `FormasPago` (Muchos pagos con una forma de pago)
- **N → M** con `DeudaCli` (a través de tabla intermedia)

#### Ejemplo de Registro:
```sql
IdPagoCli: 2355
IdCli: 1647
Pagado: 390.00
FecPago: 1967-01-21
IdForPago: 14
IdCentro: 2
```

---

### 7. **DeudaCli** (Deuda de Cliente)

**Descripción:** Registro de deuda pendiente de cobro.

**Uso:** Cada tratamiento/factura genera una línea de deuda que se va liquidando con pagos.

#### Campos Principales:

| Campo | Tipo | Tamaño | Nulo | Descripción |
|-------|------|--------|------|-------------|
| **IdDeudaCli** | int | - | NO | 🔑 ID único (PK) |
| **IdCli** | int | - | NO | FK → Cliente |
| **IdPac** | int | - | SÍ | FK → Paciente |
| **NumTto** | smallint | - | SÍ | FK → Tratamiento relacionado |
| **FecPlazo** | smalldatetime | - | NO | Fecha de vencimiento |
| **Adeudo** | float | - | NO | Importe adeudado inicialmente |
| **Pendiente** | float | - | SÍ | Importe pendiente actual |
| **Liquidado** | bit | - | NO | ¿Está totalmente pagado? |
| **NFactura** | varchar | 20 | SÍ | Número de factura |
| **Incobrable** | smalldatetime | - | SÍ | Marcado como incobrable |
| **IdCentro** | int | - | SÍ | FK → Centro |

#### Relaciones:
- **N → 1** con `Clientes` (Muchas deudas de un cliente)
- **N → 1** con `Pacientes` (Muchas deudas de un paciente)
- **N → M** con `PagoCli` (se van liquidando con pagos)

#### Cálculo de Deuda Total:
```sql
SELECT SUM(Pendiente) AS DeudaTotal
FROM DeudaCli
WHERE IdPac = ? AND Liquidado = 0
```

#### Ejemplo de Registro:
```sql
IdDeudaCli: 9530
IdCli: 1647
IdPac: 1929
Adeudo: 390.00
Pendiente: 390.00
Liquidado: 0
FecPlazo: 1967-01-21
```

---

### 8. **TAntecedentes** (Antecedentes Médicos)

**Descripción:** Antecedentes médicos del paciente.

**Uso:** Historial médico importante (enfermedades, alergias, medicación).

#### Campos Principales:

| Campo | Tipo | Tamaño | Nulo | Descripción |
|-------|------|--------|------|-------------|
| **IdPac** | int | - | NO | 🔑 FK → Paciente |
| **IdAntecedente** | int | - | NO | 🔑 ID del antecedente |
| **TipoAntecedente** | int | - | NO | FK → Tipo (1=Enfermedad, 2=Alergia, etc.) |
| **Descripcion** | varchar | 255 | SÍ | Descripción del antecedente |
| **FecIns** | datetime | - | SÍ | Fecha de inserción |
| **Fecha** | datetime | - | SÍ | Fecha del antecedente |
| **IdUsu** | int | - | NO | FK → Usuario que lo registró |
| **Publico** | char | 1 | NO | ¿Es visible públicamente? |
| **Status** | int | - | SÍ | Estado (activo/inactivo) |
| **Inactivo** | smalldatetime | - | SÍ | Fecha de inactivación |

#### Relaciones:
- **N → 1** con `Pacientes` (Un paciente tiene muchos antecedentes)
- **N → 1** con `TTipoAntecedentes` (Clasificación)

#### Ejemplo de Registro:
```sql
IdPac: 2
IdAntecedente: 55
TipoAntecedente: 1
Descripcion: "KETROFENO PENICILINA NIQUEL"
Status: 1
```

---

### 9. **AlertPac** (Alertas del Paciente)

**Descripción:** Alertas y avisos importantes del paciente.

**Uso:** Mensajes que deben mostrarse al abrir la ficha del paciente.

#### Campos Principales:

| Campo | Tipo | Tamaño | Nulo | Descripción |
|-------|------|--------|------|-------------|
| **Id** | int | - | NO | 🔑 ID único (PK) |
| **IdCentro** | int | - | NO | FK → Centro |
| **IdPac** | int | - | NO | FK → Paciente |
| **NumAlerta** | smallint | - | NO | Número de alerta |
| **Texto** | varchar | 200 | SÍ | Texto de la alerta |
| **Marcado** | bit | - | NO | ¿Está marcado/resaltado? |
| **_version** | int | - | NO | Control de versión |
| **_fechaReg** | datetime | - | NO | Fecha de registro |
| **_idUserReg** | int | - | NO | Usuario que creó |

#### Relaciones:
- **N → 1** con `Pacientes` (Un paciente tiene muchas alertas)

#### Ejemplo de Registro:
```sql
Id: 129
IdPac: 2
NumAlerta: 1
Texto: "PENICILINA"
Marcado: 1
```

---

### 10. **TTratamientos** (Catálogo de Tratamientos)

**Descripción:** Catálogo maestro de tratamientos disponibles.

**Uso:** Lista de todos los tratamientos que se pueden realizar (empastes, limpiezas, etc.).

#### Campos Principales:

| Campo | Tipo | Tamaño | Nulo | Descripción |
|-------|------|--------|------|-------------|
| **IdTto** | int | - | NO | 🔑 ID único del tratamiento (PK) |
| **Codigo** | varchar | 20 | SÍ | Código del tratamiento |
| **Descripcio** | varchar | 255 | SÍ | Descripción |
| **IdFamili** | int | - | SÍ | FK → Familia de tratamientos |
| **IdSubFam** | int | - | SÍ | FK → Subfamilia |
| **Importe** | float | - | SÍ | Precio base |
| **Tiempo** | int | - | SÍ | Tiempo estimado (minutos) |
| **Activo** | bit | - | SÍ | ¿Está activo? |

#### Relaciones:
- **1 → N** con `TtosMed` (Se usa en muchos tratamientos realizados)
- **1 → N** con `PresuTto` (Se usa en muchos presupuestos)

---

### 11. **DocPac** (Documentos del Paciente)

**Descripción:** Documentos adjuntos al paciente.

**Uso:** PDFs, imágenes, radiografías, etc.

#### Campos Principales:

| Campo | Tipo | Tamaño | Nulo | Descripción |
|-------|------|--------|------|-------------|
| **Ident** | int | - | NO | 🔑 ID único del documento (PK) |
| **IdPac** | int | - | NO | FK → Paciente |
| **TipoDoc** | int | - | SÍ | Tipo de documento |
| **Ruta** | varchar | 500 | SÍ | Ruta del archivo |
| **Descripcion** | varchar | 255 | SÍ | Descripción |
| **Fecha** | datetime | - | SÍ | Fecha del documento |

---

### 12. **FormasPago** (Formas de Pago)

**Descripción:** Catálogo de formas de pago disponibles.

**Uso:** Efectivo, tarjeta, transferencia, etc.

#### Campos Principales:

| Campo | Tipo | Tamaño | Nulo | Descripción |
|-------|------|--------|------|-------------|
| **IdForPago** | int | - | NO | 🔑 ID (PK) |
| **Descripcio** | varchar | 50 | SÍ | Descripción (Efectivo, Tarjeta, etc.) |
| **Activo** | bit | - | SÍ | ¿Está activa? |

---

## 🔗 RELACIONES ENTRE TABLAS

### Diagrama de Relaciones Principales:

```
Pacientes (1) ───────┬─────── (N) DCitas
    │                │
    │                ├─────── (N) TtosMed
    │                │
    │                ├─────── (N) Presu ──── (N) PresuTto
    │                │
    │                ├─────── (N) AlertPac
    │                │
    │                ├─────── (N) TAntecedentes
    │                │
    │                └─────── (N) DocPac
    │
Clientes (1) ────────┬─────── (N) PagoCli
    │                │
    │                └─────── (N) DeudaCli
    │
TTratamientos (1) ───┬─────── (N) TtosMed
    │                │
    │                └─────── (N) PresuTto
```

---

## 📝 REGLAS DE NEGOCIO

### 1. NumPac (Número de Paciente)
- **Generación:** Secuencial simple
- **Formato:** Número entero (ej: 6213)
- **Cálculo:** `SELECT MAX(NumPac) + 1 FROM Pacientes`

### 2. Fechas en Gesden
- **Formato:** Días desde 30/12/1899 (OLE Automation)
- **Conversión a Python:**
  ```python
  fecha = datetime(1899, 12, 30) + timedelta(days=fecha_gesden)
  ```
- **Conversión a Gesden:**
  ```python
  dias = (fecha - datetime(1899, 12, 30)).days
  ```

### 3. Horas en Gesden
- **Formato:** HHMMSS * 100
- **Ejemplo:** 143000 = 14:30:00
- **Conversión:**
  ```python
  horas = hora_gesden // 10000
  minutos = (hora_gesden % 10000) // 100
  ```

### 4. Estados de Citas (IdSitC)
- `1` = Pendiente
- `2` = Realizada
- `3` = Cancelada
- `4` = No presentado

### 5. Estados de Tratamientos (StaTto)
- `0` = Pendiente
- `7` = Realizado
- `8` = Cancelado

### 6. Deuda y Pagos
- **Deuda Total:** `SUM(DeudaCli.Pendiente WHERE Liquidado = 0)`
- **Pagos Total:** `SUM(PagoCli.Pagado WHERE IdAnulado IS NULL)`

---

## 🔍 CONSULTAS ÚTILES

### Buscar Paciente:
```sql
SELECT IdPac, NumPac, Nombre, Apellidos, TelMovil
FROM Pacientes
WHERE Nombre LIKE '%JUAN%' 
  AND Apellidos LIKE '%GARCIA%'
```

### Citas del Día:
```sql
DECLARE @FechaHoy INT = DATEDIFF(DAY, '1899-12-30', GETDATE())

SELECT c.*, p.Nombre, p.Apellidos
FROM DCitas c
JOIN Pacientes p ON c.IdPac = p.IdPac
WHERE c.Fecha = @FechaHoy
ORDER BY c.Hora
```

### Deuda Pendiente de un Paciente:
```sql
SELECT SUM(Pendiente) AS DeudaTotal
FROM DeudaCli
WHERE IdPac = 123 
  AND Liquidado = 0
```

### Historial de Tratamientos:
```sql
SELECT t.NumTto, tt.Descripcio, t.FecIni, t.Notas, t.Importe
FROM TtosMed t
JOIN TTratamientos tt ON t.IdTto = tt.IdTto
WHERE t.IdPac = 123
ORDER BY t.FecIni DESC
```

### Presupuestos Pendientes:
```sql
SELECT p.*, COUNT(pt.LinPre) AS NumLineas
FROM Presu p
LEFT JOIN PresuTto pt ON p.IdPac = pt.IdPac 
  AND p.NumSerie = pt.NumSerie 
  AND p.NumPre = pt.NumPre
WHERE p.IdPac = 123 
  AND p.StaPre = 0
GROUP BY p.IdPac, p.NumSerie, p.NumPre, ...
```

---

## ⚙️ CONFIGURACIÓN DEL SISTEMA

### Centros:
- **IdCentro = 2** → Centro principal (GABINETE2)

### Usuarios/Colaboradores:
- Tabla: `TColabos`
- Cada doctor tiene un `IdCol`

### Contadores:
- Tabla: `Contadores`
- Controla secuencias de IDs

---

## 📌 NOTAS IMPORTANTES PARA LA IA

1. **MAYÚSCULAS:** Nombre y Apellidos SIEMPRE en mayúsculas
2. **Fechas:** Convertir siempre usando función de conversión
3. **Duplicados:** Validar ANTES de insertar
4. **Transacciones:** Usar BEGIN/COMMIT/ROLLBACK
5. **Logging:** Registrar todas las operaciones
6. **IdCentro:** Siempre usar el centro correcto (2)
7. **Validaciones:** Comprobar FK antes de insertar

---

## 🎯 ESCENARIOS DE USO

### Crear Paciente:
1. Validar duplicados (nombre, apellidos, teléfono)
2. Obtener siguiente NumPac
3. Insertar en Pacientes
4. Logging

### Crear Cita:
1. Buscar paciente
2. Convertir fecha y hora a formato Gesden
3. Obtener siguiente IdOrden
4. Insertar en DCitas
5. Logging

### Crear Presupuesto:
1. Buscar paciente
2. Insertar cabecera en Presu
3. Insertar líneas en PresuTto
4. Calcular totales
5. Logging

### Registrar Pago:
1. Validar cliente
2. Insertar en PagoCli
3. Actualizar DeudaCli (restar de Pendiente)
4. Si Pendiente = 0, marcar Liquidado = 1
5. Logging

---

**Documento creado:** 29/11/2024  
**Versión:** 1.0  
**Para:** Agente IA Gesden
