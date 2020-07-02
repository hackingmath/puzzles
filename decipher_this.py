def decipher_this(string):
    result = [] #list for output
    text_list = string.split(' ')
    for word in text_list:
        word_out = '' #output for deciphered word
        word_list = list(word)
        num = '' #collect digits in a string
        for character in word_list:
            if character.isdigit():
                num += character
        length_num = len(num) #number of digits in word
        word_out += chr(int(num))
        letters = len(word) - length_num
        if letters > 1:
            word_list[-1],word_list[length_num] = word_list[length_num],word_list[-1]
            word_out += ''.join(word_list[length_num:])
        if letters == 1:
            word_out += word_list[length_num]
        result.append(word_out)
        
    return ' '.join(result)
