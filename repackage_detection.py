import os, argparse

from struct import *
from zipfile import ZipFile


class RepackageDetection:
	def __init__(self, apk_file_path):
		self.apk_file_path = apk_file_path
		self.repackage = False

	def detect(self):
		try:
			if not os.path.exists(apk_file_path):
				return
			with ZipFile(apk_file_path) as apk:
				apk.extract('classes.dex', 'dex-out')
				classes_dex_path = os.path.join(os.getcwd(), 'dex-out', 'classes.dex')
				if not os.path.exists(classes_dex_path):
					return

				with open(classes_dex_path, 'rb') as classes_dex:
					# string_ids_size
					classes_dex.seek(56)
					string_ids_size = unpack("<i", classes_dex.read(4))[0]

					# string_ids_off
					classes_dex.seek(60)
					string_ids_off = unpack("<i", classes_dex.read(4))[0]

					last_string_offset = 0
					for i in xrange(string_ids_size):
						# string_ids
						classes_dex.seek(string_ids_off + i*4)
						cur_string_offset = unpack("<i", classes_dex.read(4))[0]
						if cur_string_offset > last_string_offset:
							last_string_offset = cur_string_offset
						else:
							self.repackage = True
							break
		except Exception, ex:
			print ex

	def is_repackaged(self):
		return self.repackage

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', dest='apk_file_path', help='The full path of the APK file')
	args = parser.parse_args()
	apk_file_path = args.apk_file_path
	if apk_file_path is not None:
		repackage_detection = RepackageDetection(apk_file_path)
		repackage_detection.detect()
		if repackage_detection.is_repackaged():
			print '%s is repackaged' % apk_file_path
		else:
			print '%s is not repackaged' % apk_file_path
	else:
		print 'Usage: python repackage_detection.py -f <apk_file_path>'