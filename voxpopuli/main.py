# coding=utf-8
"""A lightweight Python wrapper of SoX's effects."""
import io
import logging
import wave
from struct import pack
from subprocess import PIPE, run
from typing import Union
import pathlib
import os
import fnmatch

import pyaudio
from os.path import isfile, join

from .phonems import PhonemList


class AudioFile:
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
            format = self.p.get_format_from_width(self.wf.getsampwidth()),
            channels = self.wf.getnchannels(),
            rate = self.wf.getframerate(),
            output = True
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

    mbrola_voices_folder = "/usr/share/mbrola"

    volumes_presets = {'fr1': 1.17138, 'fr2': 1.60851, 'fr3': 1.01283, 'fr4': 1.0964, 'fr5': 2.64384, 'fr6': 1.35412,
                       'fr7': 1.96092, 'us1': 1.658, 'us2': 1.7486, 'us3': 3.48104, 'es1': 3.26885, 'es2': 1.84053}

    def __init__(self, speed : int = 160, pitch: int = 50, lang : str ="fr",
                 voice_id : int = None, volume: float = None):

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

        self._player = None

    def _find_existing_voiceid(self, lang : str):
        """Finds any possible voice id for a given language"""
        for file in os.listdir(self.mbrola_voices_folder):
            if fnmatch.fnmatch(file, lang + "[0-9]"):
                return int(file.strip(lang))
        return 1 # default to 1 if none is found

    @property
    def player(self):
        if self._player is None:
            self._player = AudioFile()
        return self._player

    def _wav_format(self, wav: bytes):
        return wav[:4] + pack('<I', len(wav) - 8) + wav[8:40] + pack('<I', len(wav) - 44) + wav[44:]

    def _str_to_audio(self, text : str) -> bytes:
        synth_string = 'MALLOC_CHECK_=0 espeak -s %d -p %d --pho -q -v mb/mb-%s%d %s ' \
                       '| MALLOC_CHECK_=0 mbrola -v %g -e /usr/share/mbrola/%s%d/%s%d - -.wav' \
                       % (self.speed, self.pitch, self.lang, self.sex, text,  # for espeak
                          self.volume, self.lang, self.voice, self.lang, self.voice) # for mbrola
        logging.debug("Running synth command %s" % synth_string)
        return self._wav_format(run(synth_string, shell=True, stdout=PIPE, stderr=PIPE).stdout)

    def _str_to_phonems(self, text : str) -> PhonemList:
        phonem_synth_string = 'MALLOC_CHECK_=0 espeak -s %d -p %d --pho -q -v mb/mb-%s%d %s ' \
                              % (self.speed, self.pitch, self.lang, self.sex, text)

        logging.debug("Running espeak command %s" % phonem_synth_string)
        return PhonemList(run(phonem_synth_string, shell=True, stdout=PIPE, stderr=PIPE)
                          .stdout
                          .decode("utf-8")
                          .strip())

    def _phonems_to_audio(self, phonems : PhonemList) -> bytes:
        audio_synth_string = 'MALLOC_CHECK_=0 mbrola -v %g -e /usr/share/mbrola/%s%d/%s%d - -.wav' \
                             % (self.volume, self.lang, self.voice, self.lang, self.voice)

        logging.debug("Running mbrola command %s" % audio_synth_string)
        return self._wav_format(run(audio_synth_string, shell=True, stdout=PIPE,
                                    stderr=PIPE, input=str(phonems).encode("utf-8")).stdout)

    def to_phonems(self, text : str) -> PhonemList:
        return self._str_to_phonems(text)

    def to_audio(self, speech : Union[PhonemList, str], filename = None) -> bytes:
        if isinstance(speech, str):
            wav = self._str_to_audio(speech)
        elif isinstance(speech, PhonemList):
            wav = self._phonems_to_audio(speech)

        if filename is not None:
            pass

        return wav

    def say(self, speech : Union[PhonemList, str]):
        wav = self.to_audio(speech)
        self.player.set_file(io.BytesIO(wav))
        self.player.play()

