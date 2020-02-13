#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


# In[2]:


sales = pd.read_excel("SaleData.xlsx")
# sales.head(3)

imdb = pd.read_csv("imdb.csv", escapechar='\\')
# imdb.head(n=3)

diamonds = pd.read_csv("diamonds.csv")
# diamonds.head(n=3)

movie = pd.read_csv("movie_metadata.csv")
# movie.head(3)


# In[ ]:





# In[3]:


# Questions 1 - 6 Utilize the sales data set. 


# In[4]:


sales.dtypes


# In[5]:


# Q1 Find least sales amount for each item
def least_sales(df):
    ls = df.groupby(["Item"])["Sale_amt"].min().reset_index()
    return ls

least_sales(sales)


# In[6]:


# Q2 compute total sales at each year X region X Item

sales['year'] = sales['OrderDate'].dt.year

def sales_year_region(df):
    # write code to return pandas dataframe
    d = df.groupby(["year","Region","Item"])["Sale_amt"].sum().reset_index()
    return d

sales_year_region(sales).head(2)


# In[7]:


# Q3 append column with no of days difference from present date to each order date
def days_diff(df):
    # write code to return pandas dataframe
    df['days_diff'] = (pd.to_datetime("now") - df['OrderDate']).dt.days
    return(df)

days_diff(sales).head(2)


# In[8]:


# Q4 get dataframe with manager as first column and  salesman under them as lists in rows in second column.
def mgr_slsmn(df):
    # write code to return pandas dataframe
    d = df.groupby('Manager')['SalesMan'].apply(list).reset_index()
    d.rename(columns={'SalesMan':'list_of_salesmen'}, inplace=True)
    return(d)

mgr_slsmn(sales)


# In[9]:


# Q5 For all regions find number of salesman and number of units
def slsmn_units(df):
    # write code to return pandas dataframe
    d = df.groupby(["Region"])["SalesMan",'Units'].count().reset_index()
    return(d)

slsmn_units(sales)


# In[10]:


# Q6 Find total sales as percentage for each manager
def sales_pct(df):    
    d = df.groupby(['Manager'])
    d = d[['Sale_amt']].sum()
    d1 = d.apply(lambda x: 100*x/x.sum()).reset_index()
    d1.rename(columns={'Sale_amt':'percent_sales'}, inplace=True)
    return(d1)

sales_pct(sales)


# In[ ]:





# In[11]:


# Questions 7 - 10 Utilize the imdb data set 


# In[12]:


imdb.dtypes


# In[13]:


# Q7 get imdb rating for fifth movie of dataframe
def fifth_movie(df):
    print(df.loc[4,'imdbRating'])

fifth_movie(imdb)


# In[14]:


# Q8 return titles of movies with shortest and longest run time

imdb['duration'] = imdb['duration'].astype(str).astype(float)

def movies(df):
    d = df[(df['duration'] == df['duration'].max()) | (df['duration'] == df['duration'].min())]
    d = d[['title','imdbRating']]
    return(d)
    
movies(imdb)


# In[15]:


# Q9 sort by two columns - release_date (earliest) and Imdb rating(highest to lowest)
def sort_df(df):
    df.sort_values(['year', 'imdbRating'], ascending=[True, False])
    return df

sort_df(imdb).head(n=2)


# In[16]:


# Q10 subset revenue(gross) more than 2 million and spent(budget) less than 1 million & duration between 30 min to 180 min
def subset_df(df):
    d = df[(df['gross'] > 2000000) & (df['budget'] < 1000000) & (df['duration'] > 30) & (df['duration'] < 180)]
    return(d)

subset_df(movie).head(n=2)


# In[ ]:





# In[17]:


# Questions 11 - 15 Utilize the diamonds data set. 


# In[18]:


diamonds.dtypes


# In[19]:


# Q11 count the duplicate rows of diamonds DataFrame.
def dupl_rows(df):
    print("Duplicate rows of a DataFrame:")
    print(df.duplicated().sum())
    
dupl_rows(diamonds)


# In[20]:


# Q12 droping those rows where any value in a row is missing in carat and cut columns
def drop_row(df):
    print("Before dropping missing values")
    print(df.shape)
    d = df.dropna(subset=['carat', 'cut'])
    print("\nAfter dropping missing values")
    print(d.shape)

drop_row(diamonds)


# In[21]:


# Q13 subset only numeric columns

num_cols = ['carat', 'z']
diamonds[num_cols] = diamonds[num_cols].apply(pd.to_numeric, errors='coerce', axis=1)

def sub_numeric(df):
    d = df._get_numeric_data()
    return(d)
    
sub_numeric(diamonds).head(n=2)


# In[22]:


# Q14 compute volume as (x*y*z) when depth > 60 else 8
def volume(df):
    vol = df['x']*df['y']*df['z']
    df['volume'] = np.where(df['depth'] > 60, vol, 8)
    return df

volume(diamonds).head(2)


# In[23]:


# Q15 impute missing price values with mean
def impute(df):
    d = df.fillna(value=df.mean())
    return(d)

impute(diamonds).head(2)


# In[ ]:





# In[24]:


# Bonus Questions


# In[25]:


'''
1. Generate a report that tracks the various Genre combinations for each type year on year. 
The result data frame should contain type, Genre_combo, year, avg_rating, min_rating, max_rating, total_run_time_mins 
'''


# In[26]:


def bonus1(imdb):
    
    genre = imdb[['Action', 'Adult', 'Adventure', 'Animation', 'Biography',
       'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy',
       'FilmNoir', 'GameShow', 'History', 'Horror', 'Music', 'Musical',
       'Mystery', 'News', 'RealityTV', 'Romance', 'SciFi', 'Short', 'Sport',
       'TalkShow', 'Thriller', 'War', 'Western']] 
    
    lst = []
    for i in range(0,genre.shape[0]):
        d = genre.columns[genre.iloc[i,]==1].tolist()
        lst.append(d)

    imdb['Genre_combo'] = lst
    imdb['Genre_combo'] = imdb['Genre_combo'].astype(str)
    
    g = imdb.groupby(['year','type','Genre_combo']).agg({'imdbRating':['mean','min','max'],
                                                        'duration':'sum'})

    return(g)

bonus1(imdb).head(3)


# In[27]:


'''2. Is there a relation between the length of a movie title and the ratings ? 
Generate a report that captures the trend of the number of letters in movies titles over years. 
We expect a cross tab between the year of the video release and the quantile that length fall under. 
The results should contain year, min_length, max_length, num_videos_less_than25Percentile, 
num_videos_25_50Percentile , num_videos_50_75Percentile, num_videos_greaterthan75Precentile '''


# In[28]:


def bonus2(imdb):
    
    ## relation between the length of a movie title and the ratings
    imdb['title'] = imdb['title'].str[:-6]
    imdb['title_length'] = imdb['title'].str.len()

    # calculate the correlation between two variables - length of a movie title and the ratings

    cor = imdb['title_length'].corr(imdb['imdbRating'])
    print('Pearsons correlation - length of a movie title and the ratings: %.3f' % cor)

    #-------------
    
    imdb['TitleLength_Quantiles'] = pd.qcut(imdb['title_length'], 4, labels = ['0-25','25-50','50-75','75-100'])

    g1 = imdb.groupby(['year']).agg({'title_length':['min','max']})
    # g1.head(3)

    g2 = pd.crosstab(imdb['year'], imdb['TitleLength_Quantiles'])
    # g2.head(3)

    d = pd.concat([g1, g2], axis=1)
    
    return(d)

bonus2(imdb).head(3)


# In[29]:


'''
3. In diamonds data set Using the volumne calculated above, create bins that have equal population within them. 
Generate a report that contains cross tab between bins and cut.
Represent the number under each cell as a percentage of total.
'''


# In[30]:


def bonus3(diamonds):
    
    diamonds['bins'] = pd.qcut(diamonds['volume'], 10)
    #diamonds['bins']
    
    d = pd.crosstab(diamonds['bins'],diamonds['cut'], normalize='all') * 100
    return(d)

bonus3(diamonds)


# In[31]:


'''
4. Generate a report that tracks the Avg. imdb rating quarter on quarter,
in the last 10 years, for movies that are top performing. 
You can take the top 10% grossing movies every quarter. 
Add the number of top performing movies under each genere in the report as well.'''


# In[32]:


# Data merge is of no use because there are some "tid" which are not present in imdb data but present in "movie_metadata"
# so there is loss of genre info. in combined data

# Have done string split on "generes" columns in movies data to avoid loss of info when doing data merge
#---------------------------------

# imdb = pd.read_csv("imdb.csv",escapechar='\\')
# # imdb.head(3)

# data = pd.merge(movie, imdb, how='left', on='tid')
# # data.head(2)


# In[33]:


movie['tid'] = movie['movie_imdb_link'].str[26:35]
movie.drop_duplicates(subset = 'tid', inplace=True)


# In[34]:


# n=0.1

def bonus4(movie,n):
    
    movie["genres"] = movie["genres"].str.split("|",expand = False) 
    
    for genres in set.union(*movie.genres.apply(set)):
        movie[genres] = movie.apply(lambda _: int(_.genres.count(genres)), axis=1)
    
    q1 = [2007, 2008, 2009]
    q2 = [2010, 2011, 2012]
    q3 = [2013, 2014, 2015]
    q4 = [2016]

    a = [q1,q2,q3,q4]
    b = ['q1','q2','q3','q4']

    for i in a:
        movie.loc[movie['title_year'].isin(i),'quarter_year'] = b[a.index(i)]

    df = movie[movie['quarter_year'].isin(b)]

    df1 = (df.groupby('quarter_year',group_keys=False)
            .apply(lambda x: x.nlargest(int(len(x) * n), 'gross')))

    # df1.groupby('quarter_year')['imdb_score'].mean()
    
    lst = df1.iloc[:,29:].columns.tolist()
    df2 = df1.groupby('quarter_year')[lst].sum()
    df2['avg_imdb'] = df1.groupby('quarter_year')['imdb_score'].mean()
    
    return(df2)

bonus4(movie,0.1).head(3)


# In[35]:


'''
5. Bucket the movies into deciles using the duration. 
Generate the report that tracks various features like nomiations, wins, count, top 3 genres in each decile.
'''


# In[36]:


# n = 3

def bonus5(imdb,n):
    
    imdb["DecilesDuration"] = pd.qcut(imdb['duration'], 10)
    
    genre = ['Action', 'Adult', 'Adventure', 'Animation', 'Biography',
       'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy',
       'FilmNoir', 'GameShow', 'History', 'Horror', 'Music', 'Musical',
       'Mystery', 'News', 'RealityTV', 'Romance', 'SciFi', 'Short', 'Sport',
       'TalkShow', 'Thriller', 'War', 'Western']
    
    df = imdb.groupby('DecilesDuration')[genre].sum()
    # df

    arank = df.apply(np.argsort,axis=1)
    ranked_cols = df.columns.to_series()[arank.values[:,::-1][:,:n]]
    df1 = pd.DataFrame(ranked_cols,index=df.index)
    
    df1['top3Genre'] = df1.values.tolist()
    df1.drop([0,1,2], axis = 1,inplace=True)
    
    df2 = imdb.groupby('DecilesDuration')['nrOfNominations','nrOfWins'].count()
    
    new_df = pd.concat([df2,df1], axis=1)
    
    return(new_df)

bonus5(imdb,3)

