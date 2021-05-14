import hashlib
from User import User
from Course import Course




class EducationAdmin(User):

    @staticmethod
    def create_course(course):
        """
        create instance course and add new course to file
        :return: object course
        """
        check = Course.search_file_crs('id_crs', course[0])
        if check is False:
            crs = [i.strip() if i.isdigit() else i for i in course]
            obj_course = Course(*crs)
            obj_course.file_crs()

            return 1
        else:
            return 0

    @staticmethod
    def register_stu(student):
        """
        register student
        :param student: list information student
        :return:list attributes student
        """
        sts_reg = User.register(student[0], student[1],
                                'file_student.csv')  # register student
        student[1] = hashlib.md5(student[1].encode()).hexdigest()
        stu = [i.strip() if i.isdigit() else i for i in student]
        if sts_reg == 0:
            # student already register
            return 0
        else:
            return stu
