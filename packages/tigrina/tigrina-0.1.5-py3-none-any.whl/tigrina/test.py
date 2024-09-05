import re
from Tigrinya_alphabet_coder_decoder import Tigrina_info as code_word


# mycode=code_word.code_translation("ፈተነ","code","")
# print("mycode:",mycode)
# code and decode....................................
# mydecode=code_word.code_translation(mycode,'decode','yes')
# print("mydecode:",mydecode)

# convert=code_word.convert_sentence_to_tigrina("ezi natey iyu")
# print("convert:",convert)


# verb to be.....................................
# verbtobetrans = code_word.verb_to_be_trans()
# verbtobetrans_item = next((item for item in verbtobetrans if item.get('id') == 67), None)
# print("verbtobetrans:", verbtobetrans_item)
# verbtobeInfo=code_word.verb_to_be("ይመጽእ ኣሎ")
# print("verbtobeInfo:", verbtobeInfo)


#verb................................
# verb from stem
# resultVerb_createVerbFromStemVerb=code_word.verb.create_verb_from_stem("መጽአ",'future','we',"he",'ዘይ',"yes")
# print("resultVerb_createVerbFromStemVerb:",resultVerb_createVerbFromStemVerb)

# stem from verb
# resultVerb_createStemFromVerb=code_word.verb.create_stem_from_verb("ኣሲርዎ")
# print("resultVerb_createStemFromVerb:",resultVerb_createStemFromVerb)


# noun........................
# resultnoun=code_word.noun("ቦርሳታት")
# print("resultnoun:",resultnoun)


#adjective..............................
#adjective from stem
# resultAdjective_makeAdjectiveFromStem=code_word.adjective.make_adjective_from_stem('ብርቱዕ','','her','','','እንተዘይ')
# print("resultAdjective_makeAdjectiveFromStem:",resultAdjective_makeAdjectiveFromStem)

# stem from adjective
# resultAdjective_makeStemFromAdjective=code_word.adjective.make_stem_from_adjective('እንተዝብርትዕ')
# print("resultAdjective_makeStemFromAdjective:",resultAdjective_makeStemFromAdjective)

# breakingtest=code_word.break_text("test text here. This is another test.","")
# print("breakingtest:",breakingtest)

# locale.setlocale(locale.LC_COLLATE, 'ti_ER.UTF-8')

# sort_test = [
#     {'name': 'ሃብቶም', 'age': 40},
#     {'name': 'ግደ', 'age': 74},
#     {'name': 'መሓሪ', 'age': 45},
#     {'name': 'ሰለሙን', 'age': 50},
#     {'name': 'ጅሮም', 'age': 60}
# ]
# array=['ሃብቶም','ግደ','መሓሪ','ሰለሙን','ጅሮም']
# result=code_word.order_tg(array,'','asc')
# print("result:",result)

result_select=code_word.Data.select("SELECT * from tb1 where city LIKE 'Nijm%'")
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

def lowercase_sql_keywords(sql_query):
    keywords = [
        "INSERT INTO", "SELECT", "FROM", "INNER JOIN", "OUTER JOIN", "LEFT JOIN",
        "RIGHT JOIN", "NATURAL JOIN", "WHERE", "LIKE", "IN", "ORDER BY", 
        "GROUP BY", "UPDATE", "SET","DELETE"
    ]

    # Use regex to replace only whole words, case-insensitively
    for keyword in keywords:
        pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
        sql_query = pattern.sub(keyword.lower(), sql_query)

    return sql_query

# Example usage
# query = "DELETE INTO tb1 SET NAME='GIDE'"
# query = lowercase_sql_keywords(query)
# print("query:",query)