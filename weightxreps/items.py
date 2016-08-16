# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class WeightxrepsItem(Item):
    user_name = Field()
    exercise_date = Field()
    user_weight = Field()
    exercise_name = Field()
    exercise_category = Field()
    exercise_load = Field()
    repetitions_done = Field()
