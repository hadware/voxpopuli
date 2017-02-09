import unittest
from os import path
import logging
from voxpopuli.main import Voice
from voxpopuli.phonemes import PhonemeList

logging.getLogger().setLevel(logging.DEBUG)


class TestStrToPhonems(unittest.TestCase):

    def test_french(self):
        voice = Voice(lang="fr")
        self.assertEqual(voice.to_phonemes("bonjour").phonemes_str, "bo~ZuR__")

    def test_english(self):
        voice = Voice(lang="en")
        self.assertEqual(voice.to_phonemes("hello").phonemes_str, "h@l@U__")

    def test_german(self):
        voice = Voice(lang="de")
        self.assertEqual(voice.to_phonemes("hallo").phonemes_str, "halo:__")


class TestStrToAudio(unittest.TestCase):
    data_folder = path.join(path.dirname(path.realpath(__file__)), "data")

    def test_salut(self):
        voice = Voice(lang="fr")
        wav_byte = voice.to_audio("Salut les amis")
        with open(path.join(self.data_folder, "salut.wav"), "rb") as wavfile:
            self.assertEqual(wavfile.read(), wav_byte)

    def test_hallo(self):
        voice = Voice(lang="de")
        wav_byte = voice.to_audio("Hallo Freunde")
        with open(path.join(self.data_folder, "hallo.wav"), "rb") as wavfile:
            self.assertEqual(wavfile.read(), wav_byte)


class TestPhonemsToAudio(unittest.TestCase):
    data_folder = path.join(path.dirname(path.realpath(__file__)), "data")

    def test_fr(self):
        with open(path.join(self.data_folder, "salut.pho")) as pho_file:
            pho_list = PhonemeList(pho_file.read())
            self.assertEqual(pho_list.phonemes_str, "saly__")
            wav_byte = Voice(lang="fr").to_audio(pho_list)
        with open(path.join(self.data_folder, "salut_from_pho.wav"), "rb") as wavfile:
            self.assertEqual(wavfile.read(), wav_byte)


class TestVoiceParams(unittest.TestCase):
    data_folder = path.join(path.dirname(path.realpath(__file__)), "data")

    def test_all_fr(self):
        voice = Voice(lang="fr", speed=110, pitch=60, voice_id=1)
        wav_byte = voice.to_audio("PK LA VIE")
        with open(path.join(self.data_folder, "params_all.wav"), "rb") as wavfile:
            self.assertEqual(wavfile.read(), wav_byte)