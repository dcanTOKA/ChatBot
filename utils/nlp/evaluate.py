import torch

from model.nlp.qa import QAPair
from service.nlp.embedding_words import EmbeddingWords
from service.nlp.normalize_service import normalize

from decouple import config

CUDA = torch.cuda.is_available()
device = torch.device("cuda" if CUDA else "cpu")


def evaluate(searcher, voc, sentence, max_length=int(config("MAX_LEN"))):
    print(sentence)
    test_batches = (
        EmbeddingWords(voc, sentence)
        .sentence_as_index()
        .zero_padding()
        .binary_matrix()
        .convert_to_tensor()
    )

    indexes_batch = test_batches.index_input_sentence_matrix
    lengths = test_batches.index_input_sentence_matrix_lens
    input_batch = torch.LongTensor(indexes_batch).transpose(0, 1)
    input_batch = input_batch.to(device)
    lengths = lengths.to("cpu")

    tokens, scores = searcher(input_batch, lengths, max_length)
    # indexes -> words
    output = []
    for cand in tokens:
        output.append(cand)
        if cand == int(config("EOS_token")):
            print("break")
            break
    print(output)
    decoded_words = [voc.index2word[token.item()] for token in output]

    decoded_words = [x for x in decoded_words if not (x == "PAD" or x == "EOS")]
    return decoded_words


def evaluateInput(searcher, voc, input_sentence):
    try:
        # Normalize sentence
        input_sentence = normalize(input_sentence)
        # Create QAPair. Answer will bee blank
        qa_pair_as_list = [QAPair(question=input_sentence, answer="")]
        # Evaluate sentence
        output_words = evaluate(searcher, voc, qa_pair_as_list)
        print('Bot:', ' '.join(output_words))
        return ' '.join(output_words)

    except KeyError:
        print("Error: Encountered unknown word.")
