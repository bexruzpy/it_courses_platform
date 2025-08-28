from .base import BaseModel
from django.db import models
from multiselectfield import MultiSelectField

class Roles(models.TextChoices):
    TEACHER = 'teacher', "Teacher"

    FOUNDER = 'founder', "Founder"

    BACKEND_BEGINNER = 'backend_beginner', "Beginner Backend Developer"
    FRONTEND_BEGINNER = 'frontend_beginner', "Beginner Frontend Developer"

    BACKEND_JUNIOR = 'backend_junior', "Junior Backend Developer"
    FRONTEND_JUNIOR = 'frontend_junior', "Junior Frontend Developer"

    BACKEND_MIDDLE = 'backend_middle', "Middle Backend Developer"
    FRONTEND_MIDDLE = 'frontend_middle', "Middle Frontend Developer"

    BACKEND_SENIOR = 'backend_senior', "Senior Backend Developer"
    FRONTEND_SENIOR = 'frontend_senior', "Senior Frontend Developer"
class User(BaseModel):
    name = models.CharField(max_length=255)
    login = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    roles = MultiSelectField(choices=Roles.choices, blank=True)

    profile_picture = models.CharField(max_length=255, blank=True, default="None")

    rank = models.IntegerField(default=150)

    solved_tasks = models.ManyToManyField('Task', related_name='solved_by', blank=True)

    auth_token = models.CharField(max_length=255, blank=True, null=True, unique=True)
    def __str__(self):
        return self.name



class Course(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    teacher = models.ForeignKey(User, related_name='courses', on_delete=models.CASCADE)
    students = models.ManyToManyField(User, related_name='enrolled_courses', blank=True, default=[])
    graduates = models.ManyToManyField(User, related_name='completed_courses', blank=True, default=[])
    def __str__(self):
        return self.title

class Module(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Lesson(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(default="")
    module = models.ForeignKey(Module, related_name='lessons', on_delete=models.CASCADE)
    victorina = models.BooleanField(default=False)
    contents = models.JSONField(blank=True, null=True)
    auto_end_access = models.BooleanField(default=True)
    def check_end_access(self, user):
        result = True
        if self.auto_end_access:
            tasks = self.tasks.all()
            for task in tasks:
                if user not in task.solved_by.all():
                    return False
            return True
        try:
            CompletedLesson.objects.get(user=user, lesson=self)
        except CompletedLesson.DoesNotExist:
            return False
        return result
        

    def __str__(self):
        return self.title

class CompletedCourseStatuses(models.TextChoices):
    IN_PROGRESS = 'in_progress', "In Progress"
    COMPLETED = 'completed', "Completed"

class CompletedLesson(BaseModel):
    user = models.ForeignKey(User, related_name='completed_lessons', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='completed_by', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default=CompletedCourseStatuses.COMPLETED, choices=CompletedCourseStatuses.choices)
    completed_at = models.DateTimeField(auto_now_add=True)


class ChatMessage(BaseModel):
    course = models.ForeignKey(Course, related_name='chat_messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='chat_messages', on_delete=models.CASCADE)
    content = models.JSONField()

    def __str__(self):
        return str(self.course) + " message"

class Languages(models.TextChoices):
    PYTHON = 'python', "Python"
    JAVASCRIPT = 'javascript', "JavaScript"
    CSHARP = 'csharp', "CSharp"
    CPP = 'cpp', "C++"

class Task(BaseModel):
    title = models.CharField(max_length=255)
    description = models.JSONField()
    lesson = models.ForeignKey(Lesson, related_name='tasks', on_delete=models.SET_NULL, null=True)
    language = models.CharField(max_length=50, blank=True, null=True, choices=Languages.choices)
    inputs = models.JSONField()
    outputs = models.JSONField()

    def __str__(self):
        return self.title
class TestCase(models.Model):
    task = models.ForeignKey(Task, related_name='test_cases', on_delete=models.CASCADE)
    input_data = models.JSONField()
    expected_output = models.JSONField()

    def __str__(self):
        return f"TestCase for {self.task.title}"

class CodeSnippetStatuses(models.TextChoices):
    SUCCESS = 'success', "Success"
    WRONG = 'wrong', "Wrong Answer"
    RUNTIME = 'runtime', "Runtime Error"
    ERROR = 'error', "Error"
    TIME_LIMIT_EXCEEDED = 'time_limit_exceeded', "Time Limit Exceeded"
    MEMORY_LIMIT_EXCEEDED = 'memory_limit_exceeded', "Memory Limit Exceeded"


class CodeSnippet(models.Model):
    task = models.ForeignKey(Task, related_name='code_snippets', on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices=CodeSnippetStatuses.choices)
    user = models.ForeignKey(User, related_name='code_snippets', on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return f"CodeSnippet for {self.task.title}"



class TaskSolution(BaseModel):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    code_snippet = models.OneToOneField(CodeSnippet, on_delete=models.CASCADE)
    language = models.CharField(max_length=50)
    user = models.ForeignKey(User, related_name='solutions', on_delete=models.CASCADE)
    times = models.IntegerField(default=1)
    def __str__(self):
        return f"Solution for {self.task.title}"