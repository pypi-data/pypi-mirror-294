from typing import Any

from requests.exceptions import ConnectionError
from requests import Response
from json.decoder import JSONDecodeError
from bc_pulse.cli import color

from bc_pulse.core import (
    country_code,
    crypto,
    game,
    game_version,
    io,
    locale_handler,
    log,
    server,
    theme_handler,
    max_value_helper,
)
from bc_pulse.core.country_code import CountryCode, CountryCodeType
from bc_pulse.core.crypto import Hash, HashAlgorithm, Hmac, NyankoSignature, Random
from bc_pulse.core.game.battle.battle_items import BattleItems
from bc_pulse.core.game.battle.cleared_slots import ClearedSlots
from bc_pulse.core.game.battle.slots import LineUps
from bc_pulse.core.game.battle.enemy import Enemy, EnemyNames
from bc_pulse.core.game.catbase.beacon_base import BeaconEventListScene
from bc_pulse.core.game.catbase.cat import Cat, Cats, UnitBuy, TalentData
from bc_pulse.core.game.catbase.gatya import Gatya, GatyaInfos, GatyaDataSet
from bc_pulse.core.game.catbase.gatya_item import GatyaItemBuy, GatyaItemNames
from bc_pulse.core.game.catbase.item_pack import (
    ItemPack,
    Purchases,
    PurchaseSet,
    PurchasedPack,
)
from bc_pulse.core.game.catbase.login_bonuses import LoginBonus
from bc_pulse.core.game.catbase.matatabi import Matatabi
from bc_pulse.core.game.catbase.drop_chara import CharaDrop
from bc_pulse.core.game.catbase.medals import Medals, MedalNames
from bc_pulse.core.game.catbase.mission import Missions, MissionNames, MissionConditions
from bc_pulse.core.game.catbase.my_sale import MySale
from bc_pulse.core.game.catbase.nyanko_club import NyankoClub
from bc_pulse.core.game.catbase.officer_pass import OfficerPass
from bc_pulse.core.game.catbase.powerup import PowerUpHelper
from bc_pulse.core.game.catbase.scheme_items import SchemeItems
from bc_pulse.core.game.catbase.special_skill import (
    SpecialSkills,
    SpecialSkill,
    AbilityData,
    AbilityDataItem,
)
from bc_pulse.core.game.catbase.stamp import StampData
from bc_pulse.core.game.catbase.talent_orbs import (
    TalentOrb,
    TalentOrbs,
    OrbInfo,
    OrbInfoList,
    RawOrbInfo,
    SaveOrb,
    SaveOrbs,
)
from bc_pulse.core.game.catbase.unlock_popups import UnlockPopups
from bc_pulse.core.game.catbase.upgrade import Upgrade
from bc_pulse.core.game.catbase.user_rank_rewards import (
    UserRankRewards,
    RankGifts,
    RankGiftDescriptions,
)
from bc_pulse.core.game.catbase.playtime import PlayTime
from bc_pulse.core.game.gamoto.base_materials import BaseMaterials
from bc_pulse.core.game.gamoto.cat_shrine import CatShrine, CatShrineLevels
from bc_pulse.core.game.gamoto.gamatoto import (
    Gamatoto,
    GamatotoLevels,
    GamatotoMembersName,
)
from bc_pulse.core.game.gamoto.ototo import Ototo
from bc_pulse.core.game.localizable import Localizable
from bc_pulse.core.game.map.aku import AkuChapters
from bc_pulse.core.game.map.challenge import ChallengeChapters
from bc_pulse.core.game.map.chapters import Chapters
from bc_pulse.core.game.map.dojo import Dojo
from bc_pulse.core.game.map.enigma import Enigma
from bc_pulse.core.game.map.event import EventChapters
from bc_pulse.core.game.map.ex_stage import ExChapters
from bc_pulse.core.game.map.gauntlets import GauntletChapters
from bc_pulse.core.game.map.item_reward_stage import ItemRewardChapters
from bc_pulse.core.game.map.legend_quest import LegendQuestChapters
from bc_pulse.core.game.map.map_reset import MapResets
from bc_pulse.core.game.map.outbreaks import Outbreaks
from bc_pulse.core.game.map.story import StoryChapters, TreasureText, StageNames
from bc_pulse.core.game.map.timed_score import TimedScoreChapters
from bc_pulse.core.game.map.tower import TowerChapters
from bc_pulse.core.game.map.uncanny import UncannyChapters
from bc_pulse.core.game.map.zero_legends import ZeroLegendsChapters
from bc_pulse.core.game.map.map_names import MapNames
from bc_pulse.core.game_version import GameVersion
from bc_pulse.core.io.adb_handler import AdbHandler, AdbNotInstalled
from bc_pulse.core.io.bc_csv import CSV, Delimeter, Row
from bc_pulse.core.io.command import Command, CommandResult
from bc_pulse.core.io.config import Config, ConfigKey
from bc_pulse.core.io.data import Data
from bc_pulse.core.io.json_file import JsonFile
from bc_pulse.core.io.path import Path
from bc_pulse.core.io.save import SaveError, SaveFile, CantDetectSaveCCError
from bc_pulse.core.io.thread_helper import thread_run_many, Thread
from bc_pulse.core.io.yaml import YamlFile
from bc_pulse.core.io.git_handler import GitHandler, Repo
from bc_pulse.core.io.root_handler import RootHandler
from bc_pulse.core.locale_handler import (
    LocalManager,
    ExternalLocaleManager,
    ExternalLocale,
)
from bc_pulse.core.log import Logger
from bc_pulse.core.server.client_info import ClientInfo
from bc_pulse.core.server.game_data_getter import GameDataGetter
from bc_pulse.core.server.headers import AccountHeaders
from bc_pulse.core.server.managed_item import BackupMetaData, ManagedItem, ManagedItemType
from bc_pulse.core.server.request import RequestHandler
from bc_pulse.core.server.server_handler import ServerHandler
from bc_pulse.core.server.updater import Updater
from bc_pulse.core.theme_handler import ThemeHandler, ExternalTheme, ExternalThemeManager
from bc_pulse.core.max_value_helper import MaxValueHelper


class CoreData:
    def init_data(self):
        self.config = Config()
        self.logger = Logger()
        self.local_manager = LocalManager()
        self.theme_manager = ThemeHandler()
        self.max_value_manager = MaxValueHelper()
        self.game_data_getter: GameDataGetter | None = None
        self.gatya_item_names: GatyaItemNames | None = None
        self.gatya_item_buy: GatyaItemBuy | None = None
        self.chara_drop: CharaDrop | None = None
        self.gamatoto_levels: GamatotoLevels | None = None
        self.gamatoto_members_name: GamatotoMembersName | None = None
        self.localizable: Localizable | None = None
        self.abilty_data: AbilityData | None = None
        self.enemy_names: EnemyNames | None = None
        self.rank_gift_descriptions: RankGiftDescriptions | None = None
        self.rank_gifts: RankGifts | None = None
        self.treasure_text: TreasureText | None = None
        self.cat_shrine_levels: CatShrineLevels | None = None
        self.medal_names: MedalNames | None = None
        self.mission_names: MissionNames | None = None
        self.mission_conditions: MissionConditions | None = None

    def get_game_data_getter(
        self, save: SaveFile | None = None, cc: CountryCode | None = None
    ) -> GameDataGetter:
        if self.game_data_getter is None:
            if cc is None and save is not None:
                cc = save.cc
            if cc is None:
                raise ValueError("cc must be provided if save is not provided")
            self.game_data_getter = GameDataGetter(cc)
        return self.game_data_getter

    def get_gatya_item_names(self, save: SaveFile) -> GatyaItemNames:
        if self.gatya_item_names is None:
            self.gatya_item_names = GatyaItemNames(save)
        return self.gatya_item_names

    def get_gatya_item_buy(self, save: SaveFile) -> GatyaItemBuy:
        if self.gatya_item_buy is None:
            self.gatya_item_buy = GatyaItemBuy(save)
        return self.gatya_item_buy

    def get_chara_drop(self, save: SaveFile) -> CharaDrop:
        if self.chara_drop is None:
            self.chara_drop = CharaDrop(save)
        return self.chara_drop

    def get_gamatoto_levels(self, save: SaveFile) -> GamatotoLevels:
        if self.gamatoto_levels is None:
            self.gamatoto_levels = GamatotoLevels(save)
        return self.gamatoto_levels

    def get_gamatoto_members_name(self, save: SaveFile) -> GamatotoMembersName:
        if self.gamatoto_members_name is None:
            self.gamatoto_members_name = GamatotoMembersName(save)
        return self.gamatoto_members_name

    def get_localizable(self, save: SaveFile) -> Localizable:
        if self.localizable is None:
            self.localizable = Localizable(save)
        return self.localizable

    def get_ability_data(self, save: SaveFile) -> AbilityData:
        if self.abilty_data is None:
            self.abilty_data = AbilityData(save)
        return self.abilty_data

    def get_enemy_names(self, save: SaveFile) -> EnemyNames:
        if self.enemy_names is None:
            self.enemy_names = EnemyNames(save)
        return self.enemy_names

    def get_rank_gift_descriptions(self, save: SaveFile) -> RankGiftDescriptions:
        if self.rank_gift_descriptions is None:
            self.rank_gift_descriptions = RankGiftDescriptions(save)
        return self.rank_gift_descriptions

    def get_rank_gifts(self, save: SaveFile) -> RankGifts:
        if self.rank_gifts is None:
            self.rank_gifts = RankGifts(save)
        return self.rank_gifts

    def get_treasure_text(self, save: SaveFile) -> TreasureText:
        if self.treasure_text is None:
            self.treasure_text = TreasureText(save)
        return self.treasure_text

    def get_cat_shrine_levels(self, save: SaveFile) -> CatShrineLevels:
        if self.cat_shrine_levels is None:
            self.cat_shrine_levels = CatShrineLevels(save)
        return self.cat_shrine_levels

    def get_medal_names(self, save: SaveFile) -> MedalNames:
        if self.medal_names is None:
            self.medal_names = MedalNames(save)
        return self.medal_names

    def get_mission_names(self, save: SaveFile) -> MissionNames:
        if self.mission_names is None:
            self.mission_names = MissionNames(save)
        return self.mission_names

    def get_mission_conditions(self, save: SaveFile) -> MissionConditions:
        if self.mission_conditions is None:
            self.mission_conditions = MissionConditions(save)
        return self.mission_conditions

    def get_lang(self, save: SaveFile) -> str:
        return self.get_localizable(save).get_lang() or "en"


def update_external_content(_: Any = None):
    """Updates external content."""

    color.ColoredText.localize("updating_external_content")
    print()
    ExternalThemeManager.update_all_external_themes()
    ExternalLocaleManager.update_all_external_locales()
    core_data.init_data()


def print_no_internet():
    color.ColoredText.localize("no_internet")


core_data = CoreData()
core_data.init_data()


__all__ = [
    "server",
    "io",
    "locale_handler",
    "country_code",
    "log",
    "game_version",
    "crypto",
    "game",
    "theme_handler",
    "max_value_helper",
    "AdbHandler",
    "AdbNotInstalled",
    "CountryCode",
    "Path",
    "Data",
    "CSV",
    "ServerHandler",
    "GameVersion",
    "SaveFile",
    "JsonFile",
    "ManagedItem",
    "ManagedItemType",
    "BackupMetaData",
    "Cat",
    "Upgrade",
    "PowerUpHelper",
    "TalentOrb",
    "TalentOrbs",
    "OrbInfo",
    "OrbInfoList",
    "RawOrbInfo",
    "SaveOrb",
    "SaveOrbs",
    "ConfigKey",
    "SpecialSkill",
]
