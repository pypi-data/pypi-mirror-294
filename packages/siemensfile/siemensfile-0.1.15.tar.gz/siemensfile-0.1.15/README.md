# SIEMENSFile

**SIEMENSFile** es un paquete para leer y procesar archivos `.dat` de Siemens y realizar reconstrucciones de imagenes de resonancia magnetica (MRI). Este paquete facilita la extraccion de datos del  `rawdata` y su reconstruccion preliminar en imagenes utilizando transformadas rapidas de Fourier (FFT). La única reconstruccion implementada es la cartesiana; proximamente se implementará la reconstruccion no cartesiana.

## Instalacion

Puedes instalar el paquete directamente desde PyPI con el siguiente comando:

```bash
pip install siemensfile
```
# Importar la funcion siemensfile desde el paquete
from siemensfile import siemensfile

# Usar la funcion siemensfile para procesar un archivo .dat

```bash
[metadata, rawdata] = siemensfile(r'tests/datatest/siemens_file_test_cartesian_sample.dat', reconstruction="Cartesiana")

```