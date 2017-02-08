# coding=utf-8
"""A lightweight Python wrapper of espeak and mbrola"""
import fnmatch
import io
import logging
import os
import wave
from os.path import isfile, join
from shlex import quote
from struct import pack
from subprocess import PIPE, run
from sys import platform
from typing import Union
import re
from typing import List, Dict

import pyaudio

from .phonems import PhonemList


class AudioPlayer:
    """A sound player"""
    chunk = 1024

    def __init__(self):
        """ Init audio stream """
        self.wf, self.stream = None, None
        self.p = pyaudio.PyAudio()

    def set_file(self, file):
        if self.stream is not None:
            self.stream.close()

        self.wf = wave.open(file, 'rb')
        self.stream = self.p.open(
            format=self.p.get_format_from_width(self.wf.getsampwidth()),
            channels=self.wf.getnchannels(),
            rate=self.wf.getframerate(),
            output=True
        )

    def play(self):
        """ Play entire file """
        data = self.wf.readframes(self.chunk)
        while data != '':
            self.stream.write(data)
            data = self.wf.readframes(self.chunk)

    def close(self):
        """ Graceful shutdown """
        self.stream.close()
        self.p.terminate()


class Voice:

    class InvalidVoiceParameters(Exception):
        pass

    if platform == 'linux':
        espeak_binary = 'espeak'
        mbrola_binary = 'mbrola'
        mbrola_voices_folder = "/usr/share/mbrola"
    elif platform == 'win32':
        # If the path has spaces it needs to be enclosed in double quotes.
        espeak_binary = '"C:\\Program Files (x86)\\eSpeak\\command_line\\espeak"'
        mbrola_binary = '"C:\\Program Files (x86)\\Mbrola Tools\\mbrola"'
        # TODO: a default value on Windows for mbrola_voices_folder
        # TODO: raise error if no binary is installed
    else:
        raise ValueError('Unsupported system.')

    volumes_presets = {'fr1': 1.17138, 'fr2': 1.60851, 'fr3': 1.01283, 'fr4': 1.0964, 'fr5': 2.64384, 'fr6': 1.35412,
                       'fr7': 1.96092, 'us1': 1.658, 'us2': 1.7486, 'us3': 3.48104, 'es1': 3.26885, 'es2': 1.84053}

    def __init__(self, speed: int = 160, pitch: int = 50, lang: str ="fr",
                 voice_id: int = None, volume: float = None):
        """All parameters are optional, but it's still advised that you pick a language,
        else it **will** default to French, which is a default to the most beautiful language on earth.
        Any invalid parameter will raise an `InvalidVoiceParameter` exception."""

        self.speed = speed

        if 99 >= pitch >= 0:
            self.pitch = pitch
        else:
            raise self.InvalidVoiceParameters("Pitch adjustment has to be an integer between 0 and 99")

        # if no voice ID is specified, just defaults to one it can find
        voice_id = voice_id if voice_id is not None else self._find_existing_voiceid(lang)
        voice_name = lang+str(voice_id)
        if isfile(join(self.mbrola_voices_folder, voice_name, voice_name)):
            self.lang = lang
            self.voice_id = voice_id
        else:
            raise self.InvalidVoiceParameters("Voice %s not found. Check language and voice id, or install"
                                              "by running 'sudo apt install mbrola-%s'" % (voice_name, voice_name))

        if volume is not None:
            self.volume = volume
        else:
            if voice_name in self.volumes_presets:
                self.volume = self.volumes_presets[voice_name]
            self.volume = 1

        if lang != 'fr':
            self.sex = self.voice_id
        else:
            self.sex = 4 if self.voice_id in (2, 4) else 1

        self._player = None

    def _find_existing_voiceid(self, lang: str):
        """Finds any possible voice id for a given language"""
        for file in os.listdir(self.mbrola_voices_folder):
            if fnmatch.fnmatch(file, lang + "[0-9]"):
                return int(file.strip(lang))
        return 1  # default to 1 if no voice are found (although it'll probably fail then)

    @property
    def player(self):
        if self._player is None:
            self._player = AudioPlayer()
        return self._player

    def _wav_format(self, wav: bytes):
        return wav[:4] + pack('<I', len(wav) - 8) + wav[8:40] + pack('<I', len(wav) - 44) + wav[44:]

    def _str_to_phonems(self, text: str) -> PhonemList:
        
        voice_filename = ('mb/mb-%s%d' if platform == 'linux' else 'mb-%s%d') % (self.lang, self.sex)

        # Detailed explanation of options:
        # http://espeak.sourceforge.net/commands.html
        phonem_synth_args = [
            self.espeak_binary,
            '-s', str(self.speed),
            '-p', str(self.pitch),
            '--pho',    # outputs mbrola phoneme data
            '-q',       # quiet mode
            '-v', voice_filename,
            text]

        # Linux-specific memory management setting
        # Tells Clib to ignore allocations problems (which happen but don't compromise espeak's outputs)
        if platform == 'linux':
            phonem_synth_args.insert(0, 'MALLOC_CHECK_=0')

        logging.debug("Running espeak command %s" % " ".join(phonem_synth_args))

        # Since MALLOC_CHECK_ has to be used before anything else, we need to compile the full command as a single
        # string and we need to use `shell=True`.
        return PhonemList(run(' '.join(phonem_synth_args), shell=True, stdout=PIPE, stderr=PIPE)
                          .stdout
                          .decode("utf-8")
                          .strip())

    def _phonems_to_audio(self, phonems: PhonemList) -> bytes:

        database = '%s%s%d/%s%d' % (self.mbrola_voices_folder, self.lang, self.voice_id, self.lang, self.voice_id)

        audio_synth_string = [
            self.mbrola_binary,
            '-v', str(self.volume),
            '-e',       # ignores fatal errors on unknown diphone
            database,
            '-',        # command or .pho file; `-` instead of a file means stdin
            '-.wav'     # output file; `-` instead of a file means stdout
        ]

        if platform == 'linux':
            audio_synth_string.insert(0, 'MALLOC_CHECK_=0')

        logging.debug("Running mbrola command %s" % " ".join(audio_synth_string))
        return self._wav_format(run(" ".join(audio_synth_string), shell=True, stdout=PIPE,
                                    stderr=PIPE, input=str(phonems).encode("utf-8")).stdout)

    def _str_to_audio(self, text: str) -> bytes:

        phonems = self._str_to_phonems(text)
        audio = self._phonems_to_audio(phonems)

        return audio

    def to_phonems(self, text: str) -> PhonemList:
        return self._str_to_phonems(quote(text))

    def to_audio(self, speech: Union[PhonemList, str], filename=None) -> bytes:
        """Renders a str or a `PhonemList` to a wave byte object. If a filename is specified, it saves the
        audio file to wave as well"""
        if isinstance(speech, str):
            wav = self._str_to_audio(quote(speech))
        elif isinstance(speech, PhonemList):
            wav = self._phonems_to_audio(speech)

        if filename is not None:
            with open(filename, "wb") as wavfile:
                wavfile.write(wav)

        return wav

    def say(self, speech: Union[PhonemList, str]):
        """Renders a string or a `PhonemList` object to audio, then plays it using the PyAudio lib"""
        wav = self.to_audio(speech)
        self.player.set_file(io.BytesIO(wav))
        self.player.play()

    def listvoices(self):
        """Returns a dictionary listing available voice id's for each language"""
        langs = {}  # type:Dict[List]
        for file in os.listdir(self.mbrola_voices_folder):
            match = re.match(r"([a-z]{2})([0-9])", file)
            if match is not None:
                lang, voice_id = match.groups()
                if lang not in langs:
                    langs[lang] = []
                langs[lang].append(voice_id)
        return langs

