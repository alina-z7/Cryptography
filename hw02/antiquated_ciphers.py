added_commands = ["block5upper", "prepare_text", "caeser_cipher", "reorder", "permcipher_rand", "permutation_cipher", "substitution_cipher", "vigenere_cipher"]
print("added commands: " + ", ".join(added_commands))

import string

def block5upper(text):
    """
    Assume text is a string of lowercase letters (and possibly numbers); with no spaces or punctuation.

    Return the capitalized version, in five-letter blocks separated by spaces.
    """
    text = text.upper()
    blocks = [text[0]]
    for n in range(1,len(text)):
        if n % 5 == 0:
            blocks.append(" ")
        blocks.append(text[n])

    return "".join(blocks)

def prepare_text(plaintext):
    """
    Removes punctuation, and makes lowercase.
    """
    import string

    # remove punctuation & newlines
    out = plaintext.translate(str.maketrans("", "", string.punctuation))
    out = "".join(out.split("\n"))  # what about other control characters?
    # transform to lowercase
    out = out.lower()
    # remove spaces
    out = "".join(out.split(" "))
    return out


#caeser cipher from class
def caeser_cipher(tst, N, contains_numbers=False):
    """
    A more robust implementation of Caesar encryption (and decryption).

    Input: a message, possibly with punctution represented as a string.

    Output: the same letters shifted `N` places to the left in the alphabet (without punctuation and capitalized).
    """
    import string
    domain = string.ascii_lowercase
    codomain = string.ascii_uppercase
    if contains_numbers:
        domain = domain + '0123456789'
        codomain = codomain + '0123456789'
    D = len(domain)
    encryption_rule = {domain[n]:codomain[ (n + N) % D] for n in range(D)}

    # remove punctuation & transform to lowercase
    tst = tst.translate(str.maketrans("", "", string.punctuation))
    tst = tst.lower()
    # remove spaces
    tst = "".join(tst.split(" "))

    encrypt = "".join(encryption_rule[a] for a in tst)

    # group output in 5-letter blocks
    return block5upper(encrypt)

def reorder(string, perm):
    """
    A helper function for `permutation_cipher`.

    Assumes `len(string) == len(perm)`
    """
    #rearrange the characters of a string according to a permutation

    output = ''.join([string[i] for i in perm])
    return output

    output = ''
    for i in range(0, len(string)):
        output = output + string[perm[i]]

    return output


def permcipher_rand(plaintext, blocksize):
    """
    Input:
      - `plaintext` a string of plain text, suitably prepared (no spaces or punctuation)
      - `blocksize` an integer, used to build a random permutation of that length.

    Encrypt plaintext via the permutation cipher corresponding to randomly chosen permutation.
    """
    import random

    #create a random permutation of size blocksize, save as perm
    perm = []
    for j in range(0, blocksize):
        perm = perm + [j]
    random.shuffle(perm)

    return permutation_cipher(plaintext, perm)

def permutation_cipher(plaintext, perm):
    """
    Input:
      - `plaintext` a string of plain text, suitably prepared (no spaces or punctuation)
      - `perm` a permutation of some length (independent of length of `plaintext`)

    Encrypt plaintext via the permutation cipher corresponding to `perm`.
    """
    n = len(perm)

    #fill in plaintext to produce an even multiple of blocksize
    r = len(plaintext) % n
    plaintext = plaintext + 'x'*(n-r)

    #take out part of the plaintext, save as subplaintext, reorder and add to ciphertext
    ciphertext = ''
    for k in range(0, int(len(plaintext)/n)):
        subplaintext = plaintext[k * n : (k + 1) * n]
        ciphertext = ciphertext + reorder(subplaintext, perm)

    # display output in blocks of size 5, and uppercase
    return block5upper(ciphertext)


def substitution_cipher(plaintext, subs_dict):
    """
    Input:
      - `plaintext` a string of plain text, suitably prepared (no spaces or punctuation)
      - `subs_dict` a dictionary, describing a permutation/rearrangement of the domain

    Assumption: domain contains lowercase letters and possibly numbers.
    Assumption: allow for `subs_dict` to be a list, in which case it would be either of:
      + a "one line notation permutation" from input domain being ordered by lower_case + numbers
      + or a rearrangement of the numbers [0,...,25] or [0,...,35]

    Return: the encryption of plaintext via the substituion cipher corresponding to `subs_dict`.
    """
    import string
    domain = string.ascii_lowercase

    if isinstance(subs_dict, (list,tuple)):
        n = len(subs_dict)
        if n > 26:
            domain = domain + '0123456789'
        if isinstance(subs_dict[0], int):
            # build the corresponding rearrangement of `domain`
            subs_dict = [domain[i] for i in subs_dict]

        # convert the above list into a dictionary
        subs_dict = {domain[i]:subs_dict[i] for i in range(len(subs_dict))}
    else:
        assert isinstance(subs_dict, dict)

    #encryption of prepared plaintext
    msg = ''.join([subs_dict[lett] for lett in plaintext])
    return block5upper(msg)

def vigenere_cipher(msg, key, contains_numbers=False):
    """
    Input:
     - `msg` is a string of plain text, suitably prepared (no spaces or punctuation)
     - `key` the polyalphabetic caesar cipher instructions for Vigenere.
     - `contains_numbers` (optional) If True, then our caesar-shift cycle has length 36, not 26

    Return the vigenere cipher encryption of `msg` according to the keyword `key`.

    Allows `key` to be a word or a list of nonnegative integers between 0 and 35.
    """
    import string
    domain = string.ascii_lowercase
    if contains_numbers:
        domain = domain + '0123456789'
    D = len(domain)

    #We create the list of shifts for vigenere
    if isinstance(key, str):
        key = [domain.index(k) for k in key]

    #encrypt letter by letter
    encrypt = []
    for n in range (0,len(msg)):
        p = n % len(key) #which character of the key do we want to read?
        next_letter = caeser_cipher(msg[n], key[p], contains_numbers) #msg[n] is the nth plaintext character and key[p] is the pth letter-shift
        encrypt.append(next_letter)

    # print uppercase in five-letter blocks
    msg_e = "".join(encrypt)
    return block5upper(msg_e)