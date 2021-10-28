from datetime import date
from datetime import datetime
from tests.common import DummyPostData
from unittest import TestCase
from wtforms_dateutil import DateField
from wtforms_dateutil import DateTimeField

from wtforms.form import Form


class DateutilTest(TestCase):
    class F(Form):
        a = DateTimeField()
        b = DateField(default=lambda: date(2004, 9, 12))
        c = DateField(parse_kwargs=dict(yearfirst=True, dayfirst=False))

    def test_form_input(self):
        f = self.F(DummyPostData(a="2008/09/12 4:17 PM", b="04/05/06", c="04/05/06"))
        self.assertEqual(f.a.data, datetime(2008, 9, 12, 16, 17))
        self.assertEqual(f.a._value(), "2008/09/12 4:17 PM")
        self.assertEqual(f.b.data, date(2006, 4, 5))
        self.assertEqual(f.c.data, date(2004, 5, 6))
        self.assertTrue(f.validate())
        f = self.F(DummyPostData(a="Grok Grarg Rawr"))
        self.assertFalse(f.validate())

    def test_blank_input(self):
        f = self.F(DummyPostData(a="", b=""))
        self.assertEqual(f.a.data, None)
        self.assertEqual(f.b.data, None)
        self.assertFalse(f.validate())

    def test_defaults_display(self):
        f = self.F(a=datetime(2001, 11, 15))
        self.assertEqual(f.a.data, datetime(2001, 11, 15))
        self.assertEqual(f.a._value(), "2001-11-15 00:00")
        self.assertEqual(f.b.data, date(2004, 9, 12))
        self.assertEqual(f.b._value(), "2004-09-12")
        self.assertEqual(f.c.data, None)
        self.assertTrue(f.validate())

    def test_render(self):
        f = self.F()
        self.assertEqual(
            f.b(), r'<input id="b" name="b" type="text" value="2004-09-12">'
        )
