from functools import cmp_to_key

def is_consonant(s:str) -> bool:
    """Returns True if symbol is consonant, False otherwise"""
    consonants = 'bcdfghjklmnpqrstvwxyz'
    return True if consonants.count(s.lower()) > 0 else False 

def number_of_words_with_first_consonant(words:list[str]) -> int:
    """Returns the number of words with first consonant letter"""
    res = 0
    for word in words:
        res += is_consonant(word[0])
    return res

def words_with_double_letter(words:list[str]) -> list[(str, int)]:
    """Returs the words with double letter"""
    res = []
    index = 0
    for word in words:
        add = False
        for i in range(len(word) - 1):
            if word[i] == word[i + 1]:
                add = True
        if add:
            res.append((word, index))
        index += 1     
    return res   

def compare(a:str, b:str) -> int:
    "Return result of comparison two strings"
    if a.lower() < b.lower():
        return -1
    if a.lower() > b.lower():
        return 1
    return 0

def words_in_alphabetic_order(words:list[str]) -> list[str]:
    "Return words in alphabetic order"
    return sorted(words, key=cmp_to_key(compare))

def task4():
    """Return the number of words that begin with a consonant\n
    Return words containing two identical letters in a row and their indecies\n
    Returns words in alphabetical order
    """
    text = 'So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her.'
    text = text.replace(',', '')
    text = text.replace('.', '')
    words = text.split(' ')
    return number_of_words_with_first_consonant(words), words_with_double_letter(words), words_in_alphabetic_order(words)