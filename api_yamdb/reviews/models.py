from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.constants import NUMBER_OF_CHARS


class Reviews(models.Model):
    """Модель отзывов."""
    text = models.TextField('текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение'
    )
    score = models.IntegerField(
        'оценка',
        validators=[
            MinValueValidator(1, message='Оценка должна быть не меньше 1'),
            MaxValueValidator(10, message='Оценка должна быть не больше 10')
        ]
    )
    pub_date = models.DateTimeField('дата публикации', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        models.UniqueConstraint(
            fields=['author', 'title'], name='unique_review'
        )

    def __str__(self):
        return self.text[NUMBER_OF_CHARS]


class Comments(models.Model):
    """Модель комментариев."""
    reviews = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='комментируемый отзыв'
    )
    text = models.TextField('текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор'
    )
    pub_date = models.DateTimeField('дата публикации', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[NUMBER_OF_CHARS]
