#!/usr/bin/env python3
"""
Style checker for the human-natural writing rules.
Scans HTML/MD/text for em dashes and other non-keyboard characters, banned
words and phrases, filler weight, negation reframes, self-answered questions,
anaphora, rule-of-three patterns, tailing participles, unnamed sources,
stacked one-line paragraphs, "My view" opinion labels, and Title Case
headers.

Usage: python style-check.py <file> [file...]
"""
import sys, re, html, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BANNED_WORDS = [
    "delve", "tapestry", "unlock", "unleash", "harness", "leverage", "robust",
    "seamless", "seamlessly", "elevate", "foster", "empower", "resonate",
    "spearhead", "realm", "beacon", "vibrant", "bustling", "nestled", "boasts",
    "myriad", "plethora", "utilize", "facilitate", "holistic", "synergy",
    "paradigm", "streamline", "streamlines", "streamlined", "streamlining",
    "transformative", "transformational",
    "game-changer", "game-changing", "cutting-edge", "comprehensive",
    "actionable insights", "best practices", "paving the way", "a testament to",
    "the intersection of", "ensure", "ensures", "ensuring", "whilst",
    "underscore", "underscores", "underscoring",
]

# Metaphorical-only or context-dependent: flag for human review, may be legitimate
CONTEXT_WORDS = [
    "landscape", "navigate", "journey", "sphere", "domain", "key", "various",
    "a variety of", "ecosystem",
]

# Banned as filler weight. Test: if deleting the word leaves the meaning
# intact, it was filler.
FILLER_WEIGHT = [
    "crucial", "vital", "essential", "fundamental", "pivotal", "significant",
    "powerful", "meaningful", "profound",
]

# Adverbs that make an ordinary claim sound deep
DEPTH_ADVERBS = [
    "quietly", "deeply", "fundamentally", "remarkably", "arguably", "notably",
    "importantly", "interestingly",
]

BANNED_PHRASES = [
    "it's important to note", "it is important to note", "it's worth noting",
    "it's worth mentioning", "it should be noted", "it bears mentioning",
    "in today's fast-paced", "in this digital age", "ever-evolving",
    "in an era of", "in an age where", "when it comes to",
    "at the end of the day", "plays a crucial role", "plays a vital role",
    "plays a pivotal role", "not only", "whether you're a", "look no further",
    "that being said", "with that said", "in conclusion", "in summary",
    "to sum up", "dive deep", "deep dive", "embark on", "rich tapestry",
    # false suspense
    "here's the thing", "here's the kicker", "here's where it gets interesting",
    "here's the deal", "but here's the problem",
    # false exclusivity
    "what most people miss", "nobody talks about this",
    "the part everyone overlooks", "the dirty secret",
    # teacher voice
    "let's break this down", "let's unpack", "let's explore", "think of it as",
    "imagine a world where", "picture this",
    # asserted obviousness
    "the truth is simple", "the reality is", "make no mistake",
    "history is clear", "the real story is",
    # dead idioms
    "the smoking gun", "a perfect storm", "move the needle",
    "double-edged sword", "tip of the iceberg",
    "between a rock and a hard place", "on the same page", "raise the bar",
]

# Substitutes for "is" that inflate the sentence
IS_SUBSTITUTES = [
    r"\bserves as\b", r"\bstands as\b", r"\brepresents a\b", r"\bmarks a\b",
    r"\bembodies\b", r"\bfunctions as\b",
]

UNNAMED_SOURCES = [
    "experts say", "experts agree", "studies show", "studies suggest",
    "research suggests", "research shows", "industry reports indicate",
    "observers note", "critics argue", "it is widely believed",
]

# Opinion labels that read as machine-written. Word-bounded, so "my viewpoint"
# and "review" don't match.
OPINION_LABELS = [
    (r"\bmy view\b", 'OPINION LABEL: "my view" (use My advice, IME, IMO, My opinion or My technique, and vary it)'),
]

AI_TRANSITIONS = ["furthermore", "moreover", "additionally", "notably", "significantly", "ultimately"]

NEGATION_REFRAMES = [
    (r"\bit'?s not (?:just )?[^,.;]{2,45}, it'?s\b", "It's not X, it's Y"),
    (r"\b(?:is|are|was|were)n'?t just [^,.;]{2,45}, (?:it|they)'?s?\b", "X isn't just Y, it's Z"),
    (r"\bis more than just\b", "X is more than just Y"),
    (r"\bnot because [^,.;]{2,55}, but because\b", "not because X, but because Y"),
    (r"\bthe question isn'?t\b", "The question isn't X, the question is Y"),
    (r"\bthis isn'?t about [^,.;]{2,45}\. (?:It|This)'?s about\b", "It's not about X, it's about Y"),
]

TAILING_PARTICIPLES = r",\s+(underscoring|reflecting|highlighting|showcasing|demonstrating|emphasizing|solidifying|cementing|contributing to|marking a|signaling)\b"

# Characters that cannot be typed on a keyboard
NON_KEYBOARD = {
    '—': 'em dash',
    '‘': 'curly apostrophe', '’': 'curly apostrophe',
    '“': 'curly quote', '”': 'curly quote',
    '…': 'ellipsis character',
    ' ': 'non-breaking space',
    '→': 'arrow', '←': 'arrow', '⇒': 'arrow',
    '•': 'bullet glyph', '▪': 'bullet glyph', '●': 'bullet glyph',
    '–': 'en dash (allowed, check it is deliberate)',
}

SMALL_WORDS = {'a', 'an', 'the', 'and', 'or', 'but', 'of', 'to', 'in', 'on', 'at',
               'for', 'with', 'vs', 'up', 'as', 'is', 'it', 'from', 'by'}


def strip_html(s):
    s = re.sub(r'<script[^>]*>.*?</script>', ' ', s, flags=re.S | re.I)
    s = re.sub(r'<style[^>]*>.*?</style>', ' ', s, flags=re.S | re.I)
    s = re.sub(r'<!--.*?-->', ' ', s, flags=re.S)
    s = re.sub(r'<[^>]+>', ' ', s)
    return html.unescape(s)


def sentences(line):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', line) if s.strip()]


def is_title_case(inner):
    words = re.findall(r"[A-Za-z][A-Za-z'&-]*", inner)
    if len(words) < 3:
        return False
    caps = [w for w in words[1:] if w[0].isupper()]
    lowers = [w for w in words[1:] if w[0].islower() and w.lower() not in SMALL_WORDS]
    return len(caps) >= 2 and not lowers


def check(path):
    raw = open(path, encoding='utf-8').read()
    findings = []

    # 1. Non-keyboard characters, checked on the whole file including comments
    for i, line in enumerate(raw.splitlines(), 1):
        if '&mdash;' in line or '&#8212;' in line:
            findings.append(('EM DASH (entity)', i, line.strip()[:120]))
        for ch, label in NON_KEYBOARD.items():
            if ch in line:
                findings.append(('CHARACTER: ' + label, i, line.strip()[:120]))

    # Fenced code blocks are not prose. Blank them out but keep the line
    # numbering intact so findings still point at the right line.
    text = strip_html(raw)
    lines, in_fence = [], False
    for line in text.splitlines():
        if re.match(r'^\s*```', line):
            in_fence = not in_fence
            lines.append('')
        else:
            lines.append('' if in_fence else line)

    for i, line in enumerate(lines, 1):
        low = line.lower()
        snip = line.strip()[:120]
        for w in BANNED_WORDS:
            if re.search(r'\b' + re.escape(w) + r'\b', low):
                findings.append(('BANNED WORD: ' + w, i, snip))
        for p in BANNED_PHRASES:
            if p in low:
                findings.append(('BANNED PHRASE: ' + p, i, snip))
        for w in FILLER_WEIGHT:
            if re.search(r'\b' + re.escape(w) + r'\b', low):
                findings.append(('FILLER WEIGHT: ' + w, i, snip))
        for w in DEPTH_ADVERBS:
            if re.search(r'\b' + re.escape(w) + r'\b', low):
                findings.append(('DEPTH ADVERB: ' + w, i, snip))
        for w in CONTEXT_WORDS:
            if re.search(r'\b' + re.escape(w) + r'\b', low):
                findings.append(('REVIEW (context): ' + w, i, snip))
        for p in UNNAMED_SOURCES:
            if p in low:
                findings.append(('UNNAMED SOURCE: ' + p, i, snip))
        for pat, label in OPINION_LABELS:
            if re.search(pat, low):
                findings.append((label, i, snip))
        for pat in IS_SUBSTITUTES:
            if re.search(pat, low):
                findings.append(('USE "IS" INSTEAD', i, snip))
        for pat, label in NEGATION_REFRAMES:
            if re.search(pat, low):
                findings.append(('NEGATION REFRAME: ' + label, i, snip))
        if re.search(TAILING_PARTICIPLES, low):
            findings.append(('TAILING PARTICIPLE', i, snip))
        if re.search(r'\bdespite (?:its|the|these) \w+,', low):
            findings.append(('DESPITE ITS CHALLENGES FORMULA', i, snip))
        for t in AI_TRANSITIONS:
            if re.match(r'^\s*' + t + r'\b', low):
                findings.append(('AI TRANSITION: ' + t, i, snip))
        for m in re.finditer(r'\bfrom [a-z]{3,20} to [a-z]{3,20}\b', low):
            findings.append(('REVIEW (false range?): ' + m.group(0), i, snip))

        # Self-posed question answered immediately by a short fragment
        for m in re.finditer(r"(?:^|(?<=[.!?]) )([A-Z][^.!?]{2,40}\?)\s+([A-Z][^.!?]{2,45}[.!])", line):
            if len(m.group(1).split()) <= 8 and len(m.group(2).split()) <= 8:
                findings.append(('SELF-ANSWERED QUESTION', i, m.group(0)[:110]))

        # Rule of three: exactly three items. A 4+ item list is fine per the rules,
        # so skip matches whose run of commas starts earlier in the sentence.
        for m in re.finditer(r'\b([\w][\w\s\-/]{2,28}),\s+([\w][\w\s\-/]{2,28}),\s+and\s+([\w][\w\s\-/]{2,28})\b', line):
            if line[:m.start()].rstrip().endswith(','):
                continue
            findings.append(('RULE OF THREE', i, m.group(0)[:110]))

    # 2. Anaphora: three or more consecutive sentences opening with the same word
    flat = []
    for i, line in enumerate(lines, 1):
        for s in sentences(line):
            flat.append((i, s))
    run_word, run = None, []
    for i, s in enumerate(flat):
        first = re.findall(r"[A-Za-z']+", s[1])
        first = first[0].lower() if first else None
        if first and first == run_word:
            run.append(s)
        else:
            if len(run) >= 3:
                findings.append(('ANAPHORA: "%s" x%d' % (run_word, len(run)), run[0][0], run[0][1][:100]))
            run_word, run = first, [s]
    if len(run) >= 3:
        findings.append(('ANAPHORA: "%s" x%d' % (run_word, len(run)), run[0][0], run[0][1][:100]))

    # 3. Stacked one-line paragraphs used for emphasis
    paras, cur, start = [], [], 1
    for i, line in enumerate(lines, 1):
        if line.strip():
            if not cur:
                start = i
            cur.append(line.strip())
        elif cur:
            paras.append((start, ' '.join(cur)))
            cur = []
    if cur:
        paras.append((start, ' '.join(cur)))
    short_run = []
    for ln, p in paras:
        if p.startswith(('-', '*', '#', '|', '>', '1.')) or len(p) > 200:
            if len(short_run) >= 3:
                findings.append(('STACKED ONE-LINE PARAGRAPHS x%d' % len(short_run), short_run[0][0], short_run[0][1][:100]))
            short_run = []
            continue
        if len(sentences(p)) <= 1:
            short_run.append((ln, p))
        else:
            if len(short_run) >= 3:
                findings.append(('STACKED ONE-LINE PARAGRAPHS x%d' % len(short_run), short_run[0][0], short_run[0][1][:100]))
            short_run = []
    if len(short_run) >= 3:
        findings.append(('STACKED ONE-LINE PARAGRAPHS x%d' % len(short_run), short_run[0][0], short_run[0][1][:100]))

    # 4. Title Case headers, HTML and Markdown
    for m in re.finditer(r'<h([1-3])[^>]*>(.*?)</h\1>', raw, flags=re.S | re.I):
        inner = html.unescape(re.sub(r'<[^>]+>', '', m.group(2))).strip()
        if is_title_case(inner):
            findings.append(('TITLE CASE HEADER', raw[:m.start()].count('\n') + 1, inner[:110]))
    for i, line in enumerate(raw.splitlines(), 1):
        m = re.match(r'^\s{0,3}#{1,4}\s+(.*\S)\s*$', line)
        if m and is_title_case(m.group(1)):
            findings.append(('TITLE CASE HEADER', i, m.group(1)[:110]))

    # 5. Conclusion or recap section
    for i, line in enumerate(raw.splitlines(), 1):
        if re.match(r'^\s{0,3}(#{1,4}\s+|<h[1-4][^>]*>)?\s*(conclusion|summary|final thoughts|wrapping up|key takeaways)\b',
                    line.strip(), flags=re.I):
            findings.append(('CONCLUDING SECTION', i, line.strip()[:110]))

    return findings


def main():
    if len(sys.argv) < 2:
        print(__doc__.strip())
        return 2
    total = 0
    for path in sys.argv[1:]:
        f = check(path)
        total += len(f)
        print('=' * 72)
        print('FILE:', path)
        print('=' * 72)
        if not f:
            print('  clean')
        else:
            by_kind = {}
            for kind, ln, snip in f:
                by_kind.setdefault(kind.split(':')[0], []).append((kind, ln, snip))
            for group in sorted(by_kind):
                items = by_kind[group]
                print('\n  %s  (%d)' % (group, len(items)))
                for kind, ln, snip in items:
                    label = kind if ':' in kind else ''
                    print('    line %-5s %s' % (ln, (label + '  ' if label else '') + snip))
        print()
    print('TOTAL FINDINGS:', total)
    return 1 if total else 0


if __name__ == '__main__':
    sys.exit(main())
