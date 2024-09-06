import re
from tg_main import Tigrina_words as code_word

# sample to test fetching data
result_select=code_word.Data.select("SELECT * from adjectives where word_tigrina='መበቈል'")
print("result_select:",result_select)

# result_insert=code_word.Data.insert("insert into tb1 (id, name, age, city) values(1,'xegay segid', 38, 'Germany')")
# print("result_insert:",result_insert)

# result_update=code_word.Data.update("update tb1 set name='gide segid test', age=578 where name='gide segid test'")
# print("result_update:",result_update)

# result_delete=code_word.Data.delete("delete * from tb1")
# print("result_delete:",result_delete)

# result_tables=code_word.Data.get_tables("show tables")
# print("result_tables:",result_tables)

# result_fields=code_word.Data.get_fields("describe verbs")
# print("result_fields:",result_fields)

