# passwordGenerator
Script en Python para generar contraseñas seguras y personalizables por CLI

# 🔐 Generador de Contraseñas Seguras
### Herramienta CLI con Verificación Have I Been Pwned y Código QR

[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Security](https://img.shields.io/badge/security-HIBP%20verified-red.svg)](https://haveibeenpwned.com/)

---

## 📋 Tabla de Contenidos

1. [Descripción](#-descripción)
2. [Características](#-características)
3. [Instalación](#-instalación)
4. [Uso](#-uso)
5. [Ejemplos](#-ejemplos)
6. [APIs Utilizadas](#-apis-utilizadas)
7. [Seguridad](#-seguridad)
8. [Contribución](#-contribución)

---

## 🎯 Descripción

**Password Generator** es una herramienta de línea de comandos desarrollada en Python que combina tres funcionalidades esenciales para la gestión segura de contraseñas:

- **🎲 Generación**: Contraseñas aleatorias con parámetros personalizables
- **🔍 Verificación**: Comprobación automática contra filtraciones conocidas (Have I Been Pwned)
- **📱 Visualización**: Códigos QR para fácil transferencia a dispositivos móviles

> [!IMPORTANT]
> Esta herramienta está diseñada para uso educativo y personal. Para entornos de producción críticos, realiza una revisión adicional de seguridad.

---

## ✨ Características

### 🛠️ Funcionalidades Principales

| Característica | Descripción |
|---|---|
| **Generación Personalizable** | Longitud configurable (4-50 caracteres) |
| **Tipos de Caracteres** | Números, símbolos especiales, mayúsculas/minúsculas |
| **Verificación Have I Been Pwned** | Protocolo k-anonymity para máxima privacidad |
| **Códigos QR** | Generación automática para transferencia móvil |
| **Interfaz CLI** | Argumentos intuitivos con validaciones |
| **Manejo de Errores** | Gestión robusta de fallos de red y API |

### 🎨 Interfaz de Usuario

```
==============================================
           GENERADOR DE CONTRASEÑAS
           © 2025 - Victor Belmonte
==============================================

[*] Generando contraseña de 16 caracteres...
[+] Contraseña generada: K9$mPx2Qw7nF!8aE
[*] Verificando en Have I Been Pwned...
[+] SEGURO: No aparece en filtraciones conocidas
[*] Generando código QR en password.png...
[+] QR guardado correctamente en password.png

==============================================
[ ✓ ] PROCESO COMPLETADO EXITOSAMENTE
==============================================
```

---

## 🚀 Instalación

### 1️⃣ Requisitos del Sistema

| Componente | Versión Mínima | Propósito |
|---|---|---|
| **Python** | 3.6+ | Lenguaje base |
| **pip** | 20.0+ | Gestor de paquetes |
| **Conexión a Internet** | - | APIs externas |

### 2️⃣ Instalación de Dependencias

```bash
# Clonar el repositorio
git clone https://github.com/victorbelmontee/passwordGenerator.git
cd passwordGenerator

# Instalar dependencias
pip install -r requirements.txt
```

### 3️⃣ Verificar Instalación

```bash
python password_generator.py --version
# Salida esperada: password_generator 1.0
```

> [!NOTE]
> La opción `qrcode[pil]` incluye PIL (Python Imaging Library) necesaria para generar imágenes PNG.

---

## 💻 Uso

### Sintaxis Básica

```bash
python password_generator.py [opciones]
```

### Argumentos Disponibles

| Argumento | Forma Corta | Descripción | Valor por Defecto |
|---|---|---|---|
| `--length` | `-l` | Longitud de contraseña | 12 |
| `--no-numbers` | `-n` | Excluir números (0-9) | False |
| `--no-special` | `-s` | Excluir símbolos (!@#$...) | False |
| `--no-caps` | `-u` | Excluir mayúsculas (A-Z) | False |
| `--file` | `-f` | Nombre archivo QR | password.png |
| `--version` | - | Mostrar versión del script | - |

> [!TIP]
> Las letras minúsculas (a-z) siempre se incluyen para garantizar contraseñas válidas.

### Validaciones Automáticas

- **Longitud**: Entre 4 y 50 caracteres
- **Tipos de caracteres**: Al menos uno además de minúsculas
- **Conectividad**: Verificación de APIs disponibles

---

## 📚 Ejemplos

### Uso Básico

```bash
# Contraseña estándar de 12 caracteres (recomendado)
python password_generator.py
```

### Contraseñas Personalizadas

```bash
# Contraseña larga sin símbolos especiales
python password_generator.py -l 20 -s

# Solo letras (sin números ni símbolos)
python password_generator.py -n -s

# Contraseña corta para sistemas legacy
python password_generator.py -l 8

# QR con nombre personalizado
python password_generator.py -f mi_password_segura.png
```

### Casos de Uso Avanzados

```bash
# Máxima seguridad (50 caracteres, todos los tipos)
python password_generator.py -l 50

# Compatible con sistemas restrictivos (solo alfanumérico)
python password_generator.py -s
```

---

## 🌐 APIs Utilizadas

### 1️⃣ Genratr API - Generación de Contraseñas

**Endpoint**: `https://api.genratr.com/`

| Parámetro | Tipo | Descripción | Ejemplo |
|---|---|---|---|
| `length` | integer | Longitud (4-128) | `?length=16` |
| `numbers` | boolean | Incluir dígitos | `&numbers=true` |
| `special` | boolean | Incluir símbolos | `&special=true` |
| `uppercase` | boolean | Incluir mayúsculas | `&uppercase=true` |

**Ejemplo de Respuesta**:

```json
{
  "password": "Kf9$mPx2Qw7n"
}
```

### 2️⃣ Have I Been Pwned API - Verificación de Seguridad

**Endpoint**: `https://api.pwnedpasswords.com/range/{hash-prefix}`

#### Protocolo k-anonymity

> [!IMPORTANT]
> **Privacidad garantizada**: Tu contraseña nunca se envía completa. Solo los primeros 5 caracteres del hash SHA-1.

**Proceso de Verificación**:

1. **Hash SHA-1** de la contraseña
2. **División**: Prefijo (5 chars) + Sufijo (35 chars)
3. **Consulta**: Solo el prefijo se envía a la API
4. **Verificación local**: Búsqueda del sufijo en la respuesta

```python
# Ejemplo del proceso interno
password = "ejemplo123"
sha1_hash = "A94A8FE5CCB19BA61C4C0873D391E987982FBBD3"
prefijo = "A94A8"  # Se envía a la API
sufijo = "FE5CCB19BA61C4C0873D391E987982FBBD3"  # Se verifica localmente
```

**Interpretación de Resultados**:

| Valor | Significado | Acción Recomendada |
|---|---|---|
| `0` | ✅ Contraseña segura | Usar con confianza |
| `> 0` | ⚠️ Filtrada X veces | **Generar nueva** |
| `-1` | 🔄 Error de verificación | Reintentar |

---

## 🔒 Seguridad

### Principios de Privacidad

> [!IMPORTANT]
> **Zero-Knowledge**: El script nunca almacena, registra o transmite contraseñas completas.

| Aspecto | Implementación |
|---|---|
| **Transmisión** | Solo hash SHA-1 parcial (k-anonymity) |
| **Almacenamiento** | Sin logs ni archivos de contraseñas |
| **Códigos QR** | Contienen texto plano (eliminar después del uso) |
| **Timeouts** | 10 segundos máximo por consulta API |

### Recomendaciones de Uso

#### ✅ Buenas Prácticas

- **Longitud mínima**: 12 caracteres (16+ para alta seguridad)
- **Diversidad**: Incluir todos los tipos de caracteres
- **Unicidad**: Contraseña diferente por cada servicio
- **Gestión**: Usar administradores de contraseñas dedicados

#### ⚠️ Consideraciones Importantes

```bash
# ❌ Evitar: Contraseñas muy cortas
python password_generator.py -l 6

# ✅ Recomendado: Longitud segura
python password_generator.py -l 16

# ❌ Evitar: Solo un tipo de carácter
python password_generator.py -n -s -u

# ✅ Recomendado: Máxima diversidad
python password_generator.py -l 20
```

### Códigos de Estado

| Situación | Mensaje | Acción Recomendada |
|---|---|---|
| Sin conexión | `Error conectando a la API` | Verificar conectividad |
| Respuesta inválida | `Respuesta de API inesperada` | Reintentar más tarde |
| Contraseña comprometida | `PELIGRO: Apareció X veces` | **Generar nueva contraseña** |
| Error QR | `Error generando QR` | Verificar permisos de escritura |

---

## 🛡️ Manejo de Errores

### Validaciones de Entrada

```python
# Validación de longitud
if args.length < 4 or args.length > 50:
    print("[-] ERROR: La longitud debe estar entre 4 y 50 caracteres")

# Validación de tipos de caracteres
if args.no_numbers and args.no_special and args.no_caps:
    print("[-] ERROR: Al menos debes incluir números, caracteres especiales o mayúsculas")
```

### Gestión de Fallos de Red

```python
try:
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"[-] Error conectando a la API: {e}")
    return None
```

---

## 🤝 Contribución

¿Quieres mejorar el proyecto? ¡Las contribuciones son bienvenidas!

### Desarrollo

```bash
# Fork del repositorio
git fork https://github.com/victorbelmontee/passwordGenerator

# Crear rama de desarrollo
git checkout -b feature/nueva-funcionalidad

# Realizar cambios y commit
git commit -m "feat: añadir nueva funcionalidad"

# Push y crear Pull Request
git push origin feature/nueva-funcionalidad
```

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
