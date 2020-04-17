import fasttext

model = fasttext.train_unsupervised('words.txt', model='skipgram')

model.save_model("embeddings.bin")
