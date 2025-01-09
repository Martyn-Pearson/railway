from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.urls import reverse
from .models import Location, TrainLocation, Train

class IndexView(ListView):
    model = Location
    context_object_name = "location_list"
    queryset = Location.objects.order_by("order")
    template_name="storage/index.html"

class UpdateView(DetailView):
    model = Location
    template_name="storage/update.html"

    def index_response(self):
        return HttpResponseRedirect(reverse("storage:index"))

    def get(self, request, *args, **kwargs):
        # Don't support gets, so just redirect to the index
        return self.index_response()

    def post(self, request, *args, **kwargs):
        location = get_object_or_404(Location, pk=kwargs["location_id"])
        for postval, operation in [("CycleLeft",self.cycle_left), ("CycleRight", self.cycle_right)]:
            if postval in request.POST:
                return operation(location)
            
        for key in request.POST:
            if key.startswith("Remove_"):
                return self.remove(location, request, key)
            elif key.startswith("Add_"):
                return self.addtrain(location, request, key)
            elif key.startswith("Add"):
                return self.add(location, request, key)

        
        return HttpResponse("Probably not got round to doing that bit.<br />")

    def cycle_left(self, location):
        trains = TrainLocation.objects.filter(location=location)
        for train in trains:
            train.order = len(trains) if train.order == 1 else train.order - 1
            train.save()
        return self.index_response()

    def cycle_right(self, location):
        trains = TrainLocation.objects.filter(location=location)
        for train in trains:
            train.order = 1 if train.order == len(trains) else train.order + 1
            train.save()
        return self.index_response()

    def add(self, location, request, key):
        context = {
            "trains" : Train.objects.filter(trainlocation__isnull = True),
            "direction" : "left" if key == "AddLeft" else "right",
            "location" : location
        }

        return render(request, "storage/update.html", context)

    def addtrain(self, location, request, key):
        trainid = int(key[4:])
        train = get_object_or_404(Train, pk=trainid)
        direction = request.POST["direction"]
        if direction == "left":
            others = TrainLocation.objects.filter(location=location)
            for other in others:
                other.order += 1
                other.save()
            tl = TrainLocation(location=location, train=train, order=1)
            tl.save()
        else:
            order = TrainLocation.objects.filter(location=location).count() + 1
            tl = TrainLocation(location=location, train=train, order=order)
            tl.save()
        return self.index_response()


    def remove(self, location, request, key):
        remove_train = int(key[7:])
        train = get_object_or_404(Train, pk=remove_train)
        trainlocation = TrainLocation.objects.filter(location=location, train=train)[0]
        for tl in TrainLocation.objects.filter(location = location):
            if tl.order > trainlocation.order:
                tl.order -= 1
                tl.save()
        trainlocation.delete()

        return self.index_response()
            
