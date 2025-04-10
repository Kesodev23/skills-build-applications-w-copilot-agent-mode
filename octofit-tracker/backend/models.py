from django.db import models

class UserProfile(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    height = models.FloatField()  # in cm
    weight = models.FloatField()  # in kg
    target = models.FloatField(default=0.0)  # Fitness target in terms of calories or activity duration
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (Target: {self.target})"

class FitnessTracking(models.Model):
    tracking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50)  # e.g., running, cycling
    duration = models.IntegerField()  # in minutes
    calories_burned = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return f"{self.user.name} - {self.activity_type} on {self.date}"

class Leaderboard(models.Model):
    leaderboard_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    total_points = models.IntegerField()
    rank = models.IntegerField()

    def __str__(self):
        return f"{self.user.name} - Rank {self.rank}"
