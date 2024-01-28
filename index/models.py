from django.db import models
class Otp(models.Model):
	RegNo=models.CharField(max_length=50)
	Code=models.CharField(max_length=50)
class Election(models.Model):
	Year=models.IntegerField()
	Status=models.CharField(max_length=50, null=True)
	Start=models.DateTimeField(null=True)
	End=models.DateTimeField(null=True)
	Type=models.CharField(max_length=50, null=True)
	def __str__(self):
		return self.Type
class Voter(models.Model):
	RegNo=models.CharField(max_length=50)
	FirstName=models.CharField(max_length=60)
	LastName=models.CharField(max_length=50)
	School=models.CharField(max_length=50)
	Email=models.CharField(max_length=60)
	Number=models.CharField(max_length=50)
	Leader=models.BooleanField(default=False)
	Cohort=models.CharField(max_length=50, null=True)
	Activated=models.BooleanField(default=False)
	Year=models.IntegerField(null=True)
	Eligible=models.BooleanField(default=True)
	Explanation=models.TextField(null=True)
	def __str__(self):
		return self.RegNo
class Post(models.Model):
	Election=models.ForeignKey(Election, on_delete=models.CASCADE, 	null=True)
	Name=models.CharField(max_length=60)
	Type=models.CharField(max_length=50)
	def __str__(self):
		return self.Name
class Contestant(models.Model):
	Individual=models.ForeignKey(Voter, on_delete=models.CASCADE)
	Post=models.ForeignKey(Post, on_delete=models.CASCADE)
	Votes=models.IntegerField()
	Pic=models.ImageField(null=True)
	def __str__(self):
		return self.Individual.RegNo
class Vote(models.Model):
	Voter=models.ForeignKey(Voter, on_delete=models.CASCADE)
	Contestant=models.ForeignKey(Contestant, on_delete=models.CASCADE)
	Date=models.DateField()
	Time=models.TimeField()
	Election=models.ForeignKey(Election, on_delete=models.CASCADE, null=True)
	Key=models.CharField(max_length=50, null=True)
	def __str__(self):
		return self.Key
class School(models.Model):
	Initials=models.CharField(max_length=15)
	Name=models.CharField(max_length=60)
	def __str__(self):
		return self.Name
class StudentCvs(models.Model):
	Name=models.CharField(max_length=70,)
	File=models.FileField(max_length=1000, upload_to='files')
		