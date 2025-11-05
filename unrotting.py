import os
import codecs
import requests
from bs4 import _s

def height(leafname: str):
  with open(leafname, "rb") as lines:
    return sum(1 for _ in lines)

def isWordlike(word: str, i: int):
  if word.isalpha() and word.islower():
    return True

  say(word, "is not wordlike", i)

def kindOf(soup: _s, word: str, i: int):
  for kind in wordkinds:
    if soup.find_all("li", id=f"toc-{kind}"):
      return kind
  
  say(word, "is unkind", i)

def asEnglishSoup(word: str, i: int):
  def findWord(needle: str):
    return requests.get(url.format(needle), headers=headers).text
  
  def cleanWord(answer: str):
    return _s(answer, "html.parser")

  def fandWord(soup: _s):
    return soup.find("li", id="toc-English")
  
  found = fandWord(cleanWord(findWord(word)))
  if found:
    return found

  say(word, "is not English", i)

def say(word: str, ordeal: str, i: int):
  word = word if len(word) <= 24 else "…"
  print(f"{f"{i/utheight:.2f}% {i}: {word} {ordeal}":<{utline-len(word)-len(ordeal)}}", end="\r", flush=True)

url = "https://en.wiktionary.org/wiki/{}?printable=yes"
headers = { "User-Agent": "kbaki (klausmbaki@gmail.com)", }

wordkinds = [
  "noun", "verb", "adjective", "adverb",
  "determiner", "article", "preposition", "conjunction",
  "pronoun", "particle", "predicative", "participle",
]

utline: int = os.get_terminal_size().columns
utheight: int = height("wiktionary-hoard")

with open("wiktionary-hoard") as lines:
  for i, line in enumerate(lines):
    word = line.strip()
    if not isWordlike(word, i): continue

    eng = asEnglishSoup(word, i)
    if not eng: continue

    kind = kindOf(eng, word, i)
    if not kind: continue

    jbeq = codecs.encode(word, "rot_13")

    rat = asEnglishSoup(jbeq, i)
    if not rat: continue

    xvaq = kindOf(rat, jbeq, i)
    if kind != xvaq: continue

    say(f"{word} <-> {jbeq} ({kind})", i)