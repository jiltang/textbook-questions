import torch
import torch.nn as nn

device = 'cpu'

class Embedding(nn.Module):
    def __init__(self, vocab, emb_dim, trainable=False):
        super(Embedding, self).__init__()
        self.embed = nn.Embedding(len(vocab), emb_dim)
        self.embed.weight.data.copy_(vocab.vectors)
        self.embed.weight.requires_grad = trainable
    def forward(self, x):
        out = self.embed(x)
        return out

class EncoderRNN(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(EncoderRNN, self).__init__()
        self.hidden_size = hidden_size
        self.gru = nn.GRU(input_size, hidden_size)

    def forward(self, embedded, hidden):
        print(embedded.shape)
        output = embedded.unsqueeze(0)
        print(output, hidden)
        output, hidden = self.gru(output, hidden)
        return output, hidden

    def initHidden(self, batch_size):
        return torch.zeros(1, batch_size, self.hidden_size, device=device)

class DecoderRNN(nn.Module):
    def __init__(self, hidden_size, output_size, dropout_p=0.1, max_length=100):
        super(DecoderRNN, self).__init__()
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.dropout_p = dropout_p
        self.max_length = max_length

        self.embedding = nn.Embedding(self.output_size, self.hidden_size)
        self.attn = nn.Linear(self.hidden_size * 2, self.max_length)
        self.attn_combine = nn.Linear(self.hidden_size * 2, self.hidden_size)
        self.dropout = nn.Dropout(self.dropout_p)
        self.gru = nn.GRU(self.hidden_size, self.hidden_size)
        self.out = nn.Linear(self.hidden_size, self.output_size)

    def forward(self, input, hidden, encoder_outputs):
        embedded = self.embedding(input).view(1, 1, -1)
        embedded = self.dropout(embedded)

        attn_weights = F.softmax(
            self.attn(torch.cat((embedded[0], hidden[0]), 1)), dim=1)
        attn_applied = torch.bmm(attn_weights.unsqueeze(0),
                                 encoder_outputs.unsqueeze(0))

        output = torch.cat((embedded[0], attn_applied[0]), 1)
        output = self.attn_combine(output).unsqueeze(0)

        output = F.relu(output)
        output, hidden = self.gru(output, hidden)

        output = F.log_softmax(self.out(output[0]), dim=1)
        return output, hidden, attn_weights

    def initHidden(self):
        return torch.zeros(1, 1, self.hidden_size, device=device)


# class EncoderDecoder(nn.Module):
#     def __init__(self, vocab, hidden_dim):
#         emb_dim = vocab.vectors.shape[1]
#         print("Embedding dim is", emb_dim)
#         self.embedding = Embedding(vocab, emb_dim)
#         self.encoder = EncoderRNN(emb_dim, hidden_dim)
#         self.decoder = DecoderRNN(hidden_dim, emb_dim)
#     def forward(self, x):
#         optimizer.zero_grad()
#         # encoder_optimizer.zero_grad()
#         # decoder_optimizer.zero_grad()
#
#         input_length = input_tensor.shape[1])
#         target_length = target_tensor.size(0)
#
#         encoder_outputs = torch.zeros(batch_size, max_length, encoder.hidden_size, device=device)
#
#         loss = 0
#
#         for ei in range(input_length):
#             encoder_output, encoder_hidden = encoder(x[:, ei], encoder_hidden)
#             encoder_outputs[:, ei] = encoder_output[0, 0]
#
#         decoder_input = torch.tensor([[SOS_token]], device=device)
#
#         decoder_hidden = encoder_hidden
#
#         use_teacher_forcing = True if random.random() < teacher_forcing_ratio else False
#
#         if use_teacher_forcing:
#             # Teacher forcing: Feed the target as the next input
#             for di in range(target_length):
#                 decoder_output, decoder_hidden, decoder_attention = decoder(
#                     decoder_input, decoder_hidden, encoder_outputs)
#                 loss += criterion(decoder_output, target_tensor[di])
#                 decoder_input = target_tensor[di]  # Teacher forcing
#
#         else:
#             # Without teacher forcing: use its own predictions as the next input
#             for di in range(target_length):
#                 decoder_output, decoder_hidden, decoder_attention = decoder(
#                     decoder_input, decoder_hidden, encoder_outputs)
#                 topv, topi = decoder_output.topk(1)
#                 decoder_input = topi.squeeze().detach()  # detach from history as input
#
#                 loss += criterion(decoder_output, target_tensor[di])
#                 if decoder_input.item() == EOS_token:
#                     break
#         x = self.embedding(x)
#         x = self.encoder(x)
#         x = self.decoder(x)
#         return x
