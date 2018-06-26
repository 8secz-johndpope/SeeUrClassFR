import class_management as cm
import student_management as sm


if __name__ == "__main__":
    class_name = 'tic3_v6'
    institution_bucket = 'instituciondiegoportales'
    imageFile = './instituciondiegoportales/alumno_juan_hahn.jpg'
    student_name, _ = sm.pars_name(imageFile)
    #cm.create_class(class_name)
    cm.add_student_class(institution_bucket, class_name, student_name)
