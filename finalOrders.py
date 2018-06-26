import boto3
from PIL import Image
import os, os.path
import datetime
import rekogOrders as r
import s3Orders as s
import dynamoDBOrders as d
import assistance_table_managment as ctm


def agregarDetalles(nombre):
    nombre = nombre.lower().replace(' ','_')
    nombre = 'alumno_' + nombre.lower() + '.jpg'
    return nombre


def pruebaRevisarFoto(table, curso, imageFile):
    ### Realizar Comparación ###
    faceIdsList = r.comprarConColleccion(curso, imageFile)
    now = datetime.datetime.now()
    fecha = [now.year, now.month, now.day]
    fecha_1 = '-'.join(str(e) for e in fecha)
    hora = [now.hour, now.minute, now.second]
    hora_1 = ':'.join(str(e) for e in hora)
    if faceIdsList != {}:
        for key, value in faceIdsList.items():
            nombre = d.conseguirNombreDynamo(table, key)
            valor = str(round(value, 3))
            data = {
                    'curso': curso,
                    'nombre': nombre,
                    'fecha': fecha_1,
                    'hora': hora_1,
                    'rekog_value': valor
                    }
            ctm.save_asistance_register(data)
    else:
        print('No hubo coincidencia')

   
def pruebaBorrar(table, curso, listaAlumnos):
    idPorBorrar = []
    diccionario = r.retornarCurso(curso)

    for elemento in listaAlumnos:
        if elemento in diccionario:
            idPorBorrar.append(diccionario[elemento])
    if idPorBorrar != []:
        r.borrarAlumnoCurso(table, curso, idPorBorrar)
    else:
        for elemento in listaAlumnos:
            print('Alumno ' + elemento + ' no se encuentran en el curso')


def pruebaAgregarAlCurso(table, curso, listaAlumnos):
    ### Agregar Alumnos al Curso ###
    if len(listaAlumnos) != 0:
        for i in range(len(listaAlumnos)):
            r.agregarAlumnoCurso(table, curso, agregarDetalles(listaAlumnos[i]))


if __name__ == "__main__":
    bucket = 'instituciondiegoportales'
    path = './instituciondiegoportales/'
    #table = 'testtic3v2'
    curso = 'tic3_1'
    #path = './' + curso + '/'
    #path = './respaldo_imagees/tics3/'
    valid_images = [".jpg"]
    lista_archivos = os.listdir(path)
    for ruta_foto in lista_archivos:
        extension = os.path.splitext(ruta_foto)[1]
        if extension.lower() not in valid_images:
            continue
        pruebaRevisarFoto(bucket, curso, Image.open(os.path.join(path, ruta_foto)))
        os.remove(os.path.join(path, ruta_foto))


    #s.add_student_s3(bucket, imageFile)

    #print('Guillermo Agregado')
    #alumnos = ['Andrea Nieto', 'Chris Pratt', 'Juan Daniel Hahn Quintanilla']
    #print(r.retornarCurso(curso))
    #pruebaRevisarFoto(table, curso, imageFile)#, alumno)
    #pruebaAgregarAlCurso(table, curso, alumno)#Agregar)
    #pruebaBorrar(table, curso, alumnoBorrar)
