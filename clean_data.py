import os
import string

files  = os.listdir('txt_gen')

'''
#run this code to remove all blank spaces from each song txt file
for i in files:
	with open('txt_gen/' + i, encoding='utf-8') as f:
		lines = f.readlines()

	with open('txt_gen/' + i, 'w', encoding='utf-8') as f:
		lines = filter(lambda x: x.strip(), lines)
		f.writelines(lines)


	with open('txt_gen/' + i, encoding='utf-8') as f:
		lines = f.read()
		
	with open('txt_gen/' + i, 'w', encoding='utf-8') as f:
		f.write(lines[:-1])
'''

song_list = []

for i in files:
    with open('txt_gen/' + i, encoding='utf-8') as f:
        song = f.read()
        #data preprocessing........
        table = str.maketrans('', '', string.ascii_letters + string.digits + string.punctuation + '०१२३४५६७८९') #x maps to y, and z gets replaced with none.
        song = song.translate(table) 

        song = song.split()
        song_list.append(song)





#finding total number of words in all songs
words = []
for i in range(len(song_list)):
    for j in range(len(song_list[i])):
        words.append(song_list[i][j])

word_vocab = set(words)
print('the number of songs : ', len(song_list))
print('-----------------------------------------------------')
print('total number of words in all songs are : ', len(words))
print('-----------------------------------------------------')
print('total number of unique words in all songs are : ', len(word_vocab))
print('-----------------------------------------------------')

print('#####################################################')
#selecting songs based on words it contains 
new_song_list = []
req_words = 50
for i in range(len(song_list)):
	if len(song_list[i]) > req_words:
		new_song_list.append(song_list[i])

#finding total number of words in all songs of new song list
new_words = []
for i in range(len(new_song_list)):
    for j in range(len(new_song_list[i])):
        new_words.append(new_song_list[i][j])
new_word_vocab = set(new_words)
print('total number of songs in new song list are : ', len(new_song_list))
print('-----------------------------------------------------')
print('total number of words in new songs list are : ', len(new_words))
print('-----------------------------------------------------')
print('total number of unique words in new song list : ', len(new_word_vocab))


#creating sequences.....
length = 10 + 1 #10 for timesteps and 1 for output, we can vary timesteps..
sequences = []
for i in range(len(new_song_list)):
	for j in range(length, len(new_song_list[i])):
		seq = new_song_list[i][j-length:j]
		line = ' '.join(seq)
		sequences.append(line)


with open('train_songs.txt','w', encoding='utf-8') as f:
	song_data = '\n'.join(sequences)
	f.write(song_data)





