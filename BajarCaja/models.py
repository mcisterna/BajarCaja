from django.db import models

class File(models.Model):
    filename = models.CharField(max_length=200)
    upload_date = models.DateTimeField('date published')
    filepath = models.CharField(max_length=200)
    size = models.IntegerField(default=0)
    public = models.BooleanField(default=False)

    def __unicode__(self):
    	return "Name: "+self.filename+", Size: "+str(self.size)
