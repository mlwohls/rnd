[app]

title = RND Golf
package.name = rndgolf
package.domain = wohls.com

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.2
requirements = python3,kivy,kivymd,sqlite3,datetime,uuid

orientation = portrait
fullscreen = 0
#my changes below
android.arch = arm64-v8a
#android.archs = arm64-v8a, armeabi-v7a
android.release_artifact = apk
#p4a.branch = develop


# iOS specific
#ios.kivy_ios_url = https://github.com/kivy/kivy-ios
#ios.kivy_ios_branch = master
#ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
#ios.ios_deploy_branch = 1.7.0

[buildozer]
log_level = 2
