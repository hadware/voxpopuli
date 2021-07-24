import argparse
import asyncio
from pathlib import Path
from typing import List

import aiohttp
import aiofile

BASE_URL = "https://github.com/numediart/MBROLA-voices/raw/master/data/{vn}/{vn}"
MBROLA_FOLDER = Path("/usr/share/mbrola/")

LANG_FILES = {'cn': [1],
              'ir': [1],
              'hu': [1],
              'ar': [2, 1],
              'ca': [1, 2],
              'cz': [2, 1],
              'pt': [1],
              'it': [3, 1, 2, 4],
              'nl': [3, 1, 2],
              'fr': [7, 2, 1, 3, 4, 6, 5],
              'cr': [1],
              'mx': [1, 2],
              'ee': [1],
              'en': [1],
              'lt': [2, 1],
              'es': [2, 1, 4, 3],
              'de': [1, 3, 5, 8, 4, 7, 2, 6],
              'us': [1, 3, 2],
              'jp': [2, 3, 1],
              'bz': [1],
              'br': [1, 2, 3, 4],
              'tr': [2, 1],
              'ma': [1],
              'ro': [1],
              'hn': [1],
              'hb': [1, 2],
              'tl': [1],
              'vz': [1],
              'af': [1],
              'id': [1],
              'sw': [2, 1],
              'in': [1, 2],
              'la': [1],
              'gr': [1, 2],
              'nz': [1],
              'ic': [1],
              'pl': [1],
              "all": []}

async def main():
    args = argparser.parse_args()
    languages: List[str] = args.languages
    if "all" in languages:
        languages = list(LANG_FILES.keys())

    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(*(
            install_voice(session, lang, voice_id)
            for lang in languages
            for voice_id in LANG_FILES[lang]
        ))

async def install_voice(
    session: aiohttp.ClientSession,
    lang: str, voice_id: int,
):
    """Automatically downloads and extracts all the voices for one language in the /usr/share/mbrola folder"""
    print(f"Installing voice {lang} {voice_id}")
    voice_name = lang + str(voice_id)

    print(f"Downloading MBROLA language file for voice {voice_name}")
    async with session.get(BASE_URL.format(vn=voice_name)) as resp:
        voice_data = await resp.read()

    # creating folder for the language file
    print(f"Writing data for language {voice_name}")
    voice_folder = MBROLA_FOLDER / Path(voice_name)
    voice_folder.mkdir(parents=True, exist_ok=True)

    lang_path = voice_folder / Path(voice_name)
    async with aiofile.AIOFile(lang_path, "wb") as lang_file:
        await lang_file.write(voice_data)


argparser = argparse.ArgumentParser()
argparser.add_argument(
    "languages", nargs="+", choices=list(LANG_FILES.keys()),
    type=str, help="Languages to install"
)

if __name__ == "__main__":
    asyncio.run(main())
