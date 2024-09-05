# Tigrina alphabets manipulation
### General Overview of the Tigrina Language Processing Application

This application is designed to facilitate the use of Tigrina alphabets for writing and linguistic analysis on computers and mobile devices. It provides a comprehensive set of tools to make working with the Tigrina language more efficient and accessible, whether you are a native speaker, language learner, or researcher.

#### Key Features

1. **Tigrina Alphabet Input and Conversion**:
   - The application allows users to type and manipulate text using the Tigrina script. It includes features for converting text written in Tigrina alphabets into numeric codes and vice versa. This is particularly useful for encoding sensitive information or integrating Tigrina text into systems that require numeric data.

2. **Transliteration Support**:
   - Users can easily convert Tigrina words written in the English alphabet into the proper Tigrina script. This feature helps bridge the gap for users more familiar with English keyboards but who want to write in Tigrina.

3. **Linguistic Tools for Verb, Noun, and Adjective Management**:
   - The application includes advanced tools for creating and analyzing verbs, nouns, and adjectives in the Tigrina language. It can generate conjugated verbs from their stems, extract stems from fully conjugated verbs, create noun stems, and manage adjective forms. These tools are invaluable for language learning, grammatical analysis, and content creation in Tigrina.

4. **Text Processing and Sentence Management**:
   - For ease of translation and text manipulation, the application provides features to break down long sentences into smaller, manageable chunks. This functionality is crucial for accurately translating or processing complex text, making the application versatile for both casual and professional use.

#### Application Purpose

The primary purpose of this application is to enhance the ability to write, translate, and analyze text in Tigrina using digital devices. By integrating a range of linguistic tools and conversion features, the application supports both everyday communication and more specialized tasks, such as language education, research, and digital content creation. Whether you're composing a message, translating a document, or studying Tigrina grammar, this application offers a streamlined, user-friendly platform for all your needs.

### User Manual: Code Word Functions for Tigrina Language Processing

This manual provides a brief explanation of the functions available in the `code_word` module for processing Tigrina language text. Each function performs a specific task related to translating, encoding, or identifying Tigrina language elements.

#### 1. **Convert Tigrina Alphabet to Numeric Code**
   - **Function**: `code_word.code_translation("ፈተነ","code","")`
   - **Description**: Converts a Tigrina word or sentence (e.g., "ፈተነ") into its corresponding numeric code. This is useful for encoding Tigrina text.

#### 2. **Decode Numeric Code to Tigrina Alphabet**
   - **Function**: `code_word.code_translation(mycode, 'decode', 'yes')`
   - **Description**: Decodes a numeric code back into the original Tigrina alphabet. The `mycode` variable contains the numeric code that will be decoded.

#### 3. **Convert English-Alphabet Tigrina to Tigrina Alphabet**
   - **Function**: `code_word.convert_sentence_to_tigrina("ezi natey iyu")`
   - **Description**: Converts Tigrina words written using the English alphabet (e.g., "ezi natey iyu") into the Tigrina alphabet. This helps in converting transliterated text back to its original script.

#### 4. **Translate Verb to Be in Tigrina**
   - **Function**: `code_word.verb_to_be_trans()`
   - **Description**: Provides translations of the verb "to be" in Tigrina across different forms. This function contains a dictionary or lookup table for verb conjugations.

#### 5. **Identify Verb to Be and Other Verbs in a Sentence**
   - **Function**: `code_word.verb_to_be("ይመጽእ ኣሎ")`
   - **Description**: Analyzes a given Tigrina sentence (e.g., "ይመጽእ ኣሎ") to identify and extract the verb "to be" and other verbs present in the sentence. This is useful for linguistic analysis and sentence parsing.

### Usage Examples
Each function is designed for specific use cases, such as encoding/decoding text, converting transliterations, or analyzing verbs in Tigrina sentences. For example, if you have a numeric code and need to retrieve the original Tigrina word, use the decoding function with the appropriate parameters.

### User Manual: Additional Functions in `code_word` Module for Tigrina Language Processing

This section of the manual explains additional functions available in the `code_word` module that focus on verb and adjective creation, stem extraction, noun processing, and sentence breaking for easier translation.

#### 1. **Create Verbs from Stem in Tigrina**
   - **Function**: `code_word.verb.create_verb_from_stem("መጽአ", 'future', 'we', "he", 'ዘይ', "yes")`
   - **Description**: Generates a complete verb from a given stem verb (e.g., "መጽአ") by specifying tense (e.g., 'future'), subject (e.g., 'we'), gender (e.g., 'he'), and other grammatical markers like negation (e.g., 'ዘይ') and aspect (e.g., "yes"). This is useful for constructing conjugated verbs in various forms.

#### 2. **Create Stem Verb from Tigrina Verbs**
   - **Function**: `code_word.verb.create_stem_from_verb("ኣሲርዎ")`
   - **Description**: Extracts the stem from a given Tigrina verb (e.g., "ኣሲርዎ"). The stem is the base form used to create various conjugations of the verb.

#### 3. **Create Stem Noun from Nouns in Tigrina**
   - **Function**: `code_word.noun("ቦርሳታት")`
   - **Description**: Extracts the stem form of a noun (e.g., "ቦርሳታት") in Tigrina. The stem noun is the base form that can be used to create plural forms, possessives, and other noun modifications.

#### 4. **Create Adjectives from Stem Adjectives in Tigrina**
   - **Function**: `code_word.adjective.make_adjective_from_stem('ብርቱዕ', '', 'her', '', '', 'እንተዘይ')`
   - **Description**: Constructs a full adjective from a stem (e.g., 'ብርቱዕ') by specifying gender, possession, and negation markers (e.g., 'እንተዘይ' for negation). This is useful for generating descriptive words that match the grammatical context.

#### 5. **Create Stem from Adjectives in Tigrina**
   - **Function**: `code_word.adjective.make_stem_from_adjective('እንተዝብርትዕ')`
   - **Description**: Extracts the stem form of an adjective (e.g., 'እንተዝብርትዕ'), which can be used to create different forms of the adjective based on gender, number, or negation.

#### 6. **Break Long Sentences into Chunks**
   - **Function**: `code_word.break_text("test text here. This is another test.", "")`
   - **Description**: Splits a long sentence or paragraph (e.g., "test text here. This is another test.") into smaller, more manageable chunks. This is particularly useful for processing or translating large texts where sentence-by-sentence translation is required.

### Usage Examples
These functions are essential for building or breaking down words and sentences in the Tigrina language, whether for translation, linguistic analysis, or language learning. For instance, if you need to generate a verb from its stem for future tense and a specific subject, you can use the `create_verb_from_stem` function with the relevant parameters. Similarly, to simplify long translations, you can use the `break_text` function to segment the content.


## Highlights

### Importing the Library

To use the library, first import it as follows:

```python
from Tigrinya_alphabet_coder_decoder import Tigrina_info as code_word

Functionality
Get Alphabet Family Information

To get the alphabet family of each alphabet:
    get_family_info = code_word.get_family("ይመጽእ")

Encode Text
To get the encoded value of any text:
    mycode = code_word.code_translation("ዘይብርትዕቲ ኔራ", 'code')
Decode Text
To decode the encoded text:
    mydecode = code_word.code_translation(mycode, 'decode', 'yes')

Convert English to Tigrina Alphabet
To convert any English alphabet-written text into Tigrina alphabet-written text:
    convert = code_word.convert_sentence_to_tigrina("ezi natey iyu")

Get Alphabet Information
To get a list of functions that help with alphabet retrievals, positions in a family, or other family information:
   tg_alphabets = code_word.alphabets_info

Order Tigrina Words
To order Tigrina words in ascending or descending order. For array of objects, provide the column name as an additional parameter:
   orderIt = code_word.order_tg(array, '', 'asc')

Get Verb Translations
To get translations of verbs to Tigrina with filtering options:
   verbtobetrans = code_word.verb_to_be_trans()

Create Verb from Stem
To create a verb from a stem:
   resultVerb_createVerbFromStemVerb = code_word.verb.create_verb_from_stem("መጽአ", 'future', 'we', "he", 'ዘይ', "yes")

Create Stem from Verb
To create a stem from a verb:
   resultVerb_createStemFromVerb = code_word.verb.create_stem_from_verb("ኣሲራቶም")
Create Singular Noun
To create a singular form of a plural noun for easier searching:
   resultnoun = code_word.noun("ቦርሳታት")

Create Adjective from Stem
To create an adjective from a stem adjective:
   resultAdjective_makeAdjectiveFromStem = code_word.adjective.make_adjective_from_stem('ብርቱዕ', '', 'her', '', '', 'እንተዘይ')
Create Stem Adjective from Non-Stem Adjective
To create a stem adjective from a non-stem adjective:
  resultAdjective_makeStemFromAdjective = code_word.adjective.make_stem_from_adjective('ሓይላ')

Break Long Text into Chunks
To break long text into chunks of sentences, separated by periods or commas:
   breakingtest = code_word.break_text("test text here. This is another test.", "")

Order Tigrina Words Alphabetically
To order arrays or array objects of Tigrina words alphabetically:
   order_alphabetically = code_word.order_tg(["ግደ", 'ጸጋይ', 'ዝፋን', 'ሂወት'], "", "asc")


Database Operations
Select Data from a Table:
   result_select = code_word.Data.select("select * from tb1")

Insert Data into a Table:
   result_insert = code_word.Data.insert("insert into tb1 (id, name, age, city) values(1, 'xegay segid', 38, 'Germany')")

Update Data in a Table:
   result_update = code_word.Data.update("update tb1 set name='gide segid test', age=4856 where name='gide segid test'")

Delete Data from a Table:
   result_delete = code_word.Data.delete("delete from tb1")

Show All Tables in a Database/File:
   result_tables = code_word.Data.get_tables("show tables")

Show All Fields of a Table:
   result_fields = code_word.Data.get_fields("describe verbs")

