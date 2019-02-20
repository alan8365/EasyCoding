from django.shortcuts import render

from .models import *
from .apps import WikiMenuContent, clean_table_content
from assessment.apps import execute_sql


# Create your views here.

def wiki(request, lesson, chapter):
    if request.method == "GET":

        template = "wiki/wiki.html"

        all_wiki = []
        for i in range(1, WikiMenuContent.get_wiki_size()):
            all_wiki.append(
                WikiMenuContent(i)
            )

        choice_wiki = Wiki.objects.get(lesson=lesson, chapter=chapter)
        all_content = list(Content.objects.filter(wiki=choice_wiki))
        all_content.sort()

        return render(request, template, {
            "title": str(choice_wiki),
            "all_content": all_content,
            "all_wiki": all_wiki,
        })

    search = request.POST['search']

    search_for_sql = '@'.join(search) + '@'

    sql = """
    SELECT lesson, chapter, `name`
    FROM wiki_wiki 
    WHERE `name` LIKE "%%%s%%"
    ESCAPE "@"
    """ % search_for_sql

    search_title_result = execute_sql(sql)

    sql = """
    SELECT w.lesson, w.chapter, w.name, c.content
    FROM wiki_content as c, wiki_wiki as w
    WHERE (c.isText = 1 OR c.isTitle = 1) AND c.content LIKE "%%%s%%" AND c.wiki_id = w.id
    ESCAPE "@"
    """ % search_for_sql

    search_content_result = execute_sql(sql)

    sql = '''
    select w.lesson, w.chapter, w.name, c.content
    from wiki_content as c, wiki_wiki as w 
    where isTable = 1 and c.wiki_id = w.id
    '''

    search_table_result = execute_sql(sql)
    search_table_result = ((i[0], i[1], i[2], clean_table_content(i[3])) for i in search_table_result)
    search_table_result = (i for i in search_table_result if i[3].find(search) != -1)



