Hotel Location Analysis Supporting Tools

Required software:
Apache Http Server 2.x with mod_wsgi
Python 2.7 with GDAL, reportlab, PIL, web.py

Installation:
Clone and copy everything to /var/www. If you put them in other folder, you need change "basedir" in code.py as well as several hard-coded url.

Install mod_wsgi and configure mod_wsgi. Here is one example:
    WSGIScriptAlias /hotel /var/www/HotelDemo/code.py/
    Alias /hotel/static /var/www/HotelDemo/static/
    AddType text/html .py
    <Directory /var/www/HotelDemo>
        Order allow,deny
        allow from all
    </Directory>

Change permission of folder "maps" to 755 or 777. Make sure www-data(nobody,www) has full permission there.

Enjoy.

LICENSE:
This project is licensed under X11/MIT license

Copyright (c) 2013 [striges@ufl.edu]

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
