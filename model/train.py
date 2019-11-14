import torch
import torch.nn as nn
import time

import data
import model
MAX_LENGTH = 100


def train(x, y, embedding, encoder, decoder, vocab, encoder_optimizer, decoder_optimizer, criterion, max_length=MAX_LENGTH, device='cpu'):
    batch_size = x.shape[1]
    encoder_hidden = encoder.initHidden(batch_size)

    encoder_optimizer.zero_grad()
    decoder_optimizer.zero_grad()
    # encoder_optimizer.zero_grad()
    # decoder_optimizer.zero_grad()
    input_length = x.size(0)
    target_length = y.size(0)

    encoder_outputs = torch.zeros(max_length, encoder.hidden_size, device=device)

    loss = 0
    embedded = embedding(x)
    for ei in range(input_length):
        encoder_output, encoder_hidden = encoder(embedded[ei], encoder_hidden)
        encoder_outputs[ei] = encoder_output[0, 0]


    start = torch.LongTensor(1, batch_size)
    start.fill_(vocab.stoi['[SOS]'])
    start = embedding(start)
    decoder_input = torch.tensor(start, device=device)

    decoder_hidden = encoder_hidden

    # use_teacher_forcing = True if random.random() < teacher_forcing_ratio else False

    # if use_teacher_forcing:
        # Teacher forcing: Feed the target as the next input
    for di in range(target_length):
        decoder_output, decoder_hidden, decoder_attention = decoder(
            decoder_input, decoder_hidden, encoder_outputs)
        loss += criterion(decoder_output, target_tensor[di])
        decoder_input = target_tensor[di]  # Teacher forcing

    # else:
    #     # Without teacher forcing: use its own predictions as the next input
    #     for di in range(target_length):
    #         decoder_output, decoder_hidden, decoder_attention = decoder(
    #             decoder_input, decoder_hidden, encoder_outputs)
    #         topv, topi = decoder_output.topk(1)
    #         decoder_input = topi.squeeze().detach()  # detach from history as input
    #
    #         loss += criterion(decoder_output, target_tensor[di])
    #         if decoder_input.item() == EOS_token:
    #             break

    loss.backward()

    optimizer.step()
    optimizer.step()

    return loss.item() / target_length

def trainIters(trainLoader, embedding, encoder, decoder, vocab, n_iters, print_every=1000, plot_every=100, learning_rate=0.01):


    start = time.time()
    plot_losses = []
    print_loss_total = 0  # Reset every print_every
    plot_loss_total = 0  # Reset every plot_every

    encoder_optimizer = torch.optim.SGD(encoder.parameters(), lr=learning_rate)
    decoder_optimizer = torch.optim.SGD(decoder.parameters(), lr=learning_rate)
    # training_pairs = [tensorsFromPair(random.choice(pairs))
    #                   for i in range(n_iters)]
    criterion = nn.NLLLoss()

    for iter in range(1, n_iters + 1):
        for (x_batch, y_batch), _ in trainLoader:
            loss = train(x_batch, y_batch, embedding, encoder, decoder, vocab, encoder_optimizer, decoder_optimizer, criterion)

    #     print_loss_total += loss
    #     plot_loss_total += loss
    #
    #     if iter % print_every == 0:
    #         print_loss_avg = print_loss_total / print_every
    #         print_loss_total = 0
    #         print('%s (%d %d%%) %.4f' % (timeSince(start, iter / n_iters),
    #                                      iter, iter / n_iters * 100, print_loss_avg))
    #
    #     if iter % plot_every == 0:
    #         plot_loss_avg = plot_loss_total / plot_every
    #         plot_losses.append(plot_loss_avg)
    #         plot_loss_total = 0
    #
    # showPlot(plot_losses)


def __main__():
    hidden_size = 256
    trainLoader, valLoader, testLoader, vocab = data.loadData('fake_data')


    # encoderDecoder = model.EncoderDecoder(vocab)
    emb_dim = 50
    embedding = model.Embedding(vocab, emb_dim)
    encoder = model.EncoderRNN(emb_dim, hidden_size)
    decoder = model.DecoderRNN(hidden_size, emb_dim)

    trainIters(trainLoader, embedding, encoder, decoder, vocab, 75000, print_every=5000)

if __name__ == "__main__":
    __main__()
