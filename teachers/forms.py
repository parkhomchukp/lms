from teachers.models import Teacher
from student.forms import PersonBaseForm


class TeacherBaseForm(PersonBaseForm):
    class Meta:
        model = Teacher
        fields = ["first_name", "last_name", "email", "phone_number", "course"]


class TeacherUpdateForm(PersonBaseForm):
    class Meta(TeacherBaseForm.Meta):
        pass
