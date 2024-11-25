import cv2
import face_recognition as fr
import numpy as np
import mediapipe as mp
import os
from tkinter import *
from PIL import Image, ImageTk
import imutils
import math

def get_ruta(ruta_relativa):
    ruta_base = os.path.dirname(__file__)  # Obtiene el directorio actual del archivo
    ruta_completa = os.path.join(ruta_base, ruta_relativa)  # Crea la ruta completa
    return os.path.abspath(ruta_completa)  # Convierte a absoluta

# Inicializa las soluciones de mediapipe
mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
mpFaceDetection = mp.solutions.face_detection

# Configuración de la red de detección de cara
ConfigDraw = mpDraw.DrawingSpec(thickness=1, circle_radius=1)

FacemeshObject = mp.solutions.face_mesh
FaceMesh = FacemeshObject.FaceMesh(max_num_faces=1)

FaceObject = mp.solutions.face_detection
# Cambia el argumento a min_detection_confidence
detector = FaceObject.FaceDetection(min_detection_confidence=0.5, model_selection=1)

def get_ruta(ruta_relativa):
    ruta_base = os.path.dirname(__file__)  # Obtiene el directorio actual del archivo
    ruta_completa = os.path.join(ruta_base, ruta_relativa)  # Crea la ruta completa
    return os.path.abspath(ruta_completa)  # Convierte a absoluta

def Code_Face(images):
    listacod = []

    # Iteramos
    for img in images:
        # Correccion de color
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_encodings = fr.face_encodings(img)
        if len(face_encodings) > 0:
            cod = face_encodings[0]
            listacod.append(cod)
        else:
            print("No se detectaron rostros en la imagen")


    return listacod

def Profile():
    global step, conteo, UserName, RegUser, OutFolderPathUser
    # Reset Variables
    conteo = 0
    step = 0

    # Crear la ventana Toplevel
    pantalla4 = Toplevel(pantalla)
    pantalla4.title("Perfil")
    pantalla4.geometry("800x400")

    # Crear un Canvas para colocar la imagen de fondo
    canvas = Canvas(pantalla4, width=800, height=400)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, anchor="nw", image=imagenB)

    # Leer archivo del usuario
    UserFile = open(f"{OutFolderPathUser}/{RegUser}.txt", 'r')
    InfoUser = UserFile.read().split(',')
    cedula = InfoUser[0]
    UserFile.close()

    # Check
    if cedula in clases:
        # Interfaz
        texto1 = Label(pantalla4, text=f"BIENVENIDO CC {cedula}")
        texto1.place(x=350, y=50)

        lblImgUser = Label(pantalla4)
        lblImgUser.place(x=90, y=80)

        # Cargar imagen desde archivo
        ImgUser = cv2.imread(f"{OutFolderPathFace}/{cedula}.png")
        if ImgUser is None:
            print(f"No se encontró la imagen para {cedula}")
            return

        # Convertir de BGR a RGB
        ImgUser = cv2.cvtColor(ImgUser, cv2.COLOR_BGR2RGB)

        # Convertir a formato PIL
        ImgUser = Image.fromarray(ImgUser)

        ImgUser = ImgUser.resize((250, 200))
        # Convertir a PhotoImage para Tkinter
        IMG = ImageTk.PhotoImage(image=ImgUser)

        # Configurar label
        lblImgUser.configure(image=IMG)
        lblImgUser.image = IMG 

def Close_Windows():
    global step, conteo
    # Reset Variables
    conteo = 0
    step = 0
    if pantalla2.winfo_exists():
        pantalla2.destroy()

def Close_Windows2():
    global step, conteo
    # Reset Variables
    conteo = 0
    step = 0
    pantalla3.destroy()

def log_biometric():
    global pantalla2, conteo, parpadeo, img_info, step, glass, capHat
    if cap is not None:
        ret, frame = cap.read()
        frameSave = frame.copy()
        frame = imutils.resize(frame, width=980)
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if ret == True:
            res = FaceMesh.process(frameRGB)
            px = []
            py = []
            lista = []
            if res.multi_face_landmarks:
                for rostros in res.multi_face_landmarks:
                    mpDraw.draw_landmarks(frame, rostros, FacemeshObject.FACEMESH_CONTOURS, ConfigDraw, ConfigDraw )
                    for id, puntos in enumerate(rostros.landmark):
                        al, an, c = frame.shape
                        x,y = int(puntos.x * an), int(puntos.y * al)
                        px.append(x)
                        py.append(y)
                        lista.append([id, x, y])
                        
                        if len(lista) == 468:
                            # Ojo derecho
                            x1, y1 = lista[145][1:]
                            x2, y2 = lista[159][1:]
                            longitud1 = math.hypot(x2-x1, y2-y1)
                            
                            # Ojo izquierdo
                            x3, y3 = lista[374][1:]
                            x4, y4 = lista[386][1:]
                            longitud2 = math.hypot(x4-x3, y4-y3)
                            
                            # Parietal Derecho
                            x5, y5 = lista[139][1:]

                            # Parietal Izquierdo
                            x6, y6 = lista[368][1:]

                            # Ceja Derecha
                            x7, y7 = lista[70][1:]
                            
                            # Ceja Izquierda 
                            x8,y8 = lista[300][1:]
                            
                            faces = detector.process(frameRGB)
                            if faces.detections is not None:
                                for face in faces.detections:
                                    score = face.score
                                    score = score[0]
                                    bbox = face.location_data.relative_bounding_box

                                    if score > confThreshold:
                                        xi, yi, anc, alt = bbox.xmin, bbox.ymin, bbox.width, bbox.height
                                        xi, yi, anc, alt = int(xi* an), int(yi*al), int(anc * an), int(alt * al)
                                        
                                        offsetan = (offsetx / 100) * anc
                                        xi = int(xi - int(offsetan/2))
                                        anc = int(anc + offsetan)
                                        xf = xi + an

                                        offsetal = (offsety / 100) * alt
                                        yi = int(yi - offsetal)
                                        alt = int(alt + offsetal)
                                        yf = yi + al

                                        if xi < 0: xi = 0
                                        if yi < 0: yi = 0
                                        if anc < 0: anc = 0
                                        if alt < 0: alt = 0

                                        if step == 0:
                                            cv2.rectangle(frame, (xi, yi, anc, alt),(255,0,0), 2)
                                            alis0, anis0, c = img_step0.shape
                                            frame[10:10 + alis0, 10:10 + anis0] = img_step0

                                            # IMG Step1
                                            alis1, anis1, c = img_step1.shape
                                            # img_step1 = cv2.resize(img_step1, (50, alis1))
                                            frame[10:10 + alis1, 810:810 + anis1] = img_step1

                                            # IMG Step2
                                            alis2, anis2, c = img_step2.shape
                                            frame[190:190 + alis2, 810:810 + anis2] = img_step2

                                            # Condiciones
                                            if x7 > x5 and x8 < x6:
                                                # IMG check
                                                alich, anich, c = img_check.shape
                                                frame[100:100 + alich, 862:862 + anich] = img_check

                                                # Cont Parpadeos
                                                if longitud1 <= 10 and longitud2 <= 10 and parpadeo == False:  # Parpadeo
                                                    conteo = conteo + 1
                                                    parpadeo = True

                                                elif longitud1 > 10 and longitud2 > 10 and parpadeo == True:  # Seguridad parpadeo
                                                    parpadeo = False

                                                # Parpadeos
                                                # Conteo de parpadeos
                                                cv2.putText(frame, f'Parpadeos: {int(conteo)}', (830, 270), cv2.FONT_HERSHEY_COMPLEX, 0.5 ,(255, 255, 255), 1)


                                                if conteo >= 3:
                                                    # IMG check
                                                    alich, anich, c = img_check.shape
                                                    frame[285:285 + alich, 862:862 + anich] = img_check

                                                    # Open Eyes
                                                    if conteo >= 3 and longitud1 > eye_open_threshold and longitud2 > eye_open_threshold:
                                                        # xi = max(0, xi - 20)
                                                        # yi = max(0, yi - 40)
                                                        # anc = min(anc + 40, frame.shape[1] - xi)
                                                        # alt = min(alt + 80, frame.shape[0] - yi)
                                                        cut = frameSave[yi:yf, xi:xf]

                                                        cv2.imwrite(f"{OutFolderPathFace}/{RegUser}.png", cut)
                                                        step = 1
                                            else:
                                                conteo = 0
                                    
                                        if step == 1:
                                            # Draw
                                            cv2.rectangle(frame, (xi, yi, an, al), (0, 255, 0), 2)
                                            # IMG check Liveness
                                            allich, anlich, c = img_liche.shape
                                            frame[10:10 + allich, 10:10 + anlich] = img_liche
                                            # cap.release()
                                            # pantalla2.destroy()
                                            Close_Windows()
                            # close = pantalla2.protocol("WM_DELETE_WINDOW", Close_Windows)
        # Rendimensionamos el video
        frame = imutils.resize(frame, width=1080)
        im = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=im)

        # Verificar si lblVideo existe antes de actualizarlo
        try:
            lblVideo.configure(image=img)
            lblVideo.image = img
        except TclError:
            print("lblVideo ya no existe")

        # Ejecutar después de un pequeño delay
        if pantalla2.winfo_exists():  # Verifica si la ventana sigue existiendo
            lblVideo.after(10, log_biometric)
    else:
        cap.release()

def Log():
    global RegUser, InputUserReg, InputPassReg, cap, lblVideo, pantalla2
    RegUser = InputUserReg.get()
    if len(RegUser) == 0:
        print('Formulario incompleto')
    else:
        UserList = os.listdir(PathUserCheck)
        UserName = [lis.split('.')[0] for lis in UserList]

        if RegUser in UserName:
            print('Usuario registrado anteriormente')
            return  # No abrir la ventana ni la cámara si el usuario ya está registrado
        else:
            info.append(RegUser)
            with open(f'{OutFolderPathUser}/{RegUser}.txt', "w") as f:
                f.write(RegUser)
        InputUserReg.delete(0, END)

    pantalla2 = Toplevel(pantalla)
    pantalla2.title('Login Biometrico')
    pantalla2.geometry('1080x600')

    # Aquí es donde inicias la cámara solo si el usuario es nuevo
    imagenB_ = Image.open(get_ruta('./SetUp/Back2.png'))
    imagen_redimensionada_BR = imagenB_.resize((100, 20))
    imagenB = ImageTk.PhotoImage(imagen_redimensionada_BR)

    back = Label(pantalla2, image=imagenB, text="Back")
    back.place(x=0, y=0, relwidth=1, relheight=1)

    lblVideo = Label(pantalla2)
    lblVideo.place(x=0, y=0)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, 1080)
    cap.set(4, 600)
    log_biometric()  # Solo se llama si el usuario es nuevo

def Sign_biometric():
    global pantalla, pantalla3, conteo, parpadeo, img_info, step, RegUser, prueba, cap
    
    if cap is not None:
        ret, frame = cap.read()
        frameSave = frame.copy()
        frame = imutils.resize(frame, width=980)
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if ret == True:
            res = FaceMesh.process(frameRGB)
            px = []
            py = []
            lista = []
            if res.multi_face_landmarks:
                for rostros in res.multi_face_landmarks:
                    mpDraw.draw_landmarks(frame, rostros, FacemeshObject.FACEMESH_CONTOURS, ConfigDraw, ConfigDraw)
                    for id, puntos in enumerate(rostros.landmark):
                        al, an, c = frame.shape
                        x, y = int(puntos.x * an), int(puntos.y * al)
                        px.append(x)
                        py.append(y)
                        lista.append([id, x, y])
                        
                        if len(lista) == 468:
                            # Ojo derecho
                            x1, y1 = lista[145][1:]
                            x2, y2 = lista[159][1:]
                            longitud1 = math.hypot(x2 - x1, y2 - y1)
                            
                            # Ojo izquierdo
                            x3, y3 = lista[374][1:]
                            x4, y4 = lista[386][1:]
                            longitud2 = math.hypot(x4 - x3, y4 - y3)
                            
                            # Parietal Derecho
                            x5, y5 = lista[139][1:]

                            # Parietal Izquierdo
                            x6, y6 = lista[368][1:]

                            # Ceja Derecha
                            x7, y7 = lista[70][1:]
                            
                            # Ceja Izquierda 
                            x8, y8 = lista[300][1:]
                            
                            faces = detector.process(frameRGB)
                            if faces.detections is not None:
                                for face in faces.detections:
                                    score = face.score
                                    score = score[0]
                                    bbox = face.location_data.relative_bounding_box

                                    if score > confThreshold:
                                        xi, yi, anc, alt = bbox.xmin, bbox.ymin, bbox.width, bbox.height
                                        xi, yi, anc, alt = int(xi * an), int(yi * al), int(anc * an), int(alt * al)
                                        
                                        offsetan = (offsetx / 100) * anc
                                        xi = int(xi - int(offsetan / 2))
                                        anc = int(anc + offsetan)
                                        xf = xi + an

                                        offsetal = (offsety / 100) * alt
                                        yi = int(yi - offsetal)
                                        alt = int(alt + offsetal)
                                        yf = yi + al

                                        if xi < 0: xi = 0
                                        if yi < 0: yi = 0
                                        if anc < 0: anc = 0
                                        if alt < 0: alt = 0

                                        if step == 0:
                                            cv2.rectangle(frame, (xi, yi, anc, alt), (255, 0, 0), 2)
                                            alis0, anis0, c = img_step0.shape
                                            frame[10:10 + alis0, 10:10 + anis0] = img_step0

                                            # IMG Step1
                                            alis1, anis1, c = img_step1.shape
                                            frame[10:10 + alis1, 810:810 + anis1] = img_step1

                                            # IMG Step2
                                            alis2, anis2, c = img_step2.shape
                                            frame[190:190 + alis2, 810:810 + anis2] = img_step2

                                            # Condiciones
                                            if x7 > x5 and x8 < x6:
                                                # IMG check
                                                alich, anich, c = img_check.shape
                                                frame[100:100 + alich, 862:862 + anich] = img_check

                                                # Cont Parpadeos
                                                if longitud1 <= 10 and longitud2 <= 10 and parpadeo == False:  # Parpadeo
                                                    conteo = conteo + 1
                                                    parpadeo = True

                                                elif longitud1 > 10 and longitud2 > 10 and parpadeo == True:  # Seguridad parpadeo
                                                    parpadeo = False

                                                # Parpadeos
                                                # Conteo de parpadeos
                                                cv2.putText(frame, f'Parpadeos: {int(conteo)}', (830, 270), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

                                                if conteo >= 3:
                                                    # IMG check
                                                    alich, anich, c = img_check.shape
                                                    frame[285:285 + alich, 862:862 + anich] = img_check

                                                    # Open Eyes
                                                    if conteo >= 3 and longitud1 > eye_open_threshold and longitud2 > eye_open_threshold:
                                                        # # Detener la cámara
                                                        # cap.release()
                                                        # # Cerrar la ventana
                                                        # pantalla3.destroy()
                                                        step = 1
                                            else:
                                                conteo = 0
                                    
                                        if step == 1:
                                            # Draw
                                            cv2.rectangle(frame, (xi, yi, an, al), (0, 255, 0), 2)
                                            # IMG check Liveness
                                            allich, anlich, c = img_liche.shape
                                            frame[10:10 + allich, 10:10 + anlich] = img_liche

                                            # Encontrar rostros
                                            faces = fr.face_locations(frameRGB)
                                            facescod = fr.face_encodings(frameRGB, faces)

                                            for facecod, faceloc in zip(facescod, faces):
                                                Match = fr.compare_faces(FaceCode, facecod)
                                                simi = fr.face_distance(FaceCode, facecod)
                                                if len(simi) > 0:
                                                    min = np.argmin(simi)
                                                    if Match[min]:
                                                        RegUser = clases[min].upper()
                                                        Profile()
                                                else:
                                                    print("No se encontraron coincidencias de rostro.")
                                            Close_Windows2()
        # Rendimensionamos el video
        frame = imutils.resize(frame, width=1080)
        im = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=im)

        # Verificar si el widget lblVideo existe antes de actualizarlo
        try:
            if lblVideo.winfo_exists():
                lblVideo.configure(image=img)
                lblVideo.image = img
                lblVideo.after(10, Sign_biometric)
            else:
                print("Widget lblVideo no existe más.")
        except Exception as e:
            print(f"Error al actualizar lblVideo: {e}")
    else:
        cap.release()

def Sign():
    global LogUser, LogPass, OutFolderPath, cap, lblVideo, pantalla3, FaceCode, clases, images

    # DB Faces
    # Accedemos a la carpeta
    images = []
    clases = []
    lista = os.listdir(OutFolderPathFace)

    # Leemos los rostros del DB
    for lis in lista:
        # Leemos las imagenes de los rostros
        imgdb = cv2.imread(f'{OutFolderPathFace}/{lis}')
        # Almacenamos imagen
        images.append(imgdb)
        # Almacenamos nombre
        clases.append(os.path.splitext(lis)[0])

    # Face Code
    FaceCode = Code_Face(images)

    # 3° Ventana
    pantalla3 = Toplevel(pantalla)
    pantalla3.title("BIOMETRIC SIGN")
    pantalla3.geometry("1080x600")

    imagenB_ = Image.open(get_ruta('./SetUp/Back2.png'))
    imagen_redimensionada_BR = imagenB_.resize((100, 20))
    imagenB = ImageTk.PhotoImage(imagen_redimensionada_BR)

    # Usamos imagenB_tk en el Label
    back2 = Label(pantalla3, image=imagenB, text="Back")
    back2.place(x=0, y=0, relwidth=1, relheight=1)

    # Video
    lblVideo = Label(pantalla3)
    lblVideo.place(x=0, y=0)

    # Elegimos la camara
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, 1080)
    cap.set(4, 600)
    Sign_biometric()

OutFolderPathUser = get_ruta('DataBase/Usuarios')
PathUserCheck = get_ruta('DataBase/Usuarios')
OutFolderPathFace = get_ruta('DataBase/Caras')

img_cap = cv2.imread( get_ruta("SetUp/cap.png") )
img_glass = cv2.imread( get_ruta("SetUp/glass.png"))
img_check = cv2.imread( get_ruta("SetUp/check.png"))
img_step0 = cv2.imread( get_ruta("SetUp/Step0.png"))
img_step1 = cv2.imread(get_ruta("SetUp/Step1.png"))
img_step2 = cv2.imread(get_ruta("SetUp/Step2.png"))
img_liche = cv2.imread(get_ruta("SetUp/LivenessCheck.png"))

parpadeo = False
conteo = 0
step = 0

eye_open_threshold = 10

offsety = 20
offsetx = 20

confThreshold = 0.5

info = []

pantalla = Tk()
pantalla.title("Sistema Reconocimiento Facial")
pantalla.geometry('800x400')
imagen_original = Image.open(get_ruta('./SetUp/Inicio.png'))
imagen_redimensionada = imagen_original.resize((800, 400))
imagenF = ImageTk.PhotoImage(imagen_redimensionada)

background = Label(image=imagenF, text="Inicio")
background.place(x=0, y=0, relheight=1, relwidth=1)

InputUserReg = Entry(pantalla)
InputUserReg.place(x=25, y=220)

imagen_original_BR = Image.open(get_ruta('./SetUp/BtLogin.png'))
imagen_redimensionada_BR = imagen_original_BR.resize((100, 20))
imagenBR = ImageTk.PhotoImage(imagen_redimensionada_BR)

BtReg = Button(pantalla, text='Registro', image=imagenBR, height="20", width="100", command=Log)
BtReg.place(x=160, y=350)

imagen_original_BL = Image.open(get_ruta('./SetUp/BtSign.png'))
imagen_redimensionada_BL = imagen_original_BL.resize((100, 20))
imagenBL = ImageTk.PhotoImage(imagen_redimensionada_BL)

BtSign = Button(pantalla, text='Login', image=imagenBL, height="20", width="100", command=Sign)
BtSign.place(x=540, y=350)

imagenB_ = Image.open(get_ruta('./SetUp/Back2.png'))
imagen_redimensionada_BR = imagenB_.resize((800, 400))
imagenB = ImageTk.PhotoImage(imagen_redimensionada_BR)

pantalla.mainloop()