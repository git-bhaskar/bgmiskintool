[app]

title = Skin
package.name = skin
package.domain = org.bgmi

source.dir = .
source.main = main.py
source.include_exts = py,txt,png,jpg,kv,atlas

version = 1.0

requirements = python3,kivy,kivymd

orientation = portrait
fullscreen = 0

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a

android.accept_sdk_license = True
android.allow_backup = True
android.debug_artifact = apk


[buildozer]

log_level = 2
warn_on_root = 1
