# CodeChallenges-Transcription_DataParsing
A code Challenge that requires the challenger to parse out a json formatted recording transcription


THE CHALLENGE (Below the line):
----------------------------------------------------------------------------

We generate a lot of transcriptions from the AWS Transcribe service. The output of the services are json files.

I've included two example files:
Transcription-structure.json is a very short (one word) transcription that shows you the layout of the file.
Transcription-example.json is a complete conversation between two people (it has been de-identified so don't worry!)

We'd like you to write a conversion program that can read in a transcription file and convert it into a CSV file (empty CSV file with headers attached).

Each row in the output file should be one 'turn' of the conversation
(A turn is the term for one complete set of words said by one participant before another participant talks)
The participant column is who said the turn and is either Payer or Provider - in the example file the Payer talks first.
Start and End time columns are the start and end times of that turn
Duration is how long the turn takes.
Confidence is the average confidence of the turn.

Once complete, just commit your code into Main and let us know!

You can use whatever language you like and please don't spend more than a couple of hours on this! 
If you don't finish it in time, send us what you have.
