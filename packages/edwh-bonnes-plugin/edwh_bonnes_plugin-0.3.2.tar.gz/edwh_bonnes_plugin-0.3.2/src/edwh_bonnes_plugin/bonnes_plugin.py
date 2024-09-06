from time import sleep

from invoke import task
import random
import webbrowser

@task()
def yell(c):
    print("AAAAAAAaaaafdffAHHH")


@task()
def open(c, a_way):
    match a_way:
        case 'base':
            webbrowser.open_new('https://educationwarehouse.org/nextcloud/apps/spreed/')
            webbrowser.open('https://realpython.com/python-virtual-environments-a-primer/#how-can-you-work-with-a-python-virtual-environment')
            webbrowser.open('https://www.perplexity.ai/')
        case 'talk':
            link = 'https://educationwarehouse.org/nextcloud/apps/spreed/'
        case 'pp':
            link = 'https://www.perplexity.ai/'
        case _:
            link = 'https://www.' + a_way + '.com/'
    webbrowser.open(link)