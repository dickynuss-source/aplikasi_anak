[app]
title = MathApp
package.name = mathappv1
package.domain = org.mathapp.game

source.dir = .
source.include_exts = py,kv,png,jpg,atlas,wav
source.exclude_exts = spec

version = 1.0

# PENTING: Tambah ffpyplayer untuk audio support
requirements = python3,kivy==2.1.0,ffpyplayer

orientation = portrait
fullscreen = 0

android.api = 33
android.minapi = 21
android.private_storage = True
android.accept_sdk_license = True

android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

android.debug_artifact = apk
android.release_artifact = apk

p4a.branch = master
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1
