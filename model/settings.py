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

from utils.load_json import load_from_pickle

DATA_PATH = "./data"


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

        self.voc = Vocabulary("movie")
        self.voc.num_word = 13149
        self.voc.index2word = load_from_pickle(DATA_PATH+"/index2word.pkl")
        self.voc.word2index = load_from_pickle(DATA_PATH + "/word2index.pkl")
        self.voc.word2count = load_from_pickle(DATA_PATH + "/word2count.pkl")

        self.output_size = self.voc.num_word
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
