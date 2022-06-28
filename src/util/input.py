#!/usr/bin/env python
# coding=utf-8
'''
Author: BATU1579
CreateDate: 2022-06-28 22:30:19
LastEditor: BATU1579
LastTime: 2022-06-29 01:52:56
FilePath: \\src\\util\\input.py
Description: 交互控制器
'''
from abc import ABCMeta, abstractmethod
from os import system
from pynput.keyboard import Listener, Key
from typing import Callable


class InputController(metaclass=ABCMeta):
    '''
    输入基类
    '''

    def __init__(self, title: str, data: list[str] = None):
        self.title = title
        self.data = data

    def show_title(self):
        system("cls")
        print(f"{'=' * 15} {self.title} {'=' * 15}\n")

    @abstractmethod
    def get_input(self): pass


class Form(InputController):
    '''
    表单输入
    '''

    def get_input(self) -> dict[str, str]:
        self.show_title()
        return {question: input(f"[{question}]: ") for question in self.data}


class SingleChoice(InputController):
    '''
    单选输入
    '''

    def get_input(self) -> int:
        pitch_on = 0

        self.show_all(pitch_on)

        def check():
            '''
            pitch_on 的边界检查
            '''
            nonlocal pitch_on
            if pitch_on < 0:
                pitch_on = len(self.data) - 1
            elif pitch_on == len(self.data):
                pitch_on = 0

        def on_press(key: Key):
            nonlocal pitch_on
            if key == Key.up:
                pitch_on -= 1
            if key == Key.down:
                pitch_on += 1
            if key == Key.enter:
                # 捕获回车
                input()
                return False
            check()
            self.show_all(pitch_on)

        with Listener(on_press=on_press) as listener:
            listener.join()

        return pitch_on

    def show_choice(self, pitch_on: int):
        assert 0 <= pitch_on < len(
            self.data), "pitch on number is out of range"

        if type(self.data[0]) == dict:
            for index, choice in enumerate(self.data):
                if index == pitch_on:
                    print(f" => {choice['title']} - {choice['info']}")
                else:
                    print(f"    {choice['title']}")
        else:
            for index, choice in enumerate(self.data):
                print(f"{' => ' if index == pitch_on else '    '} {choice}")

    def show_all(self, pitch_on: int):
        self.show_title()
        self.show_choice(pitch_on)


class Confirm(SingleChoice):
    def __init__(self, title: str, info: str, confirm_action: Callable,
                 cancel_action: Callable):
        super().__init__(title, ['confirm', 'cancel'])
        self.info = info
        self.confirm_action = confirm_action
        self.cancel_action = cancel_action

    def show_all(self, pitch_on: int):
        self.show_title()
        print(f"\n     {self.info}    \n\n")
        self.show_choice(pitch_on)

    def get_input(self) -> int:
        result = super().get_input()

        if result == 0:
            self.confirm_action()
        else:
            self.cancel_action()

        return result


def main():
    controller = SingleChoice("title", [
        "A", "B", "C", "D", "E", "F"
    ])
    print(controller.get_input())

    controller = Form("title", ['username', 'password'])
    print(controller.get_input())

    controller = Confirm("title", "xxxxx", lambda: print("yes"), lambda: print("no"))
    print(controller.get_input())


if __name__ == "__main__":
    main()