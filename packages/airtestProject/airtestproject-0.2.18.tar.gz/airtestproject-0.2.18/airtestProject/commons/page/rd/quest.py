import math
import os
import time
from airtestProject.factory.operateFactory import operate
import threading
from airtestProject.commons.stateMachine.task import check_func, TaskCaseTemplate, put_task, stop_machine_f, \
    only_run_this, start_tag, TaskRunner
from airtestProject.airtest.core.helper import G
from airtestProject.commons.utils.logger import log
import numpy as np
from airtestProject.commons.utils.tools import run_with_timer

# snp_list = [(slice(884, 939), slice(412, 705))]

null_pos = [0.7, 0.45]  # 空位置
close_pos = [0.8, 0.16]  # 关闭位置
move_init_pos = [0.15, 0.75]  # 摇杆默认位置
move_forward_pos = [0.15, 0.65]  # 摇杆向前移动位置
move_backward_pos = [0.15, 0.85]  # 摇杆向后移动位置
move_left_pos = [0.05, 0.75]  # 摇杆向左移动位置
move_right_pos = [0.25, 0.75]  # 摇杆向右移动位置
attack_pos = [0.84, 0.82]  # 攻击键
skill_1_pos = [0.77, 0.9]   # 小技能
skill_2_pos = [0.77, 0.75]  # 大招
change_soul = [0.9, 0.55]   # 切换技
my_command = None

# 自动战斗通用
def auto_fight():
    move_forward()
    operate().click(attack_pos)
    operate().click(attack_pos)
    operate().click(attack_pos)
    operate().click(attack_pos)
    operate().click(attack_pos)
    operate().click(attack_pos)
    operate().click(attack_pos)
    operate().click(attack_pos)
    operate().click(attack_pos)
    operate().click(skill_1_pos)
    operate().click(skill_2_pos)
    operate().click(skill_1_pos)
    operate().click(skill_2_pos)
    operate().click(change_soul)


# 前进通用
def move_forward():
    operate().swipe((move_init_pos[0], move_init_pos[1]), (move_forward_pos[0], move_forward_pos[1]))


# 跳过剧情通用
def do_quest(quest_id, next_pos="MainSetting", interval=1, max_executions=50):
    @check_func(f'正在播放剧情-{quest_id}')
    def _do_quest():
        run_with_timer(quest_start, interval, max_executions, quest_end)

    def quest_start():
        if operate().exists("SkipBtn"):
            operate().click("SkipBtn")
        else:
            operate().click(move_init_pos)

    def quest_end():
        btn_state = operate().exists(next_pos)
        log.step(f"当前按钮{next_pos}状态为{btn_state}")
        return btn_state

    _do_quest()


# 战斗通用
def fight_to_boss(quest_id, boss_pos, is_exists, interval=1, max_executions=120):
    @check_func(f'正在播放剧情-{quest_id}')
    def _fight_to_boss():
        run_with_timer(fight_start, interval, max_executions, fight_end)

    def fight_start():
        auto_fight()

    def fight_end():
        if is_exists:
            return operate().exists(boss_pos)
        else:
            return not operate().exists(boss_pos)

    _fight_to_boss()


# 跑剧情通用
def run_quest(quest_id, next_pos, is_exists, interval=1, max_executions=120, command="&AutoRunQuest"):
    @check_func(f'正在进行剧情-{quest_id}寻路')
    def _run_quest():
        global my_command
        if operate().exists("Send"):
            operate().click("KuaiJie")
            operate().sleep(1.0)
        else:
            if my_command == command:
                operate().click("KuaiJie")
                send_command()
            else:
                operate().set_text("KuaiJie", command)
                send_command()
                my_command = command

        run_with_timer(start_run, interval, max_executions, stop_run)
        log.step(f'当前gm为-{my_command}')

    def send_command():
        operate().sleep(1.0)
        operate().click("Send", ocrPlus=True)
        operate().click("KuaiJie")

    def start_run():
        operate().sleep(1.0)

    def stop_run():
        if is_exists:
            return operate().exists(next_pos)
        else:
            return not operate().exists(next_pos)

    _run_quest()


# 移动至点击任务按钮通用
def move_to_click_quest(quest_id, click_pos, interval=1, max_executions=15):
    @check_func(f'正在进行剧情-{quest_id}')
    def _move_to_click_quest():
        run_with_timer(move_forward(), interval, max_executions, click_end)

    def is_click_pos_exist():
        return operate().exists(click_pos)

    def click_end():
        if is_click_pos_exist():
            return True

    _move_to_click_quest()


# 容错,兼容需要一直点击才有反馈的操作
def click_most(click_pos, interval=1, max_executions=15):
    @check_func(f'尝试点击-{click_pos}')
    def _click_most():
        run_with_timer(click_func, interval, max_executions, end_func)

    def click_func():
        operate().click(click_pos)

    def end_func():
        return not operate().exists(click_pos)

    _click_most()


# 通用过指引方法
def guide_click(quest_id, posList):
    @check_func(f'过指引-{quest_id}')
    def _guide_click():
        for pos in posList:
            if not pos:
                log.step(f'未发现指引所需的元素')
                return
            operate().click(pos)
            operate().sleep(1.0)

    _guide_click()


class QuestPage(TaskCaseTemplate):
    def __init__(self, script_root, Project=None):
        super().__init__()
        if Project is not None:
            operate('air').set_dict(script_root, Project)

    @put_task(is_profile=True)
    def quest_first_q(self):  # 主线第1个剧情TimeLine
        quest_id = 10110101
        do_quest(quest_id)

    @put_task
    def quest_first_r(self):  # 主线第1个剧情寻路
        quest_id = 10110103
        run_quest(quest_id, "MainSetting", False)

    @put_task
    def quest_first_f(self):    # 主线第1场战斗，打蛇
        quest_id = 10110106
        fight_to_boss(quest_id, "SnakeBoss", True, 1, 20)

    @put_task
    def quest_first_b(self):    # 主线第1场BOSS战斗，打蛇
        quest_id = 10110108
        fight_to_boss(quest_id, "SnakeBoss", False, 1, 20)

    @put_task
    def quest_absorb(self):   # 主线吸收魂环
        quest_id = 10110110
        move_to_click_quest(quest_id, "AbsorbSoulBtn")
        click_most("AbsorbSoulBtn")

    @put_task
    def quest_absort_q(self):   # 主线吸收魂环后的剧情
        quest_id = 10110111
        do_quest(quest_id)

    @put_task
    def quest_first_g(self):   # 主线第一次指引
        quest_id = 101101111
        guide_click(quest_id, ["MainSetting", "SoulBtn", "SoulRing", "SnakeRing", "GuideReplace", null_pos, "CloseSoulBtn"])

    @put_task
    def quest_npc_q(self):   # 主线吸收魂环后的剧情
        quest_id = 10110113
        do_quest(quest_id)

    @start_tag()
    def quest_fb_r(self):  # 主线福伯寻路
        quest_id = 10110114
        run_quest(quest_id, "FuBo", True)
        click_most("FuBo")

    @put_task
    def quest_fb_q(self):  # 主线福伯剧情
        quest_id = 10110115
        do_quest(quest_id)

    @put_task
    def quest_village_r(self):  # 主线村口寻路
        quest_id = 10110117
        run_quest(quest_id, "MainSetting", False)

    @put_task
    def quest_village_q(self):  # 主线村口寻路
        quest_id = 10110117
        do_quest(quest_id)

    @put_task
    def quest_teacher_r(self):  # 主线招生老师寻路
        quest_id = 10110118
        run_quest(quest_id, "MainSetting", False)

    @put_task
    def quest_teacher_q(self):  # 主线招生老师剧情
        quest_id = 10110118
        do_quest(quest_id, "ExitBtn")

    @put_task
    def fight_lch_f(self):
        quest_id = 10110119  # 主线路重华战斗
        fight_to_boss(quest_id, "ExitBtn", False)

    @put_task
    def quest_master_q(self):  # 主线大师剧情
        quest_id = 10110120
        do_quest(quest_id)

    @put_task
    def quest_lel_r(self):  # 主线继续找福伯
        quest_id = 10110201
        run_quest(quest_id, "FuBo", True)
        click_most("FuBo")

    @put_task
    def quest_lel_q(self):  # 主线福伯对话
        quest_id = 10110201
        do_quest(quest_id, "ExitBtn", True)

    # @put_task
    # def quest_lel_f_1(self):  # 主线柳二龙战斗小怪
    #     quest_id = 10110202
    #     fight_to_boss(quest_id, "ExitBtn", True)

    @put_task
    def quest_lel_f_2(self):  # 主线柳二龙战斗贝亚顿
        quest_id = 10110202
        fight_to_boss(quest_id, "ExitBtn", False)

    @put_task
    def quest_byd_q(self):  # 主线贝亚顿对话
        quest_id = 10110203
        do_quest(quest_id)

    @put_task
    def quest_gd_g(self):   # 主线第一次指引
        quest_id = 10110205
        guide_click(quest_id, ["MainSetting", "SoulBtn", "GuangDiBtn", "UpLevelBtn", "AutoPlaced", "UpLevelBtn", null_pos, null_pos, "ExitSoulBtn", "CloseSoulBtn"])

    @put_task
    def quest_gd_q(self):   # 主线光帝赞美你
        quest_id = 10110207
        do_quest(quest_id)

    @put_task
    def quest_master_r(self):   # 主线找大师
        quest_id = 10110301
        run_quest(quest_id, "MainSetting", False)

    @put_task
    def quest_wxg_q(self):  # 主线和王小刚对话
        quest_id = 10110301
        do_quest(quest_id)

    @put_task
    def quest_wxg_r(self):  # 主线和王小刚同行
        quest_id = 10110302
        run_quest(quest_id, "MainSetting", False)

    @put_task
    def quest_wxg_q_2(self):   # 主线和王小刚第二次对话
        quest_id = 101103021
        do_quest(quest_id)

    @put_task
    def quest_ndc_r(self):
        quest_id = 101103022   # 主线前往诺丁城
        run_quest(quest_id, "MainSetting", False)

    @put_task
    def quest_ndc_q(self):
        quest_id = 10110303   # 主线诺丁城剧情对话
        do_quest(quest_id)

    @put_task
    def quest_ndc_r_2(self):
        quest_id = 101103031   # 主线前往诺丁城
        run_quest(quest_id, "WangXiaoGang", True)
        click_most("WangXiaoGang")

    @put_task
    def quest_ndc_q_2(self):
        quest_id = 101103032   # 主线诺丁城王小刚剧情对话
        do_quest(quest_id)

    @put_task
    def quest_nrr_r(self):
        quest_id = 101103033   # 主线诺丁城寻找宁荣荣
        run_quest(quest_id, "MainSetting", False)

    @put_task
    def quest_nrr_q(self):
        quest_id = 101103034    # 主线诺丁城询问李荣荣
        do_quest(quest_id)

    @put_task
    def quest_nrr_r_2(self):
        quest_id = 101103035    # 主线诺丁城继续寻找李荣荣
        run_quest(quest_id, "ZongMenDiZi", True)
        click_most("ZongMenDiZi")

    @put_task
    def quest_nrr_q(self):
        quest_id = 101103035    # 主线诺丁城询问宗门弟子
        do_quest(quest_id)

    # @put_task
    # def quest_zm_f(self):
    #     quest_id = 101103036    # 主线宗门弟子战斗
    #     fight_to_boss(quest_id, "ExitBtn", False)
    #
    # @put_task
    # def quest_zm_q(self):
    #     quest_id = 101103037    # 主线宁荣荣拦住了你
    #     do_quest(quest_id)
