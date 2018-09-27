import unittest
from vconvert import value_convert
from vconvert import int_convert
# private methods
from vconvert.vconvert import key_value
from vconvert.vconvert import set_key_value
from vconvert.vconvert import last_element


class TestDrugbankUtils(unittest.TestCase):

    def test_key_value(self):
        d = {
            'drugbank': {
                'pharmacology': {
                    'actions': '123',
                    'xref': {
                        'wikipedia': 'www.wiki.com'
                        }
                    }
                }
            }
        res = key_value(d, "drugbank.pharmacology.xref.wikipedia")
        self.assertEqual(res, "www.wiki.com")

        res = key_value(d, "drugbank.udef_field.xref")
        self.assertEqual(res, None)
        
    def test_set_key_value(self):
        d = {
            'drugbank': {
                'pharmacology': {
                    'actions': '123',
                    'xref': {
                        'wikipedia': 'www.wiki.com'
                        }
                    }
                }
            }

        res = set_key_value(d, "drugbank.pharmacology.xref.wikipedia", "www.myurl.com")
        self.assertEqual(res['drugbank']['pharmacology']['xref']['wikipedia'], "www.myurl.com")

    def test_last_element(self):
        d = {
            'drugbank': {
                'measurement': [
                    {'pH': '6'},
                    {'pH': '7.5'},
                    {'pH': '8'},
                    ]
                }
            }
        key_list = ["drugbank", "measurement", "pH"]
        for k in last_element(d, key_list):
            print(k)
        raise ValueError

    def test_value_convert(self):
        d = {
            'drugbank': {'id': '123'},
            'pharmgkb': {'id': '456'},
            'chebi': {'id': '789'}
            }
        res = int_convert(d,
                          include_keys=[
                                "drugbank.id",
                                "pharmgkb.id",
                                "chebi.id"
                                ])
        r = key_value(d, "drugbank.id")
        self.assertEquals(r, 123)
        r = key_value(d, "pharmgkb.id")
        self.assertEquals(r, 456)
        r = key_value(d, "chebi.id")
        self.assertEquals(r, 789)
