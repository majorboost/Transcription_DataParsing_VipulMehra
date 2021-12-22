import json
import pandas as pd


class AwsTranscriptionProcessor:
    def __init__(self):
        self.__channel_speakers = {0: 'Provider', 1: 'Payer'}
        self.__segment_words = []
        self.__result_set = []
        self.__channel_tokens = []
        self.__result_set_classes = []
        self.__columns_for_df = ['Transcription', 'Start time', 'End time', 'Duration', 'Confidence']
        self.__no_class_label = "N.A."

    def __generate_df(self, data, labels):
        """
        Generates dataframe for data wrangling
        :param data: List of data
        :param labels: List of labels for each segment
        :return: dataframe
        """
        df = pd.DataFrame(data, columns=self.__columns_for_df)
        df['Participant'] = labels
        df = df[['Participant', 'Transcription', 'Start time', 'End time', 'Duration', 'Confidence']]
        return df

    def load_json(self, path_to_json_file):
        """
        Loads the JSON data and returns in dictionary format
        :param path_to_json_file: string of path to json file
        :return: dictionary of data
        """
        f = open(path_to_json_file)
        data = json.load(f)
        f.close()
        return data

    def process_data(self, data):
        """
        This function processes the data
        :param data: dictionary of JSON data
        :return: __result_set and __segment_words
        """
        for segment in data['results']['segments']:
            first_alt = segment['alternatives'][0]
            transcript = first_alt['transcript']
            start = float(segment['start_time'])
            end = float(segment['end_time'])

            duration = end - start
            num_items = 0
            confidence_sum = 0.0

            items = first_alt['items']
            seg_words = []

            for i, item in enumerate(items):
                num_items = i + 1
                confidence_sum += float(item['confidence'])
                seg_word = item['content']
                seg_words.append(seg_word)

            self.__segment_words.append(seg_words)
            avg_conf = confidence_sum / float(num_items)
            self.__result_set.append([transcript, start, end, duration, avg_conf])

        return self.__result_set, self.__segment_words

    def get_all_channel_tokens(self, data):
        """
        This function returns all the tokens in each channel
        :param data: input data
        :return: channel_tokens list with label and word
        """
        num_channels = data['results']['channel_labels']['number_of_channels']
        channel_data = data['results']['channel_labels']['channels']

        for i in range(num_channels):
            for item in channel_data[i]['items']:
                curr_channel = i
                token = item['alternatives'][0]['content']
                self.__channel_tokens.append((token, curr_channel))

        return self.__channel_tokens

    def label_speakers(self, segment_words, channel_tokens):
        """
        This function labels the speakers for each of the segment
        :param segment_words: List contains tokens for each segment
        :param channel_tokens: List contains tuple of token and channel
        :return: dataframe
        """
        idx_channel_tokens = 0
        for seg_item in segment_words:
            for i in range(len(channel_tokens)):
                idx_channel_tokens = i
                j = 0
                while j < len(seg_item) and j < len(channel_tokens):
                    if seg_item[j] != channel_tokens[i + j][0]:
                        break
                    j += 1
                if j == len(seg_item):
                    speaker = channel_tokens[i][1]
                    self.__result_set_classes.append(self.__channel_speakers[speaker])
                    break

            if idx_channel_tokens == len(channel_tokens) - 1:
                self.__result_set_classes.append(self.__no_class_label)

        df = self.__generate_df(self.__result_set, self.__result_set_classes)
        return df

    def generate_csv_from_data(self, df, filename):
        """
        This function generates CSV from dataframe
        :param df: dataframe
        :param filename: name of the CSV file to output
        :return: CSV
        """
        df.to_csv(filename, encoding='utf-8', index=False)