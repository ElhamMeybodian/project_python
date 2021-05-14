import csv
import os
import pandas as pd


class Course:
    def __init__(self, id_crs, name, unit, capacity, name_prof, time_exam, time_class, field_crs,
                 status_capacity=0):
        """
        :param id_crs: id course is unique
        :param name:name of course
        :param unit:unit of course
        :param capacity:capacity of course
        :param name_prof:name professor present course
        :param time_exam:course exam time
        :param time_class:course time class
        :param field_crs:field course
        :param status_capacity:number of filled capacity
        """
        self.id_crs = id_crs
        self.name = name
        self.unit = unit
        self.capacity = capacity
        self.name_prof = name_prof
        self.time_exam = time_exam
        self.time_class = time_class
        self.field_crs = field_crs
        self.status_capacity = status_capacity

    def file_selective_crs(self, username_student, term):
        """
        write selective courses any student in file(create file selective course)
        :param username_student: username student for write student any course
        :param term: term student
        :return: no return just create file and write in file
        """
        check_file = os.path.exists('file_select_course.csv')
        # add course student to file
        if check_file:
            with open('file_select_course.csv', 'a', newline='') as write_csv:
                fieldnames = ['username_student', 'term', 'id_crs', 'name', 'unit', 'name_prof', 'time_exam',
                              'time_class',
                              'field_crs']
                csv_writer = csv.DictWriter(write_csv, fieldnames=fieldnames)
                csv_writer.writerow({'username_student': username_student,
                                     'term': term,
                                     'id_crs': self.id_crs,
                                     'name': self.name,
                                     'unit': self.unit,
                                     'name_prof': self.name_prof,
                                     'time_exam': self.time_exam,
                                     'time_class': self.time_class,
                                     'field_crs': self.field_crs,
                                     })
        # create file selection course
        else:
            with open('file_select_course.csv', 'a', newline='') as create_file:
                fieldnames = ['username_student', 'term', 'id_crs', 'name', 'unit', 'name_prof', 'time_exam',
                              'time_class',
                              'field_crs']
                csv_writer = csv.DictWriter(create_file, fieldnames=fieldnames)
                csv_writer.writeheader()
                csv_writer.writerow({'username_student': username_student,
                                     'term': term,
                                     'id_crs': self.id_crs,
                                     'name': self.name,
                                     'unit': self.unit,
                                     'name_prof': self.name_prof,
                                     'time_exam': self.time_exam,
                                     'time_class': self.time_class,
                                     'field_crs': self.field_crs,
                                     })

    def update_file_course(self):
        """
        :return: if id course exit in file so course file update  and return True else return 'not find id course'
        """
        df = pd.read_csv("file_course.csv")
        with open('file_course.csv', 'r') as edit_file:
            fieldnames = ['id_crs', 'name', 'unit', 'capacity', 'name_prof', 'time_exam', 'time_class', 'field_crs',
                          'status_capacity']
            file_crs_r = csv.DictReader(edit_file, fieldnames=fieldnames)
            line = 0
            for row in file_crs_r:
                if row['id_crs'].isdigit():
                    if int(self.id_crs) == int(row['id_crs']):
                        df.loc[line - 1, 'status_capacity'] = self.status_capacity
                        df.to_csv("file_course.csv", index=False)
                        return True
                line += 1
            return 'not find id course'

    def update_file_slc_course(self):
        """
        :return:if id course exit in file so selective course file update and return True else return 'not find id course'
        """
        df1 = pd.read_csv("file_select_course.csv")
        df_s = df1[:9]
        with open('file_select_course.csv', 'r') as edit_file:
            fieldnames = ['username_student', 'term', 'id_crs', 'name', 'unit', 'name_prof', 'time_exam',
                          'time_class', 'field_crs']
            file_slc_crs_r = csv.DictReader(edit_file, fieldnames=fieldnames)
            line = 0
            for row in file_slc_crs_r:
                if row['id_crs'].isdigit():
                    if int(self.id_crs) == int(row['id_crs']):
                        df_s = df_s.drop(df_s[(df_s.id_crs == self.id_crs)].index)
                        df_s.to_csv("file_select_course.csv", index=False)
                        return True
                line += 1
            return 'not find id course'

    def file_crs(self):
        """
        :return: create file course and write attributes class course in file
        """
        check_file = os.path.exists('file_course.csv')
        if check_file:
            with open('file_course.csv', 'a', newline='') as write_course_csv:
                fieldnames = ['id_crs', 'name', 'unit', 'capacity', 'name_prof', 'time_exam', 'time_class', 'field_crs',
                              'status_capacity']
                csv_writer = csv.DictWriter(write_course_csv, fieldnames=fieldnames)
                csv_writer.writerow({'id_crs': self.id_crs,
                                     'name': self.name,
                                     'unit': self.unit,
                                     'capacity': self.capacity,
                                     'name_prof': self.name_prof,
                                     'time_exam': self.time_exam,
                                     'time_class': self.time_class,
                                     'field_crs': self.field_crs,
                                     'status_capacity': self.status_capacity})
        else:
            with open('file_course.csv', 'a', newline='') as create_file:
                fieldnames = ['id_crs', 'name', 'unit', 'capacity', 'name_prof', 'time_exam', 'time_class', 'field_crs',
                              'status_capacity']
                csv_writer = csv.DictWriter(create_file, fieldnames=fieldnames)
                csv_writer.writeheader()
                csv_writer.writerow({'id_crs': self.id_crs,
                                     'name': self.name,
                                     'unit': self.unit,
                                     'capacity': self.capacity,
                                     'name_prof': self.name_prof,
                                     'time_exam': self.time_exam,
                                     'time_class': self.time_class,
                                     'field_crs': self.field_crs,
                                     'status_capacity': self.status_capacity})

    @classmethod
    def search_file_crs(cls, metric, value_metric):
        """
        :param metric:name attribute
        :param value_metric:value attribute
        :return:make a instance of course class
        """
        try:
            with open('file_course.csv', 'r') as read_course_csv:
                csv_read = csv.DictReader(read_course_csv)
                for row in csv_read:
                    if row[metric].isdigit():
                        if int(row[metric]) == int(value_metric):
                            row = [int(i.strip()) if i.isdigit() else i for i in row.values()]
                            return cls(*row)
            return False
        except FileNotFoundError:
            return False

    @staticmethod
    def search_file_slc_crs(metric, value_metric, term_now):
        """
        :param term_now: term of student
        :param metric:name attribute
        :param value_metric:value attribute
        :return:make a instance of course class
        """
        try:
            with open('file_select_course.csv', 'r') as crs_file:
                csv_read = csv.DictReader(crs_file)
                for row in csv_read:
                    if row[metric].isdigit():
                        if int(row[metric]) == int(value_metric) and int(row['term']) == int(term_now):
                            return True
            return False
        except FileNotFoundError:
            return False
