#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

homepage = """
<html>
<head></head>
<body>
<h1>Un generatore di password italiano nello stile di xkcd</h1>
<form action="/generate" method="get">
<p>
<h3>numero di parole</h3>
<select name="nwords">
  <option value="3">tre</option>
  <option value="4" selected>quattro</option>
  <option value="5">cinque</option>
  <option value="6">sei</option>
</select>
</p>
<p>
<h3>acronimo</h3>
<input type="text" name="acrostic" value="no">
<input type="submit" value="Genera password">
</form>
<p>
L'idea per questo server, che genera password con più o meno 92 bit di entropia, viene da questa vignetta</p>
<p>
<a href="http://xkcd.com/936/">
<img src="http://imgs.xkcd.com/comics/password_strength.png" alt="Clic per andare al sito originale"/>
</a>
</p>
<p>
Se avete constraint sul tipo di caratteri e la lunghezza, come di solito accade con i siti bancari, c'&egrave; un generatore utile, open source e scritto in Perl, <a href="https://www.xkpasswd.net/c/index.cgi">a questo indirizzo</a>.
<p>
Wordlist grazie a <a href="http://coding.napolux.com/post/42114980272/ruzzle-lista-parole-italiane">Napolux</a>.
</p>
<p>
Basato sul <a href="https://github.com/redacted/XKCD-password-generator">modulo python di Steven Tobin e altri</a>.
</p>
<pre>
Contributors: Steven Tobin,
              Rob Lanphier <robla@robla.net>,
              Mithrandir <mithrandiragain@lavabit.com>,
              Daniel Beecham <daniel@lunix.se>,
              Kim Slawson <kimslawson@gmail.com>,
              Stanislav Bytsko <zbstof@gmail.com>,
              Lowe Thiderman <lowe.thiderman@gmail.com>,
              Daniil Baturin <daniil@baturin.org>

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the <organization> nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
</pre>
</html>
"""

import webapp2
import logging

# import the generate_xkcdpassword and generate_wordlist functions
from xkcd_password import generate_wordlist, generate_xkcdpassword

# create a wordlist
mywords = generate_wordlist(wordfile='static/italian.txt', min_length=5, max_length=8,)
logging.getLogger().setLevel(logging.DEBUG)
logging.info("wordlist generata")


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
        self.response.write(homepage)


class Generate(webapp2.RequestHandler):
    def get(self):
        nwords = self.request.get('nwords')
        acrostic = self.request.get('acrostic')
        passwd = 'error'
        acrostic = acrostic.strip().lower()

        if acrostic in ('no', ''):
            passwd = generate_xkcdpassword(mywords, n_words=4)
        else:
            try:
                passwd = generate_xkcdpassword(mywords, acrostic=acrostic)
            except:
                passwd = "errore nella stringa specificata come acronimo"

        self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
        self.response.write('<h1>' + passwd + '</h1>')

    
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/generate', Generate)
],
debug=True)
