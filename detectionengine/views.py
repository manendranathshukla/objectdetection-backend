
from rest_framework import status
from django.shortcuts import render
from rest_framework import generics
from django.http import HttpResponse
import io
import csv
import pandas as pd
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import *
from datetime import datetime
from rest_framework.renderers import JSONRenderer
from django.core.serializers import serialize
from django.http import HttpResponse


class UploadFileView(generics.CreateAPIView):
    serializer_class = FileUploadSerializer

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('csv')
        reader = pd.read_csv(file)
        for _, row in reader.iterrows():
            new_file = ProcessedData(
                image_name=row["image_name"],
                objects_detected=row['objects_detected'],
                timestamp=row["timestamp"],
            )
            new_file.save()
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)


class GenerateReport(generics.ListAPIView):
    serializer_class = ReportSerializer

    def post(self, request, *args, **kwargs):
        fromDate = request.POST['startDate']
        toDate = request.POST['endDate']
        date_format = '%a %b %d %Y %H:%M:%S GMT%z (%Z)'
        sDate = datetime.strptime(fromDate, date_format).strftime('%Y-%m-%d')
        eDate=datetime.strptime(toDate, date_format).strftime('%Y-%m-%d')
        filtered = ProcessedData.objects.filter(
            timestamp__range=[sDate, eDate])
        occDict={}
        for o in filtered:
            objects=o.objects_detected.split(',')
            for ob in objects:
                if(ob in occDict):
                    occDict[ob]+=1
                else:
                    occDict[ob]=1
        # Define the file name and column names
        file_name = 'report.csv'
        field_names = ['threat', 'occurrence']
        # Open the file for writing and write the data to it
        with open(file_name, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=field_names)

            # Write the header row
            writer.writeheader()

            # Write the data rows
            for threat, occurrence in occDict.items():
                writer.writerow({'threat': threat, 'occurrence': occurrence})
        json_data = serialize('json',filtered)
        return HttpResponse(json_data,content_type='application/json')

