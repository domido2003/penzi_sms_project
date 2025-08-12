from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    age = models.IntegerField()
    gender = models.CharField(max_length=20)
    county = models.CharField(max_length=100)
    town = models.CharField(max_length=100)

    education_level = models.CharField(max_length=100, null=True, blank=True)
    profession = models.CharField(max_length=100, null=True, blank=True)
    marital_status = models.CharField(max_length=100, null=True, blank=True)
    religion = models.CharField(max_length=100, null=True, blank=True)
    ethnicity = models.CharField(max_length=100, null=True, blank=True)
    self_description = models.TextField(null=True, blank=True)

    date_created = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'users'
        managed = False

    def __str__(self):
        return f"{self.full_name} ({self.phone_number})"


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    message_from = models.CharField(max_length=20)
    message_to = models.CharField(max_length=20)
    content = models.TextField()
    direction = models.CharField(max_length=10)  # incoming or outgoing
    date_created = models.DateTimeField()

    class Meta:
        db_table = 'messages'
        managed = False

    def __str__(self):
        return f"{self.direction}: {self.message_from} -> {self.message_to} @ {self.date_created}"


class MatchTracking(models.Model):
    id = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=20)
    seen_count = models.IntegerField(default=0)
    last_updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'match_tracking'
        managed = False

    def __str__(self):
        return f"{self.phone_number} (seen: {self.seen_count})"
