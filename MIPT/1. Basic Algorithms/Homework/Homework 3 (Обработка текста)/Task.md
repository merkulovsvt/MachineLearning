### Домашнее задание:

Реализовать предсказание настроений с помощью классических алгоритмов + **TF-IDF** на основе
данных [твиттов](https://www.kaggle.com/arkhoshghalb/twitter-sentiment-analysis-hatred-speech?select=train.csv) и
наивным байесом.

На "отлично" - попробовать обучить любой из пройденных алгоритмов на
основе [эмбеддингов взвешенных по attention](https://huggingface.co/sberbank-ai/sbert_large_nlu_ru) или с
помощью классических от TruncatedSVD на основе полиномиальных от **TF-IDF** с (1-3) биграммами.

Поскольку глубокие сети еще впереди код конвертации списка предложений в эмбеддинг по ссылке выше.

Т.к. мы чаще всего работаем с **numpy** массивами в обучении, используйте: `sentence_embeddings.detach().numpy()`