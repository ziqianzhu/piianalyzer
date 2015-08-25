import pandas as pd
from commonregex import CommonRegex
from nltk.tag.stanford import StanfordNERTagger


class PiiAnalyzer(object):
    def __init__(self, filepath):
        self.filepath = filepath

    def analysis(self):
        # reading and preparing the data
        data = pd.read_csv(self.filepath, parse_dates=True).fillna('').to_string(index=False, header=False)
        cleaned_data = ' '.join(data.split())
        split_data = list(set(i.title() for i in cleaned_data.split()))

        # setting up parsers
        standford_ner = StanfordNERTagger('classifiers/english.conll.4class.distsim.crf.ser.gz')
        parser = CommonRegex()

        people = []
        organizations = []
        locations = []

        # using standford ner
        for title, tag in standford_ner.tag(split_data):
            if tag == 'PERSON':
                people.append(title)
            if tag == 'LOCATION':
                locations.append(title)
            if tag == 'ORGANIZATION':
                organizations.append(title)

        # using regex
        emails = parser.emails(cleaned_data)
        phone_numbers = parser.phones(cleaned_data)
        street_addresses = parser.street_addresses(cleaned_data)
        credit_cards = parser.credit_cards(cleaned_data)
        ips = parser.ips(cleaned_data)

        return {'people': people, 'locations': locations, 'organizations': organizations,
                'emails': emails, 'phone_numbers': phone_numbers, 'street_addresses': street_addresses,
                'credit_cards': credit_cards, 'ips': ips
                }