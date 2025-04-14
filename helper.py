from wordcloud import WordCloud
import matplotlib.pyplot as plt
from urlextract import URLExtract

def fetch_stats(df, selected_user):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    num_words = df['message'].str.split().apply(len).sum()
    num_media = df[df['message'] == '<Media omitted>\n'].shape[0]

    ex = URLExtract()
    urls = []
    for message in df['message']:
        urls.extend(ex.find_urls(message))
    num_links = len(urls)

    return num_messages, num_words, num_media, num_links, urls





def fetch_most_active_users(df):
    x = df['user'].value_counts().head()
    df = round(df['user'].value_counts() / df.shape[0] * 100, 2)
    df = df.reset_index().rename(columns={'index': 'user', 'user': 'percentage'})
    return x, df






def create_wordcloud(df, selected_users):

    if selected_users != 'Overall':
        df = df[df['user'] == selected_users]

    wc = WordCloud(width=500, height=500, background_color='white')
    wc_image = wc.generate(df['message'].str.cat(sep=" "))

    return wc_image