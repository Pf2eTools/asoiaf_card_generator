import csv
import json
import re
from generate_tactics import generate_tactics
from generate_units import generate_unit
from generate_ncus import generate_ncu
from generate_attachments import generate_attachment


def csv_to_dict(path):
    with open(path, "r", encoding="utf-8") as csv_file:
        line = csv_file.readline()
        headers = [h if h else str(ix) for ix, h in enumerate(line.strip().split(","))]
        csv_reader = csv.DictReader(csv_file, fieldnames=headers)
        data = [dict(row) for row in csv_reader if len([v for v in dict(row).values() if v]) > 0]
    return data


# def parse_ability_trigger(paragraphs):
#     if len(paragraphs) > 1:
#         return {
#             "trigger": paragraphs[0],
#             "effect": paragraphs[1:],
#         }
#     else:
#         ix_end_bold = [i for i, v in enumerate(paragraphs[0]) if v.endswith("**")][0]
#         return {
#             "trigger": paragraphs[0][:ix_end_bold + 1],
#             "effect": paragraphs[0][ix_end_bold + 1:],
#         }


# def parse_ability_text(text):
#     def parse_para(para, split_func=None):
#         para = para.strip()
#         if split_func is not None:
#             return split_func(para)
#         else:
#             return [line.strip() for line in para.split("\n")]
#
#     split_by_double = re.split(r"\n\s*?\n", text.strip())
#     split_by_single = re.split(r"\n+\s*", text.strip())
#     # FIXME/TODO: This heuristic is terrible!
#     if max([max([len(l) for l in p.split("\n")]) for p in split_by_double]) > 50:
#         max_line_len = 38 if len(text) / 32 < 16 else 41
#         split_function = lambda x: split_paragraph(x, max_line_len)
#         paragraphs = [parse_para(p, split_function) for p in split_by_single if p]
#     else:
#         paragraphs = [parse_para(p) for p in split_by_double if p]
#
#     return paragraphs


def split_paragraph(paragraph_text, max_len=None, ignore_hurenkind=False):
    max_len = max_len or 38
    # Split on space or hyphen, but not a hyphen before a space
    words = [w for w in re.split(r"([^\s-]+-)(?!\s)|\s", paragraph_text.strip()) if w]
    lines = []
    line = []
    for word in words:
        len_2 = lambda x: 2 if x.startswith("[") else len(x.replace("*", ""))
        len_line = sum([len_2(w) + 1 for w in line]) + len_2(word)
        if len_line > max_len and not line:
            line = [word]
            lines.append(line)
            line = []
        elif line and (len_line > max_len or word.startswith("•")):
            lines.append(line)
            line = [word]
        else:
            line.append(word)
    if line:
        lines.append(line)

    if not ignore_hurenkind and len(lines) > 1 and len(lines[-1]) == 1 and len(lines[-2]) > 1:
        word = lines[-2].pop()
        lines[-1].insert(0, word)

    def join(l):
        out = ""
        for w in l:
            if out == "" or out.endswith("-"):
                out += w
            else:
                out += f" {w}"
        return out

    return [join(l) for l in lines]


def parse_tactics_text(text_trigger_effect):
    single_split = [re.sub(r"\s", " ", s.strip()) for s in text_trigger_effect.split("\n") if s.strip()]
    double_split = [re.sub(r"\s", " ", s.strip()) for s in text_trigger_effect.split("\n\n")]
    out = {
        "trigger": "",
        "effect": []
    }
    if len([ln for ln in single_split if len(ln) > 50]) < 2:
        if double_split[0].endswith("**"):
            out["trigger"] = double_split[0].strip("*")
            out["effect"] = double_split[1:]
        elif single_split[0].endswith("**"):
            out["trigger"] = single_split[0].strip("*")
            out["effect"] = single_split[1:]
        else:
            raise Exception("Problem?")
    else:
        if single_split[0].endswith("**"):
            out["trigger"] = single_split[0].strip("*")
            out["effect"] = single_split[1:]
        else:
            ix_end_bold = [i for i, v in enumerate(single_split) if v.endswith("**")][0]
            out["trigger"] = " ".join(single_split[:ix_end_bold + 1]).strip("*")
            out["effect"] = single_split[ix_end_bold + 1:]

    if len(out["effect"]) == 0:
        del out["effect"]
        out["remove"] = out["trigger"]
        del out["trigger"]

    return out


def parse_tactics():
    translations = [
        "de",
    ]
    data = csv_to_dict(f"{CSV_PATH}/tactics.csv")
    parsed_cards = {
        "en": {}
    }
    for card_data in data:
        id = card_data.get("Id")
        parsed = {
            "id": id,
            "name": card_data.get("Name").replace("\n", " ").strip(),
            "version": card_data.get("Version"),
            "faction": card_data.get("Faction"),
            "text": [parse_tactics_text(p) for p in card_data.get("Text").replace("./", ". /").split(" /")],
        }
        if card_data.get("Remove") != "":
            parsed["remove"] = card_data.get("Remove")
        if card_data.get("Unit") != "":
            parsed["commander_id"] = card_data.get("Unit")
            parsed["commander_name"] = card_data.get("Deck").split(", ")[0].strip()
            parsed["commander_subname"] = card_data.get("Deck").split(", ")[1].strip()
        parsed_cards["en"][id] = parsed
    for lang in translations:
        translated_data = csv_to_dict(f"{CSV_PATH}/tactics.{lang}.csv")
        parsed_cards[lang] = {}
        for card_data in translated_data:
            id = card_data.get("Id")
            parsing = parsed_cards["en"][id].copy()
            parsing["name"] = card_data.get("Name").replace("\n", " ").strip()
            parsing["text"] = [parse_tactics_text(p) for p in card_data.get("Text").replace("./", ". /").split(" /")]
            if not re.search(r"deck", card_data.get("Deck")):
                cmdr_name_split = card_data.get("Deck").split(", ")
                parsing["commander_name"] = cmdr_name_split[0].strip()
                if len(cmdr_name_split) == 2:
                    parsing["commander_subname"] = cmdr_name_split[1].strip()
                else:
                    del parsing["commander_subname"]
            parsed_cards[lang][id] = parsing
    return parsed_cards


def parse_abilities():
    data = csv_to_dict(f"{CSV_PATH}/newskills.csv")
    parsed_abilities = {
        "en": {}
    }
    icons_to_long = {
        "M": "melee",
        "Melee": "melee",
        "R": "ranged",
        "W": "wounds",
        "F": "faith",
        "Fire": "fire",
        "P": "pillage",
        "V": "venom",
    }
    for ability_data in data:
        name = ability_data.get("Name")
        description = ability_data.get("Description")
        if name.startswith("Order:"):
            parts = [p for p in re.split(r"(\*\*.*?\*\*)", description) if p]
            parsed = {
                "trigger": parts[0].strip("*"),
                "effect": ["".join(parts[1:]).strip()],
            }
        else:
            parsed = {
                "effect": [description]
            }
        if name.startswith("Order:"):
            parsed["icons"] = ["order"]
        if ability_data.get("Icons") != "":
            parsed["icons"] = parsed.get("icons") or []
            for icon in ability_data.get("Icons").split(","):
                parsed_icon = icons_to_long.get(icon)
                if parsed_icon is None:
                    print(f"Nice icon: {icon}, {name}")
                    parsed_icon = icon
                parsed["icons"].append(parsed_icon)
        parsed_abilities["en"][name.upper()] = parsed

    return parsed_abilities


def parse_units():
    data = csv_to_dict(f"{CSV_PATH}/units.csv")
    parsed_cards = {
        "en": {}
    }

    def parse_attack(name_type, hit, dice):
        t, name = name_type.split("]")
        return {
            "name": name,
            "type": "melee" if t == "[M" else "short" if t == "[RS" else "long",
            "hit": int(hit.strip("+")),
            "dice": [int(d) for d in dice.split(".")],
        }

    for card_data in data:
        card_id = card_data.get("Id")
        parsed = {
            "id": card_id,
            "name": card_data.get("Name"),
            "version": card_data.get("Version"),
            "faction": card_data.get("Faction"),
            "type": card_data.get("Type").replace(" ", ""),
            "cost": "C" if card_data.get("Cost") == "C" else int(card_data.get("Cost")),
            "speed": int(card_data.get("Spd")),
            "defense": int(card_data.get("Def").strip("+")),
            "morale": int(card_data.get("Moral").strip("+")),
            "attacks": [],
            "abilities": [a.strip() for a in re.split(r"\s/|/\s", card_data.get("Abilities"))],
        }
        parsed["attacks"].append(parse_attack(card_data.get("Attack 1"), card_data.get("7"), card_data.get("8")))
        if card_data.get("Attack 2") != "":
            parsed["attacks"].append(parse_attack(card_data.get("Attack 2"), card_data.get("10"), card_data.get("11")))

        parsed_cards["en"][card_id] = parsed

    return parsed_cards


def parse_ncus():
    data = csv_to_dict(f"{CSV_PATH}/ncus.csv")
    parsed_cards = {
        "en": {}
    }

    for card_data in data:
        card_id = card_data.get("Id")
        name_parts = card_data.get("Name").split(", ")
        parsed = {
            "id": card_id,
            "name": name_parts[0].strip(),
            "version": card_data.get("Version"),
            "faction": card_data.get("Faction"),
            "abilities": [],
        }
        if len(name_parts) > 1:
            parsed["subname"] = name_parts[1]
        ability_names = [n.strip() for n in re.split(r"\s/|/\s", card_data.get("Names"))]
        ability_text = [n.strip() for n in re.split(r"\s/|/\s", card_data.get("Descriptions"))]
        for name, text in zip(ability_names, ability_text):
            ability = {
                "name": name,
                "effect": [t.strip() for t in text.split("\n\n") if t.strip()]
            }
            parsed["abilities"].append(ability)
        parsed_cards["en"][card_id] = parsed

    return parsed_cards


def parse_attachments():
    data = csv_to_dict(f"{CSV_PATH}/attachments.csv")
    parsed_cards = {
        "en": {}
    }

    for card_data in data:
        card_id = card_data.get("Id")
        name_parts = card_data.get("Name").split(", ")

        parsed = {
            "id": card_id,
            "name": name_parts[0].strip(),
            "version": card_data.get("Version"),
            "faction": card_data.get("Faction"),
            "type": card_data.get("Type").replace(" ", ""),
            "cost": "C" if card_data.get("Cost") == "C" else int(card_data.get("Cost")),
            "abilities": [a.strip() for a in re.split(r"\s/|/\s", card_data.get("Abilities"))],
        }
        if len(name_parts) > 1:
            parsed["subname"] = name_parts[1]
        if parsed["cost"] == "C":
            parsed["commander"] = True

        parsed_cards["en"][card_id] = parsed

    return parsed_cards


# def main():
#     parsed = parse_attachments()
#     abilities = parse_abilities()
#     delete = [k for k in abilities["en"].keys() if k.startswith("LOYALTY:")]
#     for k in delete:
#         del abilities["en"][k]
#     for lang, data in parsed.items():
#         for ix, u in enumerate(data.values()):
#             if ix != 129:
#                 pass
#             try:
#                 gen = generate_attachment(u, abilities[lang]).convert("RGB")
#                 outpath = f"./generated/{lang}/attachments/{u['id']}.jpg"
#                 print(f"Saving \"{u['name']}\" (ix: {ix}) to {outpath}...")
#                 gen.save(outpath)
#             except FileNotFoundError:
#                 pass

# def main():
#     units = parse_units()
#     abilities = parse_abilities()
#     delete = [k for k in abilities["en"].keys() if k.startswith("LOYALTY:")]
#     for k in delete:
#         del abilities["en"][k]
#     for lang, data in units.items():
#         for ix, u in enumerate(data.values()):
#             if ix != 116:
#                 pass
#             gen = generate_unit(u, abilities[lang]).convert("RGB")
#             outpath = f"./generated/{lang}/units/{u['id']}.jpg"
#             print(f"Saving \"{u['name']}\" (ix: {ix}) to {outpath}...")
#             gen.save(outpath)


# def main():
#     # In the future, dump this info as JSON (It's useful for TTS).
#     tactics = parse_tactics()
#     for lang, data in tactics.items():
#         if lang == "en":
#             pass
#         for ix, t in enumerate(data.values()):
#             if ix != 220:
#                 pass
#             gen = generate_tactics(t).convert("RGB")
#             outpath = f"./generated/{lang}/tactics/{t['id']}.jpg"
#             print(f"Saving \"{t['name']}\" (ix: {ix}) to {outpath}...")
#             gen.save(outpath)


def main():
    ncus = parse_ncus()
    for lang, data in ncus.items():
        if lang == "en":
            pass
        for ix, ncu in enumerate(data.values()):
            if ix != 16:
                pass
            gen = generate_ncu(ncu).convert("RGB")
            outpath = f"./generated/{lang}/ncus/{ncu['id']}.jpg"
            print(f"Saving \"{ncu['name']}\" (ix: {ix}) to {outpath}...")
            gen.save(outpath)


CSV_PATH = "./data/warcouncil"

if __name__ == "__main__":
    main()
