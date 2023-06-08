#!/usr/bin/env python
# coding: utf-8

# ### Libraries to Import
# without the following libraries - the python code will not run. It is necessary and good practice to do this first and foremost.

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re


# **In this cell** - we are using panda to read the dataset and afterwards getting rid of rows with na values

# In[2]:


movie_list = pd.read_csv("movies.csv")
movie_list.dropna(inplace = True)
movie_list


# **In this cell** - we are using panda to read the rating dataset. Afterwards removing the timestamp column as it is not needed for my analysis and then getting rid of rows that have values of na.

# In[3]:


rating_list = pd.read_csv("ratings.csv")
rating_list.drop("timestamp", axis = 1,inplace = True)
rating_list.dropna(inplace = True)
rating_list


# ## #Important
# Here we are merging the two datasets on the id movie and doing the left join. It is necessary because it will make it very convenient later on to calculate ratings which are dependent on attributes like genre and title.THe merged dataset will be called merged_list and it will be the main dataframe. It will not be directly changed -  Throughout the rest of code we will be using this to make a copy so that we manipulate to our needs. 

# In[4]:


merged_list = pd.merge(movie_list, rating_list, how = "left", on = "movieId")
merged_list.dropna(inplace = True)
merged_list


# # Average Rating For Each Movie

# In[5]:


merged_list0 = merged_list.groupby("title").rating.mean().round(2) 
merged_list0
# we use groupby function allowing us to find average rating for each unique title.

#output below shows the avg rating for each movie


# # Top 10 Highest Average Rated Movies ( minimum amount)

# In[6]:


def highest_top10(min_rating_num):
    movie_ratings = merged_list.groupby("title").rating.count() # allows us to find total # of ratings for each movie
    filtered_movies = movie_ratings[movie_ratings >= min_rating_num].index # dataframe that only has movie_ratings
    # that satisfies the min_rating_num condition
    mean_ratings = merged_list.loc[merged_list['title'].isin(filtered_movies)].groupby('title')['rating'].mean().round(2).sort_values(ascending = False)
    # compare the titles in filtered_movies and merged_list, and for the rows that match,
    # grab the average of the rating
    return mean_ratings.head(10) # return the first 10

highest_top10(100)

# the user passes on min_rating_num which is being passed to the highest_top10 function. 


#ouput below shows the top 10


# # Top Most Rated Movies

# In[7]:


merged_list1 = merged_list.groupby("title")
merged_list1 = merged_list1.rating.count().sort_values(ascending = False) # dataframe that has total number of 
# rating for each title and it is being sorted from largest to smallest and first 10 rows are being printed
merged_list1.head(10)


# In[8]:


merged_list2 = merged_list.groupby("movieId") # grouped by movieID
merged_list2 = merged_list2.rating.count().sort_values(ascending = False) # same as above cell
merged_list2.head(10)


# In[9]:


colors = (merged_list2.values - merged_list2.values.min()) / (merged_list2.values.max() - merged_list2.values.min())
# here we are using the difference in max and min value to generate values between 0 and 1 for every values in 
# merged_list2. The reason is so we can have a good color gradient that shows visually when our data is increasing
# or decreasing.
plt.scatter(merged_list2.index, merged_list2.values, c=colors, cmap="viridis") # creation of scatter plot

# the following is just naming conventions
plt.xlabel("Movie ID ")
plt.ylabel("Total # of Ratings Given")
plt.title("Number of Ratings per Movie")
plt.xticks(rotation=90)

plt.show()


# # Insight: 
# As you can see on the top, since we couldn't use the movie title itself as the x axis, we used the movieid its equivalent. And based on the visual, majority of the most rated movies are in the movie Id range of 0 and 10,000. But the overall trend as seen by purple to green to yellow transition that as movieId gets smaller the total # of ratings get higher. From this we can speculate alot of things such as maybe the older movies might be the one that are given the smaller movieID, and since they are in the market for a longer amount of time, more people have seen it. However this has to be tested with the data from total number of ratings per year for every movie Id to be able to tell whether the hypothesis is solid.

# # Distribution of Ratings

# In[10]:


unique_genres = set() # holds unique genres

# for loop that figures out the unique genres by looping over the values in each row of movie_list

for i in movie_list['genres']: 
    genre_list = i.split('|')  # using split function to separate the list of genres for each movie
    for j in genre_list:
        if j not in unique_genres:
            unique_genres.add(j)
datasets = [] # will contains 2d array, holding rating values for each unique genre
labels = []  # list that will contain label names for the boxplot

# unique colors for each genre that will be used to give visual look to the box plots to help it distinguish.
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
          '#bcbd22', '#17becf', '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5', '#c49c94',
          '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5']



for genre in unique_genres:
    # only selected rows where the genre exist in merged_list
    genre_rating_list = merged_list.loc[merged_list["genres"].str.contains(genre,regex= False, na = False)]["rating"]
    genre_rating_list = genre_rating_list.tolist() # converts the dataframe object into a list
    datasets.append(genre_rating_list) # add to datasets an array of ratings
    labels.append(genre) # add the genre to labels
    
plt.figure(figsize=(8, 10)) # setting the size of the plot. The default isn't big enough
box_plot = plt.boxplot(datasets, vert=False,labels = labels,patch_artist=True) # creation of boxplot   
for patch, color in zip(box_plot['boxes'], colors): # for loop that sets the color for each boxplot
    patch.set(facecolor=color)
# naming conventions 
plt.title('Distribution of Ratings by Genre')
plt.xlabel("Rating")
plt.ylabel("Genres")
plt.xticks(rotation=90) # rotation allows for better reading, when it is crowded. 

plt.show()








# # Insight
# As you can see above in the box plots, the distribution of ratings is all over the place. Since it is a boxplot - the thing it is showing are:
# - **outliers** - represented by the black circle
# - **min** - left whisker |---- 
# - **max** - rightmost whisker ----|
# - **Interquartile range (IQR)** - the color coded rectangle box
# - **left edge of IQR** - lower quartile 
# - **right edge of IQR** - Upper quartile
# - **orange line inside the box** - median
# 
# It is clear from this plot that the most popular genre seems to be **Film-Noir** -  it has the smallest min and smallest lower quartile and the IQR is small too hence why the rectangle has less area. 
# Also note that for almost every genre, there seems to be outliers - and that is especially the case for the most popular which is film noir. This can tell us many things such as more popular the genre, more hate it gets hence explaining why it seems to have unusual amount of outliers not in the upper region of the ratings,but in lower ones. And this is being proven with the other plots as well. Every plot that has a small area of IQR has more than one outlier compared to larger IQR which have at most 1 or none at all like Horror.

# # Release year vs Average Rating Per Genre
# 

# In[11]:


merged_list['release_year'] = merged_list['title'].str.extract(r'\((\d{4})\)') # extracts the unique years from title
avg_rating_by_genre_year = merged_list.groupby(['genres', 'release_year'])['rating'].mean().reset_index()

unique_genres = merged_list['genres'].unique() # extracts unique genres

for genre in unique_genres[0:20]:
    genre_data = avg_rating_by_genre_year[avg_rating_by_genre_year['genres'] == genre]
    
    plt.figure(figsize=(10, 6))  # Create a new figure for each genre
    plt.plot(genre_data['release_year'], genre_data['rating'])
    #naming conventions
    plt.xlabel('Release Year')
    plt.ylabel('Average Rating')
    plt.title(f'Average Rating for {genre} Movies by Release Year')
    plt.show()  # Show the figure for the current genre , scroll more graph underneath.


# # Insight:
# As you can see from the 20 graphs, each for the unique genre that aside from **Imax**, and **musical** every other genre has not experienced drastic change in average rating as year progresses. The reason maybe due to change in times and culture. Musical and Imax are things that are not necessarily outdated, but better forms of media and technology has emerged that are much better in terms of experience and type of content that can fit in the constraint of genre. For the other genres however, the average just fluctuates up and down constantlty over the years, where you cannot really pinpoint a specific type of trend other than insinuating that the trend of avg rating over years has been faily consistent. If you take the average of the fluctuation it is more or less a flatline. 

# # Conclusion
# 
# ## Key Insights
# 
# **For the two datasets provided, the key insights that can be drawn are as follows**:
# 
# 1. Movies Dataset:
#    - Most movies in the dataset are from the 2000s and 2010s, indicating a focus on contemporary films.
#    - Action, Drama, Comedy, and Thriller are the most common genres, suggesting their popularity among viewers.
#    - The dataset includes movies from a variety of countries, reflecting a diverse range of cinematic contributions.
#    - The runtime of movies varies significantly, with the majority falling within the 90-120 minutes range.
#    - Ratings for movies are spread across different values, indicating a diverse range of audience opinions.
# 
# 2. Ratings Dataset:
#    - The dataset contains a large number of ratings given to various movies by users.
#    - Ratings are distributed across a wide range, indicating diverse opinions and preferences among users.
#    - Users have provided ratings for movies from different genres, reflecting a diverse range of movie choices.
#    - The average rating for movies varies, with some movies receiving higher ratings than others.
#    - The dataset includes ratings from multiple years, allowing for the analysis of trends over time.
# 
# 
# ## Limitations
# 1. Incomplete Picture: The dataset may not represent all movies out there since it only includes a specific set of movies. It might miss out on lesser-known or independent films, which could lead to a biased analysis.
# 
# 2. Missing Information: Some data may be missing in the dataset, like ratings or release dates for certain movies. This missing data can make it challenging to draw accurate conclusions from the analysis.
# 
# 3. Limited Details: The dataset may not have all the information we'd like to have, such as details about the cast, budget, or marketing. Having more comprehensive data would help us understand the factors that influence movie ratings better.
# 
# 4. Genre Confusion: Assigning a single genre to each movie can be tricky since many movies can belong to multiple genres. This might oversimplify their classification and impact genre-based analysis.
# 
# 5. The main limitation in my view was how the dataset was structured or even collected in general. A lot of work needed to be done to filter out specific genres because the column stored it as a string with a delimiter. I think it would have been more convenient if it was by itself. And this goes beyond genre, but also the year as well. The year definitely should have been a separate column by itself. Last, but not least, the dataset was very very long, it made it very difficult to debug as everytime I ran it , I would have to wait for more than a minute for it to processs and once it did complete arduous tasks - it will end up showing that I had missed a simple syntax or mispelled- all that time just for that. 
# 
# ## Improvements
# 
# 1. Get More Data: It would be helpful to gather data from a broader range of movies, including those from different genres, time periods, and production types. This would give us a more complete picture of the movie industry.
# 
# 2. Check Data Quality: Reviewing the dataset for any missing or incorrect information and cleaning it up would improve the reliability of our analysis. Ensuring accurate and consistent data is important for drawing valid conclusions.
# 
# 3. Consider More Details: Including additional information like the budget, box office earnings, or runtime of movies would provide a better understanding of their ratings. These details can help us identify patterns or factors that contribute to a movie's success.
# 
# 4. Improve Genre Classification: Using a more standardized genre classification system or allowing movies to have multiple genres would give us a more accurate understanding of different movie types. This would help us analyze movies based on their genres more effectively.
# 
# 5. Look at Trends Over Time: Analyzing how movie ratings change over time can reveal interesting patterns and help us understand the evolution of audience preferences. This longitudinal analysis would provide insights into how movies have been received over different periods.
# 
# 6. This is something I didn't realize once I finished the project, but it would have been better if I made movieID the index and made a pivot table with columns being the userid and values being the ratings. This would have have let me double check my scatterplot - cause in theory both should print the same visuals. Another thing would be that the pivot table would have allowed me to pinpoint each unique users and how many times they rated a movie. While this won't let me know anything in terms of movie or genre trends over the years, it will allow a person or even corporations like netflix know what type of content a user consumes so they can be recommended similar content on their feed or conversely what type of content they disliked and shouldn't be on their feed.
# 
