# -*- coding:utf-8 -*-

from elasticsearch_dsl import Nested, Text, Keyword, Date, InnerDoc, Document, connections

connections.create_connection(hosts=['localhost:9200'])
index_name = 'job-info'


class Category(InnerDoc):
    main_cate = Text()
    sub_cate = Text()


class Salary(InnerDoc):
    max_salary = Text()
    min_salary = Text()


class JobInfo(Document):
    name = Text(analyzer='ik_max_word')
    salary = Nested(Salary)
    pubdate = Date()
    update = Date()
    education = Keyword()
    experience = Keyword()
    company = Text()
    com_logo = Keyword()
    com_logo_url = Keyword()
    location = Text(analyzer='ik_max_word')
    description = Text(analyzer='ik_max_word')
    category = Nested(Category)
    pub_url = Keyword()

    def add_salary(self, max_salary, min_salary):
        self.salary.append(Salary(max_salary=max_salary, min_salary=min_salary))

    def add_category(self, main_cate, sub_cate):
        self.category.append(Category(main_cate=main_cate, sub_cate=sub_cate))


if __name__ == '__main__':
    JobInfo.init(index=index_name)
