from TamilNLP import Tamil
import pandas as pd

news = pd.read_csv("./TamilNLP/tamilmurasu_dataset.csv")
 
tamil_text = news["news_article"][14]

print("Initial Text")
print("")
print(tamil_text)
print("\n\n")

tamil_text = Tamil.Tamil(tamil_text)
tamil_text.summarize()
