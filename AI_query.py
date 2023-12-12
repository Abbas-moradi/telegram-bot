from gensim.models import Word2Vec

data = [
    {"question": "چطور اطلاعات حساب کاربری را تغییر دهم؟", "answer": "برای تغییر اطلاعات حساب کاربری به قسمت تنظیمات مراجعه کنید."},
    {"question": "سلام چطور می‌توانم به شما کمک کنم؟", "answer": "سلام! خوش آمدید. لطفاً سوال خود را بپرسید."},
]

sentences = [question["question"].split() for question in data]

model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, workers=4)


from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def get_most_similar_question(input_text):
    input_vector = np.mean([model.wv[word] for word in input_text.split() if word in model.wv], axis=0)

    similarities = [cosine_similarity([input_vector], [model.wv[word] for word in question["question"].split() if word in model.wv])[0][0] for question in data]

    most_similar_index = np.argmax(similarities)
    most_similar_question = data[most_similar_index]["question"]
    most_similar_answer = data[most_similar_index]["answer"]

    return most_similar_question, most_similar_answer


user_input = "کمک"
most_similar_question, most_similar_answer = get_most_similar_question(user_input)

print(f"سوال شما: {user_input}")
print(f"سوال مشابه: {most_similar_question}")
print(f"پاسخ: {most_similar_answer}")
