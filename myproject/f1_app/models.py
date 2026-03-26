from django.db import models

class Session(models.Model):
    session_key = models.IntegerField(primary_key=True)
    meeting_key = models.IntegerField()
    session_type = models.TextField()
    session_name = models.TextField()
    date_start = models.DateTimeField()
    date_end = models.TextField()
    circuit_short_name = models.TextField()
    country_name = models.TextField()
    location = models.TextField()
    year = models.IntegerField()

    class Meta:
        db_table = "f1_sessions"
        managed = False

    def __str__(self):
        return f"{self.year} - {self.location} ({self.session_name}) [{self.date_start}]"

class Lap(models.Model):
    lap_number = models.IntegerField(primary_key=True)
    session_key = models.IntegerField()
    driver_number = models.IntegerField()
    date_start = models.DateTimeField() # у вас в БД TIMESTAMP
    lap_duration = models.FloatField()

    sector1 = models.FloatField()
    sector2 = models.FloatField()
    sector3 = models.FloatField()
    is_pit_out = models.BooleanField()

    class Meta:
        db_table = "f1_laps"
        managed = False
