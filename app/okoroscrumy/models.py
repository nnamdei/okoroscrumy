from django.db import models


class ScrumyUser(models.Model):

	ROLES = (
		('OW', 'Owner'),
		('AD', 'Admin'),
		('QA', 'Quality Analyst'),
		('DE', 'Developer'),
	)

	first_name = models.CharField(max_length = 50, null = False)
	last_name = models.CharField(max_length=50, null=False)
	user_name = models.EmailField(max_length=100,blank=True, null = False)
	role = models.CharField(max_length=2,choices=ROLES)


	def __str__(self):
		return ( self.user_name + ' | ' + self.first_name)

	def get_daily_goals(self):
		return self.scrumygoals_set.filter(status_id=1)

	def get_weekly_goals(self):
		return self.scrumygoals_set.filter(status_id=2)

	def get_verified_goals(self):
		return self.scrumygoals_set.filter(status_id=3)

	def get_done_goals(self):
		return self.scrumygoals_set.filter(status_id=4)


class GoalStatus(models.Model):
	STATUSES = (

		('DT', 'Daily Task'),
        ('WT', 'Weekly Task'),
        ('V', 'Verified'),
        ('D', 'Done'),

	)
	status = models.CharField(choices=STATUSES, max_length=20, default="Check Status")
	name = models.CharField(max_length=255, default='ScrumStatus')

	def __str__(self):
		return self.status

class ScrumyGoals(models.Model):

	user_id = models.ForeignKey(ScrumyUser, on_delete=models.CASCADE)
	status_id = models.ForeignKey(GoalStatus, on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)
	task = models.TextField()
	task_id = models.IntegerField(default=0)
	moved_by = models.CharField(max_length=60, default='No Movement')

	def __str__(self):
		return self.task
