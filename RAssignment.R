#----- Working directory

#getwd()
#setwd("C:\\Users\\monisha.premalat\\Downloads\\R assignment")

#----- Install Packages

# install.packages("readxl")
library(readxl)

# install.packages("dplyr")
library(dplyr)

# installing "plyr" package after dplyr , doesnt give proper results for groupby function

# install.packages('tidyr')
library(tidyr)

#----- Reading files

excel_sheets("SaleData.xlsx")

sales <- read_excel("SaleData.xlsx",sheet = "Sales Data")
# head(sales)

imdb <- read.csv("imdb.csv")
# head(imdb)

movie <- read.csv("movie_metadata.csv")
# head(movie)

diamonds <- read.csv("diamonds.csv",na.strings="") # convert blanks to NA
# head(diamonds)

#------------------------------------------------------

"
## Questions 1 - 6 Utilize the sales data set. 
`The sales data contians transactional sales information for each sales person. It also contains the date of sales, item sold , price of each item, sales amount, region and their corresponding manager information.`

1. Find the least amount sale that was done for each item. 
2. Compute the total sales for each year and region across all items
3. Create new column 'days_diff' with number of days difference between reference date passed and each order date
4. Create a dataframe with two columns: 'manager', 'list_of_salesmen'. Column 'manager' will contain the unique managers present and column 'list_of_salesmen' will contain an array of all salesmen under each manager.
5. For all regions find number of salesman and total sales. Return as a dataframe with three columns - Region, salesmen_count and total_sales
6. Create a dataframe with total sales as percentage for each manager. Dataframe to contain manager and percent_sales

"
str(sales)

# Changing data types
sales$OrderDate <- as.Date(sales$OrderDate)
sales$Orderyear <- format(sales$OrderDate,"%Y")

factor_col <- c(2:5,9)
sales[factor_col] <- lapply(sales[factor_col], function(x){as.factor(x)})

# Q1 Find least sales amount for each item

least_sales <- function(df){
  df %>%
    group_by(Item) %>%
    summarise(total_sales = min(Sale_amt))
}

least_sales(sales)

# Q2 compute total sales at each year X region X Item

sales_year_region <- function(df){
  df %>%
    group_by(Orderyear,Region,Item) %>%
    summarise(total_sales = sum(Sale_amt)) 
}
sales_year_region(sales)

# Q3 append column with no of days difference from present date to each order date

days_diff <- function(df){
  df$diff_in_days <- Sys.Date() - df$OrderDate
  return(df)
}
View(days_diff(sales)) 

# Q4 get dataframe with manager as first column and  salesman under them as lists in rows in second column.

#install.packages("data.table")
library(data.table)

mgr_slsmn <- function(df){
  x1 <- unique(df$Manager)
  x2 <- sapply(x1,function(x) {unique((filter(df,df$Manager==x))$SalesMan)})
  data.table(Managers = x1,list_salesman = x2)
}
mgr_slsmn(sales)

# Q5 For all regions find number of salesman and total sales

slsmn_units <- function(df){
  df %>%
    group_by(Region) %>%
    summarise(
      total_sales = sum(Sale_amt, na.rm = T),
      salesmen_count = length(unique(na.omit(SalesMan))))
}
slsmn_units(sales)

# Q6 Find total sales as percentage for each manager

sales_pct <- function(df){
  d <- df %>%
    group_by(Manager) %>%
    summarise(total_sales = sum(Sale_amt)) %>%
    mutate(percent_sales=paste0(round(100*total_sales/sum(total_sales),2),'%'))
  d1 <- subset(d, select = -c(total_sales))
  return(d1)
}

sales_pct(sales)

#----------------------------------
"
Questions 7 - 10 Utilize the imdb data set.The imdb data contains the 
rating and other information related to movies and episodes across a 
lot of generes and years
"
str(imdb)

# Q7 Get the imdb rating for fifth movie of dataframe

fifth_movie <- function(df){
  df[5,"imdbRating"]
}
fifth_movie(imdb)

# Q8 Return titles of movies with shortest and longest run time

imdb$duration <-  as.numeric(as.character(imdb$duration))
sum(is.na(imdb$duration))

movies <- function(df){
  subset(df,duration == max(df$duration,na.rm = TRUE) | duration == min(df$duration,na.rm = TRUE))['title']
  # df[(df$duration == max(df$duration,na.rm = TRUE)) | (df$duration == min(df$duration,na.rm = TRUE)),]
}
movies(imdb)

# Q9 sort by two columns - release_date (earliest) and Imdb rating(highest to lowest)

imdb$year <-  as.numeric(as.character(imdb$year))
imdb$imdbRating <-  as.numeric(as.character(imdb$imdbRating))

sort_df <- function(df){
  df[order(df['year'], -df['imdbRating']),]
}

View(sort_df(imdb))

# Q10 subset revenue more than 2 million and spent less than 1 million & duration between 30 mintues to 180 minutes

subset_df <- function(df){
  filter(df,gross>2000000,budget<1000000,30<=duration,duration<=180)
}

View(subset_df(movie)) 

#--------------------------------
"
# Questions 11 - 15 Utilize the diamonds data set.
`
The diamonds data set contains the various dimensions and information for each diamond.

11. Count the duplicate rows of diamonds DataFrame.
12. Drop rows in case of missing values in carat and cut columns.
13. Subset the dataframe with only numeric columns.
14. Compute volume as (x*y*z) when depth is greater than 60. 
    In case of depth less than 60 default volume to 8.
15. Impute missing price values with mean.
"

str(diamonds)

# Q11 count the duplicate rows of diamonds DataFrame.

dupl_rows <- function(df){
  nrow(df[duplicated(df),])
}
View(diamonds[duplicated(diamonds),])
dupl_rows(diamonds)

# Q12 droping those rows where any value in a row is missing in carat and cut columns

# library(tidyr)

drop_row <- function(df){
  df %>% drop_na(carat,cut)
}
View(drop_row(diamonds))
print(paste0("Before dropping missing rows : ",nrow(diamonds)))
print(paste0("After dropping missing rows : ",nrow(drop_row(diamonds))))

# Q13 subset only numeric columns

# diamonds[37,1]
numeric_columns <- c(1,5:10)
diamonds[numeric_columns] <- lapply(diamonds[numeric_columns], function(x){as.numeric(as.character(x))})

sub_numeric <- function(df){
  select_if(df, is.numeric)
}
View(sub_numeric(diamonds))

# Q14 compute volume as (x*y*z) when depth > 60 else 8

volume <- function(df){
  vol = df$x * df$y * df$z
  df$volume <- ifelse(df$depth > 60,vol,8)
  return(df)
}
View(volume(diamonds))

# Q15 impute missing price values with mean

impute <- function(df){
  df$price[is.na(df$price)] <- mean(df$price, na.rm = TRUE)
  return(df)
}
View(impute(diamonds))




