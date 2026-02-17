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
source.include_exts = py,png,jpg,kv,atlas,wav,json

# (list) Source files to exclude (let empty to not exclude anything)
source.exclude_exts = spec

# (str) Application versioning
version = 1.1

# ---------------------------
# Requirements
# ---------------------------
requirements = python3,kivy==2.1.0

# (list) Supported orientations
orientation = portrait

# (bool) fullscreen (0 = windowed, 1 = fullscreen)
fullscreen = 0

# (list) Permissions
# PENTING: INTERNET diperlukan untuk membuka link WhatsApp (webbrowser)
android.permissions = INTERNET

# ---------------------------
# Android settings
# ---------------------------
# Target Android API
android.api = 33
# Minimum API
android.minapi = 21
# Use private storage
android.private_storage = True
# Auto accept SDK licenses
android.accept_sdk_license = True

# Build archs
android.archs = arm64-v8a, armeabi-v7a

# Enable Android backup
android.allow_backup = True

# Build artifact format
android.release_artifact = apk
android.debug_artifact = apk

# Python for android (p4a) specific
p4a.branch = master
p4a.bootstrap = sdl2

# iOS settings (tidak dipakai di Android)
ios.kivy_ios_dir = ../kivy-ios
ios.codesign.allowed = false

[buildozer]
# Log level
log_level = 2
warn_on_root = 1
