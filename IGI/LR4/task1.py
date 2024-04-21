import csv
import pickle
import utility
from functools import cmp_to_key

class Student:
    def __init__(self, name, sprint, jump):
        self.name = name
        self.sprint = sprint
        self.jump = jump
        
    def __str__(self):
        return f'Name: {self.name} Sprint: {self.sprint} Jump: {self.jump}'

class GTOData:
    
    __jump_norm = 0
    __sprint_norm = 0
    
    def __init__(self):
        self.students = []
    
    @property
    def jump_norm(self):
        return self.__jump_norm
    
    @property
    def sprint_norm(self):
        return self.__sprint_norm
    
    @jump_norm.setter
    def jump_norm(self, jn):
        self.__jump_norm = jn
        
    @sprint_norm.setter
    def sprint_norm(self, jn):
        self.__sprint_norm = jn
        
        
    def deserialize_from_dict(self, students_dict):
        """Method for deserializing dictionary"""
        for student in students_dict.keys():
            student = Student(student, *students_dict[student])
            self.students.append(student)     
            
    def serialize_csv(self, filename):
        """Method for serializing to csv"""
        try:
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = ['Name', 'Sprint', 'Jump']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for student in self.students:
                    writer.writerow({'Name': student.name, 'Sprint': student.sprint, 'Jump': student.jump})
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
        

    def deserialize_csv(self, filename):
        """Method for deserializing from csv"""
        self.students = []
        try:
            with open(filename, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    student = Student(row['Name'], float(row['Sprint']), int(row['Jump']))
                    self.students.append(student)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def serialize_pickle(self, filename):
        """Method for serializing to pickle"""
        try:
            with open(filename, 'wb') as file:
                pickle.dump(self.students, file)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def deserialize_pickle(self, filename):
        """Method for deserialisng from pickle"""
        self.students = []
        try:
            with open(filename, 'rb') as file:
                self.students = pickle.load(file)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
            
    def not_complete_gto(self):
        result = []
        for student in self.students:
            if student.sprint > self.sprint_norm or student.jump < self.jump_norm:
                result.append(student)
        return result
    
    
    def not_complete_gto(self):
        result = []
        for student in self.students:
            if student.sprint > self.sprint_norm or student.jump < self.jump_norm:
                result.append(student)
        return result
         
    def complete_gto(self):
        result = []
        for student in self.students:
            if student.sprint <= self.sprint_norm and student.jump >= self.jump_norm:
                result.append(student)
        return result
    
    def get_student(self, name):
        for student in self.students:
            if student.name == name:
                return student
            
    def top3(self):
        result = []
        temp = self.complete_gto()
        temp.sort(key=cmp_to_key(comparator))
        for i in range(min(3, len(temp))):
            result.append(temp[i])
        return result
    
    def add_student(self, *args):
        print(args)
        self.students.append(Student(*args))
            
         
def comparator(one, two):
    if one.sprint < two.sprint:
        return -1
    if one.sprint > two.sprint:
        return 1    
    if one.jump > two.jump:
        return -1
    if one.jump < two.jump:
        return 1
    return 0
    

def task1():
    students = {
        "Zhenya" : [10.2, 250],
        "Kirill" : [15.1, 200],
        "Sasha" : [12.9, 225],
        "Anton" : [17.5, 260],
        "Oleg" : [14.3, 250]
    }
    
    gto_data = GTOData()
    
    
    while(True):
        print('1 - deserialize from dict')
        print('2 - cerialize csv')
        print('3 - decerialize csv')
        print('4 - cerialize with pickle')
        print('5 - decerialize with pickle')
        print('6 - set norms')
        print('7 - print all students')
        print('8 - print students not complete gto')
        print('9 - print students complete gto')
        print('10 - print students by name')
        print('11 - get top3 students')
        print('12 - add student')
        t = utility.get_int_from_input('option')
        if t == 1:
            gto_data.deserialize_from_dict(students)
            print('---------------ALL STUDENTS---------------')
            for student in gto_data.students:
                print(student)
            print('------------------------------------------')
        
        if t == 2:
            gto_data.serialize_csv('LR4/file.csv')
        
        if t == 3:
            gto_data.deserialize_csv('LR4/file.csv')
            print('---------------ALL STUDENTS---------------')
            for student in gto_data.students:
                print(student)
            print('------------------------------------------')
        
        if t == 4:
            gto_data.serialize_pickle('LR4/file2.txt')
        
        if t == 5:
            gto_data.deserialize_pickle('LR4/file2.txt')
            print('---------------ALL STUDENTS---------------')
            for student in gto_data.students:
                print(student)
            print('------------------------------------------')
                    
        if t == 6:
            sn = utility.get_float_from_input('sprint norm')
            jn = utility.get_int_from_input('jump norm')
            gto_data.sprint_norm = sn
            gto_data.jump_norm = jn
        
        if t == 7:
            print('---------------ALL STUDENTS---------------')
            for student in gto_data.students:
                print(student)
            print('------------------------------------------')
            
        if t == 8:
            print('---------------NOT COMPLETE GTO---------------')
            print('Sprint norm =', gto_data.sprint_norm)
            print('Jump norm =', gto_data.jump_norm)
            not_complete = gto_data.not_complete_gto()
            for student in not_complete:
                print(student)
            print('----------------------------------------------')

        if t == 9:
            print('---------------COMPLETE GTO---------------')
            print('Sprint norm =', gto_data.sprint_norm)
            print('Jump norm =', gto_data.jump_norm)
            not_complete = gto_data.complete_gto()
            for student in not_complete:
                print(student)
            print('------------------------------------------')
    
        if t == 10:
            print('Enter name')
            name = input()
            print(gto_data.get_student(name))
    
        if t == 11:
            print('---------------TOP 3---------------')
            print('Sprint norm =', gto_data.sprint_norm)
            print('Jump norm =', gto_data.jump_norm)
            top3 = gto_data.top3()
            for student in top3:
                print(student)
            print('-----------------------------------')        
    
        if t == 12:
            print('Input name')
            name = input()
            sprint = utility.get_float_from_input('sprint time')
            jump = utility.get_int_from_input('jump time')
            gto_data.add_student(name, sprint, jump)
                
    
    
task1()
    
    