.. _mbrola-espeak:

Understanding Espeak and Mbrola
===============================

This page is a short primer on how Espeak and Mbrola work hand in hand to
synthesize speech from text.

Basic Principles
----------------

First of all, you should understand that this package's method for
synthesizing speech is divided in two main steps:

1. Translating text *in a particular language* into a list of phonemes (Espeak's job)
2. Using that list of phonemes and a voice database to synthesize audio (Mbrola's job)

Unsurprisingly, this is what a diagram describing that process looks like:


Espeak
------

Espeak is a pretty old program that used to be one of the only good  open source
option for basic text-to-speech synthesis (TTS). The synthesis quality is somewhat
rudimentary (at least compared to modern deep-learning based solutions, or even
Mbrola's speech synthesizer).

However, in order to be able to synthesize speech, espeak needs a phonetic representation
of the text that is being fed. This is the part of espeak that is used in Voxpopuli.
There are several notations for phonetics, the most commonly used in the
linguistic/phonetic world is the International Phonetic Alphabet (IPA).

.. code-block::

    'hello' ->  /həˈləʊ/

However, this notation, since it covers all of the world's languages, isn't very
handy when dealing with a single language, nor it is practical to manipulate
with a regular ASCII keyboard.

For this reason, a simplified and language-specific phonetic phonetic alphabet
was developed: SAMPA. This is that alphabet that is used in our case.
Indeed, there is specific set of SAMPA phonemes (all corresponding to an ASCII
string of 1 to 3 characters) for each language it supports.

.. code-block::

    'happy' -> "h{pi

Moreover, in order to synthesize a string of phonemes, we also need

- its duration in time (usually computed in milliseconds)
- its pitch variations, to also account for the prosody of the synthesized utterance

Espeak also computes these information from the text, using sets of rules that
are unique to each languages it supports.

In the end, this is what espeak outputs for the French sentence "c'est pas faux":

.. code-block::

    # This format is usually stored in .pho files
    s	107
    E	38	0 94 20 94 40 95 59 95 80 96 100 96
    p	70
    a	40	0 96 20 97 40 97 59 98 80 98 100 98
    f	112
    o	120	0 102 80 76 100 76
    _	350
    _	1

The first column is the phoneme name in the French SAMPA alphabet, the second
one is the duration of each phoneme in ms, and the third (and what follows) are the
pitch inflexions. These inflexions are usually only for vowels.

This data is then passed on to Mbrola.

.. note::

    The duration of each phonemes depends on the words-per-minute settings.
    The pitch of each phonemes depends several factors: if the voice is set to resemble
    a man or a woman, or a fixed value set as a parameter for espeak.

Mbrola
------

Mbrola is also a pretty old program (written in the mid 90's), that only focuses
on the audio synthesis part of TTS. From the start, it was made to rely on
Espeak's phonemization capabilities to be able to work using only phonemes as an
input.

Mbrola uses pre-processed voice databases to render voice. The databases is built using
"resynthesized" recordings of diphones (two phonemes pronounced together, such as
"ba" or "ish"). Each database contains recording from a single speaker. Thus,
ideally, when using a database from synthesize some speech, it's the voice of that
unique speaker that should be mimicked in the newly created audio.

Mbrola will then take a .pho file and a voice database as an input, and render
some audio. The *pitch* and *duration* of phonemes can be controlled through Mbrola's
parameters, as well as the *volume* of the rendered audio.

.. note::

    No new voice database have been created since the beginning of the 2000's.
    What you'll find in `Mbrola's voice repository <https://github.com/numediart/MBROLA-voices>`_
    is all there is.