# Proyecto de Análisis Exploratorio Automatizado

Este proyecto implementa un pipeline que lee un archivo tabular (CSV o Excel) y genera automáticamente un reporte en PDF con análisis exploratorio de datos (EDA).

## Contenido del repositorio

- `scripts/eda.py`: Script principal que realiza el análisis y genera el PDF.
- `main.sh`: Script ejecutable que orquesta el pipeline.
- `requirements.txt`: Dependencias de Python necesarias.
- `.gitignore`: Archivos y carpetas ignorados por git (incluye `data/`).
- `LICENSE.md`: Licencia del proyecto (opcional).
- `README.md`: Este documento.

## Requisitos

- Python 3.7 o superior.
- Instalar las dependencias:
  ```bash
  pip install -r requirements.txt
   ```
   
## Modo de uso

```bash
  ./main.sh
```

## Output

Se genera:

- `Reporte.pdf` con:

	- Tipos de datos

	- Missing values

	- Distribuciones

	- Correlaciones

	- Outliers

