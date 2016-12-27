# twitter user name = @elonmusk

import markovify

# Get raw text as string.
with open("/corpus.txt") as f:
    text = f.read()

# markov model
text_model = markovify.Text(text)

# random sentences
for i in range(5):
    print(text_model.make_sentence())


# something that he could tweet
for i in range(3):
    print(text_model.make_short_sentence(140))


