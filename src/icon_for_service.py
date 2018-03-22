import os
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GdkPixbuf, GObject, GLib

def icon_for_service(service_name):
    # TODO: Optimization
    filename = None
    icons = os.listdir(os.getcwd().rpartition('/')[0] + "/icons")
    for n in icons:
        if service_name.find(n.rpartition('.')[0]) != -1:
            filename = "icons/" + n
            break

    if filename != None:
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(os.getcwd().rpartition('/')[0] + "/" + filename)
        return pixbuf

    return None


# print (icon_theme.list_contexts())
#
# for n in icon_theme.list_icons('Mimetypes'):
#     print (n)
# icon_theme = Gtk.IconTheme.get_default()
# icon = icon_theme.load_icon("gnome-mime-application-x-compress", 32, Gtk.IconLookupFlags.FORCE_SVG)

# gnome-mime-application-x-compress
#gnome-mime-text-x-changelog
#text-x-changelog
# gnome-mime-application-x-compress
# gnome-fs-executable
# application-x-python-bytecode
# gnome-mime-text-x-readme
# libreoffice-oasis-text-template
# application-x-compress
# x-dia-diagram
# x-office-presentation
# image-x-portable-bitmap
# gnome-mime-application-x-bittorrent
# application-x-rar
# text-x-generic-template
# application-x-ole-storage
# application-vnd.oasis.opendocument.graphics-template
# audio-x-vorbis+ogg
# phatch-actionlist
# application-x-keepass
# gnome-mime-application-x-font-linux-psf
# office-document
# x-office-drawing-template
# stock_calendar
# application-vnd.ms-visio.drawing.main+xml
# gnome-mime-application-vnd.sun.xml.draw
# image-bmp
# image-png
# gnome-mime-image-x-psd
# application-x-rpm
# gnome-mime-image-x-cmu-raster
# application-vnd.ms-excel
# gnome-mime-text-x-c++
# opera-widget
# gnome-mime-application-x-python-bytecode
# gnome-exe-thumbnailer-generic
# gnome-mime-text-x-c
# application-vnd.openxmlformats-officedocument.spreadsheetml.template
# audio-x-flac+ogg
# gnome-mime-text-x-zsh
# application-vnd.sun.xml.draw
# source-smart-playlist
# gnome-mime-video-x-ms-asf
# sound
# application-7zip
# gnome-mime-application-vnd.openxmlformats-officedocument.spreadsheetml.sheet
# gnome-mime-application-x-executable
# rpm
# gnome-mime-application-x-applix-word
# audio-x-ms-wma
# application-x-msdownload
# gnome-exe-thumbnailer-template
# folder_tar
# text-x-bak
# application-vnd.wordperfect
# gnome-mime-application-vnd.oasis.opendocument.graphics
# office-illustration
# unknown
# application-x-jar
# gnome-mime-application-x-7z-compressed
# gnome-mime-application-x-dvi
# application-x-shockwave-flash
# application-x-sln
# text-xhtml+xml
# gnome-mime-application-vnd.stardivision.impress
# image-x-icon
# office-spreadsheet
# application-vnd.oasis.opendocument.text
# gnome-mime-video
# pdf
# package-x-generic
# gnome-mime-application-msword
# gnome-mime-application-vnd.oasis.opendocument.presentation-template
# gnome-mime-application-vnd.oasis.opendocument.text
# gnome-mime-application-vnd.rn-realmedia-secure
# text-spreadsheet
# gnome-mime-text-x-gtkrc
# gnome-mime-application-x-archive
# image-x-psdimage-x-psd
# application-x-flash-video
# gnome-mime-application-vnd.oasis.opendocument.presentation
# font_type1
# x-office-spreadsheet
# application-rtf
# application-x-sqlite3
# application-x-sqlite2
# application-x-csproj
# gnome-mime-application-x-javascript
# playlist-automatic
# application-vnd.openxmlformats-officedocument.presentationml.slideshow
# media-video
# empty
# gnome-mime-image-vnd.adobe.photoshop
# gnome-mime-application-x-font-sunos-news
# message-rfc822
# source-playlist
# jpg
# font_bitmap
# application-x-theme
# gtk-file
# text-x-credits
# gnome-fs-regular
# application-vnd.openxmlformats-officedocument.presentationml.presentation
# gnome-mime-application-x-kword
# gnome-mime-application-rtf
# gnome-mime-text-x-sh
# gnome-mime-application-x-tar
# application-text
# gnome-mime-application-x-deb
# gnome-mime-application-x-ruby
# audio-mpeg
# text-x-source
# text-x-script
# application-x-pem-key
# application-x-ace
# application-x-sharedlib
# gnome-mime-text-x-csrc
# gnome-mime-image-gif
# text-x-makefile
# gnome-mime-text-x-csh
# text-mht
# text-x-install
# application-x-executable
# application-illustrator
# authors
# application-vnd.oasis.opendocument.graphics
# txt
# shellscript
# gnome-mime-application-x-abiword
# gnome-mime-image-tiff
# exec
# application-x-ruby
# gnome-mime-text-x-java
# gnome-mime-application-x-gnome-theme-package
# gnome-mime-application-x-shockwave-flash
# package
# application-x-pak
# gnome-mime-image-x-xpixmap
# application-x-arc
# text-x-chdr
# application-javascript
# gnome-mime-application-magicpoint
# text-x-tex
# gnome-mime-text-x-c++hdr
# gnome-mime-application-vnd.oasis.opendocument.spreadsheet
# image-x-win-bitmap
# font
# font-x-generic
# vcalendar
# application-x-zip
# application-vnd.oasis.opendocument.spreadsheet-template
# application-x-bittorrent
# gnome-mime-application-x-glade
# x-office-drawing
# gnome-mime-application-x-php
# gnome-mime-text-x-makefile
# application-vnd.oasis.opendocument.database
# x-office-presentation-template
# application-x-trash
# gnome-mime-video-x-ms-wmv
# binary
# txt2
# application-vnd.oasis.opendocument.spreadsheet
# gnome-mime-application-vnd.openxmlformats-officedocument.presentationml.presentation
# gnome-mime-application-vnd.oasis.opendocument.spreadsheet-template
# gnome-mime-text-html
# application-x-lhz
# application-pgp-encrypted
# application-vnd.sun.xml.calc
# gnome-mime-application-x-killustrator
# image-x-eps
# audio-x-wav
# application-x-7z-compressed
# gnome-mime-text-plain
# jpeg
# gnome-mime-text-x-python
# gnome-mime-application-x-gnome-app-info
# gnome-mime-text-x-javascript
# multipart-encrypted
# gnome-mime-text-x-changelog
# gnome-mime-application-x-gnumeric
# application-vnd.openxmlformats-officedocument.spreadsheetml.sheet
# wordprocessing
# text-x-c++src
# gnome-mime-application-x-class-file
# libreoffice-oasis-drawing-template
# gnome-mime-application-vnd.stardivision.writer
# application-x-cd-image
# application-x-gnumeric
# application-x-lha
# audio-x-generic
# zip
# gnome-mime-image-jpeg
# text-xml
# gnome-mime-text-css
# application-vnd.openxmlformats-officedocument.wordprocessingml.document
# gnome-mime-image-vnd.microsoft.icon
# gnome-mime-application-postscript
# application-x-class-file
# openofficeorg3-database
# application-ogg
# gnome-mime-application-vnd.scribus
# application-mbox
# gnome-mime-text-x-credits
# document
# gnome-mime-application-x-font-afm
# gnome-mime-application-x-font-bdf
# text-htmlh
# application-x-m4
# gnome-mime-application-x-java
# gnome-mime-application-vnd.rn-realmedia-vbr
# application-x-compressed-tar
# gnome-mime-x-install
# application-vnd.oasis.opendocument.text-web
# text-x-readme
# gnome-mime-text-x-install
# application-vnd.oasis.opendocument.formula
# text-x-copying
# openofficeorg3-oasis-database
# html
# application-pkcs7-mime
# application-pdf
# text-enriched
# application-octet-stream
# application-vnd.openxmlformats-officedocument.presentationml.template
# gnome-mime-application-x-rar
# message
# none
# audio-x-mpegurl
# application-x-ms-dos-executable
# gnome-mime-application-wordperfect
# gnome-mime-application-x-ms-dos-executable
# application-vnd.visio
# gnome-mime-text-x-csharp
# gnome-mime-application-ogg
# gnome-mime-application-vnd.stardivision.calc
# gnome-mime-image-x-portable-bitmap
# openofficeorg3-extension
# text-x-bibtex
# application-x-javascript
# application-vnd.sun.xml.writer
# gnome-mime-application-x-cpio
# gnome-mime-application-x-rpm
# x-office-document
# gnome-mime-application-pdf
# gnome-mime-application-rss+xml
# image
# image-x-psd
# svg
# gnome-mime-application-x-font-pcf
# gnome-mime-application-x-bzip-compressed
# text-x-java-source
# image-gif
# image-x-svg+xml
# gnome-mime-application-vnd.sun.xml.calc
# gnome-mime-application-vnd.oasis.opendocument.graphics-template
# gnome-mime-application-x-scribus
# text-x-c
# gnome-mime-application-vnd.sun.xml.calc.template
# openofficeorg3-drawing
# image-x-xcf
# text-x-c++
# gnome-mime-application-javascript
# video-x-generic
# package_editors
# x-office-address-book
# gnome-mime-application-x-7zip
# extension
# gnome-mime-application-vnd.sun.xml.draw.template
# gnome-mime-text-x-authors
# gnome-mime-text-x-java-source
# image-svg+xml
# x-office-formula-template
# image-x-generic
# application-x-extension-html
# text-x-vcard
# gnome-mime-application-vnd.oasis.opendocument.text-web
# gnome-mime-text-vnd.wap.wml
# gnome-mime-application-x-jar
# gnome-mime-application-vnd.oasis.opendocument.text-template
# gnome-mime-application-vnd.lotus-1-2-3
# encrypted
# application-x-scribus
# package_wordprocessing
# gnome-mime-x-font-afm
# gnome-mime-audio
# gnome-exe-thumbnailer-generic-x
# misc
# playlist
# gnome-mime-application-vnd.oasis.opendocument.image
# application-x-java
# libreoffice-oasis-presentation-template
# gnome-mime-application-vnd.sun.xml.writer.template
# audio-x-speex+ogg
# gnome-mime-application-x-gzpostscript
# image-x-ico
# gnome-mime-text-x-chdr
# gnome-mime-image-bmp
# x-office-document-template
# gnome-mime-image-png
# gnome-mime-application-x-bzip-compressed-tar
# text-x-sql
# gnome-mime-application-x-shellscript
# image-jpeg2000
# application-pgp-keys
# font_truetype
# libreoffice-oasis-spreadsheet-template
# spreadsheet
# application-x-glade
# media-audio
# gnome-mime-application-vnd.sun.xml.writer
# audio-x-mp3-playlist
# text-x-generic
# text-x-authors
# gnome-mime-application-x-desktop
# gnome-mime-application-vnd.ms-excel
# audio-x-scpls
# text-x-changelog
# vnd.oasis.opendocument.drawing
# application-vnd.oasis.opendocument.presentation-template
# application-vnd.ms-visio.template.main+xml
# text-html
# application-x-tar
# opera-unite-application
# application-x-deb
# gnome-mime-text-x-copying
# gnome-mime-text-x-source
# application-vnd.scribus
# gnome-mime-application-x-gzip
# application-x-7zip
# gnome-mime-application-x-designer
# libreoffice-oasis-presentation
# template_source
# gnome-mime-application-x-compressed-tar
# gnome-mime-text-x-vcalendar
# application-vnd.oasis.opendocument.presentation
# application-x-desktop
# gnome-mime-application-x-bzip
# application-x-designer
# tar
# application-zip
# image-vnd.microsoft.icon
# audio-x-mpeg
# stock_script
# deb
# gnome-mime-application-vnd.rn-realmedia
# gnome-mime-application-x-ace
# gnome-mime-application-x-tarz
# text-x-css
# application-x-gzip
# application-xml
# gnome-mime-application-vnd.openxmlformats-officedocument.presentationml.slideshow
# gnome-mime-application-atom+xml
# gnome-mime-application-x-arj
# gnome-mime-image
# application-x-cue
# gnome-mime-text
# text-x-c++hdr
# application-vnd.openxmlformats-officedocument.wordprocessingml.template
# application-x-php
# application-atom+xml
# text-x-java
# image-tiff
# gnome-mime-application-zip
# gnome-mime-application-x-java-archive
# application-vnd.rn-realmedia
# media-image
# gnome-mime-application-x-theme
# application-x-shellscript
# gnome-mime-application-vnd.oasis.opendocument.formula
# gnome-mime-application-xhtml+xml
# gnome-mime-application-x-applix-spreadsheet
# gnome-mime-application-x-lhz
# gnome-mime-application-x-stuffit
# text-x-javascript
# gnome-mime-application-xml
# x-office-spreadsheet-template
# application-vnd.oasis.opendocument.formula-template
# gnome-mime-application-x-zip
# gnome-mime-application-vnd.openxmlformats-officedocument.wordprocessingml.document
# text-x-csrc
# gnome-mime-application-vnd.sun.xml.impress.template
# application-x-java-archive
# gnome-mime-application-x-cpio-compressed
# text-x-python
# image-x-tga
# gnome-mime-text-x-c++src
# gnome-mime-application-vnd.sun.xml.impress
# application-vnd.ms-access
# video
# application-msword
# www
# gnome-package
# gnome-mime-application-x-font-ttf
# application-rss+xml
# application-x-archive
# openofficeorg3-oasis-spreadsheet
# audio-x-generic-symbolic
# gnome-mime-application-x-lha
# gnome-mime-application-x-kspread
# opera-extension
# gnome-mime-application-x-kpresenter
# application-x-matroska
# text-css
# application-vnd.oasis.opendocument.text-template
# image-jpeg
# text-plain
# gnome-mime-application-x-tex
# stock_addressbook
# text-richtext
# application-x-gnome-theme-package
# kpresenter_kpr
# gnome-mime-application-x-sharedlib
# text-x-preview
# audio-x-adpcm
# application-vnd.ms-powerpoint
