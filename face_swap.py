import cv2
import dlib
import numpy as np

# Inicializar detector y predictor de dlib
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def get_landmarks_points(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    if len(faces) == 0:
        return None
    landmarks = predictor(gray, faces[0])
    points = []
    for n in range(0, 68):
        x = landmarks.part(n).x
        y = landmarks.part(n).y
        points.append((x, y))
    return np.array(points, np.int32)

def extract_index_nparray(nparray):
    index = None
    for i in nparray[0]:
        index = i
        break
    return index

def obtener_indices_triangulos(points):
    hull = cv2.convexHull(points, returnPoints=False)
    rect = cv2.boundingRect(points)
    subdiv = cv2.Subdiv2D(rect)
    for p in points.tolist():
        subdiv.insert((int(p[0]), int(p[1])))
    triangles = subdiv.getTriangleList()
    triangles = np.array(triangles, dtype=np.int32)

    indexes_triangles = []
    for t in triangles:
        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])

        idx_pt1 = extract_index_nparray(np.where((points == pt1).all(axis=1)))
        idx_pt2 = extract_index_nparray(np.where((points == pt2).all(axis=1)))
        idx_pt3 = extract_index_nparray(np.where((points == pt3).all(axis=1)))

        if idx_pt1 is not None and idx_pt2 is not None and idx_pt3 is not None:
            triangle = [idx_pt1, idx_pt2, idx_pt3]
            indexes_triangles.append(triangle)
    return indexes_triangles

def realizar_faceswap(ruta_usuario, ruta_personaje, ruta_salida="resultado_faceswap.jpg"):
    try:
        img = cv2.imread(ruta_usuario)
        img2 = cv2.imread(ruta_personaje)
        if img is None:
            print(f" No se pudo leer la imagen del usuario: {ruta_usuario}")
            return False
        if img2 is None:
            print(f" No se pudo leer la imagen del personaje: {ruta_personaje}")
            return False

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        points1 = get_landmarks_points(img)
        points2 = get_landmarks_points(img2)

        if points1 is None:
            print(" No se detectó rostro en la imagen del usuario.")
            return False
        if points2 is None:
            print(" No se detectó rostro en la imagen del personaje.")
            return False

        indexes_triangles = obtener_indices_triangulos(points1)
        img2_new_face = np.zeros_like(img2)

        for triangle_index in indexes_triangles:
            tr1 = np.array([points1[i] for i in triangle_index], np.int32)
            tr2 = np.array([points2[i] for i in triangle_index], np.int32)

            rect1 = cv2.boundingRect(tr1)
            x, y, w, h = rect1
            cropped_triangle = img[y:y+h, x:x+w]
            cropped_mask = np.zeros((h, w), np.uint8)

            points1_rect = np.array([[tr1[0][0]-x, tr1[0][1]-y],
                                     [tr1[1][0]-x, tr1[1][1]-y],
                                     [tr1[2][0]-x, tr1[2][1]-y]], np.int32)

            cv2.fillConvexPoly(cropped_mask, points1_rect, 255)

            rect2 = cv2.boundingRect(tr2)
            x2, y2, w2, h2 = rect2

            points2_rect = np.array([[tr2[0][0]-x2, tr2[0][1]-y2],
                                     [tr2[1][0]-x2, tr2[1][1]-y2],
                                     [tr2[2][0]-x2, tr2[2][1]-y2]], np.float32)

            points1_rect_float = np.array(points1_rect, np.float32)

            M = cv2.getAffineTransform(points1_rect_float, points2_rect)
            warped_triangle = cv2.warpAffine(cropped_triangle, M, (w2, h2))
            mask = np.zeros((h2, w2, 3), dtype=np.uint8)
            cv2.fillConvexPoly(mask, np.int32(points2_rect), (1, 1, 1))
            warped_triangle = warped_triangle * mask

            img2_area = img2_new_face[y2:y2+h2, x2:x2+w2]
            img2_area = img2_area * (1 - mask)
            img2_area = img2_area + warped_triangle
            img2_new_face[y2:y2+h2, x2:x2+w2] = img2_area

        # Clonación sin costuras
        mask = np.zeros_like(img2_gray)
        head_mask = cv2.fillConvexPoly(mask, cv2.convexHull(points2), 255)
        img2_face_mask = cv2.bitwise_not(head_mask)
        img2_noface = cv2.bitwise_and(img2, img2, mask=img2_face_mask)
        result = cv2.add(img2_noface, img2_new_face)

        (x, y, w, h) = cv2.boundingRect(cv2.convexHull(points2))
        center = (x + w // 2, y + h // 2)
        output = cv2.seamlessClone(result, img2, head_mask, center, cv2.NORMAL_CLONE)

        cv2.imwrite(ruta_salida, output)
        print(" Face swap generado con éxito.")
        return True

    except Exception as e:
        print(f" Error en face swap: {e}")
        return False