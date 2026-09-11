"""Views for the quiz app (S03 lab).

- exam_list: lists all exams (Meta ordering).
- exam_detail: shows one exam with its questions and choices.
- question_create: creates a Question with its inline Choice formset,
  enforcing that exactly one option is correct.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django import forms
from .models import Exam, Question, Choice
from .forms import ExamForm, QuestionForm, ChoiceFormSet, clean_choices_formset


def exam_list(request):
    """List all exams."""
    exams = Exam.objects.all()
    return render(request, 'quiz/exam_list.html', {'exams': exams})


def exam_detail(request, pk):
    """Show an exam with its questions and choices."""
    exam = get_object_or_404(Exam, pk=pk)
    questions = exam.questions.all().prefetch_related('choices')
    return render(
        request,
        'quiz/exam_detail.html',
        {'exam': exam, 'questions': questions},
    )


def question_create(request, pk):
    """Create a Question for Exam ``pk`` together with its options.

    Uses a ChoiceFormSet bound to the Question being created; on POST validates
    the question and that exactly one option is correct, then saves question
    and choices.
    """
    exam = get_object_or_404(Exam, pk=pk)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        formset = ChoiceFormSet(request.POST)

        exactly_one_correct = True
        if formset.is_valid():
            try:
                clean_choices_formset(formset)
            except forms.ValidationError as error:
                formset._non_form_errors = error.error_list
                exactly_one_correct = False

        if form.is_valid() and formset.is_valid() and exactly_one_correct:
            question = form.save(commit=False)
            question.exam = exam
            question.save()
            formset.instance = question
            formset.save()
            messages.success(request, f'Question "{question.text}" created.')
            return redirect('quiz:exam_detail', pk=exam.pk)
    else:
        form = QuestionForm(initial={'exam': exam})
        formset = ChoiceFormSet()
        formset.instance = Question(exam=exam)

    return render(
        request,
        'quiz/question_create.html',
        {'form': form, 'formset': formset, 'exam': exam},
    )