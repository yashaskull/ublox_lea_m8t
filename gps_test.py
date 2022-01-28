import gps
import sys
import csv
import os.path
from os import path
import time

gps_file_header = ['time', 'Latitude', 'Longtitude',  'Satellites']

gps_hostname = 'localhost'
gps_port = '2947'

gps_data = None
writer = None

def connect_gps():
	session = gps.gps(gps_hostname, gps_port)
	session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
	return session
	
def get_gps_data():

	session = gps.gps('localhost', '2947')
	session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

	report_time = ''
	report_lat = ''
	report_lon = ''
	nsat = 0
	
	while True:
		try:
			report = session.next()
			# Wait for a 'TPV' report and display the current time
			# To see all report data, uncomment the line below
			print(report)
			if report['class'] == 'TPV':
				if hasattr(report, 'time'):
				   # print(report.time)
					report_time = report.time
				if hasattr(report, 'lat'):
					# print(report.lat)
					report_lat = report.lat
				if hasattr(report, 'lon'):
					# print(report.lon)
					report_lon = report.lon
					
				return  report_time, report_lat, report_lon, nsat

			'''
			# number of satellites
			if report['class'] == 'SKY':
				for sat in report['satellites']:
					if sat['used']== True:
						nsat = nsat + 1
			'''
					
			#break
				
		except KeyError:
			pass
		except KeyboardInterrupt:
			print('Keyboard interrupt detected. Exiting....')
			gps_data.close()
			quit()
		except StopIteration:
			session = None
			print("GPSD has terminated")


if __name__ == '__main__':

	# number of arguments
	num_arg = len(sys.argv)

	if num_arg < 3:
		print('Please specify time interval in seconds and name of file to log GPS data.')
		print('Example usage:')
		print('python3 gps_test.py 1 gps_data')
		exit(0)
	
	
	# name of file to log gps data
	gps_filename = sys.argv[2]

	# append .csv to filename
	gps_filename = gps_filename + '.csv'

	
    # open file
	try:
		if path.exists(gps_filename):
			#gps_data = open(gps_filename, 'a')
			#writer = csv.writer(gps_data)
			pass
		else:
			gps_data = open(gps_filename, 'a')
			writer = csv.writer(gps_data)
			writer.writerow(gps_file_header)
			gps_data.close()
			
	except OSError as exception:
		print(exception)
		print('Error opening file to log gps data. Exiting.....')
		exit(0)

	#writer.writerow(['a', 'b', 'c'])
	#gps_data.close()

	# invertal in seconds to log gps data
	log_interval = sys.argv[1]
	print('Logging GPS data every ' + log_interval + ' seconds......')
	
	#session = gps.gps(gps_hostname, gps_port)
	#session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
	
	
	try:
		while True:
			
			# get gps data
			gps_log_data = get_gps_data()
			print(gps_log_data)
			# openfile
			gps_data = open(gps_filename, 'a')
			writer = csv.writer(gps_data)
			writer.writerow(gps_log_data)
			
			# close file
			gps_data.close()
			
			time.sleep(int(log_interval))
	
	except KeyboardInterrupt:
		print('keyboard interrupt detected')
		gps_data.close()
			
		
		
		
		
		
		
		
		
		
		
