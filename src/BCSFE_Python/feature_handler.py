"""Handler for selecting and running editor features"""

from typing import Any, Union

from . import (
    helper,
    user_input_handler,
    config_manager,
)
from .edits import basic, cats, gamototo, levels, other, save_management


def fix_elsewhere_old(save_stats: dict[str, Any]) -> dict[str, Any]:
    """Fix the elsewhere error using 2 save files"""

    main_token = save_stats["token"]
    main_iq = save_stats["inquiry_code"]
    input(
        "Select a save file that is currently loaded in-game that doesn't have the elsehere error and is not banned\nPress enter to continue:"
    )
    new_path = helper.select_file(
        "Select a clean save file",
        helper.get_save_file_filetype(),
        helper.get_save_path(),
    )
    if not new_path:
        print("Please select a save file")
        return save_stats

    data = helper.load_save_file(new_path)
    new_stats = data["save_stats"]
    new_token = new_stats["token"]
    new_iq = new_stats["inquiry_code"]
    save_stats["token"] = new_token
    save_stats["inquiry_code"] = new_iq

    helper.colored_text(f"Replaced inquiry code: &{main_iq}& with &{new_iq}&")
    helper.colored_text(f"Replaced token: &{main_token}& with &{new_token}&")
    return save_stats


FEATURES: dict[str, Any] = {
    "저장데이터 관리": {
        "저장데이터 저장": save_management.save.save_save,
        "변경 사항을 저장하고 게임 서버에 업로드(이어하기 코드 및 인증번호 받기)": save_management.server_upload.save_and_upload,
        "파일에 변경 사항을 저장": save_management.save.save,
        "변경 사항을 저장하고 adb를 사용하여 저장 데이터를 게임에 업로드(게임 다시열기X)": save_management.save.save_and_push,
        "변경 사항을 저장하고 adb를 사용하여 저장 데이터를 게임에 업로드(게임 다시 열기O)": save_management.save.save_and_push_rerun,
        "저장 데이터를 JSON으로 내보내기": save_management.other.export,
        "adb로 저장 데이터 지우기(게임을 다시 설치하지 않고 새로운 계정 생성)": save_management.other.clear_data,
        "추적된 금지 가능 항목 업로드(저장 또는 종료 시 자동으로 수행됨)": save_management.server_upload.upload_metadata,
        "저장 데이터 불러오기": save_management.load.select,
        "저장 데이터를 다른 버전으로 변환": save_management.convert.convert_save,
        # "Manage Presets": preset_handler.preset_manager,
    },
    "아이템": {
        "통조림": basic.basic_items.edit_cat_food,
        "XP": basic.basic_items.edit_xp,
        "티켓": {
            "노말 티켓": basic.basic_items.edit_normal_tickets,
            "레어 티켓": basic.basic_items.edit_rare_tickets,
            "플레티넘 티켓": basic.basic_items.edit_platinum_tickets,
            "플레티넘 티켓 조각": basic.basic_items.edit_platinum_shards,
            "레전드 티켓": basic.basic_items.edit_legend_tickets,
        },
        "NP": basic.basic_items.edit_np,
        "리더쉽": basic.basic_items.edit_leadership,
        "배틀 아이템": basic.basic_items.edit_battle_items,
        "캣츠아이": basic.catseyes.edit_catseyes,
        "개다래 씨앗 / 개다래 열매": basic.catfruit.edit_catfruit,
        "개화의 보주": basic.talent_orbs_new.edit_talent_orbs,
        "고양이 광부": basic.basic_items.edit_catamins,
        "금지 아이템(?)(금지 해제 가능한 아이템을 얻을 수 있음) ": other.scheme_item.edit_scheme_data,
    },
    "가마토토 / 오토토: {
        "오토토 개발대": basic.basic_items.edit_engineers,
        "성 재료": basic.ototo_base_mats.edit_base_mats,
        "고양이드링크": basic.basic_items.edit_catamins,
        "가마토토 XP / Level": gamototo.gamatoto_xp.edit_gamatoto_xp,
        "오토토 고양이 대포": gamototo.ototo_cat_cannon.edit_cat_cannon,
        "가마토토 도우미": gamototo.helpers.edit_helpers,
        "가마토토에서 게임이 충돌하는 문제를 해결": gamototo.fix_gamatoto.fix_gamatoto,
    },
    "고양이 / 스킬": {
        "얻기 / 지우기": {
            "얻기": cats.get_remove_cats.get_cat,
            "지우기": cats.get_remove_cats.remove_cats,
        },
        "업그레이드": cats.upgrade_cats.upgrade_cats,
        "True Form Cats": {
            "Get Cat True Forms": cats.evolve_cats.get_evolve,
            "Remove Cat True Forms": cats.evolve_cats.remove_evolve,
            "Force True Form Cats (will lead to blank cats for cats without a true form)": cats.evolve_cats.get_evolve_forced,
        },
        "Talents": {
            "Set talents for each selected cat individually": cats.talents.edit_talents_individual,
            "Max / Remove all selected cat talents": cats.talents.max_all_talents,
        },
        "Collect / Remove Cat Guide": {
            "Set Cat Guide Entries (does not give cf)": cats.clear_cat_guide.collect_cat_guide,
            "Unclaim Cat Guide Entries": cats.clear_cat_guide.remove_cat_guide,
        },
        'Get stage unit drops - removes the "Clear this stage to get special cat" dialog': cats.chara_drop.get_character_drops,
        "Upgrade special skills / abilities": cats.upgrade_blue.upgrade_blue,
    },
    "Levels / Treasures": {
        "Main Story Chapters Clear / Unclear": {
            "Clear each stage in every chapter for all selected chapters": levels.main_story.clear_all,
            "Clear each stage in every chapter for each selected chapter": levels.main_story.clear_each,
        },
        "Treasures": {
            "Treasure Groups (e.g energy drink, aqua crystal, etc)": levels.treasures.treasure_groups,
            "Specific stages and specific chapters individually": levels.treasures.specific_stages,
            "Specific stages and chapters all at once": levels.treasures.specific_stages_all_chapters,
        },
        "Zombie Stages / Outbreaks": levels.outbreaks.edit_outbreaks,
        "Event Stages": levels.event_stages.event_stages,
        "Stories of Legend": levels.event_stages.stories_of_legend,
        "Uncanny Legends": levels.uncanny.edit_uncanny,
        "Zero Legends": levels.zerolegends.edit_zl,
        "Aku Realm/Gates Clearing": levels.aku.edit_aku,
        "Unlock the Aku Realm/Gates": levels.unlock_aku_realm.unlock_aku_realm,
        "Gauntlets": levels.gauntlet.edit_gauntlet,
        "Collab Gauntlets": levels.gauntlet.edit_collab_gauntlet,
        "Towers": levels.towers.edit_tower,
        "Behemoth Culling": levels.behemoth_culling.edit_behemoth_culling,
        "Into the Future Timed Scores": levels.itf_timed_scores.timed_scores,
        "Challenge Battle Score": basic.basic_items.edit_challenge_battle,
        "Clear Tutorial": levels.clear_tutorial.clear_tutorial,
        "Catclaw Dojo Score (Hall of Initiates)": basic.basic_items.edit_dojo_score,
        "Add Enigma Stages": levels.enigma_stages.edit_enigma_stages,
        "Allow the filibuster stage to be recleared": levels.allow_filibuster_clearing.allow_filibuster_clearing,
        "Legend Quest": levels.legend_quest.edit_legend_quest,
    },
    "Inquiry Code / Token / Account": {
        "Inquiry Code": basic.basic_items.edit_inquiry_code,
        "Token": basic.basic_items.edit_token,
        "Fix elsewhere error / Unban account": other.fix_elsewhere.fix_elsewhere,
        "Old Fix elsewhere error / Unban account (needs 2 save files)": fix_elsewhere_old,
        "Generate a new inquiry code and token": other.create_new_account.create_new_account,
    },
    "Other": {
        "Rare Gacha Seed": basic.basic_items.edit_rare_gacha_seed,
        "Unlocked Equip Slots": basic.basic_items.edit_unlocked_slots,
        "Get Restart Pack / Returner Mode": basic.basic_items.edit_restart_pack,
        "Meow Medals": other.meow_medals.medals,
        "Play Time": other.play_time.edit_play_time,
        "Unlock / Remove Enemy Guide Entries": other.unlock_enemy_guide.enemy_guide,
        "Catnip Challenges / Missions": other.missions.edit_missions,
        "Normal Ticket Max Trade Progress (allows for unbannable rare tickets)": other.trade_progress.set_trade_progress,
        "Get / Remove Gold Pass": other.get_gold_pass.get_gold_pass,
        "Claim / Remove all user rank rewards (does not give any items)": other.claim_user_rank_rewards.edit_rewards,
        "Cat Shrine Level / XP": other.cat_shrine.edit_shrine_xp,
    },
    "Fixes": {
        "Fix time errors": other.fix_time_issues.fix_time_issues,
        "Unlock the Equip Menu": other.unlock_equip_menu.unlock_equip,
        "Clear Tutorial": levels.clear_tutorial.clear_tutorial,
        "Fix elsewhere error / Unban account": other.fix_elsewhere.fix_elsewhere,
        "Old Fix elsewhere error / Unban account (needs 2 save files)": fix_elsewhere_old,
        "Fix gamatoto from crashing the game": gamototo.fix_gamatoto.fix_gamatoto,
    },
    "Edit Config": {
        "Edit LOCALIZATION": config_manager.edit_locale,
        "Edit DEFAULT_COUNTRY_CODE": config_manager.edit_default_gv,
        "Edit DEFAULT_SAVE_PATH": config_manager.edit_default_save_file_path,
        "Edit FIXED_SAVE_PATH": config_manager.edit_fixed_save_path,
        "Edit EDITOR settings": config_manager.edit_editor_settings,
        "Edit START_UP settings": config_manager.edit_start_up_settings,
        "Edit SAVE_CHANGES settings": config_manager.edit_save_changes_settings,
        "Edit SERVER settings": config_manager.edit_server_settings,
        "Edit config path": config_manager.edit_config_path,
    },
    "Exit": helper.exit_check_changes,
}


def get_feature(
    selected_features: Any, search_string: str, results: dict[str, Any]
) -> dict[str, Any]:
    """Search for a feature if the feature name contains the search string"""

    for feature in selected_features:
        feature_data = selected_features[feature]
        if isinstance(feature_data, dict):
            feature_data = get_feature(feature_data, search_string, results)
        if search_string.lower().replace(" ", "") in feature.lower().replace(" ", ""):
            results[feature] = selected_features[feature]
    return results


def show_options(
    save_stats: dict[str, Any], features_to_use: dict[str, Any]
) -> dict[str, Any]:
    """Allow the user to either enter a feature number or a feature name, and get the features that match"""

    if (
        not config_manager.get_config_value_category("EDITOR", "SHOW_CATEGORIES")
        and FEATURES == features_to_use
    ):
        user_input = ""
    else:
        prompt = (
            "What do you want to edit (some options contain other features within them)"
        )
        if config_manager.get_config_value_category(
            "EDITOR", "SHOW_FEATURE_SELECT_EXPLANATION"
        ):
            prompt += "\nYou can enter a number to run a feature or a word to search for that feature (e.g entering catfood will run the Cat Food feature, and entering tickets will show you all the features that edit tickets)\nYou can press enter to see a list of all of the features"
        user_input = user_input_handler.colored_input(f"{prompt}:\n")
    user_int = helper.check_int(user_input)
    results = []
    if user_int is None:
        results = get_feature(features_to_use, user_input, {})
    else:
        if user_int < 1 or user_int > len(features_to_use) + 1:
            helper.colored_text("Value out of range", helper.RED)
            return show_options(save_stats, features_to_use)
        if FEATURES != features_to_use:
            if user_int - 2 < 0:
                return menu(save_stats)
            results = features_to_use[list(features_to_use)[user_int - 2]]
        else:
            results = features_to_use[list(features_to_use)[user_int - 1]]
    if not isinstance(results, dict):
        save_stats_return = results(save_stats)
        if save_stats_return is None:
            return save_stats
        return save_stats_return
    if len(results) == 0:
        helper.colored_text("No feature found with that name.", helper.RED)
        return menu(save_stats)
    if len(results) == 1 and isinstance(list(results.values())[0], dict):
        results = results[list(results)[0]]
    if len(results) == 1:
        save_stats_return = results[list(results)[0]](save_stats)
        if save_stats_return is None:
            return save_stats
        return save_stats_return

    helper.colored_list(["Go Back"] + list(results))
    return show_options(save_stats, results)


def menu(
    save_stats: dict[str, Any], path_save: Union[str, None] = None
) -> dict[str, Any]:
    """Show the menu and allow the user to select a feature to edit"""

    if path_save:
        helper.set_save_path(path_save)
    if config_manager.get_config_value_category("EDITOR", "SHOW_CATEGORIES"):
        helper.colored_list(list(FEATURES))
    save_stats = show_options(save_stats, FEATURES)

    return save_stats
