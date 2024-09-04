import spacy
import re
import translators as ts


class WordMatching:
    SIMILARITY_MIN_SCORE = 0.60
    TRANSLATION_MODEL = "google"

    def __init__(self):
        self.nlp = spacy.load('en_core_web_lg')

    def is_regex_matches(self, text, patterns=None):
        matched_regex = False
        for pattern in patterns:
            match = re.match(patterns[pattern], text)
            if match and len(match.string) == len(text):
                matched_regex = True
                break
        return matched_regex

    def is_alpha_match(self, text):
        return all(char.isalpha() or char.isspace() for char in text)

    def find_most_similar_word_from_list(self, sentence_list, keywords):
        most_similar_sentence = None
        max_similarity_score = 0
        for sentence in sentence_list:
            if sentence:
                split_sentence = sentence.split(' ')
                for word in split_sentence:
                    for keyword in keywords:
                        similarity_score = self.similarity_of_words(word.lower(), keyword.lower())
                        if similarity_score > max_similarity_score and similarity_score > self.SIMILARITY_MIN_SCORE:
                            max_similarity_score = similarity_score
                            most_similar_sentence = sentence
        print("SIMILARITY WINNER:")
        print(most_similar_sentence)
        print(max_similarity_score)
        return most_similar_sentence

    def similarity_of_words(self, word1, word2):
        doc1 = self.nlp(word1)
        doc2 = self.nlp(word2)
        return doc1.similarity(doc2)

    def translate_words(self, phrase_to_translate, from_language="auto", to_language="en"):
        translation = ts.translate_text(query_text=phrase_to_translate,
                                        translator=self.TRANSLATION_MODEL,
                                        from_language=from_language,
                                        to_language=to_language)
        print(f"TRANSLATE: \"{phrase_to_translate}\" -> \"{translation}\"")
        return translation


if __name__ == "__main__":
    wm = WordMatching()
    word = "Messstrecke"
    wm.translate_words(phrase_to_translate=word)
    word = "Tailles"
    wm.translate_words(phrase_to_translate=word)

