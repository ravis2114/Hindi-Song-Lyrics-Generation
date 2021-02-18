# creating TPU environment to create model architecture and initialize architecture's variable on TPU
import os
import tensorflow as tf

resolver = tf.distribute.cluster_resolver.TPUClusterResolver(tpu='grpc://' + os.environ['COLAB_TPU_ADDR'])
tf.config.experimental_connect_to_cluster(resolver)
# This is the TPU initialization code that has to be at the beginning.
tf.tpu.experimental.initialize_tpu_system(resolver)
# create a distribution stratagy
strategy = tf.distribute.TPUStrategy(resolver)



#importing basic libraries
import string
import os
import numpy as np

#generated data path
txt_gen = 'txt_gen/'

# reading dataset generated using clean_data.py file (train_songs.txt)
with open(txt_gen + 'train_songs.txt', encoding='utf-8') as f:
  df = f.read()
  df = df.split('\n')


# tokenizing list of sentences
from tensorflow.keras.preprocessing.text import Tokenizer
tokenizer = Tokenizer()
tokenizer.fit_on_texts(df)
sequences = tokenizer.texts_to_sequences(df)

# final training dataset
seq = np.array(sequences)
x,y = seq[:,:-1], seq[:,-1]


# vocab size is total number of unique words plus one for unknown word if present(this is important for embedding layer)
vocab_size = len(tokenizer.word_index) + 1



#model Architecture
import tensorflow as tf
from tensorflow.keras.models import  Sequential, load_model
from tensorflow.keras.layers import Dense, LSTM, Embedding

#model creation to use in TPU
def create_model():
  return tf.keras.Sequential(
      [Embedding(vocab_size, 69, input_length=x.shape[1]), #69 is embedding dimension
       LSTM(128, return_sequences=True),
       LSTM(128),
       Dense(100, activation='relu'),
       Dense(vocab_size, activation='softmax')])


#Note that Keras model creation needs to be inside strategy.scope, so the variables can be created on each TPU device. Other parts of the code is not necessary to be inside the strategy scope.

# creating model inside TPU
with strategy.scope():
  model = create_model()
  loss_fn=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
  model.compile(optimizer='adam', loss=loss_fn, metrics=['sparse_categorical_accuracy'])

  #load model if you want to train pre-trained model
  #model = load_model(txt_gen + 'lyrics.h5') #comment this and use above method to create model if you want to create a fresh model to train


#training...
model.fit(x=x, y=y, batch_size=4096, epochs=1000)



# generating song lyrics (next 50 words..., change this value accordingly)
from tensorflow.keras.preprocessing.sequence import pad_sequences

# randon seed text from google search
sng = 'मेरी नज़र का सफ़र तुझपे ही आके रुके कहने को' #'तू आता है सीने में जब जब सांसें भारती हूँ' use this as another example song from the movie MS DHONI
seed_text = tokenizer.texts_to_sequences([sng])[0] #sequences[randint(0,len(sequences))] use from training data itself if not from google search or typing

generated_song = []
for i in range(50):
  input_text = seed_text
  pad_seq = pad_sequences([input_text],maxlen=10, truncating='pre') #after appending after next iteration, it removes(tranucates) all words left to last 10(maxlen, change this value based on your sequencial data) words
  pred = model.predict(pad_seq) # outputs vector of length of vocab_size
  input_text.append(np.argmax(pred)) #argmax gets the index of maximum value
  generated_song.append(tokenizer.index_word[np.argmax(pred)]) # value of index of max value is supplied to index to word dict generated after fitting tokenizer


print('-------seed text---------------')
print(tokenizer.sequences_to_texts([seed_text[:10]])) #seed text, slicing is being done here coz during appending input_text, seed_text also got appended

print('-------generated text---------------')
for i in range(0,len(generated_song),10):
  print(' '.join(generated_song[i:i+10]))


'''
# outputs some funny results
-------seed text---------------
['मेरी नज़र का सफ़र तुझपे ही आके रुके कहने को']
-------generated text---------------
बाक़ी है दुःख माँगूँ खोल होगी सुनी मैं से बोले
आऊं ओहो आपकी जो न हो ओ जी तुम कहो
तुम चाक चिकी रकक नाक ऊँचा वर छल रखना तेरे
वे चली क़दम छत कोल ना आज मुडियो वे दिन
का घूँघट पट भरी चमके काली अँगड़ाइयाँ नज़रें हो तलत
'''



#save model
model.save(txt_gen + 'lyrics.h5') # use it in line 68 if already saved and comment lines 63,64,65
