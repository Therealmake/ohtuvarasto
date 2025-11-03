import unittest
from varasto import Varasto


class TestVarasto(unittest.TestCase):
    def setUp(self):
        self.varasto = Varasto(10)

    def test_konstruktori_luo_tyhjan_varaston(self):
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertAlmostEqual
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_negatiivinen_tilavuus_nollaus(self):
        v = Varasto(-1)
        self.assertEqual(v.tilavuus, 0.0)

    def test_uudella_varastolla_oikea_tilavuus(self):
        self.assertAlmostEqual(self.varasto.tilavuus, 10)

    def test_negatiivinen_alkusaldo_nollaus(self):
        v = Varasto(10, -1)
        self.assertEqual(v.saldo, 0.0)

    def test_lisays_lisaa_saldoa(self):
        self.varasto.lisaa_varastoon(8)

        self.assertAlmostEqual(self.varasto.saldo, 8)

    def test_negatiivinen_lisays(self):
        v = Varasto(10)
        v.lisaa_varastoon(-3)
        self.assertEqual(v.saldo, 0.0)

    def test_lisays_lisaa_pienentaa_vapaata_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        # vapaata tilaa pitäisi vielä olla tilavuus-lisättävä määrä eli 2
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 2)

    def test_lisattiin_liikaa(self):
        v = Varasto(10, 9)
        v.lisaa_varastoon(5)
        self.assertEqual(v.saldo, 10.0)
        self.assertEqual(v.paljonko_mahtuu(), 0.0)

    def test_ottaminen_palauttaa_oikean_maaran(self):
        self.varasto.lisaa_varastoon(8)

        saatu_maara = self.varasto.ota_varastosta(2)

        self.assertAlmostEqual(saatu_maara, 2)

    def test_negatiivinen_otto_palauttaa_nolla(self):
        v = Varasto(10, 5)
        saatu = v.ota_varastosta(-2)
        self.assertEqual(saatu, 0.0)
        self.assertEqual(v.saldo, 5.0)

    def test_liian_suuri_otto(self):
        v = Varasto(10, 4)
        saatu = v.ota_varastosta(10)
        self.assertEqual(saatu, 4.0)
        self.assertEqual(v.saldo, 0.0)

    def test_ottaminen_lisaa_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        self.varasto.ota_varastosta(2)

        # varastossa pitäisi olla tilaa 10 - 8 + 2 eli 4
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 4)

    def test_string(self):
        v = Varasto(10, 3)
        self.assertEqual(str(v), "saldo = 3, vielä tilaa 7")

    def test_negatiivinen_konstruktori(self):
        v = Varasto(-5)
        self.assertEqual(v.tilavuus, 0.0)

    def test_liian_suuri_konstruktori(self):
        v = Varasto(10, 15)
        self.assertEqual(v.saldo, 10.0)


moi