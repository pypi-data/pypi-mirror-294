import csv

from django.http import (
    HttpResponse,
)
from rest_framework import (
    status,
)


def create_log_response(log_changes, status_code=status.HTTP_200_OK):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="log_changes.csv"'
    writer = csv.writer(response)
    for change in log_changes:
        writer.writerow([change])
    response.status_code = status_code
    return response
