#------------------------------------------------------------------------------------------------
#MATRIZ INVERSA POR COFACTORES Y ADJUNTA - GENERADOR DE DOCUMENTO LaTeX
#------------------------------------------------------------------------------------------------
from pylatex import Document, Section, Subsection, Math, NoEscape
import sympy as sp


def leer_matriz_consola():
    print("Introduce la matriz línea por línea (valores separados por comas). Ejemplo: 1,2,3")
    filas = []
    while True:
        linea = input("Fila (vacía para terminar): ").strip()
        if linea == "":
            break
        valores = [sp.sympify(x) for x in linea.split(",")]
        filas.append(valores)
    if not filas:
        raise ValueError("No se ingresó ninguna fila.")
    ncols = len(filas[0])
    for f in filas:
        if len(f) != ncols:
            raise ValueError("Todas las filas deben tener el mismo número de columnas.")
    return sp.Matrix(filas)


def matriz_to_latex(M):
    return NoEscape(sp.latex(M))


def generar_documento(M, nombre_tex='inversa_procedimiento.tex'):
    doc = Document(documentclass='article')
    doc.preamble.append(NoEscape(r'\usepackage[utf8]{inputenc}'))
    doc.preamble.append(NoEscape(r'\usepackage{amsmath, amssymb}'))

    doc.append(NoEscape(r'\title{Cálculo de la inversa por cofactores y adjunta}'))
    doc.append(NoEscape(r'\author{Generado con Python y PyLaTeX}'))
    doc.append(NoEscape(r'\date{}'))
    doc.append(NoEscape(r'\maketitle'))

    with doc.create(Section('Matriz inicial')):
        doc.append(Math(data=[matriz_to_latex(M)]))

    det = sp.simplify(M.det())
    with doc.create(Section('Determinante')):
        doc.append(NoEscape('El determinante de la matriz es:'))
        doc.append(Math(data=[NoEscape(sp.latex(det))]))

    if det == 0:
        with doc.create(Section('Conclusión')):
            doc.append('La matriz es singular (determinante = 0), por lo tanto no tiene inversa.')
        doc.generate_tex(nombre_tex.replace('.tex', ''))
        print(f"Documento .tex generado: {nombre_tex}")
        return

    n = M.rows

    # Calcular matriz de cofactores paso a paso
    with doc.create(Section('Cálculo de la matriz de cofactores')):
        for i in range(n):
            for j in range(n):
                # Menor y cofactor
                minor_mat = M.minor_submatrix(i, j)
                minor_det = sp.simplify(minor_mat.det())
                cofactor = sp.simplify(((-1)**(i+j)) * minor_det)
                texto = NoEscape(r'$C_{%d%d} = (-1)^{%d+%d}\det(%s) = %s$' % (
                    i+1, j+1, i+1, j+1, sp.latex(minor_mat), sp.latex(cofactor)))
                doc.append(Math(data=[texto]))

    # Construir matriz de cofactores
    cofactor_mat = M.cofactor_matrix()
    with doc.create(Subsection('Matriz de cofactores completa')):
        doc.append(Math(data=[matriz_to_latex(cofactor_mat)]))

    # Adjunta (traspuesta de la de cofactores)
    adj = cofactor_mat.T
    with doc.create(Subsection('Adjunta de la matriz')):
        doc.append(NoEscape('La adjunta es la traspuesta de la matriz de cofactores:'))
        doc.append(Math(data=[matriz_to_latex(adj)]))

    # Inversa final
    inv = sp.simplify(adj / det)
    with doc.create(Section('Matriz inversa')):
        doc.append(NoEscape(r'Usando $A^{-1} = \frac{1}{\det(A)}\operatorname{adj}(A)$:'))
        doc.append(Math(data=[NoEscape(r'A^{-1} = \frac{1}{%s}%s' % (sp.latex(det), sp.latex(adj)))]))
        doc.append(NoEscape('Simplificando:'))
        doc.append(Math(data=[matriz_to_latex(inv)]))

    doc.generate_tex(nombre_tex.replace('.tex', ''))
    print(f"Archivo LaTeX generado: {nombre_tex}")


if __name__ == '__main__':
    print('=== Cálculo de matriz inversa paso a paso ===')
    M = leer_matriz_consola()
    print('Matriz ingresada:')
    print(M)
    generar_documento(M)
