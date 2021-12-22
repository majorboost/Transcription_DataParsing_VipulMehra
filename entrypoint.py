from aws_transcription_processor import AwsTranscriptionProcessor

"""
This file needs to be run, to generate CSV
"""

if __name__=="__main__":
    """
    You will see in the CSV file generated - "Participant" might have 
    N.A. this is the case, when no class label was found for the segment
    in the items in channel_labels. These might need to manually
    assigned the label for "Participant"
    """
    csv_file_name_to_generate = "turns.csv"
    json_file_name = "transcription-example.json"
    obj_processor = AwsTranscriptionProcessor()
    data = obj_processor.load_json(json_file_name)
    result_set, segment_words = obj_processor.process_data(data)
    channel_tokens = obj_processor.get_all_channel_tokens(data)
    df = obj_processor.label_speakers(segment_words, channel_tokens)
    obj_processor.generate_csv_from_data(df, csv_file_name_to_generate)