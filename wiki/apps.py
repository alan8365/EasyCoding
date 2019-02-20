from django.apps import AppConfig

from .models import *

import re


class WikiConfig(AppConfig):
    name = 'wiki'


class WikiMenuContent:

    def __init__(self, lesson):
        self.lesson = lesson
        self.header = str(Wiki.objects.get(lesson=lesson, chapter=0))
        self.data = list(Wiki.objects.exclude(chapter=0).filter(lesson=lesson))
        self.data.sort()

    @staticmethod
    def get_wiki_size():
        return len(Wiki.objects.filter(chapter=0))


def clean_table_content(string):
    ans = re.sub(r'[ \t\r]', "", string)
    ans = re.sub(r'<.{2,3}>', "\n", ans)
    ans = re.sub(r'\n+', '\n', ans)

    return ans


def clean_sql_content(results, search):
    results = tuple(results)
    search_highlight = "<highlight>%s</highlight>" % search
    ans = tuple()

    for result in results:
        temp = result[3]

        if len(temp) < 21:
            result = ((result[0], result[1], result[2], result[3].replace(search, search_highlight)),)
            ans += result
            continue

        ran = int((20 - len(search)) / 2)
        target = temp.find(search)

        if target < ran:
            temp = temp[:20] + '...'
        elif target > len(temp) - 20:
            print(target)
            print(len(result) - 20)
            temp = '...' + temp[-20:]
        else:
            temp = '...' + temp[target - ran:target + ran + len(search)] + '...'

        ans += ((result[0], result[1], result[2], temp.replace(search, search_highlight)),)

    print(ans)

    return ans
