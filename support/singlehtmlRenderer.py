# -*- coding: utf-8 -*-
#

import abstractRenderer
import codecs
import datetime
import books
import os

#
#   Simplest renderer. Ignores everything except ascii text.
#
STANDARD_SUFFIX = '.html'

class Renderer(abstractRenderer.AbstractRenderer):
    
    def __init__(self, inputDir, outputDir, outputName, config):
        abstractRenderer.AbstractRenderer.__init__(self, inputDir, outputDir, outputName, config)
        # Unset
        self.f = None  # output file stream
        # IO
        self.outputFilename = os.path.join(outputDir, outputName + '.html')
        self.inputDir = inputDir
        # Position
        self.cb = u''    # Current Book
        self.cc = u'001'    # Current Chapter
        self.cv = u'001'    # Currrent Verse
        self.indentFlag = False
        self.bookName = u''
        
    def render(self, order="normal"):
        self.loadUSFM(self.inputDir)
        self.f = codecs.open(self.outputFilename, 'w', 'utf_8_sig')
        h = u"""
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <meta http-equiv="content-type" content="text/html; charset=utf-8" />
            <title>Bible</title>
            <style media="all" type="text/css">
            .indent-0 {
                margin-left:0em;
                margin-bottom:0em;
                margin-top:0em;
            }
            .indent-1 {
                margin-left:0em;
                margin-bottom:0em;
                margin-top:0em;
            }
            .indent-2 {
                margin-left:1em;
                margin-bottom:0em;
                margin-top:0em;
            }
            .indent-3 {
                margin-left:2em;
                margin-bottom:0em;
                margin-top:0em;
            }
            .c-num {
                color:gray;
            }
            .v-num {
                color:gray;
            }
            .tetragrammaton {
                font-variant: small-caps;
            }
            </style>
            
        </head>
        <body>
        <h1>Table of Contents</h1>
        <p><b>Old Testament</b></p>
        {{{otlinks}}}
        <p><b>New Testament</b></p>
        <p class="indent-1"><a href="#040">Matthew</a></p>
        {{{ntlinks}}}
        
        """
        h = h.replace('{{{otlinks}}}', self.bookList(1, 39))
        h = h.replace('{{{ntlinks}}}', self.bookList(40, 66))
        self.f.write(h.encode('utf-8'))
        self.f.write('<p>Draft built ' + datetime.date.today().strftime("%A, %d %B %Y") + '</p>\n\n')
        self.run(order)
        self.f.write('</body></html>')
        self.f.close()
        
    def bookList(self, s, f):
        h = ''
        for b in range(s, f):
            if self.booksUsfm.has_key(books.silNames[b]):
                h = h + '\n<p class="indent-1"><a href="#' + str(b).zfill(3) + '">' + books.bookNames[b-1].replace(' ', '&nbsp;') + '</a></p>'
            else:
                h = h + '\n' + books.bookNames[b-1] + '<p class="indent-1">'
        return h
        
    def escape(self, s):
        return s.replace(u'~',u'&nbsp;')

    def write(self, unicodeString):
        self.f.write(unicodeString.replace(u'~', u' '))
        
    def writeIndent(self, level):
        self.write(u'\n\n')
        if level == 0:
            self.indentFlag = False
            self.write(u'<p class="indent-0">')
            return 
        if not self.indentFlag:
            self.indentFlag = True
            self.write(u'<p>')
        self.write(u'<p class="indent-' + str(level) + u'">')

    def render_id(self, token): 
        self.cb = books.bookKeyForIdValue(token.value)
        self.indentFlag = False
        self.write(u'\n\n<h1 id="' + self.cb + u'"></h1>\n')
    def render_h(self, token):       self.bookname = token.value 
    def render_mt1(self, token):      self.write(u'\n\n<h1>' + token.value + u'</h1>')
    def render_mt2(self, token):     self.write(u'\n\n<h2>' + token.value + u'</h2>')
    def render_mt3(self, token):     self.write(u'\n\n<h2>' + token.value + u'</h2>')
    def render_ms1(self, token):      self.write(u'\n\n<h3>' + token.value + u'</h3>')
    def render_ms2(self, token):     self.write(u'\n\n<h4>' + token.value + u'</h4>')
    def render_p(self, token):
        self.indentFlag = False
        self.write(u'\n\n<p>')
    def render_pi(self, token):
        self.indentFlag = False
        self.write(u'\n\n<p class"indent-2">')
    def render_m(self, token):
        self.indentFlag = False
        self.write(u'\n\n<p>')
    def render_s1(self, token):
        self.indentFlag = False
        self.write(u'\n\n<h5>' + token.getValue() + u'</h5>')
    def render_s2(self, token):
        self.indentFlag = False
        self.write(u'\n\n<p align="center">----</p>')
    def render_c(self, token):
        self.cc = token.value.zfill(3)
        self.write(u'\n\n<p class="c-num">[' + self.bookname + u' ' + token.value + u']</p>')
    def render_v(self, token):
        self.cv = token.value.zfill(3)
        self.write(u' <span class="v-num">[' + token.value + u']</span> ')
    def render_wj_s(self, token):     self.write(u'<span class="woc">')
    def render_wj_e(self, token):     self.write(u'</span>')
    def render_text(self, token):    self.write(u" " + self.escape(token.value) + u" ")
    def render_q(self, token):       self.writeIndent(1)
    def render_q1(self, token):      self.writeIndent(1)
    def render_q2(self, token):      self.writeIndent(2)
    def render_q3(self, token):      self.writeIndent(3)
    def render_nb(self, token):      self.writeIndent(0)
    def render_b(self, token):       self.write(u'\n\n<p class="indent-0">&nbsp;</p>')
    def render_i_s(self, token):      self.write(u'<i>')
    def render_i_e(self, token):      self.write(u'</i>')
    def render_nd_s(self, token):     self.write(u'<span class="tetragrammaton">')
    def render_nd_e(self, token):     self.write(u'</span>')
    def render_pbr(self, token):     self.write(u'<br />')
    def render_sc_s(self, token):     self.write(u'<b>')
    def render_sc_e(self, token):     self.write(u'</b>')
    def render_f_s(self, token):     self.write(u'[Note: ')
    def render_f_e(self, token):     self.write(u' ]')
    def render_qs_s(self, token):     self.write(u'<i>')
    def render_qs_e(self, token):     self.write(u'</i>')
    def render_em_s(self, token):     self.write(u'<i>')
    def render_em_e(self, token):     self.write(u'</i>')
    def render_d(self, token):
        self.indentFlag = False
        self.write(u'\n\n<p>' + token.value + '</p>')
        
    def render_pb(self, token):     pass
    def render_periph(self, token):  pass
        
