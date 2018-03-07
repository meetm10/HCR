import numpy as np

def load_data(filename):
    with open(filename,'r') as f:
        content = f.read()

    lines = content

    #print(lines)

    char_set = set()
    vocabulary = []
    
    for char in lines:
        if char not in char_set:
            char_set.add(char)
            vocabulary.append(char)    
        
    #for i,char in enumerate(char_set):
        #print("{0}:{1}".format(i,char))
    return lines,vocabulary

def encode_int(text,vocabulary):
	#Takes in a string of "text" and vocabulary (list of all possible output characters)
	#Returns a list of integers encoding every character w.r.t its position in vocabulary
	list_chars = list(text)
	#Returns a list of indices
	return [vocabulary.index(char) for char in list_chars]


def one_hot(text,vocabulary):
    vocab_size = len(vocabulary)

    z = encode_int(text,vocabulary)
    
    #Takes in a list of ints:
    
    #Returns a 2d Array
    print("New one_hot")
    one_hot_array = np.zeros([len(z),vocab_size]).astype(np.float32)
    for i in range(len(z)):
        el = z[i]
        one_hot_array[i][el] = 1
    
    return one_hot_array

#ToDO: Add batch_size feature.... (multiple samples in single batch)
def create_chunks(input_sequence,output_sequence,vocab_size,sequence_size=25,batch_size=1):
    
    chunks = []
    #Break down data into chunks .. of sequence_size
    for sample_start in range(0,len(input_sequence),sequence_size):
        input_sample = one_hot(input_sequence[sample_start:sample_start+sequence_size],vocab_size)
        output_sample = one_hot(output_sequence[sample_start:sample_start+sequence_size],vocab_size)
        chunks.append( (input_sample,output_sample) )
        
    return chunks


def interpret(y,vocabulary):    
    interpretation = []
    for i in range(y[0].shape[0]):
        index = np.argmax(y[0][i])
        #print(index)
        interpretation.append(vocabulary[index])
    cont = "".join(interpretation)
    #print(cont)
    return cont

def stack_batches(batch_size,chunks):
    pass
    #return input_batches