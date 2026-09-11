"""Quiz models for the S03 lab: Exam, Question and Choice.

Design decisions (field types):
- Exam.title: CharField because the title is a short text with a bounded
  length; required to identify the exam.
- Exam.description: TextField because the description can be arbitrarily long.
- Exam.created: DateTimeField (auto_now_add) to record the creation timestamp
  once, automatically.
- Question.exam: ForeignKey to Exam because each question must belong to a
  single exam; deleting the exam cascades to its questions.
- Question.text: CharField since a statement is bounded-length text.
- Question.score: PositiveIntegerField (added in a later migration) to weight
  each question in the exam.
- Choice.text: CharField for the option text.
- Choice.is_correct: BooleanField to flag the correct answer.
"""

from django.db import models


class Exam(models.Model):
    """An exam/cuestionario with a title, description and creation date."""

    title = models.CharField(max_length=200, verbose_name='title')
    description = models.TextField(blank=True, verbose_name='description')
    created = models.DateTimeField(auto_now_add=True, verbose_name='created')

    class Meta:
        ordering = ['-created']
        verbose_name = 'Exam'
        verbose_name_plural = 'Exams'

    def __str__(self):
        return self.title


class Question(models.Model):
    """A question that belongs to an Exam."""

    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='exam',
    )
    text = models.CharField(max_length=500, verbose_name='text')
    score = models.PositiveIntegerField(default=0, verbose_name='score')

    class Meta:
        ordering = ['id']
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return self.text


class Choice(models.Model):
    """One answer option of a Question, with a correct-answer flag."""

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices',
        verbose_name='question',
    )
    text = models.CharField(max_length=300, verbose_name='text')
    is_correct = models.BooleanField(default=False, verbose_name='is correct')

    class Meta:
        ordering = ['id']
        verbose_name = 'Choice'
        verbose_name_plural = 'Choices'

    def __str__(self):
        return self.text