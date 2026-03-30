import json

import genanki

with open("./quran-metadata-rub.json", "r") as f:
    quran_rub_metadata = json.load(f)
with open("./quran-metadata-surah-name.json", "r") as f:
    quran_surah_metadata = json.load(f)
with open("./quran-metadata-ayah.json", "r") as f:
    quran_ayah_metadata = json.load(f)
    quran_ayah_metadata = {v["verse_key"]: v for v in quran_ayah_metadata.values()}

my_model = genanki.Model(
    1607392319,
    "Quran Rub Model",
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
    css="""
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
    """,
)

my_deck = genanki.Deck(2059400110, "Quran Rub")

for rub_idx in range(1, len(quran_rub_metadata) + 1):
    n_rub = str(rub_idx)
    first_verse_key = quran_rub_metadata[n_rub]["first_verse_key"]
    first_surah_idx = first_verse_key.split(":")[0]
    first_surah_name = quran_surah_metadata[first_surah_idx]["name_arabic"]
    first_surah_glyph = f"surah{int(first_surah_idx):03d}"
    first_ayah_text = quran_ayah_metadata[first_verse_key]["text"]

    last_verse_key = quran_rub_metadata[n_rub]["last_verse_key"]
    last_surah_idx = last_verse_key.split(":")[0]
    last_surah_name = quran_surah_metadata[last_surah_idx]["name_arabic"]
    last_surah_glyph = f"surah{int(last_surah_idx):03d}"
    last_ayah_text = quran_ayah_metadata[last_verse_key]["text"]

    question = f"""
    <div class="rub-num">ربع {rub_idx}</div>

    <div class="verse-block">
        <div class="label">البداية</div>
        <div class="surah-name">{first_surah_glyph}</div>
        <div class="verse-ref">{first_verse_key}</div>
        <div class="ayah-text">{first_ayah_text}</div>
    </div>

    <div class="verse-block">
        <div class="label">النهاية</div>
        <div class="surah-name">{last_surah_glyph}</div>
        <div class="verse-ref">{last_verse_key}</div>
        <div class="ayah-text">{last_ayah_text}</div>
    </div>
    """

    my_note = genanki.Note(model=my_model, fields=[question.replace("\x1f", ""), ""])
    my_deck.add_note(my_note)

genanki.Package(my_deck).write_to_file("quran-rub.apkg")
