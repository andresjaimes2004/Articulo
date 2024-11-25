# **Manual de Usuario para el Sistema de Reconocimiento Facial**

---

## **ÍNDICE**
1. [Introducción](#1-introducción)  
2. [Requisitos del Sistema](#2-requisitos-del-sistema)  
3. [Instalación](#3-instalación)  
4. [Inicio del Programa](#4-inicio-del-programa)  
5. [Registro de Usuarios](#5-registro-de-usuarios)  
6. [Inicio de Sesión](#6-inicio-de-sesión)  
7. [Uso del Reconocimiento Facial](#7-uso-del-reconocimiento-facial)  
8. [Solución de Problemas](#8-solución-de-problemas)  
9. [Cierre del Programa](#9-cierre-del-programa)  

---

## **1. Introducción**
Este sistema permite registrar e identificar usuarios mediante reconocimiento facial. Utiliza tecnologías avanzadas de visión por computadora para garantizar seguridad y precisión.

---

## **2. Requisitos del Sistema**

### **Hardware**
- Cámara web funcional.
- Procesador con capacidad para ejecutar aplicaciones gráficas.
- 4GB de RAM mínimo (8GB recomendado).

### **Software**
- Python 3.9 o superior.
- Librerías necesarias: `cv2`, `face_recognition`, `numpy`, `mediapipe`, `PIL`, `imutils`, `tkinter`.

---

## **3. Instalación**

1. Descarga el código fuente del sistema desde el repositorio correspondiente.
2. Instala las dependencias ejecutando:
   ```bash
   pip install -r requirements.txt
---

## **4. Inicio del Programa**

1. Abre una terminal o consola de comandos en la carpeta del proyecto.
2. Ejecuta el siguiente comando para iniciar el programa:
   ```bash
   python SistemRecognition.py

---

## **5. Registro de Usuarios**

1. En la ventana principal, localiza el campo de texto para ingresar el nombre del usuario.
2. Escribe el nombre del usuario que deseas registrar.
3. Haz clic en el botón **"Registro"** para iniciar el proceso.
4. El sistema realizará las siguientes acciones:
   - Verificará si el nombre del usuario ya está registrado.
     - Si el usuario ya existe, mostrará un mensaje indicando que ya está registrado.
     - Si el usuario no existe, creará un nuevo archivo de usuario en la carpeta `DataBase/Usuarios`.
   - Activará la cámara para capturar datos faciales.
5. Sigue las instrucciones en pantalla para completar el registro biométrico:
   - Mantén el rostro frente a la cámara en posición central.
   - Realiza los movimientos solicitados (como parpadeo o inclinaciones de cabeza) para verificar tu identidad.
6. Una vez completado el registro:
   - Los datos faciales del usuario se almacenarán en la carpeta `DataBase/Caras`.
   - Se mostrará un mensaje de confirmación indicando que el usuario ha sido registrado exitosamente.

---

## **6. Inicio de Sesión**

1. En la ventana principal del sistema, haz clic en el botón **"Login"**.
2. Se abrirá una nueva ventana para el inicio de sesión biométrico.
3. El sistema realizará las siguientes acciones:
   - Cargará la base de datos de rostros registrados desde la carpeta `DataBase/Caras`.
   - Activará la cámara para capturar tu rostro en tiempo real.
4. Coloca tu rostro frente a la cámara:
   - Asegúrate de estar en un ambiente bien iluminado.
   - Mantén tu rostro centrado y visible en el cuadro de la cámara.
5. El sistema comparará tu rostro capturado con los datos registrados:
   - Si tu rostro coincide con un usuario registrado:
     - Se mostrará tu nombre en la pantalla.
     - El inicio de sesión se completará con éxito.
   - Si no se detecta coincidencia:
     - Aparecerá un mensaje indicando que el usuario no está registrado.
6. Si deseas volver a la ventana principal, cierra la ventana de inicio de sesión.

---

## **7. Captura de Datos Faciales**

El sistema captura y procesa datos faciales para su uso en registro e inicio de sesión. A continuación, se detallan las características del proceso:

1. **Activación de la Cámara**:
   - La cámara se activa automáticamente al iniciar el registro o inicio de sesión.
   - Se configuran parámetros como resolución y velocidad de fotogramas para optimizar el rendimiento.

2. **Procesamiento del Rostro**:
   - El sistema detecta las características faciales mediante la biblioteca **face_recognition**.
   - Se genera una codificación única para cada rostro utilizando algoritmos de aprendizaje automático.

3. **Validación del Rostro**:
   - Durante el registro:
     - El sistema solicita movimientos específicos (parpadeo o inclinaciones) para verificar la autenticidad del rostro.
   - Durante el inicio de sesión:
     - Compara el rostro capturado en tiempo real con las codificaciones almacenadas.

4. **Almacenamiento Seguro**:
   - Los datos faciales se guardan en la carpeta `DataBase/Caras` como codificaciones matemáticas únicas.
   - Este formato garantiza que no se almacenen imágenes explícitas del rostro, protegiendo la privacidad del usuario.

5. **Recomendaciones para Captura Eficiente**:
   - Asegúrate de estar en un entorno bien iluminado.
   - Evita cubrir tu rostro con accesorios como gafas de sol o sombreros.
   - Mantén una distancia adecuada de la cámara para una captura clara y precisa.

---

## **8. Solución de Problemas**

### **Problemas Comunes y Cómo Solucionarlos**

1. **No se detecta la cámara**:
   - Verifica que la cámara esté correctamente conectada y no esté en uso por otra aplicación.
   - Cierra todas las aplicaciones que puedan estar utilizando la cámara.
   - Reinicia el programa y asegúrate de que el sistema detecte la cámara al iniciar.

2. **No se detectan rostros**:
   - Asegúrate de que tu rostro esté bien iluminado.
   - Posiciona tu rostro dentro del encuadre de la cámara.
   - Revisa que la cámara esté configurada adecuadamente y no tenga obstrucciones.

3. **Usuario desconocido**:
   - Confirma que el usuario está registrado correctamente en el sistema.
   - Si persiste el problema, registra nuevamente al usuario para asegurarte de que los datos se guarden correctamente.

---

## **9. Cierre del Programa**

Para cerrar el programa, sigue estos pasos:

1. Cierra todas las ventanas del programa.
2. Si la cámara sigue activa, el sistema la desactivará automáticamente al cerrar las ventanas.

Este proceso asegura que todos los recursos sean liberados correctamente.

