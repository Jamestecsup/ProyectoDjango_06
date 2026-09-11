"""Forms and formsets for the quiz app (S03 lab).

- ExamForm: ModelForm to create/edit an Exam.
- QuestionForm: ModelForm to create a Question (of an Exam).
- ChoiceModelForm + ChoiceFormSet: inline formset so several options can be
  edited together with their question, validating that exactly one option is
  marked as correct (formset-level clean).
"""

from django import forms
from django.forms import inlineformset_factory
from .models import Exam, Question, Choice


class ExamForm(forms.ModelForm):
    """Form for creating or editing an Exam."""

    class Meta:
        model = Exam
        fields = ['title', 'description']


class QuestionForm(forms.ModelForm):
    """Form for creating or editing a Question."""

    class Meta:
        model = Question
        fields = ['exam', 'text', 'score']


class ChoiceForm(forms.ModelForm):
    """Form for a single Choice inline."""

    class Meta:
        model = Choice
        fields = ['text', 'is_correct']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget = forms.TextInput(
            attrs={'placeholder': 'Option text'}
        )


ChoiceFormSet = inlineformset_factory(
    Question,
    Choice,
    form=ChoiceForm,
    extra=4,
    max_num=4,
    validate_max=True,
    can_delete=True,
)

# Base formset with the shared validation logic; the factory above is
# instantiated in the view with this class as base_class when needed.
choice_formsets = {
    'factory': ChoiceFormSet,
}


def clean_choices_formset(formset):
    """Validates that exactly one Choice in the formset is marked correct.

    Intended to be called from the view (or used as a base formset clean) so
    the "exactly one correct option" rule is enforced.
    """
    correct = sum(
        1
        for form in formset.forms
        if form.is_valid() and form.cleaned_data.get('is_correct')
    )
    if correct != 1:
        raise forms.ValidationError(
            'Exactly one option must be marked as correct '
            f'(found {correct}).'
        )
    return formset.cleaned_data