from model.nlp.qa import QAPair

from decouple import config


class Vocabulary:
    def __init__(self, name):
        self.name = name
        self.word2index = {}
        self.word2count = {}
        self.index2word = {int(config("PAD_token")): "PAD", int(config("SOS_token")): "SOS", int(config("EOS_token")): "EOS"}

        self.num_word = 3

    def add_sentence(self, sentence):
        splitted = sentence.split()
        for word in splitted:
            self.add_word(word)

    def add_word(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.num_word
            self.word2count[word] = 1
            self.index2word[self.num_word] = word

            self.num_word += 1
        else:
            self.word2count[word] += 1

    def trim(self, min_word):

        keep_word = []

        for k, v in self.word2count.items():
            if v < min_word:
                continue

            keep_word.append(k)

        self.word2index = {}
        self.word2count = {}
        self.index2word = {int(config("PAD_token")): "PAD", int(config("SOS_token")): "SOS", int(config("EOS_token")): "EOS"}

        self.num_word = 3

        for word in keep_word:
            self.add_word(word)


def trim_rare_words(vocabulary, normalized_qa_pairs):
    trimmed_qa_pair_list = []

    for pair in normalized_qa_pairs:
        input_sentence = pair.question
        output_sentence = pair.answer

        keep_input = True
        keep_output = True

        for word in input_sentence.split():
            if word not in vocabulary.word2index:
                keep_input = False
                break

        for word in output_sentence.split():
            if word not in vocabulary.word2index:
                keep_output = False
                break

        if keep_input and keep_output:
            trimmed_qa_pair_list.append(QAPair(question=input_sentence, answer=output_sentence))
