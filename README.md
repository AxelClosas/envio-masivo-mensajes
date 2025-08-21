## Pasos para ejecutar el script
1. Clonar el repositorio (opcional - Se puede descargar la carpeta)
2. Crear el entorno virtual de python con el siguiente comando:
```bash
python -m venv venv
```
o
```bash
py -m venv venv
```
3. Activar el entorno virtual con el siguiente comando. Usar PowerShell
```bash
.\venv\Scripts\Activate.ps1
```
4. Instalar los requerimientos del proyecto de python
```bash
pip install -r req.txt
```
5. Guarda el archivo .csv para extraer la información en la misma carpeta del script. En este caso se llama enviar.csv
6. Ejecuta el script de python para generar la estructura .json que usará el script de Javascript
```bash
python main.py
```
o
```bash
py main.py
```
7. Instala las dependencias que necesita el script javascript
```bash
npm install
```
8. Ejecuta el script main.js con el siguiente comando:
```bash
node main.js
```
9. Sigue las instrucciones que se muestren en la terminal