import os
import re
import codecs
import requests

from bs4 import _s

def hord(c: str):
  return ord(c)-ord("a")

def hchr(n: int):
  return chr(n+ord("a"))

def height(leafname: str):
  with open(leafname, "rb") as lines:
    return sum(1 for _ in lines)

def anitya(*values: object):
  print(*values, end="\r", flush=True)

def rot13(word: str):
  return codecs.encode(word, "rot_13")

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
  print(f"{f"{i/len(alltwains):.2f}% {i}: {word} {ordeal}…":<{utline-len(word)-len(ordeal)}}", end="\r", flush=True)

url = "https://en.wiktionary.org/wiki/{}?printable=yes"
headers = { "User-Agent": "kbaki (klausmbaki@gmail.com)", }

wordkinds = [
  "noun", "verb", "adjective", "adverb",
  "determiner", "article", "preposition", "conjunction",
  "pronoun", "particle", "predicative", "participle",
]

utline: int = os.get_terminal_size().columns
utheight: int = height("wiktionary-hoard")

words = [set() for _ in range(26)]
twains = [set() for _ in range(13)]

# https://dumps.wikimedia.org/enwiktionary/latest/enwiktionary-latest-all-titles-in-ns0.gz
with open("wiktionary-hoard") as lines:
  for i, line in enumerate(lines):
    word = line.strip()
    if re.fullmatch(r"\b[a-z]+\b", word):
      words[hord(word[0])].add(word)
    anitya(f"trawled {i} of {utheight} lines for English words…")

anitya(utline*" ")

print(f"{sum([len(ws) for ws in words])} alphabetic words found!")
print([f"{list(head)[0][0]}: {len(head)}" for head in words])
print()

for i in range(13):
  twains[i] = list(set(map(rot13, words[(i+13)%26])).intersection(words[i]))
  anitya(f"trawled the {hchr(i)}-words for rot13 twains…")

anitya(utline*" ")

print(f"{sum([len(tws) for tws in twains])} rot13 twains found!")
print([f"{list(head)[0][0]}: {len(head)}" for head in twains])
print()

alltwains = set().union(*twains)

for i, word in enumerate(alltwains):
  eng = asEnglishSoup(word, i)
  if not eng: continue

  kind = kindOf(eng, word, i)
  if not kind: continue

  jbeq = rot13(word)

  rat = asEnglishSoup(jbeq, i)
  if not rat: continue

  xvaq = kindOf(rat, jbeq, i)
  if kind != xvaq:
    say(f"{word} and {jbeq} are of unlike kinds…")
    continue

  print(f"{word} <-> {jbeq} ({kind}) 🥳")