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
source.include_exts = py,png,jpg,kv,atlas

# (list) Source files to exclude (let empty to not exclude anything)
source.exclude_exts = spec

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
requirements = python3,kivy

# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
# PENTING: Jangan aktifkan WRITE_EXTERNAL_STORAGE. 
# Kita sudah pakai user_data_dir yang legal tanpa izin.
# android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (list) The Android archs to build for.
# PENTING: Ini mencegah crash di HP baru (64-bit)
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) The format used to package the app for release mode (aab or apk or aar).
android.release_artifact = aab

# (str) The format used to package the app for debug mode (apk or aar).
android.debug_artifact = apk

# Python for android (p4a) specific
p4a.branch = master
p4a.bootstrap = sdl2

# iOS specific
ios.kivy_ios_dir = ../kivy-ios
ios.codesign.allowed = false

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2
# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
