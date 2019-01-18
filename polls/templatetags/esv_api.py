from django import template
import re

def esv_lookup(value):
  "Replaces a given passage with javascript lookup code"
  return "<script type=\"text/javascript\" src=\"http://www.gnpcb.org/esv/share/js/?action=doPassageQuery&include-passage-references=false&include-footnotes=false&include-headings=false&include-subheadings=false&include-audio-link=false&passage=%s\"></script>" % re.sub(r'\s','%20',value)
esv_lookup.is_safe = True

register = template.Library()
register.filter('esv_lookup', esv_lookup)
