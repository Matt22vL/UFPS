import random
from pylatex import Document, Section, Math

def matriz_diagonal(n):
    """Genera matriz diagonal nxn con valores aleatorios en la diagonal."""
    return [[random.randint(1, 9) if i == j else 0 for j in range(n)] for i in range(n)]

def matriz_triangular_superior(n):
    """Genera matriz triangular superior nxn con valores aleatorios."""
    return [[random.randint(1, 9) if j >= i else 0 for j in range(n)] for i in range(n)]

def matriz_triangular_inferior(n):
    """Genera matriz triangular inferior nxn con valores aleatorios."""
    return [[random.randint(1, 9) if j <= i else 0 for j in range(n)] for i in range(n)]

def matriz_to_latex(matriz):
    """Convierte una matriz a cadena con formato LaTeX bajo entorno bmatrix."""
    filas = [" & ".join(str(x) for x in fila) for fila in matriz]
    return r"\begin{bmatrix}" + " \\\\ ".join(filas) + r"\end{bmatrix}"

def generar_documento(tipo, n=4):
    if tipo == "diagonal":
        matriz = matriz_diagonal(n)
    elif tipo == "triangular_superior":
        matriz = matriz_triangular_superior(n)
    elif tipo == "triangular_inferior":
        matriz = matriz_triangular_inferior(n)
    else:
        raise ValueError("Tipo de matriz no reconocido. Elija: diagonal, triangular_superior, triangular_inferior.")
    
    latex_str = matriz_to_latex(matriz)
    doc = Document()
    with doc.create(Section(f"Matriz tipo: {tipo}, tamaño {n}x{n}")):
        doc.append(Math(data=[latex_str]))
    nombre_archivo = f"matriz_{tipo}.tex"
    doc.generate_tex(nombre_archivo)
    print(f"Documento generado: {nombre_archivo}")

if __name__ == "__main__":
    print("Tipos válidos: diagonal, triangular_superior, triangular_inferior")
    tipo = input("Ingrese el tipo de matriz: ").strip().lower()
    n = int(input("Ingrese el tamaño de la matriz (nxn): "))
    generar_documento(tipo, n)
