from typing import List

import torch
from decouple import config

from model.nlp.batch import Batch
from model.nlp.qa import QAPair
from service.nlp.vocabulary_service import Vocabulary


class EmbeddingWords:
    def __init__(self, vocabulary: Vocabulary, pairs: List[QAPair], zero_padding_direction="right"):
        self.vocabulary = vocabulary
        self.pairs = pairs
        self.max_seq_len: int = None
        self.zero_padding_direction = zero_padding_direction

        self.index_input_sentence_matrix = []
        self.index_input_sentence_matrix_lens = []
        self.zero_padded_input = None

        self.index_output_sentence_matrix = []
        self.index_output_sentence_matrix_lens = []
        self.zero_padded_output = None

        self.mask = []

    def sentence_as_index(self):
        for pair in self.pairs:
            temp = []
            for word in pair.question.split():
                temp.append(self.vocabulary.word2index[word])
            temp.append(int(config("EOS_token")))
            self.index_input_sentence_matrix.append(temp)
            self.index_input_sentence_matrix_lens.append(len(temp))

            temp = []
            for word in pair.answer.split():
                temp.append(self.vocabulary.word2index[word])
            temp.append(int(config("EOS_token")))
            self.index_output_sentence_matrix.append(temp)
            self.index_output_sentence_matrix_lens.append(len(temp))

        return self

    def zero_padding(self):
        self.get_max_seq_count()

        assert self.max_seq_len > 0

        matrix_list = []

        for matrix in [self.index_input_sentence_matrix, self.index_output_sentence_matrix]:
            padded_matrix = []
            for row in matrix:
                padding = [0] * (self.max_seq_len - len(row))

                if self.zero_padding_direction == 'right':
                    new_row = row + padding
                elif self.zero_padding_direction == 'left':
                    new_row = padding + row
                else:
                    raise ValueError("Direction must be 'right' or 'left'")

                padded_matrix.append(new_row)

            padded_matrix = [list(row) for row in zip(*padded_matrix)]

            assert len(padded_matrix) == self.max_seq_len

            matrix_list.append(padded_matrix)

        self.zero_padded_input = matrix_list[0]
        self.zero_padded_output = matrix_list[1]

        return self

    def get_max_seq_count(self):
        temp = 0
        for pair in self.pairs:
            question_length = len(pair.question.split())
            answer_lenght = len(pair.answer.split())

            if question_length > temp:
                temp = question_length
            if answer_lenght > temp:
                temp = answer_lenght

        self.max_seq_len = temp + 1

        return self

    def binary_matrix(self):
        for i, elem in enumerate(self.zero_padded_output):
            self.mask.append([])

            for token in elem:
                if token == config("PAD_token"):
                    self.mask[i].append(0)
                else:
                    self.mask[i].append(1)

        return self

    def create_batches(self, batch_size: int) -> List[Batch]:
        n_batches = len(self.index_input_sentence_matrix) // batch_size
        batches = []

        for i in range(0, len(self.zero_padded_input.t()), batch_size):
            remaining_elements = len(self.zero_padded_input.t()) - i

            batch_size_for_current_iteration = min(batch_size, remaining_elements)

            batch_input = self.zero_padded_input.t()[i:i + batch_size_for_current_iteration].t()
            batch_output = self.zero_padded_output.t()[i:i + batch_size_for_current_iteration].t()
            batch_lengths = self.index_input_sentence_matrix_lens[i:i + batch_size_for_current_iteration]
            batch_mask = self.mask.t()[i:i + batch_size_for_current_iteration].t()
            batch_max_target_len = max(self.index_output_sentence_matrix_lens[i:i + batch_size_for_current_iteration])

            batch = Batch(
                input_variable=batch_input,
                input_length=batch_lengths,
                target_variable=batch_output,
                mask=batch_mask,
                max_target_len=batch_max_target_len
            )
            batches.append(batch)

        return batches

    def convert_to_tensor(self):
        self.index_input_sentence_matrix_lens = torch.tensor(self.index_input_sentence_matrix_lens)
        self.index_output_sentence_matrix_lens = torch.tensor(self.index_output_sentence_matrix_lens)

        self.zero_padded_input = torch.LongTensor(self.zero_padded_input)
        self.zero_padded_output = torch.LongTensor(self.zero_padded_output)

        self.mask = torch.BoolTensor(self.mask)

        return self
