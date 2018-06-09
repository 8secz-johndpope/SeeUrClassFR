import boto3
from PIL import Image
import os, os.path
import glob
import rekogOrders as r
import s3Orders as s
import dynamoDBOrders as d


def agregarDetalles(nombre):
    nombre = nombre.lower().replace(' ','_')
    nombre = 'alumno_'+nombre.lower()+'.jpg'
    return nombre


def pruebaRevisarFoto(table, curso, imageFile):
    ### Realizar Comparación ###
    faceIdsList = r.comprarConColleccion(curso, imageFile)

    if faceIdsList != {}:
        for key, value in faceIdsList.items():
            nombre = d.conseguirNombreDynamo(table, key)
            print('Alumno ' + nombre + ' del curso ' + curso + ' se encuentra en esta foto con una probabilidad de ' + str(value) )
    else:
        print('No hubo coincidencia alguna')


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
    table = 'testtic3v2'
    curso = 'tics3'
    path = './'+curso+'/'
    valid_images = [".jpg"]
    lista_archivos = os.listdir(path)
    for ruta_foto in lista_archivos:
        extension = os.path.splitext(ruta_foto)[1]
        if extension.lower() not in valid_images:
            continue
        pruebaRevisarFoto(table, curso, Image.open(os.path.join(path, ruta_foto)))
        print(ruta_foto)

    #s.agregarAlumnoS3(table, imageFile)
    #print('Guillermo Agregado')
    #alumnos = ['Andrea Nieto', 'Chris Pratt', 'Juan Daniel Hahn Quintanilla']
    #print(r.retornarCurso(curso))

    #pruebaRevisarFoto(table, curso, imageFile)#, alumno)
    #pruebaAgregarAlCurso(table, curso, alumno)#Agregar)
    #pruebaBorrar(table, curso, alumnoBorrar)
