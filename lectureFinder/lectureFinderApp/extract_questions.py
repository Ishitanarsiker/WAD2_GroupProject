from os import listdir, path
from lectureFinder.settings import BASE_DIR


def phrase_appears_in_file(filename, phrase):
    with open(filename) as transcript:
        all_spoken_lines = transcript.readlines()[4::4]

    for spoken_line in all_spoken_lines:
        # Look through each spoken line, see if the phrase appears.
        spoken_line_words = [word.lower() for word in spoken_line.split(" ")]
        phrase_parts = [word.lower() for word in phrase.split(" ")]

        for each_phrase in phrase_parts:
            if each_phrase in spoken_line_words:
                return True

    return False


def search_transcripts_for_phrase(phrase):
    files_dir = path.join(BASE_DIR, 'mock_data/transcripts')
    filenames = [f for f in listdir(files_dir) if f.endswith(".vtt")]
    files_phrase_appears_in = []

    for filename in filenames:
        does_phrase_appear_in_file = phrase_appears_in_file(f"{files_dir}/{filename}", phrase)

        if does_phrase_appear_in_file:
            files_phrase_appears_in.append(filename)

    return files_phrase_appears_in


print(search_transcripts_for_phrase("Dublin"))
