"""Starter code for Assignment 1 CSC108 Summer 2019"""

SPECIAL_CASE_SCHOOL_1 = 'Fort McMurray Composite High'
SPECIAL_CASE_SCHOOL_2 = 'Father Mercredi High School'
SPECIAL_CASE_YEAR = '2017'

NE = 0

def is_special_case(record: str) -> bool:
    """Return True iff the student represented by record is a special case.

    >>> is_special_case('Jacqueline Smith,Fort McMurray Composite High,2017,MAT,90,94,ENG,92,88,CHM,80,85,BArts')
    True
    >>> is_special_case('Jacqueline Smith,Father Something High School,2017,MAT,90,94,ENG,92,88,CHM,80,85,BArts')
    False
    >>> is_special_case('Jacqueline Smith,Fort McMurray Composite High,2015,MAT,90,94,ENG,92,88,CHM,80,85,BArts')
    False
    """
    if (SPECIAL_CASE_SCHOOL_1 or SPECIAL_CASE_SCHOOL_2) in record:
        if SPECIAL_CASE_YEAR in record:
            return True
    return False

def get_final_mark(record: str, avg_work_mark: str,
                   avg_exam_mark: str) -> float:
    """Return the student's final average mark between their average work and 
    exam mark,where a missing exam mark, NE (No Exam),counts as a zero. If the 
    student is a special case,return their final mark as an average of their 
    work mark and the mark from the exams they had written.
    
    >>> get_final_mark('Jacqueline Smith,Fort McMurray Composite High,2017,MAT,90,94,ENG,92,88,CHM,80,85,BArts','87.3','89')
    88.2
    >>> get_final_mark('Jacqueline Smith,Fort McMurray Composite High,2017,MAT,90,94,ENG,92,88,CHM,80,NE,BArts','87.3','60.7')
    89.2
    >>> get_final_mark('Jacqueline Smith,Father Something High School,2017,MAT,90,94,ENG,92,88,CHM,80,NE,BArts','87.3','60.7')
    74.0
    >>> get_final_mark('Jacqueline Smith,Fort McMurray Composite High,2015,MAT,90,94,ENG,92,88,CHM,80,NE,BArts','87.3', '60.7')
    74.0
    """
    if (SPECIAL_CASE_SCHOOL_1 or SPECIAL_CASE_SCHOOL_2) in record:
            if SPECIAL_CASE_YEAR in record:
                if 'NE' in record and record.count('NE') == 3:
                    final_mark = avg_work_mark
                    return round(final_mark, 1)
                else:
                    final_mark = (float(avg_work_mark) + float(avg_exam_mark) 
                                  * 3 /(3 - record.count('NE'))) / 2 
                    # Adjusting the average exam mark by the number of 'NE'
                    return round(final_mark, 1)                         
    final_mark = (float(avg_work_mark) + float(avg_exam_mark))/2
    return round(final_mark, 1)


def get_both_marks(course_record: str, course_code: str) -> str:
    """
    Return a string that has the coursework and exam mark for a 
    specified course code, serperated by a single space. 
    Otherwise, return and empty string.
    
    >>> get_both_marks('MAT,90,94','MAT')
    '90 94'
    >>> get_both_marks('CHM,86,80','ENG')
    ''
    >>> get_both_marks('ENG,83,NE','ENG')
    '83 NE'
    """
    if course_code in course_record:
        return course_record[4:6] + ' ' + course_record[7:9]
    return ''
            
            
def extract_course(student_transcript: str, extract: int) -> str:
    """
    Return a string of the desired extracted course from the student's transcript.
    
    >>> extract_course('MAT,90,94,ENG,92,NE,CHM,80,85',2)
    'ENG,92,NE'
    >>> extract_course('MAT,90,94,ENG,92,NE,CHM,80,85',3)
    'CHM,80,85'
    """
    return student_transcript[extract * 10 - 10 : extract * 10 - 1]
    
    
    
def applied_to_degree(record: str, degree: str) -> bool:
    """
    Return True iff the student applied to the specified degree.
    
    >>> applied_to_degree('Jacqueline Smith,Fort McMurray Composite High,2015,MAT,90,94,ENG,92,88,CHM,80,NE,BArts','BArts')
    True
    >>> applied_to_degree('Jacqueline Smith,Fort McMurray Composite High,2015,MAT,90,94,ENG,92,88,CHM,80,NE,BArts','BSci')
    False
    >>> applied_to_degree('Michael Smith,Fort McMurray Composite High,2015,MAT,90,94,ENG,92,88,CHM,80,NE,BArts','BMusic')
    False
    >>> applied_to_degree('Michael Smith,Fort McMurray Composite High,2015,MAT,90,94,ENG,92,88,CHM,80,NE,BMusic','BMusic')
    """
    if record[-1 * len(degree):] == degree:
    # accounts for changes in the length of degree name 
        return True
    return False

def decide_admission(avg_considered_courses: float, grade_cutoff: float) -> str:
    """
    Return 'accept' if the student's average of the considered courses is at 
    least the cutoff average. Return 'accept with scholarship' if the student's 
    average of consideredcourses is above the 5% threshold for a scholarship. 
    Return 'reject' if the average is below the cutoff average.
    
    >>> decide_admission(83.0,80.0)
    'accept'
    >>> decide_admission(80.2,80.0)
    'accept'
    >>> decide_admission(85,75)
    'accept with scholarship'
    >>> decide_admission(80.5,75)
    'accept with scholarship'
    >>> decide_admission(73,85.0)
    'reject'
    """
    if avg_considered_courses >= (grade_cutoff + 5):
        return 'accept with scholarship'
    elif avg_considered_courses >= grade_cutoff:
        return'accept'
    else:
        return 'reject'
    
