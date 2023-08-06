from django import forms
from tasks.models import Task


# formulario html
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'important')
