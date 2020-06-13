from api.models import *
from api.serializers import *
import csv

try:
    estate = Estate.objects.filter(isApproved=1).order_by('-id')

except KeyError:
    error_header = {'error_code': 0, 'error_message': 'Missing require fields'}

except Exception as e:
    error_header = {'error_code': 0, 'error_message': 'fail - ' + str(e)}
