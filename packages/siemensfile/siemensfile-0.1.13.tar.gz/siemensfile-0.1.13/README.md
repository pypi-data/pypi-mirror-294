# SIEMENSFile

**SIEMENSFile** es un paquete para leer y procesar archivos `.dat` de Siemens y realizar reconstrucciones de imágenes de resonancia magnética (MRI). Este paquete facilita la extracción de datos del rawdata y su reconstrucción preliminar en imágenes utilizando transformadas rápidas de Fourier (FFT), la unica reconstruccion implementada es la Cartesiana, proximamente la reconstruccion No Cartesiana.

## Instalación

Puedes instalar el paquete directamente desde PyPI con el siguiente comando:

```bash
pip install siemensfile

```
# Importar la función siemensfile desde el paquete
from siemensfile import siemensfile

# Usar la función siemensfile para procesar un archivo .dat
[metadata, rawdata] = siemensfile(r'tests/datatest/siemens_file_test_cartesian_sample.dat', reconstruction="Cartesiana")

# Ver los resultados
print("Metadata:", metadata)
print("Raw Data:", rawdata)
    
    ```