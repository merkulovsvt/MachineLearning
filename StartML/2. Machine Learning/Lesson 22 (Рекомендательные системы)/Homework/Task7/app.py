import os
from datetime import datetime
from typing import List

import pandas as pd
from catboost import CatBoostClassifier
from fastapi import FastAPI
from loguru import logger
from sqlalchemy import create_engine

from schema import PostGet

url = "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml"


def batch_load_sql(query: str) -> pd.DataFrame:
    CHUNKSIZE = 200000

    engine = create_engine(url)
    conn = engine.connect().execution_options(stream_results=True)
    chunks = []
    for chunk_dataframe in pd.read_sql(query, conn, chunksize=CHUNKSIZE):
        chunks.append(chunk_dataframe)
    conn.close()
    return pd.concat(chunks, ignore_index=True)

logger.info("Start features load")

user_data = batch_load_sql('SELECT * FROM "merkulovsvt_user_data_features_lesson_22"')
logger.info("user_data loaded")

post_data = batch_load_sql('SELECT * FROM "merkulovsvt_post_data_features_lesson_22"')
logger.info("post_data loaded")

feed_data = batch_load_sql('SELECT * FROM "merkulovsvt_feed_data_features_lesson_22"')
logger.info("feed_data loaded")

init_post_data = batch_load_sql("SELECT * FROM public.post_text_df")
logger.info("init_post_data loaded")

data = user_data.join(
    other=feed_data.set_index('user_id'),
    on='user_id',
    how='left'
).join(
    other=post_data.set_index('post_id'),
    on='post_id',
    how='left'
)
logger.info("data joined")

def get_model_path(path: str) -> str:
    if os.environ.get("IS_LMS") == "1":
        MODEL_PATH = '/workdir/user_input/model'
    else:
        MODEL_PATH = path
    return MODEL_PATH


def load_models():
    model_path = get_model_path("../Models/catboost_model")
    from_file = CatBoostClassifier()
    from_file.load_model(model_path)
    return from_file


model = load_models()
logger.info("model loaded")

app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
              title='SQLAlchemy API',
              description='Lesson10 API')


@app.get("/post/recommendations/", response_model=List[PostGet])
def get_recommended_feed(id: int, time: datetime, limit: int = 10) -> List[PostGet]:
    # формируем дф для предсказаний, на основе фичей всех постов и нашего юзера
    df = data[data['user_id'] != id].dropna().reset_index(drop=True)
    predict_prob = pd.DataFrame(model.predict_proba(df), columns=['prob1', 'prob2'])
    prob_df = pd.concat([df, predict_prob], axis=1).sort_values(['prob2'], ascending=False)
    post_ids = prob_df['post_id'].unique()[:limit]

    recommendation = []
    for id in post_ids:
        post = {
            "id": id,
            "text": init_post_data[init_post_data['post_id'] == id]['text'].values[0],
            "topic": init_post_data[init_post_data['post_id'] == id]['topic'].values[0]}
        recommendation.append(post)

    return recommendation
