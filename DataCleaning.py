import csv

files = ['Ate_10-31-24 16_46_48.csv', 'Bedrotting_10-31-24 16_55_20.csv', 'Beige flag_10-31-24 16_50_36.csv', 'Body tea_10-31-24 16_53_54.csv', 'Brat_10-31-24 16_52_29.csv', 'Coded_10-31-24 16_52_58.csv', 'Era_10-31-24 16_54_52.csv', 'Face card_10-31-24 16_53_26.csv', 'Flop_10-31-24 16_54_23.csv', 'Girl dinner_10-31-24 16_55_49.csv', 'Giving_10-31-24 16_51_33.csv', 'Onika burgers_10-31-24 16_56_45.csv', 'Pookie_10-31-24 16_48_13.csv', 'Queen_10-31-24 16_56_17.csv', 'Situationship_10-31-24 16_49_39.csv', 'Slay_10-31-24 16_47_45.csv', 'Yap_10-31-24 16_57_41.csv', 'Chronically online_10-31-24 16_46_20.csv', 'Delulu_10-31-24 16_48_41.csv', 'diva_10-31-24 16_52_01.csv', 'eating_10-31-24 16_47_16.csv', 'Queening_10-31-24 16_49_11.csv', 'Roman empire_10-31-24 16_50_07.csv', 'Serving_10-31-24 16_51_04.csv', 'Snatched_10-31-24 16_57_13.csv']
files2 = ['Skill issue_11-03-24 14_30_59.csv', 'Baby gonk_10-31-24 16_27_57.csv', 'Looksmaxxing_10-31-24 16_26_32.csv', 'Mogging_10-31-24 16_27_01.csv', 'nonchalant dreadhead_10-31-24 16_31_42.csv', 'nonchalant dreadhead_10-31-24 16_35_59.csv', 'Npc behavior_10-31-24 16_31_13.csv', 'Rizzler_10-31-24 16_24_38.csv', 'sussy baka_10-31-24 16_32_10.csv', 'Alpha_10-31-24 16_23_11.csv', 'Aura_10-31-24 16_23_41.csv', 'Edging_10-31-24 16_28_26.csv', 'Fanum Tax_10-31-24 16_25_06.csv', 'Freakbob_10-31-24 16_30_16.csv', 'Goated_10-31-24 16_29_49.csv', 'goofy ahh_10-31-24 16_35_28.csv', 'Goon_10-31-24 16_28_54.csv', 'Gooning_10-31-24 16_29_22.csv', 'Gyatt_10-31-24 16_22_39.csv', 'John pork_10-31-24 16_30_45.csv', 'Jonkler_10-31-24 16_33_08.csv', 'Mew_10-31-24 16_25_36.csv', 'Mewing_10-31-24 16_26_05.csv', 'Mog_10-31-24 16_27_29.csv', 'Rizz_10-31-24 16_24_09.csv', 'Sigma_10-31-24 16_21_42.csv', 'Skibidi_10-31-24 16_22_11.csv', 'tiktok rizz party_10-31-24 16_32_39.csv']
#files3 = files + files2
wordtimes = {}
wordviews = {}
wordhashtags = {}
hashtags = {}
all = {}

for file in files2:
  with open(file, 'r', encoding='utf-8') as f:
      dctReader = csv.DictReader(f)
      data = [row for row in dctReader]
      for dict in data:
        word = file.split('_')[0]
        word = word.lower()
        if word == 'baby gonk':
            word = 'baby gronk'
        
        viewcount = dict['views']
        if viewcount[-1] == 'K' or (viewcount[-1] != 'M' and len(viewcount) == 4):
          viewcount = float(viewcount[:-1]) * 0.001
        elif len(viewcount) == 3:
          viewcount = float(viewcount[:-1]) * 0.0001
        elif len(viewcount) == 2:
          viewcount = float(viewcount[:-1]) * 0.00001
        elif len(viewcount) == 1:
          viewcount = float(viewcount[:-1]) * 0.000001
        else:
          viewcount = float(viewcount[:-1])

        time = dict['date']
        
        dashcount = 0
        for char in time:
            if char =='-':
                dashcount +=1
        
        if 'h ago' in time:
            time = '2024-10-31'
        elif 'd ago' in time:
            time = '2024-10-' + str(31 - int(time[0]))
        elif 'm ago' in time:
            time = '2024-10-31'
        elif 'w ago' in time:
            time = '2024-10-' + str(31 - (int(time[0])*7))
        elif dashcount == 1:
            time = '2024-' + time
            
            
        text = dict['text']
        x = 0
        firsttag = ''
        for char in text:
          if firsttag == '' and char == '#':
            firsttag = x
          x += 1
        if firsttag != '':
            htext = text[firsttag:]
            textwords = htext.split(' ')
            for tag in textwords:
              if ('#' in tag) & ('fyp' not in tag) & ('viral' not in tag) & ('foryou' not in tag):
                tag = tag[1:]
                tag = tag.lower()
                set = word + ', ' + tag
                if set not in hashtags:
                  count = 1
                  hashtags[set] = {'word': word, 'hashtag': tag, 'count': 1}
                else:
                  hashtags[set]['count'] += 1
              
        wordtags = []
        if firsttag != '':
            for tag in textwords:
                tag = tag.lower()
                if ('#' in tag) & ('fyp' not in tag) & ('viral' not in tag) & ('foryou' not in tag):
                    tag = tag[1:]
                    wordtags += [tag]
            
        if word not in wordtimes:
          wordtimes[word] = {'word': word, 'dates': [time]}
          wordviews[word] = {'word': word, 'views': viewcount}
          all[word] = [{'category': 'general', 'word': word, 'date': time, 'views': viewcount, 'text': text, 'hashtags': wordtags, 'link': dict['link']}]
        else:
          wordtimes[word]['dates'] += [time]
          wordviews[word]['views'] += viewcount
          all[word] += [{'category': 'general', 'word': word, 'date': time, 'views': viewcount, 'text': text, 'hashtags': wordtags, 'link': dict['link']}]
              


for file in files:
  with open(file, 'r', encoding='utf-8') as f:
      dctReader = csv.DictReader(f)
      data = [row for row in dctReader]
      for dict in data:
        word = file.split('_')[0]
        word = word.lower()
        
        viewcount = dict['views']
        if viewcount[-1] == 'K' or (viewcount[-1] != 'M' and len(viewcount) == 4):
          viewcount = float(viewcount[:-1]) * 0.001
        elif len(viewcount) == 3:
          viewcount = float(viewcount[:-1]) * 0.0001
        elif len(viewcount) == 2:
          viewcount = float(viewcount[:-1]) * 0.00001
        elif len(viewcount) == 1:
          viewcount = float(viewcount[:-1]) * 0.000001
        else:
          viewcount = float(viewcount[:-1])

        time = dict['date']
        
        dashcount = 0
        for char in time:
            if char =='-':
                dashcount +=1
        
        if 'h ago' in time:
            time = '2024-10-31'
        elif 'd ago' in time:
            time = '2024-10-' + str(31 - int(time[0]))
        elif 'm ago' in time:
            time = '2024-10-31'
        elif 'w ago' in time:
            time = '2024-10-' + str(31 - (int(time[0])*7))
        elif dashcount == 1:
            time = '2024-' + time
            
            
        text = dict['text']
        x = 0
        firsttag = ''
        for char in text:
          if firsttag == '' and char == '#':
            firsttag = x
          x += 1
        if firsttag != '':
            htext = text[firsttag:]
            textwords = htext.split(' ')
            for tag in textwords:
              if ('#' in tag) & ('fyp' not in tag) & ('viral' not in tag) & ('foryou' not in tag):
                tag = tag[1:]
                tag = tag.lower()
                set = word + ', ' + tag
                if set not in hashtags:
                  count = 1
                  hashtags[set] = {'word': word, 'hashtag': tag, 'count': 1}
                else:
                  hashtags[set]['count'] += 1
              
        wordtags = []
        if firsttag != '':
            for tag in textwords:
                tag = tag.lower()
                if ('#' in tag) & ('fyp' not in tag) & ('viral' not in tag) & ('foryou' not in tag):
                    tag = tag[1:]
                    wordtags += [tag]
            
        if word not in wordtimes:
          wordtimes[word] = {'word': word, 'dates': [time]}
          wordviews[word] = {'word': word, 'views': viewcount}
          all[word] = [{'category': 'female', 'word': word, 'date': time, 'views': viewcount, 'text': text, 'hashtags': wordtags, 'link': dict['link']}]
        else:
          wordtimes[word]['dates'] += [time]
          wordviews[word]['views'] += viewcount
          all[word] += [{'category': 'female', 'word': word, 'date': time, 'views': viewcount, 'text': text, 'hashtags': wordtags, 'link': dict['link']}]
 


for word in all:
    columns = all[word][0].keys()

with open('All2.csv', 'w', newline = '', encoding='utf-8') as f1:
    dctWriter = csv.DictWriter(f1, fieldnames=columns)
    dctWriter.writeheader()
    for dict in all:
        dctWriter.writerows(all[dict])
