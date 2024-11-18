import spacy
import numpy as np

# Load SpaCy's small English model
nlp = spacy.load("en_core_web_sm")

class SubjectiveTest:
    def __init__(self, inputText, noOfQues):
        self.inputText = inputText
        self.noOfQues = int(noOfQues)

    def extract_keywords(self, sentence):
        """
        Tokenizes and extracts keywords (nouns in this case) from the sentence using SpaCy.
        """
        doc = nlp(sentence)
        keywords = [token.text for token in doc if token.pos_ == 'NOUN']  # Extract nouns (similar to Objective)
        return keywords

    def generate_test(self):
        """
        Generates a list of subjective questions based on the extracted keywords from input text.
        """
        # Tokenize the input text into sentences using SpaCy
        doc = nlp(self.inputText)
        sentences = [sent.text for sent in doc.sents]

        keyword_list = []
        sentence_keyword_map = {}

        # Extract keywords from each sentence
        for sent in sentences:
            keywords = self.extract_keywords(sent)
            keyword_list.extend(keywords)
            for keyword in keywords:
                sentence_keyword_map[keyword] = sent  # Map keyword to the sentence it appeared in

        # Check if the keyword list is empty
        if len(keyword_list) == 0:
            return ["No keywords found to generate questions."], ["No answers available."]

        question_list = []
        answer_list = []

        # Generate subjective questions and answers based on the extracted keywords
        for _ in range(min(self.noOfQues, len(keyword_list))):  # Ensure we don't ask for more questions than available keywords
            rand_num = np.random.randint(0, len(keyword_list))
            selected_keyword = keyword_list[rand_num]
            context_sentence = sentence_keyword_map[selected_keyword]

            # Generate a subjective question based on the selected keyword
            question = f"Explain the significance of '{selected_keyword}' in the context of the text."

            # Generate an answer based on the context and the keyword
            answer = f"'{selected_keyword}' is mentioned in the following context: '{context_sentence}'. This concept plays a critical role by {self.create_answer(selected_keyword, context_sentence)}."

            question_list.append(question)
            answer_list.append(answer)

        return question_list, answer_list

    def create_answer(self, keyword, sentence):
        """
        This method generates a basic answer by analyzing the sentence and keyword.
        You can use more advanced logic here for deeper analysis.
        """
        # Generate a simple answer explaining the significance of the keyword
        return f"providing insight into the broader theme of the text. Specifically, '{keyword}' helps to clarify the author's intent or message conveyed in the sentence."

