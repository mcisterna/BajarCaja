from django.db import models
from django.contrib.auth.models import User


class File(models.Model):
	filename = models.CharField(max_length=200)
	upload_date = models.DateTimeField('date published')
	filepath = models.CharField(max_length=200)
	size = models.FloatField(default=0.0)
	real_size = models.IntegerField(default=0)
	scale_sz = models.CharField(max_length=2,default='B')
	public = models.BooleanField(default=False)
	user = models.ForeignKey(User)

	def __unicode__(self):
		return "Name: "+self.filename+", Size: "+str(self.size)

class User_capacity(models.Model):
	user = models.ForeignKey(User)
	capacity = models.IntegerField(default=10485760)
	capacity_show = models.FloatField(default=10.0)
	scale_sz = models.CharField(max_length=2,default='MB')
	def __unicode__(self):
		return '%.2f %s' % (self.capacity_show,self.scale_sz)
