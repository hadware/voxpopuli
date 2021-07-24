import asyncio
import logging
import unittest
from os import path
from typing import Any, Awaitable, Callable

from voxpopuli.main import Voice
from voxpopuli.phonemes import PhonemeList

logging.getLogger().setLevel(logging.DEBUG)
data_folder = path.join(path.dirname(path.realpath(__file__)), "data")


def run_async(coro: Callable[[Any], Awaitable[Any]]):
    """Sync -> Async deco
    Required for tests as unittest.IsolatedAsyncioTestCase is 3.8+"""

    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(coro(*args, **kwargs))

    return wrapper

class TestStrToPhonems(unittest.TestCase):
    @run_async
    async def test_french(self):
        voice = Voice(lang="fr")
        self.assertEqual((await voice.to_phonemes("bonjour")).phonemes_str, "bo~ZuR__")

    @run_async
    async def test_english(self):
        voice = Voice(lang="en")
        self.assertEqual((await voice.to_phonemes("hello")).phonemes_str, "h@l@U__")

    @run_async
    async def test_english_letter_n(self):
        voice = Voice(lang="en")
        self.assertEqual((await voice.to_phonemes("second")).phonemes_str, "sek@nd__")

    @run_async
    async def test_german(self):
        voice = Voice(lang="de", voice_id=4)
        self.assertEqual((await voice.to_phonemes("hallo")).phonemes_str, "halo:__")


class TestStrToAudio(unittest.TestCase):
    @run_async
    async def test_salut(self):
        voice = Voice(lang="fr", voice_id=1)
        wav_byte = await voice.to_audio("Salut les amis")
        with open(path.join(data_folder, "salut.wav"), "rb") as wavfile:
            self.assertEqual(wavfile.read(), wav_byte)

    @run_async
    async def test_hallo(self):
        voice = Voice(lang="de", voice_id=4)
        wav_byte = await voice.to_audio("Hallo Freunde")
        with open(path.join(data_folder, "hallo.wav"), "rb") as wavfile:
            self.assertEqual(wavfile.read(), wav_byte)


class TestPhonemsToAudio(unittest.TestCase):
    @run_async
    async def test_fr(self):
        with open(path.join(data_folder, "salut.pho")) as pho_file:
            pho_list = PhonemeList.from_pho_str(pho_file.read())
            self.assertEqual(pho_list.phonemes_str, "saly__")
            wav_byte = await Voice(lang="fr", voice_id=4).to_audio(pho_list)
        with open(path.join(data_folder, "salut_from_pho.wav"), "rb") as wavfile:
            self.assertEqual(wavfile.read(), wav_byte)

    @run_async
    async def test_en(self):
        with open(path.join(data_folder, "hello.pho")) as pho_file:
            pho_list = PhonemeList.from_pho_str(pho_file.read())
            self.assertEqual(pho_list.phonemes_str, "h@l@U__")
            wav_byte = await Voice(lang="en").to_audio(pho_list)
        with open(path.join(data_folder, "hello_from_pho.wav"), "rb") as wavfile:
            self.assertEqual(wavfile.read(), wav_byte)


class TestVoiceParams(unittest.TestCase):
    @run_async
    async def test_all_fr(self):
        voice = Voice(lang="fr", speed=110, pitch=60, voice_id=1)
        wav_byte = await voice.to_audio("PK LA VIE")
        with open(path.join(data_folder, "params_all.wav"), "rb") as wavfile:
            self.assertEqual(wavfile.read(), wav_byte)
