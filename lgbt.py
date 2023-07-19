from termcolor import colored
from os import system
import colorama


def arcobaleno(str: str) -> None:
    colors = ["red","yellow","green","cyan","blue","magenta"]
    for i in range(len(str)):
        print(colored(str[i], colors[i%len(colors)], 'on_black', ['bold', 'blink']), end='')

colorama.init()
system("cls")
str = input("Scrivi per arcobalenizzare, mbare \n")
arcobaleno(str)
input()