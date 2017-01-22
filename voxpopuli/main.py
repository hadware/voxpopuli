# coding=utf-8
"""A lightweight Python wrapper of SoX's effects."""
import logging
import shlex
from struct import pack
from subprocess import PIPE, run
from typing import Union
from warnings import warn
import pyaudio


from .phonems import PhonemList


class AudioFile:
    """A sound player"""
    chunk = 1024

    def __init__(self, file):
        """ Init audio stream """
        self.wf = wave.open(file, 'rb')
        self.p = pyaudio.PyAudio()
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

    def __init__(self):
        self.speed, self.pitch, self.lang, self.sex, self.volume, self.voice = None, None, None, None, None, None

    @property
    def player(self):
        pass

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
        pass
