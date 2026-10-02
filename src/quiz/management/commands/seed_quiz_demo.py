"""Management command that seeds the demo exam used by the S03 lab.

Usage:
    python manage.py seed_quiz_demo

Creates one Exam with two Questions (four Choices each, exactly one correct
per question). Idempotent: skips the work when the demo exam already exists.
"""

from django.core.management.base import BaseCommand
from quiz.models import Exam, Question, Choice

DEMO_EXAM = {
    'title': 'Introduction to Django',
    'description': ('Demo exam created by the seed_quiz_demo command. '
                    'It has two questions and four options each.'),
    'questions': [
        {
            'text': 'Which command starts the Django development server?',
            'score': 5,
            'choices': [
                {'text': 'python manage.py runserver', 'is_correct': True},
                {'text': 'python manage.py startserver', 'is_correct': False},
                {'text': 'django-admin startserver', 'is_correct': False},
                {'text': 'pip install runserver', 'is_correct': False},
            ],
        },
        {
            'text': 'Which field type is used for a long free-text description?',
            'score': 5,
            'choices': [
                {'text': 'CharField', 'is_correct': False},
                {'text': 'TextField', 'is_correct': True},
                {'text': 'IntegerField', 'is_correct': False},
                {'text': 'BooleanField', 'is_correct': False},
            ],
        },
    ],
}


class Command(BaseCommand):
    help = (
        'Seeds the demo exam (1 exam, 2 questions, 4 choices each). '
        'Idempotent.'
    )

    def handle(self, *args, **options):
        if Exam.objects.filter(title=DEMO_EXAM['title']).exists():
            self.stdout.write('Demo exam already present, skipping.')
            return

        exam = Exam.objects.create(
            title=DEMO_EXAM['title'],
            description=DEMO_EXAM['description'],
        )
        for q in DEMO_EXAM['questions']:
            question = Question.objects.create(
                exam=exam, text=q['text'], score=q['score']
            )
            for c in q['choices']:
                Choice.objects.create(
                    question=question, text=c['text'], is_correct=c['is_correct']
                )
        self.stdout.write(
            self.style.SUCCESS(
                'Demo exam created: %s (%s questions, 4 choices each).'
                % (exam.title, exam.questions.count())
            )
        )