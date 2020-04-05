from django.db import models
import pytz
import calendar
from datetime import date,datetime,timedelta

class InterviewCalendar(models.Model):
    description = models.CharField(max_length=512, blank=True, null=True)
    timezone = models.CharField(
        choices=[(zone, zone) for zone in pytz.common_timezones],
        max_length=32,
    )

    min_hours_notice = models.PositiveIntegerField()
    max_hours_out = models.PositiveIntegerField()

    def __str__(self):
        return '{}'.format(self.description)


class InterviewSlot(models.Model):
    calendar = models.ForeignKey(
        'calendly_api.InterviewCalendar',
        related_name='slots',
    )
    end_time = models.TimeField()
    start_time = models.TimeField()

    monday = models.BooleanField(default=False, verbose_name='Mon')
    tuesday = models.BooleanField(default=False, verbose_name='Tue')
    wednesday = models.BooleanField(default=False, verbose_name='Wed')
    thursday = models.BooleanField(default=False, verbose_name='Thur')
    friday = models.BooleanField(default=False, verbose_name='Fri')
    saturday = models.BooleanField(default=False, verbose_name='Sat')
    sunday = models.BooleanField(default=False, verbose_name='Sun')

    max_spots = models.PositiveIntegerField(default=1)


    @property
    def local_tz(self):
        return pytz.timezone(self.calendar.timezone)


class Interview(models.Model):
    calendar = models.ForeignKey(
        'calendly_api.InterviewCalendar',
        blank=True,
        null=True,
        related_name='interviews',
    )
    created = models.DateTimeField(auto_now_add=True)

    canceled = models.BooleanField(default=False)
    canceled_at = models.DateTimeField(blank=True, null=True)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)

    def cancel_previous(self):
        previous_interviews = self.application.interviews.exclude(
            pk=self.pk,
        ).filter(canceled=False)

        previous_interviews.update(canceled=True, canceled_at=timezone.now())

    def __str__(self):
        return 'Interview at {}'.format(self.start_time)

class InterviewConflict(models.Model):
    calendar = models.ForeignKey(
        'calendly_api.InterviewCalendar',
        related_name='conflicts',
    )
    end_time = models.DateTimeField()
    start_time = models.DateTimeField()