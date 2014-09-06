##
#   :namespace  blur3d.api.motionbuilder.external
#
#   :remarks    This class can be used even outside of motionbuilder. It gives you info on where
#				motionbuilder is installed, and allows you to run scripts in motionbuilder.
#				To Access this class use: blur3d.api.external('motionbuilder')
#   
#   :author     mikeh@blur.com
#   :author     Blur Studio
#   :date       09/03/14
#

#------------------------------------------------------------------------------------------------------------------------

import os

from blur3d.api import Exceptions
from blur3d.api.abstract.external import External as AbstractExternal

#------------------------------------------------------------------------------------------------------------------------

class External(AbstractExternal):
	_hkeyBase = r'Software\Autodesk\MotionBuilder'
	# In case the software is installed but not used don't find it when not passing in a version
	_ignoredVersions = set(os.environ.get('BDEV_STUDIO_IGNORED_MOTIONBUILDER', '2013,2015').split(','))
	# map years to version numbers 
	# NOTE: I am guessing that these are correct based on 2014 being version 14000.0
	_yearForVersion = {'12': '2012', '13': '2013', '14': '2014', '15': '2015'}
	
	@classmethod
	def binariesPath(cls, version=None, architecture=64, language='English'):
		""" Finds the install path for various software installations.
		:param version: The version of the software. Default is None
		:param architecture: The bit type to query the registry for(32, 64). Default is 64
		:param language: Optional language that may be required for specific softwares.
		"""
		version = cls._yearForVersion.get(unicode(version), version)
		hive = 'HKEY_LOCAL_MACHINE'
		if version == None:
			# Get all of the installed versions so we can find the latest version.
			versions = cls._listRegKeys(hive, cls._hkeyBase, architecture=architecture)
			for v in sorted(versions, reverse=True):
				if v not in cls._ignoredVersions:
					version = v
					break
		hkey = r'{hkeyBase}\{version}'.format(hkeyBase=cls._hkeyBase, version=version)
		try:
			ret = cls._registryValue(hive, hkey, 'InstallPath', architecture)[0]
		except WindowsError:
			raise Exceptions.SoftwareNotInstalled('MotionBuilder', version=version, architecture=architecture, language=language)
		# If the version is not installed this will return '.', we want to return False.
		if ret:
			return os.path.normpath(ret)
		raise Exceptions.SoftwareNotInstalled('MotionBuilder', version=version, architecture=architecture, language=language)

	@classmethod
	def scriptPath(cls):
		return r'C:\temp\motionbuilder_script.py'

	@classmethod
	def scriptLog(cls):
		return r'C:\temp\motionbuilder_script.log'