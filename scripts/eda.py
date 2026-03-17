#!/usr/bin/env python3
"""
Script de Análisis Exploratorio de Datos (EDA)
Genera un reporte PDF con información relevante del dataset.
"""

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import os
import sys

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)


def load_data(filepath):
    """Carga el archivo según su extensión (CSV o Excel)."""
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.csv':
        return pd.read_csv(filepath)
    elif ext in ('.xlsx', '.xls'):
        return pd.read_excel(filepath)


def create_pdf_report(data, output_path):
    """Genera un reporte PDF con los análisis solicitados."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Reporte de Análisis Exploratorio", ln=True, align='C')
    pdf.ln(10)

    # 1. Tipos de datos
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "1. Tipos de datos por columna", ln=True)
    pdf.set_font("Arial", "", 10)
    dtypes_info = data.dtypes.to_string()
    pdf.multi_cell(0, 5, dtypes_info)
    pdf.ln(5)

    # 2. Valores faltantes
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "2. Análisis de valores faltantes", ln=True)
    pdf.set_font("Arial", "", 10)
    missing = data.isnull().sum()
    missing_pct = (missing / len(data)) * 100
    missing_df = pd.DataFrame({'Total': missing, 'Porcentaje': missing_pct})
    pdf.multi_cell(0, 5, missing_df.to_string())
    pdf.ln(5)

    # 3. Histogramas (distribuciones)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "3. Distribuciones de variables numéricas", ln=True)
    numeric_cols = data.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        # Crear varios histogramas en una figura
        n_cols = min(3, len(numeric_cols))
        n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(5*n_cols, 4*n_rows))
        axes = axes.flatten() if n_rows * n_cols > 1 else [axes]
        for i, col in enumerate(numeric_cols):
            data[col].hist(ax=axes[i], bins=30, edgecolor='black')
            axes[i].set_title(col)
        # Ocultar ejes sobrantes
        for j in range(i+1, len(axes)):
            axes[j].set_visible(False)
        plt.tight_layout()
        hist_path = os.path.join(os.path.dirname(output_path), 'temp_hist.png')
        plt.savefig(hist_path, dpi=100)
        plt.close()
        pdf.image(hist_path, w=180)
        os.remove(hist_path)
    else:
        pdf.cell(0, 10, "No hay variables numéricas.", ln=True)
    pdf.ln(5)

    # 4. Matriz de correlación
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "4. Matriz de correlación", ln=True)
    if len(numeric_cols) > 1:
        plt.figure(figsize=(8, 6))
        corr = data[numeric_cols].corr()
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Matriz de Correlación')
        corr_path = os.path.join(os.path.dirname(output_path), 'temp_corr.png')
        plt.savefig(corr_path, dpi=100)
        plt.close()
        pdf.image(corr_path, w=160)
        os.remove(corr_path)
    else:
        pdf.cell(0, 10, "Se necesitan al menos dos variables numéricas para correlación.", ln=True)
    pdf.ln(5)

    # 5. Boxplots (outliers)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "5. Detección de outliers (boxplots)", ln=True)
    if len(numeric_cols) > 0:
        # Crear boxplots agrupados
        n_cols = min(3, len(numeric_cols))
        n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(5*n_cols, 4*n_rows))
        axes = axes.flatten() if n_rows * n_cols > 1 else [axes]
        for i, col in enumerate(numeric_cols):
            data.boxplot(column=col, ax=axes[i])
            axes[i].set_title(col)
        for j in range(i+1, len(axes)):
            axes[j].set_visible(False)
        plt.tight_layout()
        box_path = os.path.join(os.path.dirname(output_path), 'temp_box.png')
        plt.savefig(box_path, dpi=100)
        plt.close()
        pdf.image(box_path, w=180)
        os.remove(box_path)
    else:
        pdf.cell(0, 10, "No hay variables numéricas para boxplots.", ln=True)

    # Guardar PDF
    pdf.output(output_path)
    print(f"Reporte generado exitosamente: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Genera un reporte EDA en PDF a partir de un archivo tabular.")
    parser.add_argument('-i', '--input', required=True, help='Ruta al archivo de entrada (CSV o Excel)')
    parser.add_argument('-o', '--output', required=True, help='Ruta de salida para el reporte PDF')
    args = parser.parse_args()

    # Crear directorio de salida si no existe
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    try:
        data = load_data(args.input)
        create_pdf_report(data, args.output)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()