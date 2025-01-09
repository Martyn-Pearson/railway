from django.db import models

class Locomotive(models.Model):
    number = models.CharField(max_length=10)
    address = models.CharField(max_length=5)
    description = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.description if self.description else self.number} ({self.address})"

    class Meta:
        ordering = ("description", "number")

class Load(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ("name",)

class Train(models.Model):
    CLOCKWISE = "CLW"
    ANTICLOCKWISE = "ACW"
    DIRECTION_CHOICES = { CLOCKWISE : "Clockwise", ANTICLOCKWISE : "Anticlockwise"}

    locomotives = models.ManyToManyField(Locomotive, through="TrainLocomotive")
    load = models.ForeignKey(Load, on_delete=models.CASCADE, null=True, blank=True)
    direction = models.CharField(max_length=3, choices = DIRECTION_CHOICES, default=CLOCKWISE)

    def __str__(self):
        if self.direction == Train.CLOCKWISE:
            locos = ", ".join(str(loco) for loco in self.locomotives.order_by("trainlocomotive__order")[::-1])
            return f"{self.load} + {locos}" if self.load else locos
        else:
            locos = ", ".join(str(loco) for loco in self.locomotives.order_by("trainlocomotive__order"))
            return f"{locos} + {self.load}" if self.load else locos

class TrainLocomotive(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    locomotive = models.ForeignKey(Locomotive, on_delete=models.CASCADE)
    order = models.IntegerField()

    class Meta:
        ordering = ("order",)

class Location(models.Model):
    name = models.CharField(max_length=50)
    trains = models.ManyToManyField(Train, through="TrainLocation")
    order = models.IntegerField()

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ("order",)

    def ordered_trains(self):
        return self.trains.order_by("trainlocation__order")
    
class TrainLocation(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.location} : {self.train} ({self.order})"

    class Meta:
        ordering = ("order",)

