#!/bin/bash
# run the line below only if the .pt files aren't already in place
# onmt_preprocess -train_src openNMTraw/src_train.txt -train_tgt openNMTraw/tgt_train.txt -valid_src openNMTraw/src_val.txt -valid_tgt openNMTraw/tgt_val.txt -save_data openNMTdata/
onmt_train -data openNMTdata/ -save_model opennmt-model
onmt_translate -model opennmt-model_acc_XX.XX_ppl_XXX.XX_eX.pt -src openNMTraw/src_test.txt -output openNMTdata/pred.txt -replace_unk -verbose
