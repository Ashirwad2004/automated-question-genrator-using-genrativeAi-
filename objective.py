import spacy
import numpy as np
import en_core_web_sm
nlp = en_core_web_sm.load()

# Load SpaCy's small English model
nlp = spacy.load("en_core_web_sm")

class ObjectiveTest:
    def __init__(self, inputText, noOfQues):
        self.inputText = inputText
        self.noOfQues = int(noOfQues)

    def extract_keywords(self, sentence):
        """
        Tokenizes and extracts keywords (nouns in this case) from the sentence using SpaCy.
        """
        doc = nlp(sentence)
        keywords = [token.text for token in doc if token.pos_ == 'NOUN']  # Extract nouns
        return keywords

    def generate_distractors(self, keyword_list, correct_keyword):
        """
        Generates random distractor answers by choosing other random keywords.
        Ensures that the correct keyword is not chosen as a distractor.
        """
        distractors = []
        distractor_count = 3  # Let's provide 3 distractors for each question
        
        # Ensure we don't pick the correct keyword as a distractor
        potential_distractors = [word for word in keyword_list if word != correct_keyword]
        
        # If there are fewer keywords than needed distractors, repeat some distractors
        if len(potential_distractors) < distractor_count:
            potential_distractors += np.random.choice(potential_distractors, distractor_count - len(potential_distractors)).tolist()

        # Select random distractors
        selected_distractors = np.random.choice(potential_distractors, distractor_count, replace=False)

        # Create a distractor sentence for each
        for distractor in selected_distractors:
            distractors.append(f"'{distractor}' refers to some other context or concept.")

        return distractors

    def generate_test(self):
        """
        Generates a list of objective multiple-choice questions with one correct answer
        and several distractors for each keyword extracted from the input text.
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

        # Generate objective questions and answers based on the extracted keywords
        for _ in range(min(self.noOfQues, len(keyword_list))):  # Ensure we don't ask for more questions than available keywords
            rand_num = np.random.randint(0, len(keyword_list))
            selected_keyword = keyword_list[rand_num]
            context_sentence = sentence_keyword_map[selected_keyword]

            # Generate the question
            question = f"What is '{selected_keyword}' referring to in the context?"

            # Create a list of potential answers, with one correct and others as distractors
            correct_answer = f"{selected_keyword} refers to: '{context_sentence}'"
            distractors = self.generate_distractors(keyword_list, selected_keyword)

            # Combine correct answer with distractors and shuffle them
            options = [correct_answer] + distractors
            np.random.shuffle(options)

            # Format the question as multiple-choice
            formatted_question = f"<p>{question}</p>\n<ul>\n"
            for i, option in enumerate(options):
                formatted_question += f"<li>{chr(65 + i)}. {option}</li><br>\n"  # A, B, C, D for multiple-choice with <br> for line breaks
            formatted_question += "</ul>\n"

            question_list.append(formatted_question)
            answer_list.append(f"Correct answer: {correct_answer}")  # Provide the correct answer for later reference

        return question_list, answer_list
