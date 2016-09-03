---
layout: post
title: Akses File Android di Komputer Dengan Mifile Explorer
date: '2015-02-03T08:14:00.000-08:00'
tags:
- Komputer
- Android
modified_time: '2016-06-23T14:44:44.174-07:00'
thumbnail: http://4.bp.blogspot.com/-784kKmYAz4c/VNDXyy4mNOI/AAAAAAAAAp4/BSfFP2qClmI/s72-c/Mifile%2BExplorer.jpg
blogger_id: tag:blogger.com,1999:blog-3414465807055734912.post-6185297103895761729
blogger_orig_url: http://rmsubekti.blogspot.com/2015/02/akses-file-android-di-komputer-dengan.html
---
Memindahkan file dari penyimpanan komputer ke ponsel android atau sebaliknya bisa kita lakukan dengan bantuan kabel USB atau card reader. Mungkin kamu tidak perlu mencoba cara ini karena nantinya cara lama tersebut menjadi ribet jika kamu sudah terbiasa menggunakan FTP melalui Wifi ini. Sebenarnya ini adalah salah satu fitur dari aplikasi android yang bernama Mifile Explorer. Aplikasi ini tidak ada di Playstore dan mungkin kamu bisa mencarinya di forum XDA Developer.
![mifile](https://4.bp.blogspot.com/-784kKmYAz4c/VNDXyy4mNOI/AAAAAAAAAp4/BSfFP2qClmI/s1600/Mifile%2BExplorer.jpg)

Aplikasi Mifile Explorer ini sama halnya dengan File Explorer pada umumnya, tapi ada fitur tertentu yang membuat aplikasi ini lebih unggul dibanding aplikasi file explorer lain. Pada aplikasi ini ada 3 tab diantaranya :

1. **Tab Browse** untuk mengakses file yang umum digunakan oleh user untuk melihat file mereka berdasarkan jenis file tanpa harus mencarinya langsung melalui folder.
2. **Tab SDCARD** untuk mengakses file langsung dari folder. Kamu juga bisa mengakses file system jika ponsel kamu sudah di root.
3. **Tab FTP** untuk layanan FTP. Dengan layanan ini kamu bisa mengakses penyimpanan ponsel kamu melalui komputer.

Aplikasi ini juga bisa mengekstrak file zip yang sangat berguna jika kita mendownload atau memiliki file zip di posel maka bisa langsung di ekstrak. Selain itu aplikasi ini juga tidak memakan memory penyimpanan karena ukurannya kurang dari 1 mb. Saya sendiri malah menghapus File Explorer bawaan dan menggantinya dengan Mifile Explorer karena lebih kecil di penyimpanan dan lebih banyak fitur yang bisa digunakan.

Mungkin cukup untuk perkenalannya dengan aplikasi ini, kamu bisa mencarinya di XDA Developer untuk mencoba. Sekarang langsung saja ke judulnya bagaimana cara menggunakan layanan FTPnya. Untuk menggunakan layanan ftp kamu harus terhubung dengan Wifi.

Oke langsung saja berikut ini langkah - langkahnya:

![setting](https://4.bp.blogspot.com/-17xEJTg7t_w/VNDkxz1FytI/AAAAAAAAAqI/N1QfMfFN1L8/s1600/ftp%2Bsetting.jpg)

1. Aktifkan dan koneksikan ponsel ke wifi
2. Buka mifile Explorer kemudian pilih tab FTP
3. Pilih Start Service, akan muncul setting untuk pertama kali menggunakan layanan ini
4. Ketikan username dan password sesuai keinginan
5. Pada form **Stay within folder** ketikkan `/sdcard` atau `/mnt/sdcard` agar lebih aman
6. Simpan pengaturan

Sekarang layanan FTP sudah aktif, kamu tinggal mengaksesnya dengan menggetikkan alamat FTP yang ditampilkan ke address bar di File explorer Windows yang terhubung dengan wifi yang sama untuk login dan mengakses penuh penyimpanan ponsel.

![akses ftp](https://2.bp.blogspot.com/-LcFZnnZs8Yc/VNDrpn56wkI/AAAAAAAAAqY/Z703RJS0tXA/s1600/akses%2Bftp.png)

untuk mengakses file yang ada di sdcard. Sekarang kamu bisa mengakses penyimpanan ponsel kamu seperti layaknya menggunakan usb atau Card Reader.

**Peringatan :** Folder lain bisa kamu akases jika ponsel sudah di root. Hati - hati dalam memodifikasi file dan folder lain selain yang ada di sdcard bisa merusak sistem ponsel kamu. Atur folder default di settingan ke sdcard agar lebih aman.

Link ini mungkin bisa membantu kamu menemukan aplikasi mifi explorer:

- {% include x.html l="http://forum.xda-developers.com/showthread.php?t=2051086" t="http://forum.xda-developers.com/showthread.php?t=2051086" %}
- {% include x.html l="http://forum.xda-developers.com/showthread.php?t=1739622" t="http://forum.xda-developers.com/showthread.php?t=1739622" %}
