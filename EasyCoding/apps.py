from assessment.models import Assessment
from assessment.apps import execute_sql


class assessment_list:

    def __init__(self, lesson, user):
        self.lesson = lesson
        self.label = "第%d章作業" % lesson.number

        sql = """
            SELECT a.id
            FROM assessment_assessment as a, course_course as c 
            WHERE c.lesson_id = %d and a.course_id = c.id
        """ % lesson.number

        temp = execute_sql(sql)

        all_assessment = {i.ass for i in user.assessmentcode_set.all()}

        assessments = []

        for i in temp:
            assessment = Assessment.objects.get(id=i[0])

            if assessment in all_assessment:
                assessment.is_done = True
            else:
                assessment.is_done = False

            assessments.append(assessment)

        assessments.sort()
        self.assessments = assessments

        self.lesson_progress = user.assess_progress.course.lesson
        self.chapter_progress = user.assess_progress.course.chapter

        self.is_done = False
        self.is_lock = False

        if self.lesson_progress < lesson:
            self.is_lock = True
        else:
            for assessment in assessments:
                if not assessment.is_done:
                    break
            else:
                self.is_done = True
