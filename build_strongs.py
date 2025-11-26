#!/usr/bin/env python3
"""
Build comprehensive Strong's Concordance database
Core Hebrew (H) and Greek (G) vocabulary
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

# =============================================================================
# HEBREW STRONG'S (H1 - H8674) - Core theological vocabulary
# =============================================================================

HEBREW_STRONGS = {
    # GOD / DIVINE NAMES
    "H1": {"hebrew": "אָב", "translit": "ab", "def": "father", "kjv": "father, chief, families", "occur": 1180},
    "H113": {"hebrew": "אָדוֹן", "translit": "adown", "def": "lord, master", "kjv": "lord, master, owner", "occur": 335},
    "H136": {"hebrew": "אֲדֹנָי", "translit": "Adonay", "def": "Lord (divine title)", "kjv": "Lord", "occur": 434},
    "H410": {"hebrew": "אֵל", "translit": "el", "def": "God, mighty one", "kjv": "God, god, mighty", "occur": 242},
    "H426": {"hebrew": "אֱלָהּ", "translit": "elahh", "def": "God (Aramaic)", "kjv": "God, god", "occur": 95},
    "H430": {"hebrew": "אֱלֹהִים", "translit": "elohim", "def": "God, gods, judges", "kjv": "God, gods, judges", "occur": 2606},
    "H433": {"hebrew": "אֱלוֹהַּ", "translit": "eloahh", "def": "God", "kjv": "God", "occur": 57},
    "H3050": {"hebrew": "יָהּ", "translit": "Yahh", "def": "Jah, the LORD", "kjv": "LORD, JAH", "occur": 49},
    "H3068": {"hebrew": "יְהוָה", "translit": "YHWH", "def": "the LORD, Yahweh", "kjv": "LORD, GOD, JEHOVAH", "occur": 6519},
    "H3069": {"hebrew": "יְהֹוִה", "translit": "Yehovih", "def": "GOD (variant)", "kjv": "GOD", "occur": 305},
    "H5945": {"hebrew": "עֶלְיוֹן", "translit": "elyon", "def": "Most High", "kjv": "most high, upper", "occur": 53},
    "H6635": {"hebrew": "צָבָא", "translit": "tsaba", "def": "host, army", "kjv": "host, army, war", "occur": 486},
    "H7706": {"hebrew": "שַׁדַּי", "translit": "Shadday", "def": "Almighty", "kjv": "Almighty", "occur": 48},

    # SPIRIT / SOUL / LIFE
    "H2416": {"hebrew": "חַי", "translit": "chay", "def": "living, alive, life", "kjv": "live, life, beast", "occur": 763},
    "H5315": {"hebrew": "נֶפֶשׁ", "translit": "nephesh", "def": "soul, life, self", "kjv": "soul, life, person", "occur": 753},
    "H7307": {"hebrew": "רוּחַ", "translit": "ruach", "def": "spirit, wind, breath", "kjv": "spirit, wind, breath", "occur": 378},

    # COVENANT / LAW / WORD
    "H1285": {"hebrew": "בְּרִית", "translit": "berith", "def": "covenant, treaty", "kjv": "covenant, league", "occur": 284},
    "H1697": {"hebrew": "דָּבָר", "translit": "dabar", "def": "word, speech, matter", "kjv": "word, thing, matter", "occur": 1441},
    "H2706": {"hebrew": "חֹק", "translit": "choq", "def": "statute, ordinance", "kjv": "statute, ordinance", "occur": 127},
    "H4687": {"hebrew": "מִצְוָה", "translit": "mitsvah", "def": "commandment", "kjv": "commandment, precept", "occur": 181},
    "H8451": {"hebrew": "תּוֹרָה", "translit": "torah", "def": "law, instruction", "kjv": "law", "occur": 219},

    # RIGHTEOUSNESS / JUSTICE / TRUTH
    "H571": {"hebrew": "אֶמֶת", "translit": "emeth", "def": "truth, faithfulness", "kjv": "truth, true, faithfully", "occur": 127},
    "H2617": {"hebrew": "חֶסֶד", "translit": "chesed", "def": "lovingkindness, mercy", "kjv": "mercy, kindness, lovingkindness", "occur": 248},
    "H4941": {"hebrew": "מִשְׁפָּט", "translit": "mishpat", "def": "judgment, justice", "kjv": "judgment, manner, right", "occur": 421},
    "H6662": {"hebrew": "צַדִּיק", "translit": "tsaddiq", "def": "righteous, just", "kjv": "righteous, just, lawful", "occur": 206},
    "H6663": {"hebrew": "צָדַק", "translit": "tsadaq", "def": "to be righteous", "kjv": "justify, righteous, cleanse", "occur": 41},
    "H6664": {"hebrew": "צֶדֶק", "translit": "tsedeq", "def": "righteousness", "kjv": "righteousness, just, justice", "occur": 116},
    "H6666": {"hebrew": "צְדָקָה", "translit": "tsedaqah", "def": "righteousness", "kjv": "righteousness, justice", "occur": 157},

    # SIN / EVIL / TRANSGRESSION
    "H2398": {"hebrew": "חָטָא", "translit": "chata", "def": "to sin, miss the mark", "kjv": "sin, purify, cleanse", "occur": 238},
    "H2399": {"hebrew": "חֵטְא", "translit": "chet", "def": "sin, sinful", "kjv": "sin, faults", "occur": 33},
    "H2403": {"hebrew": "חַטָּאָה", "translit": "chattaah", "def": "sin, sin offering", "kjv": "sin, sin offering", "occur": 296},
    "H5753": {"hebrew": "עָוָה", "translit": "avah", "def": "to bend, twist, pervert", "kjv": "iniquity, perverse, crooked", "occur": 17},
    "H5771": {"hebrew": "עָוֺן", "translit": "avon", "def": "iniquity, guilt", "kjv": "iniquity, punishment", "occur": 231},
    "H6588": {"hebrew": "פֶּשַׁע", "translit": "pesha", "def": "transgression, rebellion", "kjv": "transgression, trespass", "occur": 93},
    "H7451": {"hebrew": "רַע", "translit": "ra", "def": "evil, bad, wicked", "kjv": "evil, wickedness, bad", "occur": 663},
    "H7561": {"hebrew": "רָשַׁע", "translit": "rasha", "def": "to be wicked", "kjv": "condemn, wicked", "occur": 34},
    "H7562": {"hebrew": "רֶשַׁע", "translit": "resha", "def": "wickedness", "kjv": "wickedness, wicked", "occur": 30},
    "H7563": {"hebrew": "רָשָׁע", "translit": "rasha", "def": "wicked, criminal", "kjv": "wicked, ungodly", "occur": 264},

    # SALVATION / REDEMPTION
    "H1350": {"hebrew": "גָּאַל", "translit": "gaal", "def": "to redeem, act as kinsman", "kjv": "redeem, redeemer, kinsman", "occur": 104},
    "H3444": {"hebrew": "יְשׁוּעָה", "translit": "yeshuah", "def": "salvation, deliverance", "kjv": "salvation, help, deliverance", "occur": 78},
    "H3467": {"hebrew": "יָשַׁע", "translit": "yasha", "def": "to save, deliver", "kjv": "save, saviour, deliver", "occur": 205},
    "H6299": {"hebrew": "פָּדָה", "translit": "padah", "def": "to ransom, redeem", "kjv": "redeem, ransom, deliver", "occur": 59},
    "H7965": {"hebrew": "שָׁלוֹם", "translit": "shalom", "def": "peace, completeness", "kjv": "peace, well, peaceably", "occur": 236},

    # FAITH / TRUST / BELIEVE
    "H539": {"hebrew": "אָמַן", "translit": "aman", "def": "to believe, be faithful", "kjv": "believe, assurance, faithful", "occur": 108},
    "H982": {"hebrew": "בָּטַח", "translit": "batach", "def": "to trust, be confident", "kjv": "trust, confident, secure", "occur": 120},
    "H530": {"hebrew": "אֱמוּנָה", "translit": "emunah", "def": "faithfulness, firmness", "kjv": "faithfulness, truth, faithful", "occur": 49},

    # LOVE / HATE
    "H157": {"hebrew": "אָהַב", "translit": "ahab", "def": "to love", "kjv": "love, lover, friend", "occur": 208},
    "H160": {"hebrew": "אַהֲבָה", "translit": "ahabah", "def": "love", "kjv": "love", "occur": 40},
    "H8130": {"hebrew": "שָׂנֵא", "translit": "sane", "def": "to hate", "kjv": "hate, enemy, foe", "occur": 146},

    # HEAR / OBEY (SHEMA)
    "H8085": {"hebrew": "שָׁמַע", "translit": "shama", "def": "to hear, listen, obey", "kjv": "hear, hearken, obey", "occur": 1159},
    "H8104": {"hebrew": "שָׁמַר", "translit": "shamar", "def": "to keep, guard, observe", "kjv": "keep, observe, heed", "occur": 469},

    # HOLY / SANCTIFY / GLORY
    "H3513": {"hebrew": "כָּבַד", "translit": "kabad", "def": "to be heavy, honored", "kjv": "honour, glorify, heavy", "occur": 114},
    "H3519": {"hebrew": "כָּבוֹד", "translit": "kabod", "def": "glory, honor, splendor", "kjv": "glory, honour, glorious", "occur": 200},
    "H6918": {"hebrew": "קָדוֹשׁ", "translit": "qadosh", "def": "holy, sacred", "kjv": "holy, Holy One, saint", "occur": 116},
    "H6942": {"hebrew": "קָדַשׁ", "translit": "qadash", "def": "to be holy, sanctify", "kjv": "sanctify, holy, dedicate", "occur": 172},
    "H6944": {"hebrew": "קֹדֶשׁ", "translit": "qodesh", "def": "holiness, sacredness", "kjv": "holy, sanctuary, hallowed", "occur": 470},

    # BLOOD / ATONEMENT / SACRIFICE
    "H1818": {"hebrew": "דָּם", "translit": "dam", "def": "blood", "kjv": "blood, bloody", "occur": 361},
    "H2076": {"hebrew": "זָבַח", "translit": "zabach", "def": "to slaughter, sacrifice", "kjv": "sacrifice, offer, kill", "occur": 134},
    "H2077": {"hebrew": "זֶבַח", "translit": "zebach", "def": "sacrifice", "kjv": "sacrifice, offering", "occur": 162},
    "H3722": {"hebrew": "כָּפַר", "translit": "kaphar", "def": "to cover, atone", "kjv": "make atonement, purge", "occur": 102},
    "H3725": {"hebrew": "כִּפֻּר", "translit": "kippur", "def": "atonement", "kjv": "atonement", "occur": 8},
    "H5930": {"hebrew": "עֹלָה", "translit": "olah", "def": "burnt offering", "kjv": "burnt offering, burnt sacrifice", "occur": 286},

    # BLESS / CURSE
    "H1288": {"hebrew": "בָּרַךְ", "translit": "barak", "def": "to bless, kneel", "kjv": "bless, praise, kneel", "occur": 330},
    "H1293": {"hebrew": "בְּרָכָה", "translit": "berakah", "def": "blessing", "kjv": "blessing, blessed, present", "occur": 71},
    "H779": {"hebrew": "אָרַר", "translit": "arar", "def": "to curse", "kjv": "curse", "occur": 63},
    "H7043": {"hebrew": "קָלַל", "translit": "qalal", "def": "to be light, curse", "kjv": "curse, light, swift", "occur": 82},
    "H7045": {"hebrew": "קְלָלָה", "translit": "qelalah", "def": "curse", "kjv": "curse, cursing", "occur": 33},

    # CREATION / MAKE
    "H1254": {"hebrew": "בָּרָא", "translit": "bara", "def": "to create", "kjv": "create, creator, choose", "occur": 54},
    "H3335": {"hebrew": "יָצַר", "translit": "yatsar", "def": "to form, fashion", "kjv": "form, potter, fashion", "occur": 62},
    "H6213": {"hebrew": "עָשָׂה", "translit": "asah", "def": "to do, make", "kjv": "do, make, work", "occur": 2633},

    # HEAVEN / EARTH
    "H776": {"hebrew": "אֶרֶץ", "translit": "erets", "def": "earth, land", "kjv": "land, earth, country", "occur": 2504},
    "H8064": {"hebrew": "שָׁמַיִם", "translit": "shamayim", "def": "heaven, sky", "kjv": "heaven, air, sky", "occur": 421},

    # LIGHT / DARKNESS
    "H216": {"hebrew": "אוֹר", "translit": "or", "def": "light", "kjv": "light, bright, day", "occur": 122},
    "H2822": {"hebrew": "חֹשֶׁךְ", "translit": "choshek", "def": "darkness", "kjv": "darkness, dark, obscurity", "occur": 80},

    # DAY / NIGHT / TIME
    "H3117": {"hebrew": "יוֹם", "translit": "yom", "def": "day, time", "kjv": "day, time, daily", "occur": 2301},
    "H3915": {"hebrew": "לַיְלָה", "translit": "layil", "def": "night", "kjv": "night, midnight, season", "occur": 234},
    "H5769": {"hebrew": "עוֹלָם", "translit": "olam", "def": "eternity, forever", "kjv": "ever, everlasting, old", "occur": 439},

    # PEOPLE / NATION
    "H1471": {"hebrew": "גּוֹי", "translit": "goy", "def": "nation, people (gentiles)", "kjv": "nation, heathen, gentiles", "occur": 558},
    "H5971": {"hebrew": "עַם", "translit": "am", "def": "people, nation", "kjv": "people, nation, folk", "occur": 1869},

    # KING / KINGDOM
    "H4427": {"hebrew": "מָלַךְ", "translit": "malak", "def": "to reign, be king", "kjv": "reign, king, royal", "occur": 350},
    "H4428": {"hebrew": "מֶלֶךְ", "translit": "melek", "def": "king", "kjv": "king, royal, kingdom", "occur": 2523},
    "H4438": {"hebrew": "מַלְכוּת", "translit": "malkuth", "def": "kingdom, dominion", "kjv": "kingdom, reign, royal", "occur": 91},
    "H4467": {"hebrew": "מַמְלָכָה", "translit": "mamlakah", "def": "kingdom, dominion", "kjv": "kingdom, reign, royal", "occur": 117},

    # PRIEST / PROPHET
    "H3548": {"hebrew": "כֹּהֵן", "translit": "kohen", "def": "priest", "kjv": "priest, chief ruler", "occur": 750},
    "H5030": {"hebrew": "נָבִיא", "translit": "nabi", "def": "prophet, spokesman", "kjv": "prophet, prophecy", "occur": 316},

    # ANGEL / MESSENGER
    "H4397": {"hebrew": "מַלְאָךְ", "translit": "malak", "def": "messenger, angel", "kjv": "angel, messenger", "occur": 213},

    # DEATH / LIFE
    "H2421": {"hebrew": "חָיָה", "translit": "chayah", "def": "to live, be alive", "kjv": "live, save, alive", "occur": 262},
    "H4191": {"hebrew": "מוּת", "translit": "muth", "def": "to die", "kjv": "die, dead, death", "occur": 835},
    "H4194": {"hebrew": "מָוֶת", "translit": "maveth", "def": "death", "kjv": "death, dead, deadly", "occur": 160},
    "H7585": {"hebrew": "שְׁאוֹל", "translit": "sheol", "def": "grave, underworld", "kjv": "grave, hell, pit", "occur": 66},

    # PRAY / WORSHIP
    "H6419": {"hebrew": "פָּלַל", "translit": "palal", "def": "to pray, intercede", "kjv": "pray, judge, intreat", "occur": 84},
    "H7812": {"hebrew": "שָׁחָה", "translit": "shachah", "def": "to bow down, worship", "kjv": "worship, bow, fall down", "occur": 172},
    "H8605": {"hebrew": "תְּפִלָּה", "translit": "tephillah", "def": "prayer", "kjv": "prayer", "occur": 77},

    # KNOW / WISDOM
    "H998": {"hebrew": "בִּינָה", "translit": "binah", "def": "understanding", "kjv": "understanding, wisdom", "occur": 37},
    "H1847": {"hebrew": "דַּעַת", "translit": "daath", "def": "knowledge", "kjv": "knowledge, know, cunning", "occur": 93},
    "H2449": {"hebrew": "חָכַם", "translit": "chakam", "def": "to be wise", "kjv": "wise, wisdom, teach", "occur": 27},
    "H2451": {"hebrew": "חָכְמָה", "translit": "chokmah", "def": "wisdom, skill", "kjv": "wisdom, wisely, skilful", "occur": 149},
    "H3045": {"hebrew": "יָדַע", "translit": "yada", "def": "to know", "kjv": "know, knowledge, perceive", "occur": 947},

    # HEART / MIND
    "H3820": {"hebrew": "לֵב", "translit": "leb", "def": "heart, mind, will", "kjv": "heart, mind, understanding", "occur": 593},
    "H3824": {"hebrew": "לֵבָב", "translit": "lebab", "def": "heart, inner man", "kjv": "heart, consider", "occur": 252},

    # STRENGTH / POWER
    "H1369": {"hebrew": "גְּבוּרָה", "translit": "geburah", "def": "might, strength", "kjv": "might, strength, power", "occur": 61},
    "H2428": {"hebrew": "חַיִל", "translit": "chayil", "def": "strength, army, valor", "kjv": "army, man of valour, host", "occur": 243},
    "H3027": {"hebrew": "יָד", "translit": "yad", "def": "hand, power", "kjv": "hand, by, power", "occur": 1612},
    "H3581": {"hebrew": "כֹּחַ", "translit": "koach", "def": "strength, power", "kjv": "strength, power, might", "occur": 126},
    "H5797": {"hebrew": "עֹז", "translit": "oz", "def": "strength, might", "kjv": "strength, strong, power", "occur": 93},

    # FEAR / AWE
    "H3372": {"hebrew": "יָרֵא", "translit": "yare", "def": "to fear, revere", "kjv": "fear, afraid, terrible", "occur": 314},
    "H3373": {"hebrew": "יָרֵא", "translit": "yare", "def": "fearing, reverent", "kjv": "fear, afraid, fearful", "occur": 63},
    "H3374": {"hebrew": "יִרְאָה", "translit": "yirah", "def": "fear, reverence", "kjv": "fear, dreadful, fearfulness", "occur": 45},

    # CLEAN / UNCLEAN
    "H2889": {"hebrew": "טָהוֹר", "translit": "tahor", "def": "clean, pure", "kjv": "clean, pure, fair", "occur": 96},
    "H2891": {"hebrew": "טָהֵר", "translit": "taher", "def": "to be clean, pure", "kjv": "clean, purify, cleanse", "occur": 94},
    "H2930": {"hebrew": "טָמֵא", "translit": "tame", "def": "to be unclean", "kjv": "unclean, defile, pollute", "occur": 162},
    "H2931": {"hebrew": "טָמֵא", "translit": "tame", "def": "unclean, defiled", "kjv": "unclean, defiled, polluted", "occur": 88},

    # NAME
    "H8034": {"hebrew": "שֵׁם", "translit": "shem", "def": "name, reputation", "kjv": "name, renown, fame", "occur": 864},

    # WAY / PATH
    "H734": {"hebrew": "אֹרַח", "translit": "orach", "def": "path, way", "kjv": "way, path, highway", "occur": 58},
    "H1870": {"hebrew": "דֶּרֶךְ", "translit": "derek", "def": "way, road, journey", "kjv": "way, toward, journey", "occur": 706},

    # FACE / PRESENCE
    "H6440": {"hebrew": "פָּנִים", "translit": "panim", "def": "face, presence", "kjv": "before, face, presence", "occur": 2109},

    # WATER / FIRE
    "H784": {"hebrew": "אֵשׁ", "translit": "esh", "def": "fire", "kjv": "fire, burning, fiery", "occur": 379},
    "H4325": {"hebrew": "מַיִם", "translit": "mayim", "def": "water", "kjv": "water, piss, waters", "occur": 581},

    # ADAM / MAN
    "H120": {"hebrew": "אָדָם", "translit": "adam", "def": "man, mankind, Adam", "kjv": "man, Adam, person", "occur": 552},
    "H376": {"hebrew": "אִישׁ", "translit": "ish", "def": "man, husband", "kjv": "man, men, husband", "occur": 1639},
    "H802": {"hebrew": "אִשָּׁה", "translit": "ishshah", "def": "woman, wife", "kjv": "wife, woman, female", "occur": 781},

    # SON / DAUGHTER
    "H1121": {"hebrew": "בֵּן", "translit": "ben", "def": "son, child", "kjv": "son, children, child", "occur": 4906},
    "H1323": {"hebrew": "בַּת", "translit": "bath", "def": "daughter", "kjv": "daughter, town, village", "occur": 587},

    # SERVANT / SERVE
    "H5647": {"hebrew": "עָבַד", "translit": "abad", "def": "to work, serve", "kjv": "serve, do, work", "occur": 290},
    "H5650": {"hebrew": "עֶבֶד", "translit": "ebed", "def": "servant, slave", "kjv": "servant, bondman, slave", "occur": 800},

    # SEEK / FIND
    "H1245": {"hebrew": "בָּקַשׁ", "translit": "baqash", "def": "to seek, require", "kjv": "seek, require, request", "occur": 225},
    "H1875": {"hebrew": "דָּרַשׁ", "translit": "darash", "def": "to seek, inquire", "kjv": "seek, enquire, require", "occur": 164},
    "H4672": {"hebrew": "מָצָא", "translit": "matsa", "def": "to find, obtain", "kjv": "find, present, meet", "occur": 457},

    # GIVE / RECEIVE
    "H5414": {"hebrew": "נָתַן", "translit": "nathan", "def": "to give, set, put", "kjv": "give, put, deliver", "occur": 2011},
    "H3947": {"hebrew": "לָקַח", "translit": "laqach", "def": "to take, receive", "kjv": "take, receive, fetch", "occur": 966},

    # COME / GO
    "H935": {"hebrew": "בּוֹא", "translit": "bo", "def": "to come, enter", "kjv": "come, enter, go", "occur": 2577},
    "H1980": {"hebrew": "הָלַךְ", "translit": "halak", "def": "to go, walk", "kjv": "go, walk, come", "occur": 1554},
    "H3318": {"hebrew": "יָצָא", "translit": "yatsa", "def": "to go out, come forth", "kjv": "come, bring, go", "occur": 1069},

    # SEE / BEHOLD
    "H2372": {"hebrew": "חָזָה", "translit": "chazah", "def": "to see, behold (vision)", "kjv": "see, behold, look", "occur": 51},
    "H7200": {"hebrew": "רָאָה", "translit": "raah", "def": "to see, look", "kjv": "see, look, behold", "occur": 1313},

    # SPEAK / SAY
    "H559": {"hebrew": "אָמַר", "translit": "amar", "def": "to say, speak", "kjv": "say, speak, answer", "occur": 5308},
    "H1696": {"hebrew": "דָּבַר", "translit": "dabar", "def": "to speak, declare", "kjv": "speak, say, talk", "occur": 1136},

    # CALL / CRY
    "H2199": {"hebrew": "זָעַק", "translit": "zaaq", "def": "to cry out", "kjv": "cry, assemble, call", "occur": 73},
    "H7121": {"hebrew": "קָרָא", "translit": "qara", "def": "to call, proclaim", "kjv": "call, cry, read", "occur": 735},

    # REMEMBER / FORGET
    "H2142": {"hebrew": "זָכַר", "translit": "zakar", "def": "to remember", "kjv": "remember, mention, record", "occur": 233},
    "H7911": {"hebrew": "שָׁכַח", "translit": "shakach", "def": "to forget", "kjv": "forget, forgotten", "occur": 102},

    # MOUNTAIN / ZION
    "H2022": {"hebrew": "הַר", "translit": "har", "def": "mountain, hill", "kjv": "mountain, mount, hill", "occur": 546},
    "H6726": {"hebrew": "צִיּוֹן", "translit": "Tsiyyon", "def": "Zion", "kjv": "Zion", "occur": 154},

    # JERUSALEM / ISRAEL
    "H3389": {"hebrew": "יְרוּשָׁלַיִם", "translit": "Yerushalayim", "def": "Jerusalem", "kjv": "Jerusalem", "occur": 643},
    "H3478": {"hebrew": "יִשְׂרָאֵל", "translit": "Yisrael", "def": "Israel", "kjv": "Israel", "occur": 2505},

    # DAVID / MESSIAH
    "H1732": {"hebrew": "דָּוִד", "translit": "David", "def": "David (beloved)", "kjv": "David", "occur": 1076},
    "H4899": {"hebrew": "מָשִׁיחַ", "translit": "mashiach", "def": "anointed, messiah", "kjv": "anointed, Messiah", "occur": 39},
}

# =============================================================================
# GREEK STRONG'S (G1 - G5624) - Core NT vocabulary
# =============================================================================

GREEK_STRONGS = {
    # GOD / LORD / CHRIST
    "G2316": {"greek": "θεός", "translit": "theos", "def": "God, deity", "kjv": "God, god, godly", "occur": 1343},
    "G2962": {"greek": "κύριος", "translit": "kyrios", "def": "Lord, master", "kjv": "Lord, master, sir", "occur": 748},
    "G5547": {"greek": "Χριστός", "translit": "Christos", "def": "Christ, anointed", "kjv": "Christ", "occur": 569},
    "G2424": {"greek": "Ἰησοῦς", "translit": "Iesous", "def": "Jesus (Yeshua)", "kjv": "Jesus", "occur": 975},

    # SPIRIT / SOUL / LIFE
    "G4151": {"greek": "πνεῦμα", "translit": "pneuma", "def": "spirit, breath, wind", "kjv": "Spirit, Ghost, spirit", "occur": 385},
    "G5590": {"greek": "ψυχή", "translit": "psuche", "def": "soul, life, self", "kjv": "soul, life, mind", "occur": 105},
    "G2222": {"greek": "ζωή", "translit": "zoe", "def": "life", "kjv": "life", "occur": 134},
    "G166": {"greek": "αἰώνιος", "translit": "aionios", "def": "eternal, everlasting", "kjv": "eternal, everlasting", "occur": 71},

    # WORD / TRUTH
    "G3056": {"greek": "λόγος", "translit": "logos", "def": "word, reason, the Word", "kjv": "word, saying, speech", "occur": 330},
    "G4487": {"greek": "ῥῆμα", "translit": "rhema", "def": "word, saying", "kjv": "word, saying, thing", "occur": 68},
    "G225": {"greek": "ἀλήθεια", "translit": "aletheia", "def": "truth", "kjv": "truth, verity", "occur": 110},
    "G227": {"greek": "ἀληθής", "translit": "alethes", "def": "true", "kjv": "true, truly", "occur": 26},

    # FAITH / BELIEVE
    "G4102": {"greek": "πίστις", "translit": "pistis", "def": "faith, belief, trust", "kjv": "faith, assurance, belief", "occur": 244},
    "G4100": {"greek": "πιστεύω", "translit": "pisteuo", "def": "to believe, trust", "kjv": "believe, commit, trust", "occur": 248},
    "G4103": {"greek": "πιστός", "translit": "pistos", "def": "faithful, believing", "kjv": "faithful, believe, true", "occur": 67},

    # LOVE
    "G26": {"greek": "ἀγάπη", "translit": "agape", "def": "love (divine, unconditional)", "kjv": "love, charity, feast", "occur": 116},
    "G25": {"greek": "ἀγαπάω", "translit": "agapao", "def": "to love", "kjv": "love, beloved", "occur": 143},
    "G5368": {"greek": "φιλέω", "translit": "phileo", "def": "to love (friendship)", "kjv": "love, kiss", "occur": 25},

    # GRACE / MERCY
    "G5485": {"greek": "χάρις", "translit": "charis", "def": "grace, favor, thanks", "kjv": "grace, favour, thanks", "occur": 156},
    "G1656": {"greek": "ἔλεος", "translit": "eleos", "def": "mercy, compassion", "kjv": "mercy", "occur": 27},
    "G3628": {"greek": "οἰκτιρμός", "translit": "oiktirmos", "def": "compassion, mercy", "kjv": "mercy", "occur": 5},

    # SIN / TRANSGRESSION
    "G266": {"greek": "ἁμαρτία", "translit": "hamartia", "def": "sin, missing the mark", "kjv": "sin, sinful, offense", "occur": 174},
    "G264": {"greek": "ἁμαρτάνω", "translit": "hamartano", "def": "to sin", "kjv": "sin, trespass, offend", "occur": 43},
    "G268": {"greek": "ἁμαρτωλός", "translit": "hamartolos", "def": "sinner, sinful", "kjv": "sinner, sinful", "occur": 47},
    "G3900": {"greek": "παράπτωμα", "translit": "paraptoma", "def": "trespass, transgression", "kjv": "trespass, offence, sin", "occur": 23},
    "G458": {"greek": "ἀνομία", "translit": "anomia", "def": "lawlessness, iniquity", "kjv": "iniquity, transgression", "occur": 15},

    # RIGHTEOUSNESS / JUSTIFY
    "G1342": {"greek": "δίκαιος", "translit": "dikaios", "def": "righteous, just", "kjv": "righteous, just, right", "occur": 81},
    "G1343": {"greek": "δικαιοσύνη", "translit": "dikaiosyne", "def": "righteousness, justice", "kjv": "righteousness", "occur": 92},
    "G1344": {"greek": "δικαιόω", "translit": "dikaioo", "def": "to justify, declare righteous", "kjv": "justify, free, righteous", "occur": 40},

    # SALVATION / SAVE
    "G4991": {"greek": "σωτηρία", "translit": "soteria", "def": "salvation, deliverance", "kjv": "salvation, deliver, health", "occur": 46},
    "G4982": {"greek": "σῴζω", "translit": "sozo", "def": "to save, deliver", "kjv": "save, whole, heal", "occur": 110},
    "G4990": {"greek": "σωτήρ", "translit": "soter", "def": "savior, deliverer", "kjv": "Saviour", "occur": 24},
    "G629": {"greek": "ἀπολύτρωσις", "translit": "apolutrosis", "def": "redemption, release", "kjv": "redemption, deliverance", "occur": 10},
    "G3084": {"greek": "λυτρόω", "translit": "lutroo", "def": "to redeem, ransom", "kjv": "redeem", "occur": 3},

    # REPENT / FORGIVE
    "G3340": {"greek": "μετανοέω", "translit": "metanoeo", "def": "to repent, change mind", "kjv": "repent", "occur": 34},
    "G3341": {"greek": "μετάνοια", "translit": "metanoia", "def": "repentance", "kjv": "repentance", "occur": 24},
    "G863": {"greek": "ἀφίημι", "translit": "aphiemi", "def": "to forgive, leave, let", "kjv": "leave, forgive, suffer", "occur": 146},
    "G859": {"greek": "ἄφεσις", "translit": "aphesis", "def": "forgiveness, release", "kjv": "forgiveness, remission", "occur": 17},

    # HOLY / SANCTIFY
    "G40": {"greek": "ἅγιος", "translit": "hagios", "def": "holy, sacred, saint", "kjv": "holy, saint, Holy One", "occur": 233},
    "G37": {"greek": "ἁγιάζω", "translit": "hagiazo", "def": "to sanctify, make holy", "kjv": "sanctify, hallow, holy", "occur": 29},
    "G38": {"greek": "ἁγιασμός", "translit": "hagiasmos", "def": "sanctification, holiness", "kjv": "holiness, sanctification", "occur": 10},

    # BLOOD / CROSS / DEATH
    "G129": {"greek": "αἷμα", "translit": "haima", "def": "blood", "kjv": "blood", "occur": 99},
    "G4716": {"greek": "σταυρός", "translit": "stauros", "def": "cross", "kjv": "cross", "occur": 28},
    "G4717": {"greek": "σταυρόω", "translit": "stauroo", "def": "to crucify", "kjv": "crucify", "occur": 46},
    "G2288": {"greek": "θάνατος", "translit": "thanatos", "def": "death", "kjv": "death, deadly", "occur": 120},
    "G599": {"greek": "ἀποθνῄσκω", "translit": "apothnesko", "def": "to die", "kjv": "die, dead, death", "occur": 112},

    # RESURRECTION / RISE
    "G386": {"greek": "ἀνάστασις", "translit": "anastasis", "def": "resurrection, rising", "kjv": "resurrection, rise", "occur": 42},
    "G450": {"greek": "ἀνίστημι", "translit": "anistemi", "def": "to rise, raise up", "kjv": "rise, arise, stand", "occur": 112},
    "G1453": {"greek": "ἐγείρω", "translit": "egeiro", "def": "to raise, wake", "kjv": "rise, raise, arise", "occur": 141},

    # KINGDOM / REIGN
    "G932": {"greek": "βασιλεία", "translit": "basileia", "def": "kingdom, reign", "kjv": "kingdom", "occur": 162},
    "G935": {"greek": "βασιλεύς", "translit": "basileus", "def": "king", "kjv": "king", "occur": 118},
    "G936": {"greek": "βασιλεύω", "translit": "basileuo", "def": "to reign, be king", "kjv": "reign, king", "occur": 21},

    # HEAVEN / EARTH
    "G3772": {"greek": "οὐρανός", "translit": "ouranos", "def": "heaven, sky", "kjv": "heaven, air, sky", "occur": 284},
    "G1093": {"greek": "γῆ", "translit": "ge", "def": "earth, land, ground", "kjv": "earth, land, ground", "occur": 252},

    # GLORY / HONOR
    "G1391": {"greek": "δόξα", "translit": "doxa", "def": "glory, honor, splendor", "kjv": "glory, honour, praise", "occur": 168},
    "G1392": {"greek": "δοξάζω", "translit": "doxazo", "def": "to glorify, honor", "kjv": "glorify, honour, magnify", "occur": 61},

    # POWER / AUTHORITY
    "G1411": {"greek": "δύναμις", "translit": "dunamis", "def": "power, might, miracle", "kjv": "power, mighty, virtue", "occur": 120},
    "G1849": {"greek": "ἐξουσία", "translit": "exousia", "def": "authority, power", "kjv": "power, authority, right", "occur": 103},
    "G2479": {"greek": "ἰσχύς", "translit": "ischus", "def": "strength, might", "kjv": "strength, power, might", "occur": 10},
    "G2904": {"greek": "κράτος", "translit": "kratos", "def": "strength, dominion", "kjv": "power, dominion, strength", "occur": 12},

    # LIGHT / DARKNESS
    "G5457": {"greek": "φῶς", "translit": "phos", "def": "light", "kjv": "light", "occur": 73},
    "G4655": {"greek": "σκότος", "translit": "skotos", "def": "darkness", "kjv": "darkness", "occur": 31},
    "G4653": {"greek": "σκοτία", "translit": "skotia", "def": "darkness", "kjv": "darkness, dark", "occur": 16},

    # GOOD / EVIL
    "G18": {"greek": "ἀγαθός", "translit": "agathos", "def": "good", "kjv": "good", "occur": 102},
    "G2570": {"greek": "καλός", "translit": "kalos", "def": "good, beautiful", "kjv": "good, better, honest", "occur": 101},
    "G2556": {"greek": "κακός", "translit": "kakos", "def": "bad, evil", "kjv": "evil, bad, harm", "occur": 51},
    "G4190": {"greek": "πονηρός", "translit": "poneros", "def": "evil, wicked", "kjv": "evil, wicked, bad", "occur": 78},

    # FLESH / BODY
    "G4561": {"greek": "σάρξ", "translit": "sarx", "def": "flesh, body", "kjv": "flesh, carnal", "occur": 151},
    "G4983": {"greek": "σῶμα", "translit": "soma", "def": "body", "kjv": "body, slave", "occur": 146},

    # HEART / MIND
    "G2588": {"greek": "καρδία", "translit": "kardia", "def": "heart", "kjv": "heart", "occur": 160},
    "G3563": {"greek": "νοῦς", "translit": "nous", "def": "mind, understanding", "kjv": "mind, understanding", "occur": 24},

    # JOY / PEACE
    "G5479": {"greek": "χαρά", "translit": "chara", "def": "joy, gladness", "kjv": "joy, gladness", "occur": 59},
    "G5463": {"greek": "χαίρω", "translit": "chairo", "def": "to rejoice", "kjv": "rejoice, glad, hail", "occur": 74},
    "G1515": {"greek": "εἰρήνη", "translit": "eirene", "def": "peace", "kjv": "peace, quietness, rest", "occur": 92},

    # HOPE
    "G1680": {"greek": "ἐλπίς", "translit": "elpis", "def": "hope, expectation", "kjv": "hope, faith", "occur": 53},
    "G1679": {"greek": "ἐλπίζω", "translit": "elpizo", "def": "to hope, expect", "kjv": "hope, trust", "occur": 31},

    # CALL / NAME
    "G2564": {"greek": "καλέω", "translit": "kaleo", "def": "to call", "kjv": "call, bid, name", "occur": 148},
    "G3686": {"greek": "ὄνομα", "translit": "onoma", "def": "name", "kjv": "name", "occur": 231},

    # PRAY / WORSHIP
    "G4336": {"greek": "προσεύχομαι", "translit": "proseuchomai", "def": "to pray", "kjv": "pray, make prayer", "occur": 87},
    "G4335": {"greek": "προσευχή", "translit": "proseuche", "def": "prayer", "kjv": "prayer", "occur": 37},
    "G4352": {"greek": "προσκυνέω", "translit": "proskuneo", "def": "to worship", "kjv": "worship", "occur": 60},

    # ANGEL / DEMON
    "G32": {"greek": "ἄγγελος", "translit": "aggelos", "def": "angel, messenger", "kjv": "angel, messenger", "occur": 186},
    "G1140": {"greek": "δαιμόνιον", "translit": "daimonion", "def": "demon, evil spirit", "kjv": "devil, demon", "occur": 63},
    "G4567": {"greek": "Σατανᾶς", "translit": "Satanas", "def": "Satan, adversary", "kjv": "Satan", "occur": 36},
    "G1228": {"greek": "διάβολος", "translit": "diabolos", "def": "devil, slanderer", "kjv": "devil, false accuser", "occur": 38},

    # WORLD / AGE
    "G2889": {"greek": "κόσμος", "translit": "kosmos", "def": "world, order", "kjv": "world", "occur": 187},
    "G165": {"greek": "αἰών", "translit": "aion", "def": "age, eternity", "kjv": "ever, world, age", "occur": 128},

    # JUDGMENT / CONDEMNATION
    "G2917": {"greek": "κρίμα", "translit": "krima", "def": "judgment, verdict", "kjv": "judgment, damnation", "occur": 28},
    "G2920": {"greek": "κρίσις", "translit": "krisis", "def": "judgment, decision", "kjv": "judgment, damnation", "occur": 48},
    "G2919": {"greek": "κρίνω", "translit": "krino", "def": "to judge, decide", "kjv": "judge, determine, condemn", "occur": 114},
    "G2631": {"greek": "κατάκριμα", "translit": "katakrima", "def": "condemnation", "kjv": "condemnation", "occur": 3},

    # CHURCH / ASSEMBLY
    "G1577": {"greek": "ἐκκλησία", "translit": "ekklesia", "def": "church, assembly", "kjv": "church, assembly", "occur": 118},

    # APOSTLE / DISCIPLE
    "G652": {"greek": "ἀπόστολος", "translit": "apostolos", "def": "apostle, messenger", "kjv": "apostle, messenger", "occur": 81},
    "G3101": {"greek": "μαθητής", "translit": "mathetes", "def": "disciple, learner", "kjv": "disciple", "occur": 269},

    # BAPTIZE / BAPTISM
    "G907": {"greek": "βαπτίζω", "translit": "baptizo", "def": "to baptize, immerse", "kjv": "baptize, wash", "occur": 77},
    "G908": {"greek": "βάπτισμα", "translit": "baptisma", "def": "baptism", "kjv": "baptism", "occur": 22},

    # BREAD / CUP (Communion)
    "G740": {"greek": "ἄρτος", "translit": "artos", "def": "bread, loaf", "kjv": "bread, loaf", "occur": 99},
    "G4221": {"greek": "ποτήριον", "translit": "poterion", "def": "cup", "kjv": "cup", "occur": 33},

    # FATHER / SON
    "G3962": {"greek": "πατήρ", "translit": "pater", "def": "father", "kjv": "Father, father", "occur": 419},
    "G5207": {"greek": "υἱός", "translit": "huios", "def": "son", "kjv": "son, child", "occur": 382},

    # MAN / WOMAN
    "G444": {"greek": "ἄνθρωπος", "translit": "anthropos", "def": "man, human", "kjv": "man, men", "occur": 560},
    "G435": {"greek": "ἀνήρ", "translit": "aner", "def": "man, husband", "kjv": "man, husband", "occur": 216},
    "G1135": {"greek": "γυνή", "translit": "gune", "def": "woman, wife", "kjv": "woman, wife", "occur": 221},

    # KNOW / KNOWLEDGE
    "G1097": {"greek": "γινώσκω", "translit": "ginosko", "def": "to know", "kjv": "know, perceive, understand", "occur": 223},
    "G1108": {"greek": "γνῶσις", "translit": "gnosis", "def": "knowledge", "kjv": "knowledge, science", "occur": 29},
    "G1492": {"greek": "εἴδω", "translit": "eido", "def": "to know, see", "kjv": "know, see, perceive", "occur": 666},

    # HEAR / OBEY
    "G191": {"greek": "ἀκούω", "translit": "akouo", "def": "to hear", "kjv": "hear, hearken, understand", "occur": 437},
    "G5219": {"greek": "ὑπακούω", "translit": "hupakouo", "def": "to obey, listen", "kjv": "obey, hearken", "occur": 21},
    "G5218": {"greek": "ὑπακοή", "translit": "hupakoe", "def": "obedience", "kjv": "obedience, obedient", "occur": 15},

    # SPEAK / PREACH
    "G2980": {"greek": "λαλέω", "translit": "laleo", "def": "to speak, say", "kjv": "speak, say, tell", "occur": 296},
    "G3004": {"greek": "λέγω", "translit": "lego", "def": "to say, speak", "kjv": "say, speak, tell", "occur": 1343},
    "G2784": {"greek": "κηρύσσω", "translit": "kerusso", "def": "to preach, proclaim", "kjv": "preach, publish", "occur": 61},
    "G2097": {"greek": "εὐαγγελίζω", "translit": "euaggelizo", "def": "to preach gospel", "kjv": "preach, bring good tidings", "occur": 55},
    "G2098": {"greek": "εὐαγγέλιον", "translit": "euaggelion", "def": "gospel, good news", "kjv": "gospel", "occur": 77},

    # COME / GO
    "G2064": {"greek": "ἔρχομαι", "translit": "erchomai", "def": "to come, go", "kjv": "come, go, fall", "occur": 637},
    "G4198": {"greek": "πορεύομαι", "translit": "poreuomai", "def": "to go, travel", "kjv": "go, depart, walk", "occur": 154},
    "G565": {"greek": "ἀπέρχομαι", "translit": "aperchomai", "def": "to go away, depart", "kjv": "go, go away, depart", "occur": 120},

    # SEND
    "G649": {"greek": "ἀποστέλλω", "translit": "apostello", "def": "to send forth", "kjv": "send, send forth", "occur": 133},
    "G3992": {"greek": "πέμπω", "translit": "pempo", "def": "to send", "kjv": "send", "occur": 81},

    # SEE / BEHOLD
    "G991": {"greek": "βλέπω", "translit": "blepo", "def": "to see, look", "kjv": "see, behold, look", "occur": 133},
    "G3708": {"greek": "ὁράω", "translit": "horao", "def": "to see, perceive", "kjv": "see, appear, look", "occur": 454},
    "G2334": {"greek": "θεωρέω", "translit": "theoreo", "def": "to behold, observe", "kjv": "see, behold, perceive", "occur": 58},

    # GIVE / RECEIVE
    "G1325": {"greek": "δίδωμι", "translit": "didomi", "def": "to give", "kjv": "give, grant, offer", "occur": 416},
    "G2983": {"greek": "λαμβάνω", "translit": "lambano", "def": "to take, receive", "kjv": "receive, take, have", "occur": 263},

    # WORK / DO
    "G2038": {"greek": "ἐργάζομαι", "translit": "ergazomai", "def": "to work, labor", "kjv": "work, labour, do", "occur": 41},
    "G2041": {"greek": "ἔργον", "translit": "ergon", "def": "work, deed", "kjv": "work, deed, labour", "occur": 176},
    "G4160": {"greek": "ποιέω", "translit": "poieo", "def": "to do, make", "kjv": "do, make, bring forth", "occur": 576},

    # WALK / LIVE
    "G4043": {"greek": "περιπατέω", "translit": "peripateo", "def": "to walk", "kjv": "walk, go, be occupied", "occur": 96},
    "G2198": {"greek": "ζάω", "translit": "zao", "def": "to live", "kjv": "live, alive, life", "occur": 143},

    # SERVANT / SERVE
    "G1401": {"greek": "δοῦλος", "translit": "doulos", "def": "slave, servant", "kjv": "servant, bondman, slave", "occur": 127},
    "G1398": {"greek": "δουλεύω", "translit": "douleuo", "def": "to serve, be slave", "kjv": "serve, be in bondage", "occur": 25},
    "G1249": {"greek": "διάκονος", "translit": "diakonos", "def": "servant, minister", "kjv": "minister, servant, deacon", "occur": 30},
    "G1248": {"greek": "διακονία", "translit": "diakonia", "def": "service, ministry", "kjv": "ministry, service", "occur": 34},

    # TEACH / LEARN
    "G1321": {"greek": "διδάσκω", "translit": "didasko", "def": "to teach", "kjv": "teach", "occur": 97},
    "G1320": {"greek": "διδάσκαλος", "translit": "didaskalos", "def": "teacher", "kjv": "Master, teacher", "occur": 58},
    "G1322": {"greek": "διδαχή", "translit": "didache", "def": "teaching, doctrine", "kjv": "doctrine, teaching", "occur": 30},
    "G3129": {"greek": "μανθάνω", "translit": "manthano", "def": "to learn", "kjv": "learn, understand", "occur": 25},

    # LAW / COMMANDMENT
    "G3551": {"greek": "νόμος", "translit": "nomos", "def": "law", "kjv": "law", "occur": 197},
    "G1785": {"greek": "ἐντολή", "translit": "entole", "def": "commandment", "kjv": "commandment, precept", "occur": 68},

    # PROMISE / COVENANT
    "G1860": {"greek": "ἐπαγγελία", "translit": "epaggelia", "def": "promise", "kjv": "promise", "occur": 53},
    "G1242": {"greek": "διαθήκη", "translit": "diatheke", "def": "covenant, testament", "kjv": "covenant, testament", "occur": 33},

    # WILL / DESIRE
    "G2307": {"greek": "θέλημα", "translit": "thelema", "def": "will, desire", "kjv": "will, desire", "occur": 64},
    "G2309": {"greek": "θέλω", "translit": "thelo", "def": "to will, desire", "kjv": "will, desire, wish", "occur": 210},
    "G1014": {"greek": "βούλομαι", "translit": "boulomai", "def": "to will, intend", "kjv": "will, would, be minded", "occur": 37},

    # TIME / DAY
    "G2540": {"greek": "καιρός", "translit": "kairos", "def": "time, season, opportunity", "kjv": "time, season", "occur": 86},
    "G5550": {"greek": "χρόνος", "translit": "chronos", "def": "time, period", "kjv": "time, season, while", "occur": 54},
    "G2250": {"greek": "ἡμέρα", "translit": "hemera", "def": "day", "kjv": "day, time", "occur": 389},

    # FEAR
    "G5401": {"greek": "φόβος", "translit": "phobos", "def": "fear, terror, reverence", "kjv": "fear", "occur": 47},
    "G5399": {"greek": "φοβέω", "translit": "phobeo", "def": "to fear, revere", "kjv": "fear, afraid, reverence", "occur": 95},
}


def build_strongs_database():
    """Build and save comprehensive Strong's database"""
    print("="*60)
    print("BUILDING STRONG'S CONCORDANCE DATABASE")
    print("="*60)

    combined = {}

    # Add Hebrew
    print(f"\nAdding {len(HEBREW_STRONGS)} Hebrew entries...")
    for key, value in HEBREW_STRONGS.items():
        combined[key] = value

    # Add Greek
    print(f"Adding {len(GREEK_STRONGS)} Greek entries...")
    for key, value in GREEK_STRONGS.items():
        combined[key] = value

    # Save
    strongs_path = DATA_DIR / "strongs.json"
    with open(strongs_path, 'w', encoding='utf-8') as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)

    print(f"\nSaved to: {strongs_path}")
    print(f"Total entries: {len(combined)}")
    print(f"  Hebrew (H): {len(HEBREW_STRONGS)}")
    print(f"  Greek (G): {len(GREEK_STRONGS)}")

    # Stats
    hebrew_occur = sum(v.get('occur', 0) for v in HEBREW_STRONGS.values())
    greek_occur = sum(v.get('occur', 0) for v in GREEK_STRONGS.values())
    print(f"\nCoverage:")
    print(f"  Hebrew occurrences: ~{hebrew_occur:,}")
    print(f"  Greek occurrences: ~{greek_occur:,}")

    return combined


if __name__ == "__main__":
    build_strongs_database()
