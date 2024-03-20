import os

import torch
import torch.nn as nn

from model.nlp.qa import QAPair
from service.nlp.decoder_service import LuongAttnDecoderRNN
from service.nlp.encoder_service import EncoderRNN
from service.nlp.greedy_search_decoder_services import GreedySearchDecoder
from service.nlp.normalize_service import normalize
from service.nlp.vocabulary_service import Vocabulary

from decouple import config


class Settings:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.encoder_path = os.path.join("./trained/encoder", "best_model_8_0_encoder.pth")
        self.decoder_path = os.path.join("./trained/decoder", "best_model_8_0_decoder.pth")
        self.hidden_size = 512
        self.encoder_n_layers = 2
        self.decoder_n_layers = 2
        self.voc = None
        self.output_size = None
        self.embedding = None
        self.dropout = 0.3
        self.MAX_LEN = 15

        self.encoder = None
        self.decoder = None
        self.searcher = None

    def load_vocabulary(self):
        normalized_qa_pairs = []
        qa_pairs = []

        qa_file_path = os.path.join('./data', 'qa_pairs.txt')

        with open(qa_file_path, 'r') as file:
            qas = file.readlines()

        for i, qa in enumerate(qas):
            if i == len(qas) - 1:
                break
            pairs = qa.split("\t")
            source = pairs[0]
            target = pairs[1]

            if source and target:
                qa_pairs.append(QAPair(question=source, answer=target))

        for i, qa in enumerate(qa_pairs):
            source = normalize(qa.question)
            target = normalize(qa.answer)

            if (len(source.split()) < self.MAX_LEN and len(source) > 1) and (
                    len(target.split()) < self.MAX_LEN and len(target) > 1):
                normalized_qa_pairs.append(QAPair(question=source, answer=target))

        self.voc = Vocabulary("movie")

        for pair in normalized_qa_pairs:
            self.voc.add_sentence(pair.question)
            self.voc.add_sentence(pair.answer)

        self.voc.trim(int(config("MIN_COUNT")))

        self.output_size = 13149
        self.embedding = nn.Embedding(num_embeddings=self.output_size, embedding_dim=self.hidden_size)

    def load_model(self):
        loaded_encoder = EncoderRNN(self.hidden_size, self.embedding, self.encoder_n_layers, self.dropout)
        loaded_decoder = LuongAttnDecoderRNN(self.embedding, self.hidden_size, self.output_size, self.decoder_n_layers,
                                             self.dropout)

        loaded_encoder.load_state_dict(torch.load(self.encoder_path, map_location=self.device))
        loaded_decoder.load_state_dict(torch.load(self.decoder_path, map_location=self.device))

        loaded_encoder.eval()
        loaded_decoder.eval()

        searcher = GreedySearchDecoder(loaded_encoder, loaded_decoder)

        self.encoder = loaded_encoder
        self.decoder = loaded_decoder
        self.searcher = searcher


settings = Settings()
settings.load_vocabulary()
settings.load_model()
