import datetime
import uuid                                     # For unique book instances
import re

from django.db import models
from django.utils import timezone
from django.urls import reverse                 # To generate URLS by reversing URL patterns
from datetime import date
from django.contrib.auth.models import User     # To assign User as a borrower

from .views import NotFound
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class Passage(models.Model):
    """A Bible passage.
    Attributes:
        fulltext (unicode): Passage text as paragraphs
        ref (unicode): Canonical passage reference
        summary (unicode): Passage text on one line
        with_ref (unicode): Passage as paragraphs + reference
    """
    passage_text = models.CharField(max_length = 1000)

    def __init__(self, ref=u'', summary=u'', fulltext=u''):
        """Create new `Passage`."""
        self.ref = ref
        self.summary = summary
        self.fulltext = fulltext
        self.passage_text = models.CharField(max_length = 1000)
        self.with_ref = u'{}\n\n({} ESV)'.format(fulltext.rstrip(), ref)

    def __unicode__(self):
        """
        Passage as formatted Unicode string.
        Returns unicode: Full text of passage with reference.
        """
        return self.with_ref

    def __str__(self):
        #return self.passage_text
        return self.__unicode__().encode('utf-8')

    @classmethod
    def from_response(cls, data):
        """
        Create `Passage` from API response.
        Args:       data (dict): Decoded JSON API response.
        Returns:    Passage: Passage parsed from API response.
        Raises:     NotFound: Raised if ``data`` contains no passage(s).
        """
        if not data.get('canonical') or not data.get('passages'):
            raise NotFound()

        ref = data['canonical']
        s = data['passages'][0]
        summary = re.sub(r'\s+', ' ', s).strip()
        p = cls(ref, summary, s)
        return p

    @property
    def item(self):
        """ item `dict`.
        Returns dict: item for JSON serialisation.
        """
        return {
            'title': self.ref,
            'subtitle': self.summary,
            'autocomplete': self.ref,
            'arg': self.with_ref,
            'valid': True,
            'text': {
                'largetype': self.with_ref,
                'copytext': self.with_ref,
            },
        }
