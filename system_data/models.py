from django.db import models


class Date(models.Model):
    PUBLISHED = 0
    UNPUBLISHED = 1

    STATUS_CHOICES = (
        (PUBLISHED, 'Published'),
        (UNPUBLISHED, 'Unpublished'),
    )
    academic_year = models.CharField(max_length=15, verbose_name="academic year")
    start_date = models.DateTimeField(verbose_name="start date")
    closure_date = models.DateTimeField(verbose_name="closure date")
    final_closure_date = models.DateTimeField(verbose_name="final closure date")
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES, default=0, verbose_name="status"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated at")

    class Meta:
        verbose_name = "date"
        verbose_name_plural = "dates"
        ordering = ["-academic_year"]

    def __str__(self):
        return self.academic_year
