#!/bin/bash
# run the commented-out lines only if the data files aren't already in place
# you'll have to install the glove embeddings into the specified directory
# onmt_preprocess -train_src openNMTraw/src_train.txt -train_tgt openNMTraw/tgt_train.txt -valid_src openNMTraw/src_val.txt -valid_tgt openNMTraw/tgt_val.txt -save_data openNMTdata/data
# OpenNMT-py-master/tools/embeddings_to_torch.py -emb_file_both glove_dir/glove.6B.100d.txt -dict_file openNMTdata/data.vocab.pt -output_file openNMTdata/embeddings
if [ "$1" == "-gpu" ]; then
	onmt_train -data openNMTdata/data -save_model opennmt-model -word_vec_size 100 -pre_word_vecs_enc openNMTdata/embeddings.enc.pt -pre_word_vecs_dec openNMTdata/embeddings.dec.pt $2
else
	onmt_train -data openNMTdata/data -save_model opennmt-model -word_vec_size 100 -pre_word_vecs_enc openNMTdata/embeddings.enc.pt -pre_word_vecs_dec openNMTdata/embeddings.dec.pt
fi
onmt_translate -model opennmt-model_acc_XX.XX_ppl_XXX.XX_eX.pt -src openNMTraw/src_test.txt -output openNMTdata/pred.txt -replace_unk -verbose
