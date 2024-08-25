import streamlit as st
import pandas as pd
import textdistance
import re
from collections import Counter

words = []
with open('book.txt', 'r', encoding='utf-8') as f:
    file_name_data = f.read()
    file_name_data = file_name_data.lower()
    words = re.findall(r'\w+', file_name_data)


V = set(words)
word_freq_dict = Counter(words)

probs = {}
Total = sum(word_freq_dict.values())
for k in word_freq_dict.keys():
    probs[k] = word_freq_dict[k] / Total


def my_autocorrect(input_word):
    input_word = input_word.lower()
    if input_word in V:
        return 'Your word seems to be correct'
    else:
        similarities = [1 - textdistance.Jaccard(qval=2).distance(v, input_word) for v in word_freq_dict.keys()]
        df = pd.DataFrame.from_dict(probs, orient='index').reset_index()
        df = df.rename(columns={'index': 'Word', 0: 'Prob'})
        df['Similarity'] = similarities
        output = df[['Word', 'Similarity']].sort_values(['Similarity'], ascending=False).head()
        return output


# Streamlit app
st.title("WriteRight")
st.header("Write Flawlessly, Every Time!!!")

input_sentence = st.text_input("Input Sentence", "")

if input_sentence:
    words_in_sentence = re.findall(r'\w+', input_sentence.lower())
    suggestions = {}
    for word in words_in_sentence:
        if word not in V:
            suggestions[word] = my_autocorrect(word)
    
    if suggestions:
        st.write("Suggestions for misspelled words:")
        for word, suggestion_df in suggestions.items():
            st.write(f"Word: {word}")
            st.dataframe(suggestion_df)
    else:
        st.write("All words seem to be correct.")

if st.button("Check"):
    st.experimental_rerun()
