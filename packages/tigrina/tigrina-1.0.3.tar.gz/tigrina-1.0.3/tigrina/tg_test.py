import re
from tigrina.tg_main import Tigrina_words as tigrina_words

# sample to test fetching data
result_select=tigrina_words.Data.select("SELECT * from adjectives where word_tigrina='መበቈል'")
print("result_select:",result_select)

# sample to test data fetching from encode data tables
# first code the word
code=tigrina_words.code_translation("መበቈል","code","")
query=f"SELECT * from tokenized_data where tg_code like '%{code}%'"
get_result=tigrina_words.Data.select(query)
print("get_result:",get_result)
object_list = [tigrina_words.pandas_data_frame_to_object(**row.to_dict()) for _, row in get_result.iterrows()]
print(object_list)
# result_insert=tigrina_words.Data.insert("insert into tb1 (id, name, age, city) values(1,'xegay segid', 38, 'Germany')")
# print("result_insert:",result_insert)

# result_update=tigrina_words.Data.update("update tb1 set name='gide segid test', age=578 where name='gide segid test'")
# print("result_update:",result_update)

# result_delete=tigrina_words.Data.delete("delete * from tb1")
# print("result_delete:",result_delete)

# result_tables=tigrina_words.Data.get_tables("show tables")
# print("result_tables:",result_tables)

# result_fields=tigrina_words.Data.get_fields("describe verbs")
# print("result_fields:",result_fields)

