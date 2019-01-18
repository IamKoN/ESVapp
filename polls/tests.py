import datetime
import unittest

from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from django.template import Template, Context, TemplateSyntaxError
from django.conf import settings
from django_inlines.inlines import Registry

from .models import Question

class GetPassageTestCase(TestCase):
    
    def test_get_passage(self):
        value = esv.get_passage('gen 1:1')
        OUT = '<div class="esv"><h2>Genesis 1:1 <object type="application/x-shockwave-flash"  data="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001001" width="40" height="12" class="audio"><param name="movie" value="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001001" /><param name="wmode" value="transparent" /></object></h2>\n<div class="esv-text">\n<p class="chapter-first" id="p01001001.06-1"><span class="chapter-num" id="v01001001-1">1:1&nbsp;</span>In the beginning, God created the heavens and the earth.  (<a href="http://www.esv.org" class="copyright">ESV</a>)</p>\n</div>\n</div>'
        self.assertEqual(value, OUT)
        cached = esv.get_passage('gen 1:1')
        self.assertEqual(cached, OUT)

    def test_get_passage_headings(self):
        value = esv.get_passage('gen 1:1', headings=True)
        OUT = '<div class="esv"><h2>Genesis 1:1 <object type="application/x-shockwave-flash"  data="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001001" width="40" height="12" class="audio"><param name="movie" value="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001001" /><param name="wmode" value="transparent" /></object></h2>\n<div class="esv-text"><h3 id="p01001001.01-1">The Creation of the World</h3>\n<p class="chapter-first" id="p01001001.06-1"><span class="chapter-num" id="v01001001-1">1:1&nbsp;</span>In the beginning, God created the heavens and the earth.  (<a href="http://www.esv.org" class="copyright">ESV</a>)</p>\n</div>\n</div>'
        self.assertEqual(value, OUT)

    def test_get_passage_audio(self):
        value = esv.get_passage('gen 1:1', audio=False)
        OUT = '<div class="esv"><h2>Genesis 1:1</h2>\n<div class="esv-text">\n<p class="chapter-first" id="p01001001.06-1"><span class="chapter-num" id="v01001001-1">1:1&nbsp;</span>In the beginning, God created the heavens and the earth.  (<a href="http://www.esv.org" class="copyright">ESV</a>)</p>\n</div>\n</div>'
        self.assertEqual(value, OUT)

    def test_get_passage_footnotes(self):
        value = esv.get_passage('gen 1:7', footnotes=True)
        OUT = '<div class="esv"><h2>Genesis 1:7 <object type="application/x-shockwave-flash"  data="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001007" width="40" height="12" class="audio"><param name="movie" value="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001007" /><param name="wmode" value="transparent" /></object></h2>\n<div class="esv-text"><p id="p01001007.01-1"><span class="verse-num" id="v01001007-1">7&nbsp;</span>And God made<span class="footnote">&nbsp;<a href="#f1" id="b1" title="Or \'fashioned\'; also verse 16">[1]</a></span> the expanse and separated the waters that were under the expanse from the waters that were above the expanse. And it was so.  (<a href="http://www.esv.org" class="copyright">ESV</a>)</p>\n</div>\n<div class="footnotes">\n<h3>Footnotes</h3>\n<p><span class="footnote"><a href="#b1" id="f1">[1]</a></span> <span class="footnote-ref">1:7</span> Or <em>fashioned</em>; also verse 16\n</p>\n</div>\n</div>'
        self.assertEqual(value, OUT)
        value = esv.get_passage('gen 1:7', footnotes=False)
        OUT = '<div class="esv"><h2>Genesis 1:7 <object type="application/x-shockwave-flash"  data="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001007" width="40" height="12" class="audio"><param name="movie" value="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001007" /><param name="wmode" value="transparent" /></object></h2>\n<div class="esv-text"><p id="p01001007.01-1"><span class="verse-num" id="v01001007-1">7&nbsp;</span>And God made the expanse and separated the waters that were under the expanse from the waters that were above the expanse. And it was so.  (<a href="http://www.esv.org" class="copyright">ESV</a>)</p>\n</div>\n</div>'
        self.assertEqual(value, OUT)

class PassageInlineTestCase(TestCase):

    def setUp(self):
        settings.INLINE_DEBUG = True
        registry = Registry()
        registry.register('passage', PassageInline)
        self.inlines = registry
        
    def test_inline_passage(self):
        value = '{{ passage gen 1:1 }}'
        OUT = '<div class="esv"><h2>Genesis 1:1 <object type="application/x-shockwave-flash"  data="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001001" width="40" height="12" class="audio"><param name="movie" value="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001001" /><param name="wmode" value="transparent" /></object></h2>\n<div class="esv-text">\n<p class="chapter-first" id="p01001001.06-1"><span class="chapter-num" id="v01001001-1">1:1&nbsp;</span>In the beginning, God created the heavens and the earth.  (<a href="http://www.esv.org" class="copyright">ESV</a>)</p>\n</div>\n</div>'
        self.assertEqual(self.inlines.process(value), OUT)

    def test_inline_passage_headings(self):
        value = '{{ passage gen 1:1 headings=on }}'
        OUT = '<div class="esv"><h2>Genesis 1:1 <object type="application/x-shockwave-flash"  data="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001001" width="40" height="12" class="audio"><param name="movie" value="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001001" /><param name="wmode" value="transparent" /></object></h2>\n<div class="esv-text"><h3 id="p01001001.01-1">The Creation of the World</h3>\n<p class="chapter-first" id="p01001001.06-1"><span class="chapter-num" id="v01001001-1">1:1&nbsp;</span>In the beginning, God created the heavens and the earth.  (<a href="http://www.esv.org" class="copyright">ESV</a>)</p>\n</div>\n</div>'
        self.assertEqual(self.inlines.process(value), OUT)

    def test_inline_passage_audio(self):
        value = '{{ passage gen 1:1 audio=off }}'
        OUT = '<div class="esv"><h2>Genesis 1:1</h2>\n<div class="esv-text">\n<p class="chapter-first" id="p01001001.06-1"><span class="chapter-num" id="v01001001-1">1:1&nbsp;</span>In the beginning, God created the heavens and the earth.  (<a href="http://www.esv.org" class="copyright">ESV</a>)</p>\n</div>\n</div>'
        self.assertEqual(self.inlines.process(value), OUT)

    def test_inline_passage_footnotes(self):
        value = '{{ passage gen 1:7 footnotes=on }}'
        OUT = '<div class="esv"><h2>Genesis 1:7 <object type="application/x-shockwave-flash"  data="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001007" width="40" height="12" class="audio"><param name="movie" value="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001007" /><param name="wmode" value="transparent" /></object></h2>\n<div class="esv-text"><p id="p01001007.01-1"><span class="verse-num" id="v01001007-1">7&nbsp;</span>And God made<span class="footnote">&nbsp;<a href="#f1" id="b1" title="Or \'fashioned\'; also verse 16">[1]</a></span> the expanse and separated the waters that were under the expanse from the waters that were above the expanse. And it was so.  (<a href="http://www.esv.org" class="copyright">ESV</a>)</p>\n</div>\n<div class="footnotes">\n<h3>Footnotes</h3>\n<p><span class="footnote"><a href="#b1" id="f1">[1]</a></span> <span class="footnote-ref">1:7</span> Or <em>fashioned</em>; also verse 16\n</p>\n</div>\n</div>'
        self.assertEqual(self.inlines.process(value), OUT)
        value = '{{ passage gen 1:7 footnotes=off }}'
        OUT = '<div class="esv"><h2>Genesis 1:7 <object type="application/x-shockwave-flash"  data="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001007" width="40" height="12" class="audio"><param name="movie" value="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001007" /><param name="wmode" value="transparent" /></object></h2>\n<div class="esv-text"><p id="p01001007.01-1"><span class="verse-num" id="v01001007-1">7&nbsp;</span>And God made the expanse and separated the waters that were under the expanse from the waters that were above the expanse. And it was so.  (<a href="http://www.esv.org" class="copyright">ESV</a>)</p>\n</div>\n</div>'
        self.assertEqual(self.inlines.process(value), OUT)

class PassageTemplateTagTestCase(TestCase):
    
    def assert_render(self, expected, template_string, context_dict=None):
        """A shortcut for testing template output."""
        if context_dict is None:
            context_dict = {}
        
        c = Context(context_dict)
        t = Template(template_string)
        return self.assertEqual(expected, t.render(c))
        
    def test_tt_passage(self):
        template = '{% load passage %}{% passage "gen 1:1" %}'
        OUT = '<div class="esv"><h2>Genesis 1:1 <object type="application/x-shockwave-flash"  data="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001001" width="40" height="12" class="audio"><param name="movie" value="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001001" /><param name="wmode" value="transparent" /></object></h2>\n<div class="esv-text">\n<p class="chapter-first" id="p01001001.06-1"><span class="chapter-num" id="v01001001-1">1:1&nbsp;</span>In the beginning, God created the heavens and the earth.  (<a href="http://www.esv.org" class="copyright">ESV</a>)</p>\n</div>\n</div>'
        self.assert_render(OUT, template)

    def test_tt_passage_resolution(self):
        template = '{% load passage %}{% passage ref %}'
        OUT = '<div class="esv"><h2>Genesis 1:1 <object type="application/x-shockwave-flash"  data="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001001" width="40" height="12" class="audio"><param name="movie" value="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001001" /><param name="wmode" value="transparent" /></object></h2>\n<div class="esv-text">\n<p class="chapter-first" id="p01001001.06-1"><span class="chapter-num" id="v01001001-1">1:1&nbsp;</span>In the beginning, God created the heavens and the earth.  (<a href="http://www.esv.org" class="copyright">ESV</a>)</p>\n</div>\n</div>'
        self.assert_render(OUT, template, dict(ref="gen 1:1"))

    def test_tt_passage_headings(self):
        template = '{% load passage %}{% passage "gen 1:1" headings on %}'
        OUT = '<div class="esv"><h2>Genesis 1:1 <object type="application/x-shockwave-flash"  data="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001001" width="40" height="12" class="audio"><param name="movie" value="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001001" /><param name="wmode" value="transparent" /></object></h2>\n<div class="esv-text"><h3 id="p01001001.01-1">The Creation of the World</h3>\n<p class="chapter-first" id="p01001001.06-1"><span class="chapter-num" id="v01001001-1">1:1&nbsp;</span>In the beginning, God created the heavens and the earth.  (<a href="http://www.esv.org" class="copyright">ESV</a>)</p>\n</div>\n</div>'
        self.assert_render(OUT, template)

    def test_tt_passage_audio(self):
        template = '{% load passage %}{% passage "gen 1:1" audio off %}'
        OUT = '<div class="esv"><h2>Genesis 1:1</h2>\n<div class="esv-text">\n<p class="chapter-first" id="p01001001.06-1"><span class="chapter-num" id="v01001001-1">1:1&nbsp;</span>In the beginning, God created the heavens and the earth.  (<a href="http://www.esv.org" class="copyright">ESV</a>)</p>\n</div>\n</div>'
        self.assert_render(OUT, template)

    def test_tt_passage_footnotes(self):
        template = '{% load passage %}{% passage "gen 1:7" footnotes on %}'
        OUT = '<div class="esv"><h2>Genesis 1:7 <object type="application/x-shockwave-flash"  data="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001007" width="40" height="12" class="audio"><param name="movie" value="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001007" /><param name="wmode" value="transparent" /></object></h2>\n<div class="esv-text"><p id="p01001007.01-1"><span class="verse-num" id="v01001007-1">7&nbsp;</span>And God made<span class="footnote">&nbsp;<a href="#f1" id="b1" title="Or \'fashioned\'; also verse 16">[1]</a></span> the expanse and separated the waters that were under the expanse from the waters that were above the expanse. And it was so.  (<a href="http://www.esv.org" class="copyright">ESV</a>)</p>\n</div>\n<div class="footnotes">\n<h3>Footnotes</h3>\n<p><span class="footnote"><a href="#b1" id="f1">[1]</a></span> <span class="footnote-ref">1:7</span> Or <em>fashioned</em>; also verse 16\n</p>\n</div>\n</div>'
        self.assert_render(OUT, template)
        template = '{% load passage %}{% passage "gen 1:7" footnotes off %}'
        OUT = '<div class="esv"><h2>Genesis 1:7 <object type="application/x-shockwave-flash"  data="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001007" width="40" height="12" class="audio"><param name="movie" value="http://www.esvapi.org/assets/play.swf?myUrl=hw%2F01001007" /><param name="wmode" value="transparent" /></object></h2>\n<div class="esv-text"><p id="p01001007.01-1"><span class="verse-num" id="v01001007-1">7&nbsp;</span>And God made the expanse and separated the waters that were under the expanse from the waters that were above the expanse. And it was so.  (<a href="http://www.esv.org" class="copyright">ESV</a>)</p>\n</div>\n</div>'
        self.assert_render(OUT, template)

    def test_too_many_args(self):
        template = '{% load passage %}{% passage "gen 1:1" audio off maybe %}'
        self.assertRaises(TemplateSyntaxError, Template, template)

    def test_wrong_args(self):
        template = '{% load passage %}{% passage "gen 1:1" off on %}'
        self.assertRaises(TemplateSyntaxError, Template, template)

    def test_wrong_values(self):
        template = '{% load passage %}{% passage "gen 1:1" audio maybe %}'
        self.assertRaises(TemplateSyntaxError, Template, template)

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_old_question(self):
        # was_published_recently() returns False for questions whose pub_date is older than 1 day.
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        # was_published_recently() returns True for questions whose pub_date is within the last day
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_was_published_recently_with_future_question(self):
        # was_published_recently() returns False for questions whose pub_dateis in the future
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def create_question(self, question_text, days):
        """
        Create a question with the given `question_text` and published the
        given number of `days` offset to now (negative for questions published
        in the past, positive for questions that have yet to be published).
        """
        time = timezone.now() + datetime.timedelta(days=days)
        return Question.objects.create(question_text=question_text, pub_date=time)

    class QuestionIndexViewTests(TestCase):
        def test_no_questions(self):
            """
            If no questions exist, an appropriate message is displayed.
            """
            response = self.client.get(reverse('polls:index'))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "No polls are available.")
            self.assertQuerysetEqual(response.context['latest_question_list'], [])

        def test_past_question(self):
            """
            Questions with a pub_date in the past are displayed on the
            index page.
            """
            create_question(question_text="Past question.", days=-30)
            response = self.client.get(reverse('polls:index'))
            self.assertQuerysetEqual(
                response.context['latest_question_list'],
                ['<Question: Past question.>']
            )

        def test_future_question(self):
            """
            Questions with a pub_date in the future aren't displayed on
            the index page.
            """
            create_question(question_text="Future question.", days=30)
            response = self.client.get(reverse('polls:index'))
            self.assertContains(response, "No polls are available.")
            self.assertQuerysetEqual(response.context['latest_question_list'], [])

        def test_future_question_and_past_question(self):
            """
            Even if both past and future questions exist, only past questions
            are displayed.
            """
            create_question(question_text="Past question.", days=-30)
            create_question(question_text="Future question.", days=30)
            response = self.client.get(reverse('polls:index'))
            self.assertQuerysetEqual(
                response.context['latest_question_list'],
                ['<Question: Past question.>']
            )

        def test_two_past_questions(self):
            """
            The questions index page may display multiple questions.
            """
            create_question(question_text="Past question 1.", days=-30)
            create_question(question_text="Past question 2.", days=-5)
            response = self.client.get(reverse('polls:index'))
            self.assertQuerysetEqual(
                response.context['latest_question_list'],
                ['<Question: Past question 2.>', '<Question: Past question 1.>']
            )

    class QuestionDetailViewTests(TestCase):
        def test_future_question(self):
            """
            The detail view of a question with a pub_date in the future
            returns a 404 not found.
            """
            future_question = create_question(question_text='Future question.', days=5)
            url = reverse('polls:detail', args=(future_question.id,))
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)

        def test_past_question(self):
            """
            The detail view of a question with a pub_date in the past
            displays the question's text.
            """
            past_question = create_question(question_text='Past Question.', days=-5)
            url = reverse('polls:detail', args=(past_question.id,))
            response = self.client.get(url)
            self.assertContains(response, past_question.question_text)
