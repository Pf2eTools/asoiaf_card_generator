from PIL import Image

class AssetManager:
    ASSETS_DIR = "./assets"

    @staticmethod
    def get_bg(faction):
        return Image.open(f"{AssetManager.ASSETS_DIR}/Tactics/Bg_{faction}.jpg").convert('RGBA')

    @staticmethod
    def get_tactics_bg():
        return Image.open(f"{AssetManager.ASSETS_DIR}/Tactics/Bg2.jpg").convert('RGBA')

    @staticmethod
    def get_bars(faction):
        large_bar = Image.open(f"{AssetManager.ASSETS_DIR}/Units/LargeBar{faction}.webp").convert('RGBA')
        small_bar = Image.open(f"{AssetManager.ASSETS_DIR}/Attachments/Bar{faction}.webp").convert('RGBA')
        weird_bar = Image.open(f"{AssetManager.ASSETS_DIR}/Units/Corner{faction}.webp").convert('RGBA')

        return large_bar, small_bar, weird_bar

    @staticmethod
    def get_decor(faction):
        return Image.open(f"{AssetManager.ASSETS_DIR}/Tactics/Decor{faction}.webp").convert('RGBA')

    @staticmethod
    def get_crest(faction):
        return Image.open(f"{AssetManager.ASSETS_DIR}/Units/Crest{faction}.webp").convert('RGBA')

    @staticmethod
    def get_crest_tactics(faction):
        return Image.open(f"{AssetManager.ASSETS_DIR}/Tactics/Crest{faction}.webp").convert('RGBA')

    @staticmethod
    def get_unit_bg(faction):
        return Image.open(f"{AssetManager.ASSETS_DIR}/Units/UnitBg{faction}.jpg").convert("RGBA")

    @staticmethod
    def get_unit_skills_bg():
        return Image.open(f"{AssetManager.ASSETS_DIR}/Units/SkillsBg.webp").convert("RGBA")

    @staticmethod
    def get_unit_image(unit_id):
        return Image.open(f"{AssetManager.ASSETS_DIR}/Units/{unit_id}.jpg").convert("RGBA")

    @staticmethod
    def get_unit_type(unit_type, faction):
        return Image.open(f"{AssetManager.ASSETS_DIR}/Units/UnitType.{unit_type}{faction}.webp").convert("RGBA")

    @staticmethod
    def get_stat_background():
        return Image.open(f"{AssetManager.ASSETS_DIR}/Units/StatBg.webp").convert('RGBA')

    @staticmethod
    def get_stat_icon(name):
        if name == "speed":
            return Image.open(f"{AssetManager.ASSETS_DIR}/Units/Movement.webp").convert('RGBA')
        elif name == "defense":
            return Image.open(f"{AssetManager.ASSETS_DIR}/Units/Defense.webp").convert('RGBA')
        elif name == "morale":
            return Image.open(f"{AssetManager.ASSETS_DIR}/Units/Morale.webp").convert('RGBA')
        raise Exception(f'Tried to get the icon for statistic: "{name}"')

    @staticmethod
    def get_attack_bg(highlight_color):
        return Image.open(f"{AssetManager.ASSETS_DIR}/Units/AttackBg{highlight_color}.webp").convert('RGBA')

    @staticmethod
    def get_attack_dice_bg():
        return Image.open(f"{AssetManager.ASSETS_DIR}/Units/DiceBg.webp").convert('RGBA')

    @staticmethod
    def get_attack_type_bg(highlight_color):
        return Image.open(f"{AssetManager.ASSETS_DIR}/Units/AttackTypeBg{highlight_color}.webp").convert('RGBA')

    @staticmethod
    def get_attack_type(attack_type, color):
        atk_type = 'Melee' if attack_type == 'melee' else 'Ranged'
        return Image.open(f"{AssetManager.ASSETS_DIR}/Units/AttackType.{atk_type}{color}.webp").convert('RGBA')

    @staticmethod
    def get_attack_range_icon(attack_type, highlight_color):
        atk_type = attack_type.capitalize()
        return Image.open(f"{AssetManager.ASSETS_DIR}/graphics/Range{atk_type}{highlight_color}.png").convert("RGBA")

    @staticmethod
    def get_skill_icon(name, color):
        return Image.open(f"{AssetManager.ASSETS_DIR}/Units/Skill{name.capitalize()}{color}.webp").convert('RGBA')

    @staticmethod
    def get_skill_divider(faction):
        return Image.open(f"{AssetManager.ASSETS_DIR}/Units/Divider{faction}.webp").convert("RGBA")

    @staticmethod
    def get_skill_bottom(faction):
        return Image.open(f"{AssetManager.ASSETS_DIR}/Units/SkillBottom{faction}.webp").convert("RGBA")

    @staticmethod
    def get_tactics_commmander_img(commander_id):
        return Image.open(f"{AssetManager.ASSETS_DIR}/Tactics/{commander_id}.jpg").convert('RGBA')

    @staticmethod
    def get_text_icon(icon):
        return Image.open(f"{AssetManager.ASSETS_DIR}/graphics/{icon}.png").convert("RGBA")