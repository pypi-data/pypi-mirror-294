import matplotlib.pyplot as plt
import numpy as np
from siemensfile.utils import ifftnd, rms_comb


def reconstruct_image(rawdata, method="Cartesiana"):
    """
    Función para reconstruir imágenes desde los datos brutos, manejando múltiples cortes (slices).
    Los datos se esperan en formato [slices, líneas, canales, columnas] para múltiples cortes.
    """
    if method.lower() == "cartesiana":
        num_scans = len(rawdata)
        
        for scan_index, kspace_data in enumerate(rawdata):
            # Verificar si los datos contienen múltiples cortes (4D) o un solo corte (3D)
            if kspace_data.ndim == 4:
                n_slices, n_lines, n_channels, n_columns = kspace_data.shape
            elif kspace_data.ndim == 3:
                n_slices = 1
                n_lines, n_channels, n_columns = kspace_data.shape
                kspace_data = np.expand_dims(kspace_data, axis=0)  # Agregar dimensión para cortes

            print(f'Forma del kspace: {kspace_data.shape} (cortes: {n_slices}, líneas: {n_lines}, canales: {n_channels}, columnas: {n_columns})')
            
            # Iterar sobre los cortes
            for slice_index in range(n_slices):
                print(f'Procesando corte {slice_index + 1}/{n_slices}')
                
                # Crear una figura para visualizar el espacio K y la imagen reconstruida por cada corte
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
                fig.suptitle(f'Scan {scan_index + 1} - Corte {slice_index + 1}', fontsize=16)
                
                # Visualizar el espacio K (solo el primer canal)
                ax1.imshow(np.abs(kspace_data[slice_index, :, 0, :])**0.2, cmap='gray', origin='lower')
                ax1.set_title(f'Espacio K - Canal 1')
                ax1.axis('off')
                
                # Realizar la IFFT en los ejes de líneas y columnas
                image_ifft = ifftnd(kspace_data[slice_index], axes=[0, 2])
                
                # Combinación RMS de los canales
                image_combined = rms_comb(image_ifft, axis=1)
                
                # Visualizar la imagen reconstruida
                ax2.imshow(np.abs(image_combined), cmap='gray', origin='lower')
                ax2.set_title('Reconstrucción IFFT')
                ax2.axis('off')
                
                plt.tight_layout()
                plt.show()
    else:
        print(f"Método de reconstrucción '{method}' no implementado.")
