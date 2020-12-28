from flask import current_app, Blueprint, render_template, request
from textblob import TextBlob
from tweepy import OAuthHandler

from ..models.base import db
from ..models import User, Tweet, TwitterClient, StreamListener
from datetime import datetime
from datetime import timedelta
import tweepy
from sqlalchemy import desc, asc
from ..config import Config

DIY_analysis = Blueprint('DIY_analysis', __name__, url_prefix='/')
api = TwitterClient()


'''
Tag mapping as what the short form means actually in tagging the text
'''
tags_mapping={
"CC":"coordinating conjunction",
"CD":"cardinal digit",
"DT":"determiner",
"EX":"existential there (like: 'there is' ... think of it like 'there exists')",
"FW":"foreign word",
"IN":"preposition/subordinating conjunction",
"JJ":"adjective	'big'",
"JJR":"adjective, comparative	'bigger'",
"JJS":"adjective, superlative	'biggest'",
"LS":"list marker	1)",
"MD":"modal	could, will",
"NN":"noun, singular 'desk'",
"NNS":"noun plural	'desks'",
"NNP":"proper noun, singular	'Harrison'",
"NNPS":"proper noun, plural	'Americans'",
"PDT":"predeterminer	'all the kids'",
"POS":"possessive ending	parent\'s",
"PRP":"personal pronoun	I, he, she",
"PRP$":"possessive pronoun	my, his, hers",
"RB":"adverb	very, silently,",
"RBR":"adverb, comparative	better",
"RBS":"adverb, superlative	best",
"RP":"particle	give up",
"TO":"to	go 'to' the store.",
"UH":"interjection	errrrrrrrm",
"VB":"verb, base form	take",
"VBD":"verb, past tense	took",
"VBG":"verb, gerund/present participle	taking",
"VBN":"verb, past participle	taken",
"VBP":"verb, sing. present, non-3d	take",
"VBZ":"verb, 3rd person sing. present	takes",
"WDT":"wh-determiner	which",
"WP":"wh-pronoun	who, what",
"WP$":"possessive wh-pronoun	whose",
"WRB":"wh-abverb	where, when",
}


# return the DIY_analysis and returns the result with custom positive and negative marking for sentimental
# it count all positive and negative and neutal also percentage and tags for words
@DIY_analysis.route('/DIY_analysis', methods=['GET', 'POST'])
def index():
    sentiment_text=""
    text=""
    if request.method == "POST":
        print(request.form)
        text = request.form.get("tweet-text")
        pos = request.form.get("positive-range")
        neg = request.form.get("negative-range")
        sentiment_text = TextBlob(text)
        result = "neutral"
        input_text = {"text": text}

        if sentiment_text.sentiment.polarity > float(pos):
            result = "positive"
            input_text["polarity"] = result
        elif sentiment_text.sentiment.polarity < float(neg):
            result = "negative"
            input_text["polarity"] = result
        else:
            result = "neutral"
            input_text["polarity"] = result

        if sentiment_text.sentiment.subjectivity < 0.5:
            input_text["subjectivity"] = "Objective"
        elif sentiment_text.sentiment.subjectivity >= 0.5:
            input_text["subjectivity"] = "Subjective"
        else:
            input_text["subjectivity"] = "None"

        word_list = text.split(" ")
        total_words = len(word_list)
        positive_words = []
        negative_words = []
        neutral_words = []
        total_words_positive = 0
        total_words_negative = 0
        total_words_neutral = 0
        for w in word_list:
            t = TextBlob(w)
            if t.sentiment.polarity > float(pos):
                positive_words.append(w)
                total_words_positive += 1
            elif t.sentiment.polarity < float(neg):
                negative_words.append(w)
                total_words_negative += 1
            else:
                neutral_words.append(w)
                total_words_neutral += 1

        positive = (total_words_positive/total_words)*100
        negative = (total_words_negative/total_words)*100
        neutral = (total_words_neutral/total_words)*100
        positive = round(positive, 2)
        negative = round(negative, 2)
        neutral = round(neutral, 2)
    else:
        text = "this is a test string and this world is great"
        pos = 0.2
        neg = -0.2
        sentiment_text = TextBlob(text)
        result = "neutral"
        input_text = {}
        input_text["text"] = text

        if sentiment_text.sentiment.polarity > float(pos):
            result = "positive"
            input_text["polarity"] = result
        elif sentiment_text.sentiment.polarity < float(neg):
            result = "negative"
            input_text["polarity"] = result
        else:
            result = "neutral"
            input_text["polarity"] = result

        if sentiment_text.sentiment.subjectivity < 0.5:
            input_text["subjectivity"] = "Objective"
        elif sentiment_text.sentiment.subjectivity >= 0.5:
            input_text["subjectivity"] = "Subjective"
        else:
            input_text["subjectivity"] = "None"

        word_list = text.split(" ")
        total_words = len(word_list)
        positive_words = []
        negative_words = []
        neutral_words = []
        total_words_positive = 0
        total_words_negative = 0
        total_words_neutral = 0
        for w in word_list:
            t = TextBlob(w)
            if t.sentiment.polarity > float(pos):
                positive_words.append(w)
                total_words_positive += 1
            elif t.sentiment.polarity < float(neg):
                negative_words.append(w)
                total_words_negative += 1
            else:
                neutral_words.append(w)
                total_words_neutral += 1
        positive = (total_words_positive / total_words) * 100
        negative = (total_words_negative / total_words) * 100
        neutral = (total_words_neutral / total_words) * 100
        positive = round(positive, 2)
        negative = round(negative, 2)
        neutral = round(neutral, 2)


    percentage = 0
    if result=="positive":
        percentage = sentiment_text.sentiment.polarity*100
    elif result=="negative":
        percentage = (0-sentiment_text.sentiment.polarity)*100
    else:
        percentage = 0
    print("sentiment_text:"+str(sentiment_text)+":")
    language = ""
    if sentiment_text is not None:
        language = sentiment_text.detect_language()

    print("language:"+language)
    tags = sentiment_text.tags

    return render_template('DIY_analysis.html',
                           total_words=total_words,
                           result=result,
                           total_words_positive=total_words_positive,
                           total_words_negative=total_words_negative,
                           total_words_neutral=total_words_neutral,
                           positive_words=positive_words,
                           negative_words=negative_words,
                           neutral_words=neutral_words,
                           text=input_text,
                           positive=positive,
                           negative=negative,
                           neutral=neutral,
                            percentage=percentage,
                           language=language,
                           tags=tags,
                           tags_mapping=tags_mapping
                           )
