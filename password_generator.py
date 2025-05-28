#!/usr/bin/env python3
# password_generator.py – Generador + verificador + QR con parámetros CLI
# Requisitos: pip install requests qrcode[pil]
# APIs utilizadas: https://api.genratr.com/ https://api.pwnedpasswords.com/range/

import argparse
import requests
import hashlib
import qrcode

def generar_contraseña(longitud, numeros, especiales, mayus):
    # Genera una contraseña usando la API de Genratr
    url = 'https://api.genratr.com/'
    params = {
        'length': longitud
    }
    
    # Añadimos los parámetros según las opciones seleccionadas
    if numeros:
        params['numbers'] = ''
    if especiales:
        params['special'] = ''
    if mayus:
        params['uppercase'] = ''
    
    # Por defecto siempre incluimos minúsculas
    params['lowercase'] = ''
    
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()  # Lanza excepción si hay error HTTP
        data = r.json()
        
        # Verificamos si hay error en la respuesta
        if 'error' in data:
            print(f"[-] Error de la API: {data['error']}")
            return None
            
        return data['password']
    except requests.exceptions.RequestException as e:
        print(f"[-] Error conectando a la API: {e}")
        return None
    except KeyError:
        print("[-] Respuesta de API inesperada")
        return None

def comprobar_pwned(password):
    # Comprueba si la contraseña está en Have I Been Pwned
    try:
        sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefijo, sufijo = sha1[:5], sha1[5:]
        r = requests.get(f'https://api.pwnedpasswords.com/range/{prefijo}', timeout=10)
        r.raise_for_status()
        
        for linea in r.text.splitlines():
            if ':' in linea:  # Verificamos que la línea tenga el formato correcto
                h, cuenta = linea.split(':')
                if h == sufijo:
                    return int(cuenta)
        return 0
    except requests.exceptions.RequestException as e:
        print(f"[-] Error verificando Have I Been Pwned: {e}")
        return -1  # Devolvemos -1 para indicar error
    except ValueError:
        print("[-] Error procesando respuesta de Have I Been Pwned")
        return -1

def generar_qr(password, fichero):
    # Genera un código QR con la contraseña
    try:
        img = qrcode.make(password)
        img.save(fichero)
        return True
    except Exception as e:
        print(f"[-] Error generando QR: {e}")
        return False

def main():
    p = argparse.ArgumentParser(
        description="Genera una contraseña segura, verifica en Have I Been Pwned y crea un código QR",
        epilog="Ejemplos de uso:\n"
               "  python password_generator.py                   # Contraseña completa de 12 caracteres\n"
               "  python password_generator.py -l 20 -s          # 20 caracteres sin símbolos especiales\n"
               "  python password_generator.py -n -s -u          # Solo letras minúsculas\n"
               "  python password_generator.py -f mi_qr.png      # Guardar QR con nombre personalizado",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument('-l', '--length', type=int, default=12, metavar='N',
                   help='longitud de la contraseña (por defecto: 12)')
    p.add_argument('-n', '--no-numbers', action='store_true',
                   help='excluir números de la contraseña')
    p.add_argument('-s', '--no-special', action='store_true',
                   help='excluir caracteres especiales (símbolos)')
    p.add_argument('-u', '--no-caps', action='store_true',
                   help='excluir letras mayúsculas')
    p.add_argument('-f', '--file', default='password.png', metavar='ARCHIVO',
                   help='nombre del archivo para guardar el QR (por defecto: password.png)')
    p.add_argument('--version', action='version', version='password_generator 1.0')
    args = p.parse_args()
    
    
    # Validamos la longitud
    if args.length < 4 or args.length > 50:
        print("[-] ERROR: La longitud debe estar entre 4 y 50 caracteres")
        return

    # Validamos que al menos una opción esté seleccionada
    if args.no_numbers and args.no_special and args.no_caps:
        print("[-] ERROR: Al menos debes incluir números, caracteres especiales o mayúsculas")
        print("    (Las minúsculas siempre se incluyen)")
        return

    print("=" * 46)
    print("           GENERADOR DE CONTRASEÑAS")
    print("           © 2025 - Victor Belmonte")
    print("=" * 46)
    print()
    print(f"[*] Generando contraseña de {args.length} caracteres...")
    
    # Generamos la contraseña
    pwd = generar_contraseña(
        longitud=args.length,
        numeros=not args.no_numbers,
        especiales=not args.no_special,
        mayus=not args.no_caps
    )
    
    if pwd is None:
        print("[-] ERROR: No se pudo generar la contraseña")
        return
    
    # Mostramos la contraseña generada
    print(f"[+] Contraseña generada: {pwd}")
    print()

    # Verificamos en Have I Been Pwned
    passwd_filtered = False
    print("[*] Verificando en Have I Been Pwned...\n")
    veces = comprobar_pwned(pwd)
    if veces == -1:
        print("[⚠︎ ] ADVERTENCIA: No se pudo verificar en Have I Been Pwned")
        passwd_filtered = True
    elif veces > 0:
        print(f"[!] PELIGRO: Apareció {veces} veces en filtraciones conocidas")
        print("\n[+] Recomendación: Genera otra contraseña")
        passwd_filtered = True
    else:
        print("[+] SEGURO: No aparece en filtraciones conocidas")
    
    print()

    # Generamos el QR
    if passwd_filtered == True:
        print("=" * 60)
        print("\n[-] QR no generado debido a la filtración de la contraseña \n    y/o falta de verificación en Have I Been Pwned\n")
        print("[+] Recomendación: Genera otra contraseña segura")
        print()
        print("=" * 60)
        return
    
    print(f"[*] Generando código QR en {args.file}...")
    if generar_qr(pwd, args.file):
        print(f"[+] QR guardado correctamente en {args.file}")
    else:
        print("[-] ERROR: No se pudo generar el código QR")
    
    print()
    print("=" * 46)
    print("[ ✓ ] PROCESO COMPLETADO EXITOSAMENTE")
    print("=" * 46)

if __name__ == "__main__":
    main()