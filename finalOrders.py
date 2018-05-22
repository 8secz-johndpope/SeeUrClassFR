import boto3

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
    imageFile = './'+curso+'/12.jpg'
    #imageFile = './alumnos/alumno_guillermo_adolfo_iglesias_birkner.jpg'

    #s.agregarAlumnoS3(table, imageFile)
    #print('Guillermo Agregado')
    #alumnos = ['Andrea Nieto', 'Chris Pratt', 'Juan Daniel Hahn Quintanilla']
    #alumnoAgregar = ['Jennifer Aniston']
    alumnoBorrar = ['Robert Downey, Jr.']
    #alumno = ['Guillermo Adolfo Iglesias Birkner']

    #print(r.retornarCurso(curso))

    #pruebaRevisarFoto(table, curso, imageFile)#, alumno)
    #pruebaAgregarAlCurso(table, curso, alumno)#Agregar)
    pruebaBorrar(table, curso, alumnoBorrar)