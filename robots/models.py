from django.db import models


class Model(models.Model):
    name = models.CharField(max_length=2, blank=False, null=False)

    def __str__(self) -> str:
        return self.name


class Version(models.Model):
    name = models.CharField(max_length=2, blank=False, null=False)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Robot(models.Model):
    serial = models.CharField(max_length=5, blank=False, null=False)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    created = models.DateTimeField(blank=False, null=False)

    def to_dict(self):
        return {
            'id': self.id,
            'serial': self.serial,
            'model': str(self.model),
            'version': str(self.version),
            'created': self.created,
        }
