import os
# 시각화 툴관련
from matplotlib import pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import matplotlib as mpl
import warnings
warnings.filterwarnings(action='ignore') # warning 안뜨게 하기
# 유니코드 깨짐현상 해결
mpl.rcParams['axes.unicode_minus'] = False
# 나눔고딕 폰트 적용
plt.rcParams["font.family"] = 'NanumGothic'

from slacker import Slacker
slack = Slacker('xoxb-1584555113616-1705132466806-ex3Od3eiEuXvhVT7nmZ9XqKR')

import pandas as pd
from glob import glob
file_dir = 'data/*'

file_list = sorted(glob(file_dir))
# 파일 너무 많이 쌓이지 않도록 정리
if len(file_list)>10:
    for i in file_list[:-10]:
        os.remove(i)
print('--------------------------------')
file_list = file_list[-2:]
def get_merged_csv(flist, **kwargs):
    return pd.concat([pd.read_csv(f, **kwargs) for f in flist], ignore_index=True)

df = get_merged_csv(file_list, index_col=None)

df['datetime'] = pd.to_datetime('2021-'+ df['date']+' '+df['time'], format="%Y-%m-%d %H:%M")

df_reply = df[['title','datetime','reply']]
df_reply.set_index(['title','datetime'], inplace=True)
df_reply.sort_index(inplace=True)
df_reply = df_reply.unstack('datetime').droplevel(0, axis=1)
df_reply = df_reply.dropna(subset=[df_reply.columns[-2]])
df_reply = df_reply[df_reply.columns[-10:]]

df_views = df[['title','datetime','views']]
df_views.set_index(['title','datetime'], inplace=True)
df_views.sort_index(inplace=True)
df_views = df_views.unstack('datetime').droplevel(0, axis=1)
df_views = df_views.dropna(subset=[df_views.columns[-2]])
df_views = df_views[df_views.columns[-10:]]


issue = set(df_reply[df_reply.iloc[:,-1] - df_reply.iloc[:,-2] >=40].index) &\
set(df_views[df_views.iloc[:,-1] - df_views.iloc[:,-2] >=4000].index) &\
set(df_reply[df_reply.iloc[:,-2] - df_reply.iloc[:,-3] >=40].index) &\
set(df_views[df_views.iloc[:,-2] - df_views.iloc[:,-3] >=4000].index)

plt.figure(figsize=(14,10))
if issue:
    sns.lineplot(data=df_views.T[issue])
    plt.savefig('image.png')
    slack.chat.post_message('issue', '\n'.join(list(issue)))
    slack.files.upload('./image.png', channels='issue')