import datetime
import pandas as pd
import random
import numpy as np

class Forum_Page:

    def __init__(self, name):
        self.__name = name
        self.__board = pd.DataFrame(columns = ['Title','Date', 'Author', 'Post', 'Votes'])
        self.__board.set_index('Title', inplace = True)
        self.__board['Votes'] = self.__board['Votes'].astype('int')
        self.__anon_words = self.__process('words.txt')
        
    
    def __process(self, filename):
        with open(filename,'r', encoding = 'UTF8') as file:
           result = [line.rstrip() for line in file]
        return result
        
    def __exists(self, title):
        return title in self.__board.index
    
    def checker(self):
        return self.__board.copy()
    
    def get_name(self):
        return self.__name        
    
    def __generate_anon(self):
        while True:
            user_wordchoice = '_'.join(random.choices(self.__anon_words, k=2))
            user_numbers = ''.join(random.sample(['0','1','2','3','4','5','6','7','8','9'], k=2))
            username = user_wordchoice + '_' + user_numbers
            if username not in list(self.__board['Author']):
                return username


    def add_post(self, title, post, author = None, date = None):
        if author == None or author == '':
            author = self.__generate_anon()
        if not date:
            date = str(datetime.date.today())
        if not self.__exists(title):
            votes = 0
            self.__board.loc[title] = [date, author, post, votes]
        return
    
    def delete_post(self, title):
        if self.__exists(title):
            self.__board.loc[title, 'Post'] = np.nan
            self.__board.loc[title, 'Author'] = np.nan
        return

    def vote_post(self, title, up = True):
        if self.__exists(title):
            votes = self.__board.loc[title, 'Votes']
            if up == True:
                self.__board.loc[title, 'Votes'] = votes + 1
            if up == False:
                self.__board.loc[title, 'Votes'] = votes - 1
        return
    
    def get_post_date_info(self, title):
        days_in_month = {'11':30, '12':31, '01':31, '03':31, '02':28, '04':30, '05':31, '06':30, '08':31, '07':31, '09':30, '10':31} #do not change or delete
        month_number = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'] #do not change or delete
        month_name = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 
                           'September', 'October', 'November', 'December'] #do not change or delete
        if self.__exists(title):
            month = int(self.__board.loc[title, 'Date'][5:7])
            nameof_month = month_name[month-1]
            month_num = self.__board.loc[title, 'Date'][-2:]
            if month_num[0] == '0':
                month_num = month_num[1:]
            year = int(self.__board.loc[title,'Date'][0:4])
            leap = (year%4 == 0 and year%100 != 0) or year % 400 == 0
            day = sum(days_in_month[mon] for mon in month_number[:month-1]) + int(month_num)
            if month > 2 and leap:
                day += 1
            if str(day).endswith('1'):
                suffix = 'st'
            elif str(day).endswith('2'):
                suffix = 'nd'
            elif str(day).endswith('3'):
                suffix = 'rd'
            else:
                suffix = 'th'
            date_info = title + ' posted on ' + nameof_month + ' ' + month_num + ', the ' + day + suffix + ' day of ' + year
            return date_info



           
    def __str__(self):
        name = self.get_name()
        active_posts = self.__board.copy()
        active_posts = active_posts.dropna()
        titles = list(active_posts.index)
        headers = '\n'.join(titles)
        header = 'Titles for ' + name + ':' + '\n' + headers
        return header
