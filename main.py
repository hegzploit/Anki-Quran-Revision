import json

import genanki

with open("./quran-metadata-rub.json", "r") as f:
    quran_rub_metadata = json.load(f)
with open("./quran-metadata-page.json", "r") as f:
    quran_page_metadata = json.load(f)
with open("./quran-metadata-surah-name.json", "r") as f:
    quran_surah_metadata = json.load(f)
with open("./quran-metadata-ayah.json", "r") as f:
    quran_ayah_metadata = json.load(f)
    quran_ayah_metadata = {v["verse_key"]: v for v in quran_ayah_metadata.values()}

CSS = """
@font-face {
    font-family: 'surah-name-v2-icon';
    src: url('https://static-cdn.tarteel.ai/qul/fonts/surah-names/v2/surah-name-v2.ttf') format('truetype');
    font-display: swap;
}
@font-face {
    font-family: 'qpc-nastaleeq';
    src: url('https://static-cdn.tarteel.ai/qul/fonts/nastaleeq/KFGQPCNastaleeq-Regular.ttf') format('truetype');
    font-display: swap;
}
.card {
    font-size: 24px;
    text-align: center;
    direction: rtl;
    color: #ebdbb2;
    background: #282828;
    padding: 20px;
}
.rub-num {
    font-size: 18px;
    color: #928374;
    margin-bottom: 12px;
}
.verse-block {
    margin: 16px 0;
    padding: 12px;
    border-radius: 8px;
    background: #3c3836;
    border: 1px solid #504945;
}
.surah-name {
    font-family: 'surah-name-v2-icon';
    font-size: 40px;
    color: #fabd2f;
}
.verse-ref {
    font-size: 14px;
    color: #a89984;
    direction: ltr;
}
.ayah-text {
    font-family: 'qpc-nastaleeq';
    font-size: 26px;
    line-height: 2.0;
    margin-top: 8px;
    color: #ebdbb2;
}
.label {
    font-size: 14px;
    color: #83a598;
    margin-bottom: 4px;
}
"""

MODEL = genanki.Model(
    1607392319,
    "Quran Section Model",
    fields=[
        {"name": "Question"},
        {"name": "Answer"},
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "{{Question}}",
            "afmt": '{{FrontSide}}<hr id="answer">{{Answer}}',
        },
    ],
    css=CSS,
)


def verse_block(label, verse_key):
    surah_idx = verse_key.split(":")[0]
    surah_glyph = f"surah{int(surah_idx):03d}"
    ayah_text = quran_ayah_metadata[verse_key]["text"]
    return f"""
    <div class="verse-block">
        <div class="label">{label}</div>
        <div class="surah-name">{surah_glyph}</div>
        <div class="verse-ref">{verse_key}</div>
        <div class="ayah-text">{ayah_text}</div>
    </div>
    """


def build_question(header_text, first_verse_key, last_verse_key):
    return f"""
    <div class="rub-num">{header_text}</div>
    {verse_block("البداية", first_verse_key)}
    {verse_block("النهاية", last_verse_key)}
    """


def build_deck(deck_id, deck_name, out_file, cards):
    deck = genanki.Deck(deck_id, deck_name)
    for header, first_key, last_key in cards:
        question = build_question(header, first_key, last_key).replace("\x1f", "")
        deck.add_note(genanki.Note(model=MODEL, fields=[question, ""]))
    genanki.Package(deck).write_to_file(out_file)


def rub_cards():
    for i in range(1, len(quran_rub_metadata) + 1):
        m = quran_rub_metadata[str(i)]
        yield f"ربع {i}", m["first_verse_key"], m["last_verse_key"]


def page_cards():
    for i in range(1, len(quran_page_metadata) + 1):
        m = quran_page_metadata[str(i)]
        yield f"صفحة {i}", m["first_verse_key"], m["last_verse_key"]


def surah_cards():
    for i in range(1, len(quran_surah_metadata) + 1):
        m = quran_surah_metadata[str(i)]
        yield (
            f"سورة {i} · {m['name_arabic']}",
            f"{i}:1",
            f"{i}:{m['verses_count']}",
        )


build_deck(2059400110, "Quran Rub", "quran-rub.apkg", rub_cards())
build_deck(2059400111, "Quran Page", "quran-page.apkg", page_cards())
build_deck(2059400112, "Quran Surah", "quran-surah.apkg", surah_cards())
