# -*- coding: utf-8 -*-
# @Time    : 2024.09.05
# @Author  : cangyun
# @Description : 无人机编程 SDK
# @Copyright  : 版权归 cangyun 所有, 代码如有侵权请联系删除, email: 4uansi@gmail.com

from helloFly import fly
from atexit import register
from threading import Thread
import time
import socket
import json

# from helloAi import init as Ai

from enum import Enum
from _thread import start_new_thread

f = fly()


# 参考位置
class PositionType(Enum):
    current = 0
    target = 1


# 水平环绕参考位置
class HCircleReferenceType(Enum):
    absolute = 0
    relative = 1


# 垂直环绕参考位置
class VCircleReferenceType(Enum):
    FB = "FB"
    LR = "LR"


# 状态类型
class StatusType(Enum):
    open = 1
    close = 0


# 正弦环绕参考位置
class SCircleReferenceType(Enum):
    FBHorizontal = "FB+HOR"
    FBVertical = "FB+VER"
    LRHorizontal = "LR+HOR"
    LRVertical = "LR+VER"


# 方向
class DirectionType(Enum):
    Front = 1
    Rear = 2
    Left = 3
    Right = 4
    Up = 5
    Under = 6
    LeftFront = 7
    RightFront = 8
    LeftRear = 9
    RightRear = 10


# 灯光状态
class LEDStatusType(Enum):
    Always = 0
    Breath = 1
    Chroma = 2
    Close = 3


# 激光发射状态
class EmitType(Enum):
    once = 0
    continuous = 1
    stop = 2


# 无人机基础类
class Drone:
    def __init__(self, id: int = 0) -> None:
        self.id = id

        self.settings.hSpeed(90)
        self.settings.vSpeed(90)

        self.settings.opticalFlowLocation()

        self.settings.autoWait(True)

        self.functions.LEDControl(LEDStatusType.Close, [0, 0, 0])

        # 注入功能类
        self.functions = Functions(self.id)
        self.infrared = Infrared(self.id)
        self.oled = OLED(self.id)
        self.camera = Camera(self.id)
        self.message = Message(self.id)
        self.settings = Settings(self.id)
        self.fly = Fly(self.id)
        self.check = Check(self.id)

        register(self.fly.land)

        print("\n\033[1;30m{id}号无人机初始化完成\033[0m".format(id=self.id))


# 功能类
class Functions:
    def __init__(self, id) -> None:
        self.id = id

    def voice(self, s: str) -> None:
        """
        语音播报

        参数:
            s: 语音播报的字符串
        """
        f.tts(s)

    def emitLaser(self, emitType: EmitType) -> None:
        """
        发射激光

        参数:
            emitType: 发射类型
        """
        f.shootCtrl(self.id, emitType)

    def electromagnet(self, status: bool) -> None:
        """
        是否打开电磁铁

        参数:
            status: True 打开, False 关闭
        """
        f.magnetCtrl(self.id, int(status))

    def servo(self, angle: int) -> None:
        """
        舵机

        参数:
            angle: 舵机打开角度
        """
        f.servoCtrl(self.id, angle)

    def switch(self, status: bool) -> None:
        """
        电子开关

        参数:
            status: True 打开, False 关闭
        """
        f.switchCtrl(self.id, int(status))

    def LEDControl(self, status: LEDStatusType, colorValue: list) -> None:
        """
        灯光控制

        参数:
            status: 灯光状态
            colorValue: 灯光颜色值
        """
        f.ledCtrl(self.id, status, colorValue)

    def clearConsole(self) -> None:
        """
        清空控制台
        """
        f.clearConsole()

    def run(self, fun: function) -> None:
        """
        运行线程

        参数：
            fun: 需要运行的多线程函数
        """
        start_new_thread(fun, ())

    def wait(self, sec: int) -> None:
        """
        等待时间

        参数：
            sec: 等待时间，单位秒
        """
        f.sleep(sec)

    def waitUntil(self, condition: bool) -> None:
        """
        等待直到条件满足

        参数:
            condition: 等待直到条件满足
        """
        while not (condition):
            f.sleep(0.01)


# 红外
class Infrared:
    def __init__(self, id) -> None:
        self.id = id

    def NEC(self, cont: list) -> None:
        """
        红外 NEC 发送

        参数:
            cont: 内容, 示例  [0x12, 0x34, 0x56, 0x78]
        """
        f.irSend(self.id, 0, list)

    def Encry(self, cont: list) -> None:
        """
        红外保密发送

        参数:
            cont: 内容, 示例  [0x12, 0x34, 0x56, 0x78]
        """
        f.irSend(self.id, 1, list)


# 屏幕
class OLED:
    def __init__(self, id) -> None:
        self.id = id

    def showStr(self, x: int, y: int, s: str, multiple: int) -> None:
        """
        oled 显示字符串

        参数:
            x: x坐标
            y: y坐标
            s: 显示的字符串
            multiple: 放大倍数
        """
        f.showStr(self, x, y, str(s), multiple)

    def clear(self) -> None:
        """
        OLED 清屏
        """
        f.showCtrl(0, 8)

    def display() -> None:
        """
        OLED 生效
        """
        f.showCtrl(0, 4)


# 相机
class Camera:
    def __init__(self, id) -> None:
        self.id = id

    def cameraAngle(self, angle: int) -> None:
        """
        镜头角度

        参数:
            angle: 角度
        """
        f.cameraDeg(self.id, angle)

    def photoBack(self) -> None:
        """
        拍照回传
        """
        f.photographMode(self.id, 1)

    def photoSaveSD(self) -> None:
        """
        拍照保存内存卡
        """
        f.photographMode(self.id, 129)

    def colorSampleBack(self) -> None:
        """
        颜色采样回传
        """
        f.photographMode(self.id, 2)

    def colorSampleSaveSD(self) -> None:
        """
        颜色采样保存内存卡
        """
        f.photographMode(self.id, 130)

    def colorrRecognitionBack(self) -> None:
        """
        颜色识别回传
        """
        f.photographMode(self.id, 3)

    def colorrRecognitionSaveSD(self) -> None:
        """
        颜色识别保存内存卡
        """
        f.photographMode(self.id, 131)

    def countRecognitionMode0Back(self) -> None:
        """
        计数识别模式0 回传
        """
        f.photographMode(self.id, 4)

    def countRecognitionMode0SaveSD(self) -> None:
        """
        计数识别模式0 保存内存卡
        """
        f.photographMode(self.id, 132)

    def countRecognitionMode1Back(self) -> None:
        """
        计数识别模式1 回传
        """
        f.photographMode(self.id, 5)

    def countRecognitionMode1SaveSD(self) -> None:
        """
        计数识别模式1 保存内存卡
        """
        f.photographMode(self.id, 133)


# 消息发送
class Message:
    def __init__(self, id) -> None:
        self.id = id

    def sendMsg(self, msg: str) -> None:
        """
        发送消息

        参数:
            msg: 发送的字符串
        """
        f.roleCtrl(self.id, str(msg))

    def clearMsg(self) -> None:
        f.clearRoleNews(self.id)


# 设置类
class Settings:
    def __init__(self, id) -> None:
        self.id = id

    def hSpeed(self, speed: int) -> None:
        """
        设置水平速度

        参数:
            speed: 速度, 单位 cm/s
        """
        f.xySpeed(self.id, speed)

    def vSpeed(self, speed: int) -> None:
        """
        设置垂直速度

        参数:
            speed: 速度, 单位 cm/s
        """
        f.zSpeed(self.id, speed)

    def centerOfGravityShift(self, x: int, y: int) -> None:
        """
        设置重心偏移

        参数:
            x: x轴重心偏移
            y: y轴重心偏移
        """
        f.setCenterOffset(self.id, [x, y])

    def currentLocation(self, x: int, y: int) -> None:
        """
        设置当前位置坐标

        参数:
            x: x轴坐标
            y: y轴坐标
        """
        f.setLocation(self.id, [x, y])

    def tagDistance(self, distance: int) -> None:
        """
        设置标签间距

        参数:
            distance: 间距, 单位 cm
        """
        f.setTagDistance(self.id, distance)

    def autoWait(self, status: bool) -> None:
        """
        设置自动等待

        参数:
            status: True 打开, False 关闭
        """
        f.setAutoDelay(self.id, int(status))

    def laserFixedHeight(self, status: StatusType) -> None:
        """
        设置激光定高

        参数:
            status: 状态
        """
        f.tofSwitch(self.id, status)

    def opticalFlowLocation(self) -> None:
        """
        光流定位
        """
        f.flyMode(self.id, 0)

    def tagLocation(self) -> None:
        """
        标签定位
        """
        f.flyMode(self.id, 1)

    def autoLine(self) -> None:
        """
        自主巡线
        """
        f.flyMode(self.id, 2)

    def lockDirection(self, isLock: bool) -> None:
        """
        设置是否锁定机头
        """
        f.lockDir(self.id, int(isLock))

    def repeatMaxCount(self, count: int) -> None:
        """
        设置最大重发次数

        参数:
            count: 重发次数
        """
        f.setRepeatCountMax(count)


# 飞行类
class Fly:
    def __init__(self, id) -> None:
        self.id = id

    def takeOff(self, height: int) -> None:
        """
        起飞

        参数:
            height: 起飞高度
        """
        f.takeOff(self.id, height)

    def forwardFly(self, distance: int) -> None:
        """
        向前飞

        参数:
            distance: 飞行距离, 单位 cm
        """
        f.moveCtrl(self.id, 1, distance)

    def forwardFlySearchBlackBlock(self, distance: int) -> None:
        """
        向前飞寻找黑色色块

        参数:
            distance: 飞行距离, 单位 cm
        """
        f.moveSearchDot(self.id, 1, distance)

    def forwardFlySearchBlock(self, distance: int, thresholdValue: list) -> None:
        """
        向前飞寻找阈值对应的色块

        参数:
            distance: 飞行距离, 单位 cm
            thresholdValue: 阈值
        """
        f.moveSearchBlob(self.id, 1, distance, thresholdValue)

    def forwardFlySearchTag(self, distance: int, tagId: int) -> None:
        """
        向前飞行寻找标签

        参数:
            distance: 飞行距离, 单位 cm
            tagId: 标签 ID
        """
        f.moveSearchTag(self.id, 1, distance, tagId)

    def forwardFlyFollowTag(self, distance: int, tagId: int) -> None:
        """
        向前飞行跟随标签

        参数:
            distance: 飞行距离, 单位 cm
            tagId: 标签 ID
        """
        f.moveFollowTag(self.id, 1, distance, tagId)

    def hCircle(
        self, reference: HCircleReferenceType, x: int, y: int, angle: int, speed: int
    ) -> None:
        """
        水平环绕

        参数:
            reference: 参考位置
            x: x轴
            y: y轴
            angle: 角度, 0~360
            speed: 速度, 单位 cm/s
        """
        f.ShuiPingHuanRao(self.id, reference, x, y, angle, speed)

    def vCircle(
        self,
        reference: VCircleReferenceType,
        distance: int,
        height: int,
        angle: int,
        speed: int,
    ) -> None:
        """
        垂直环绕

        参数:
            reference: 参考位置
            distance: 距离
            heinght: 圆心高度
            angle: 角度, 0~360
            speed: 速度, 单位 cm/s
        """
        f.ChuiZhiHuanRao(self.id, reference, distance, height, angle, speed)

    def sCircle(
        self,
        reference: SCircleReferenceType,
        startAngle: int,
        endAngle: int,
        period: int,
        amplitude: int,
        speed: int,
    ) -> None:
        """
        正弦环绕

        参数:
            reference: 参考位置
            startAngle: 开始角度
            endAngle: 结束角度
            period: 周期长度
            amplitude: 振幅大小
            speed: 速度, 单位 cm/s
        """
        f.ZhengXianHuanRao(
            self.id, reference, startAngle, endAngle, period, amplitude, speed
        )

    def moveToCoordinates(self, x: int, y: int, distance: int, speed: int) -> None:
        """
        向指定坐标点移动

        参数:
            x: x坐标
            y: y坐标
            distance: 移动距离, 单位 cm
            speed: 速度, 单位 cm/s
        """
        f.WangDianYiDong(self.id, x, y, distance, speed)

    def moveByAngle(self, angle: int, distance: int, speed: int) -> None:
        """
        向指定角度移动

        参数:
            angle: 角度
            distance: 距离
            speed: 速度, 单位 cm/s
        """
        f.WangDegYiDong(self.id, angle, distance, speed)

    def roll(self, direction: DirectionType, turns: int) -> None:
        """
        翻滚

        参数:
            direction: 方向, 支持前后左右
            turns: 翻滚圈数
        """
        f.flipCtrl(self.id, direction, turns)

    def moveByCoordinates(self, position: PositionType, coordinates: list) -> None:
        """
        移动到坐标位置

        参数:
            position: 参考位置
            coordinates: 坐标
        """
        f.move(self.id, position, coordinates)

    def goToTag(self, tagId: int, height: int) -> None:
        """
        直达标签, 并飞到指定高度

        参数:
            tagId: 标签 ID
            height: 飞行高度, 单位 cm
        """
        f.goToTag(self.id, tagId, height)

    def goToCoordinates(self, coordinates: list) -> None:
        """
        直达坐标位置

        参数:
            coordinates: 坐标
        """
        f.goTo(self.id, coordinates)

    def rotation(self, angle: int) -> None:
        """
        旋转

        参数:
            angle: 角度
        """
        f.rotation(self.id, angle)

    def height(self, height: int) -> None:
        """
        飞行高度

        参数:
            height: 高度
        """
        f.flyHigh(self.id, height)

    def land(self) -> None:
        """
        降落
        """
        f.flyCtrl(self, 0)

    def brake(self) -> None:
        """
        刹车
        """
        f.flyCtrl(self, 1)

    def hover(self) -> None:
        """
        悬停
        """
        f.flyCtrl(self, 2)

    def scram(self) -> None:
        """
        急停
        """
        f.flyCtrl(self, 3)

    def calibrate(self) -> None:
        """
        校准
        """
        f.flyCtrl(self, 4)


# 检测类
class Check:
    def __init__(self, id) -> None:
        self.id = id

    def blackPoint(self) -> None:
        """
        检测黑点
        """
        self.f.mvCheckMode(self.id, 1)

    def blackLine(self) -> None:
        """
        检测黑线
        """
        self.f.mvCheckMode(self.id, 2)

    def tag(self, tagId: int = -1) -> None:
        """
        检测标签

        参数:
            tagId: 标签号, 不填写则检测所有标签
        """
        (
            self.f.mvCheckMode(self.id, 3)
            if tagId == -1
            else self.f.mvCheckTag(self.id, tagId)
        )

    def qrCode(self) -> None:
        """
        检测二维码
        """
        self.f.mvCheckMode(self.id, 7)

    def barCode(self) -> None:
        """
        检测条形码
        """
        self.f.mvCheckMode(self.id, 8)

    def colorBlock(self, thresholdValue: list) -> None:
        """
        检测色块

        参数:
            thresholdValue: 阈值, 示例 [0, 0, 0, 0, 0, 0]
        """
        f.mvCheckBlob(self.id, 4, thresholdValue)

    def colorLine(self, thresholdValue: list) -> None:
        """
        检测色线

        参数:
            thresholdValue: 阈值, 示例 [0, 0, 0, 0, 0, 0]
        """
        f.mvCheckBlob(self.id, 5, thresholdValue)

    def keyPress(self, key: int) -> bool:
        """
        检测按键

        参数:
            key: 需要检测的按键
        """
        return f.getKeyPress(key)
