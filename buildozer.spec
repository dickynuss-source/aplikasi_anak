[app]
# (str) Title of your application
title = MathApp

# (str) Package name
package.name = mathappv1

# (str) Package domain (needed for android/ios packaging)
package.domain = org.mathapp.game

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
# include wav + kv + common image extensions and atlas
source.include_exts = py,kv,png,jpg,atlas,wav,mp3,ogg

# (list) Source files to exclude (let empty to not exclude anything)
source.exclude_exts = spec,pyc

# (str) Application versioning
version = 1.0

# ---------------------------
# Requirements
# ---------------------------
# python3 + kivy + ffpyplayer for stable audio on Android
requirements = python3,kivy==2.1.0,ffpyplayer

# (list) Supported orientations
orientation = portrait

# (bool) fullscreen (0 = windowed, 1 = fullscreen)
fullscreen = 0

# (list) Permissions
# Uncomment if your app needs internet or other permissions
# android.permissions = INTERNET

# ---------------------------
# Android settings
# ---------------------------
# Target Android API (set reasonably high)
android.api = 33
# Minimum API supported
android.minapi = 21

# Use private storage (no external storage permission required)
android.private_storage = True

# Auto accept SDK license to avoid interactive prompt during build
android.accept_sdk_license = True

# The Android archs to build for (both 32 & 64 bit)
android.archs = arm64-v8a, armeabi-v7a

# Enable Android auto backup feature
android.allow_backup = True

# Build artifact format for debug/release
android.debug_artifact = apk
android.release_artifact = apk

# Python-for-Android settings
p4a.branch = master
p4a.bootstrap = sdl2

# (Optional) Pin NDK version if you have known issues (uncomment to use)
# android.ndk = 23b

# (Optional) If you hit issues with ffpyplayer native deps on CI, consider:
# p4a.source_dir = /path/to/p4a   (not usually needed)

# ---------------------------
# Extra buildozer options
# ---------------------------
# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2
# (int) Warn if buildozer is run as root
warn_on_root = 1

# (Optional) Increase the timeout for CI builders (comment/uncomment as needed)
# build_timeout = 120

# (Optional) Specify requirements for recipes that need system libs (rare)
# android.gradle_dependencies = com.android.support:appcompat-v7:26.1.0

