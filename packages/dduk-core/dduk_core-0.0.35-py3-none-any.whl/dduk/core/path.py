#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Callable, Iterator, Optional, Type, TypeVar, Union, Tuple, List, Dict, Set, cast
import os
from .builtins import Builtins
from .environment import PlatformType, GetPlatformType


#--------------------------------------------------------------------------------
# 상수 목록.
#--------------------------------------------------------------------------------
SLASH : str = "/"
BACKSLASH : str = "\\"
TILDE : str = "~"
ROOTMARKERS : list[str] = [
	# 저장소.
	".svn",				# Subversion (SVN) version control system folder.
	".p4config",		# Perforce configuration file.
	".p4ignore",		# Perforce ignore patterns file.
	".git",				# Git version control system folder.
	".hg",				# Mercurial version control system folder.

	# 개발환경.
	".vscode",			# Visual Studio Code settings directory.
	".vs",				# Visual Studio settings directory.
	".idea",			# JetBrains IDE (PyCharm, IntelliJ IDEA, etc.) settings directory.

	# 파이썬 루트 파일.
	"setup.py",			# Python project setup script.
	"requirements.txt",	# Python project dependencies file.
	"Pipfile",			# Python project Pipenv dependency management file.
	"pyproject.toml",	# Python project configuration file.
	
	# "package.json",  # Node.js project configuration file.
	# "composer.json", # PHP project Composer configuration file.
	# "CMakeLists.txt",# CMake project configuration file.
	# "Makefile",      # Unix/Linux project build automation script.
	# "Cargo.toml",    # Rust project configuration file.
	# "gradle.build",  # Gradle project build script.
	# "pom.xml",       # Maven project configuration file.
	# ".terraform",    # Terraform configuration directory.
	# "Gemfile",       # Ruby project dependency management file.
	# "Rakefile",      # Ruby project build automation script.
	# "config.yml",    # Common YAML configuration file.
	# "config.yaml",   # Common YAML configuration file.
	# ".circleci",     # CircleCI configuration directory.
	# ".travis.yml",   # Travis CI configuration file.
]



#--------------------------------------------------------------------------------
# 프로젝트 패스.
#--------------------------------------------------------------------------------
class Path:
	#--------------------------------------------------------------------------------
	# 대상 파일을 기준으로 상위 경로로 거슬러 올라가며 프로젝트 루트 경로 찾기.
	# - rootMarkers를 None으로 두면 일반적으로 루트 디렉터리에 반드시 존재하는 저장소 디렉터리나 셋팅 파일 등을 기준으로 검색.
	# - rootMarkers를 커스텀 할 경우 루트 디렉터리에만 존재하는 독자적인 파일 혹은 디렉터리를 마커로 두고 그 이름을 입력.
	# - start의 경우 검색을 시작할 대상 파일로, 해당 파일의 조상 중에는 반드시 루트 폴더를 식별할 수 있는 이름의 마커가 존재해야함.
	#--------------------------------------------------------------------------------
	@staticmethod
	def GetRootPath(start : str, rootMarkers : list[str] = None) -> str:
		current = os.path.abspath(start)
		if os.path.isfile(current):
			current = os.path.dirname(current)
		if not rootMarkers: rootMarkers = ROOTMARKERS
		while True:
			if any(os.path.exists(os.path.join(current, marker)) for marker in rootMarkers):
				return current.replace(BACKSLASH, SLASH)
			parent = os.path.dirname(current)
			if parent == current: break
			current = parent
		raise FileNotFoundError("Project root not found.")
	

	#--------------------------------------------------------------------------------
	# 현재 사용자 전용 데이터 공간 경로 찾기. (윈도우는 사용상 주의!!)
	# - 윈도우 (사용자) : C:\Users\{사용자이름}
	# - 윈도우 (서비스) : C:\WINDOWS\system32\config\systemprofile
	# - 리눅스 : /home/{사용자이름}
	# - 맥OS : /Users/{사용자이름}
	#--------------------------------------------------------------------------------
	@staticmethod
	def GetUserPath() -> str:
		userPath : str = os.path.expanduser(TILDE)
		userPath = userPath.replace(BACKSLASH, SLASH)
		return userPath


	#--------------------------------------------------------------------------------
	# 현재 사용자 전용 애플리케이션 데이터 공간 경로 찾기. (윈도우는 사용상 주의!!)
	# - 윈도우 (사용자) : C:\Users\{사용자이름}\AppData\Local
	# - 윈도우 (서비스) : C:\WINDOWS\system32\config\systemprofile\AppData\Local
	# - 리눅스 : /home/{사용자이름}/.cache
	# - 맥OS : /Users/{사용자이름}/Library/Caches
	#--------------------------------------------------------------------------------
	@staticmethod
	def GetUserCachePath() -> str:
		platformType : PlatformType = GetPlatformType()
		userPath : str = Path.GetUserPath()
		userCachePath : str = str()
		if platformType == PlatformType.WINDOWS:
			userCachePath = os.path.join(userPath, "AppData", "Local").replace(BACKSLASH, SLASH)
		elif platformType == PlatformType.LINUX:
			userCachePath = os.path.join(userPath, ".cache")
		elif platformType == PlatformType.MACOS:
			userCachePath = os.path.join(userPath, "Library", "Caches")
		return userCachePath


	#--------------------------------------------------------------------------------
	# 모든 사용자 공용 데이터 저장 공간 경로 찾기.
	# - 윈도우 : C:\Users\Public
	# - 리눅스 : /usr/local/share
	# - 맥OS : /Users/Shared
	#--------------------------------------------------------------------------------
	@staticmethod
	def GetSharedPath() -> str:
		platformType : PlatformType = GetPlatformType()
		sharedPath : str = str()
		if platformType == PlatformType.WINDOWS:
			sharedPath = os.path.join("C:\\", "Users", "Public").replace(BACKSLASH, SLASH)
		elif platformType == PlatformType.LINUX:
			sharedPath = os.path.join("/", "usr", "local", "share")
		elif platformType == PlatformType.MACOS:
			sharedPath = os.path.join("/", "Users", "Shared")
		return sharedPath

	#--------------------------------------------------------------------------------
	# 애플리케이션 전용 데이터 저장 공간의 경로 찾기.
	# - 뒤에 애플리케이션 등의 고유 이름으로 된 폴더를 만들어서 사용할 것.
	# - 윈도우 : C:\ProgramData
	# - 리눅스 : /var/lib
	# - 맥OS : /Library/Application Support
	#--------------------------------------------------------------------------------
	@staticmethod
	def GetApplicationDataPath() -> str:
		platformType : PlatformType = GetPlatformType()
		applicationDataPath : str = str()
		if platformType == PlatformType.WINDOWS:
			applicationDataPath = os.path.join("C:\\", "ProgramData").replace(BACKSLASH, SLASH)
		elif platformType == PlatformType.LINUX:
			applicationDataPath = os.path.join("/", "var", "lib")
		elif platformType == PlatformType.MACOS:
			applicationDataPath = os.path.join("/", "Library", "Application Support")
		return applicationDataPath

	#--------------------------------------------------------------------------------
	# 애플리케이션 전용 데이터 저장 공간에서의 추가 경로 찾기.
	# - 예를 들어 Path.GetApplicationDataPathWithRelativePath("MyApplication") 식으로 내 애플리케이션 경로를 입력.
	#--------------------------------------------------------------------------------
	@staticmethod
	def GetApplicationDataPathWithRelativePaths(*relativePaths : str) -> str:
		platformType : PlatformType = GetPlatformType()
		applicationDataPath : str = Path.GetApplicationDataPath()
		absolutePath : str = str()
		if platformType == PlatformType.WINDOWS:
			absolutePath = os.path.join(applicationDataPath, *relativePaths).replace(BACKSLASH, SLASH)
		elif platformType == PlatformType.LINUX:
			absolutePath = os.path.join(applicationDataPath, *relativePaths)
		elif platformType == PlatformType.MACOS:
			absolutePath = os.path.join(applicationDataPath, *relativePaths)
		return absolutePath