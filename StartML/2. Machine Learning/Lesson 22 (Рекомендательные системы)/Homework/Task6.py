import numpy as np
import pandas as pd
from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sqlalchemy import create_engine


class DateTimeTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.dayofweek_feature_names = None
        self.month_feature_names = None
        self.hour_feature_names = None

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        hour_data = pd.cut(X.dt.hour, bins=[0, 6, 11, 18, 20, 23],
                           labels=['0-6', '7-11', '12-18', '19-20', '21-23'])

        hour_feature = pd.get_dummies(hour_data, drop_first=True)
        self.hour_feature_names = ['hour_7-11', 'hour_12-18', 'hour_19-20', 'hour_21-23']

        dayofweek_feature = pd.get_dummies(X.dt.dayofweek, drop_first=True, prefix='dayofweek')
        self.dayofweek_feature_names = dayofweek_feature.columns

        month_feature = pd.get_dummies(X.dt.month, drop_first=True, prefix='month')
        self.month_feature_names = month_feature.columns

        result = pd.concat([month_feature,
                            dayofweek_feature,
                            hour_feature], axis=1)

        return result

    def get_feature_names_out(self, input_features):
        return np.concatenate([self.month_feature_names, self.dayofweek_feature_names, self.hour_feature_names])


class AgeTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        age_data = pd.cut(X, bins=[0, 20, 30, 40, 50, float('inf')],
                          labels=['age0_20', 'age21_30', 'age31_40', 'age41_50', 'age50+'])

        age_feature = pd.get_dummies(age_data, drop_first=True)

        return age_feature

    def get_feature_names_out(self, input_features):
        return ['age21_30', 'age31_40', 'age41_50', 'age50+']


class TfidfClusterTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, max_df=0.8, min_df=2, stop_words='english'):
        self.max_df = max_df
        self.min_df = min_df
        self.stop_words = stop_words
        self.vectorizer = TfidfVectorizer(max_df=self.max_df,
                                          min_df=self.min_df,
                                          stop_words=self.stop_words)

    def fit(self, X, y=None):
        self.vectorizer.fit(raw_documents=X)
        return self

    def transform(self, X):
        tfidf_matrix = self.vectorizer.transform(X)
        res = KMeans(n_clusters=5).fit_transform(PCA(n_components=5).fit_transform(tfidf_matrix)) * -1
        return StandardScaler().fit_transform(res)

    def get_feature_names_out(self, input_features):
        return ['pca1', 'pca2', 'pca3', 'pca4', 'pca5']


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


def upload_user_features():
    user_data = batch_load_sql("SELECT * FROM public.user_data")

    t = [
        ('AgeTransformer', AgeTransformer(), 'age'),
        ('OneHotEncoder', OneHotEncoder(drop='first'), ['source', 'os', 'exp_group', 'gender']),
        # ('CatBoostEncoder', CatBoostEncoder(), ['city', 'country'])
    ]

    col_transform = ColumnTransformer(transformers=t,
                                      remainder='passthrough',
                                      force_int_remainder_cols=False)

    user_data = pd.DataFrame(col_transform.fit_transform(user_data),
                             columns=pd.Series(col_transform.get_feature_names_out()).apply(lambda x: x.split('__')[1]))

    user_data.to_sql('merkulovsvt_user_data_features_lesson_22',
                     con=create_engine(url),
                     index=False,
                     if_exists='replace')


def upload_post_features():
    post_data = batch_load_sql("SELECT * FROM public.post_text_df")

    t = [
        ('OneHotEncoder', OneHotEncoder(drop='first'), ['topic']),
        ('TF-IDF_Cluster', TfidfClusterTransformer(), 'text'),
    ]

    col_transform = ColumnTransformer(transformers=t,
                                      remainder='passthrough',
                                      force_int_remainder_cols=False)

    post_data = pd.DataFrame(col_transform.fit_transform(post_data),
                             columns=pd.Series(col_transform.get_feature_names_out()).apply(lambda x: x.split('__')[1]))

    post_data.to_sql('merkulovsvt_post_data_features_lesson_22',
                     con=create_engine(url),
                     index=False,
                     if_exists='replace')


def upload_feed_features():
    feed_data = batch_load_sql("SELECT * FROM public.feed_data LIMIT 2000000").sort_values('timestamp',
                                                                                           ascending=False)

    t = [
        ('DateTimeTransformer', DateTimeTransformer(), 'timestamp'),
        ('OneHotEncoder', OneHotEncoder(drop='first'), ['action'])
    ]

    col_transform = ColumnTransformer(transformers=t,
                                      remainder='passthrough',
                                      force_int_remainder_cols=False)

    feed_data = pd.DataFrame(col_transform.fit_transform(feed_data),
                             columns=pd.Series(col_transform.get_feature_names_out()).apply(lambda x: x.split('__')[1]))

    feed_data.to_sql('merkulovsvt_feed_data_features_lesson_22',
                     con=create_engine(url),
                     index=False,
                     if_exists='replace')


def load_features() -> pd.DataFrame:
    user_data = batch_load_sql('SELECT * FROM "merkulovsvt_user_data_features_lesson_22"')
    post_data = batch_load_sql('SELECT * FROM "merkulovsvt_post_data_features_lesson_22"')
    feed_data = batch_load_sql('SELECT * FROM "merkulovsvt_feed_data_features_lesson_22"')

    data = user_data.join(
        other=feed_data.set_index('user_id'),
        on='user_id',
        how='left'
    ).join(
        other=post_data.set_index('post_id'),
        on='post_id',
        how='left'
    )

    return data


upload_feed_features()
