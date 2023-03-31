from TamilNLP import Tamil
import pandas as pd
import nltk
import pickle 

news = pd.read_csv("./TamilNLP/tamilmurasu_dataset.csv")

tamil_text = news["news_article"][15]

tamil_text_new = tamil_text

tamil_text = Tamil.Tamil(tamil_text)
tamil_text.summarize()

print("Actual Text")
print(tamil_text)

z = nltk.sent_tokenize(tamil_text_new)

data = pd.read_csv("./TamilNLP/values.txt")
cols = data.shape[1]

X = data.iloc[:,0:cols]

model = pickle.load(open("final_model.sav", 'rb'))
Y = model.predict(X)

print("\n\nModel Prediction")
print(Y)
p=""

for i in range(len(Y)):
    if Y[i]==1:
        p+=z[i]

print("\n\nSummary")
print(p)



