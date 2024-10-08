from setuptools import setup, find_packages

setup(
	name="spotify-dlp",
	author="zWolfrost",
	version="2.0.1",
	description="Command line downloader for spotify tracks, playlists, albums and top artists tracks.",
	long_description=open("README.md").read(),
	long_description_content_type="text/markdown",
	url="https://github.com/zWolfrost/spotify-dlp",
	packages=find_packages(),
	install_requires=[
		"yt_dlp>=2024.4.9",
		"music-tag==0.4.3",
		"pillow==10.4.0"
	],
	entry_points={
		"console_scripts": [
			"spotify-dlp = spotify_dlp:main"
		]
	}
)
