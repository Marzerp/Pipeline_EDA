#!/bin/bash
# Pipeline de análisis exploratorio

# Definir rutas
DATA_FILE="data/Base.xlsx"        
OUTPUT_DIR="out"
REPORT_FILE="${OUTPUT_DIR}/Reporte.pdf"

# Verificar que existe el archivo de datos
if [ ! -f "$DATA_FILE" ]; then
    echo "Error: No se encuentra el archivo de datos en $DATA_FILE"
    exit 1
fi

# Crear carpeta de salida si no existe
mkdir -p "$OUTPUT_DIR"

# Ejecutar script de Python
python3 scripts/eda.py -i "$DATA_FILE" -o "$REPORT_FILE"

# Mensaje
if [ $? -eq 0 ]; then
    echo "Pipeline completado. Revisa el reporte en $REPORT_FILE"
else
    echo "Ocurrió un error durante la ejecución."
    exit 1
fi