import re


class Subtitle:

    def __init__(self, id, time=None, text=""):
        self.id = id
        self.time = time
        self.text = text

    def __repr__(self):
        return f"{self.id} ({self.time}): {self.text}"


class SRT:

    def __init__(self, file_path):
        self.subtitles = self.open(file_path)
        self.n_subtitles = len(self.subtitles)


    def __repr__(self):
        [print(subtitle) for subtitle in self.subtitles]
        return "EOF"

        
    def open(self, file_path):
        srt = []    # Container of subtitles on memory

        with open(file_path, "r", errors='ignore') as files:
            lines = files.readlines()

            for line in lines:
                # Id of line
                if re.search('^[0-9]+$', line) is not None:
                    new_subtitle_line = Subtitle(id=line[:-1])
                    srt.append(new_subtitle_line)
                # Time of line
                elif re.search('^[0-9]{2}:[0-9]{2}:[0-9]{2}', line) is not None:
                    srt[-1].time = line[:-1]
                # Content of line
                elif re.search('^$', line) is None:
                    srt[-1].text += line[:-1]

        return srt


    def extract_portion(self, id_i, max_size=5000):
        text = ""

        # From initial id, count max_size of caracters to append without counting the time or ids
        for i in range(id_i, len(self.subtitles)):
            text_to_insert = self.subtitles[i].text
            n_letters = len(text) + len(text_to_insert)

            if n_letters < max_size:
                text += f"{text_to_insert}\n"
                id_f = i
            else:
                break

        return text, id_f + 1


    def update_text(self, first_sub_id, traslation):

        for i in range(len(traslation)):
            self.subtitles[first_sub_id + i].text = traslation[i]


    def wrap_lines(self, max_letters=20):
        for subtitle in self.subtitles:
            if max_letters >= len(subtitle.text):
                continue

            phrases = [[]]
            for word in subtitle.text.split():
                if len(phrases[-1]) + len(word) < max_letters:
                    phrases[-1].append(word)
                else:
                    phrases.append([word])
            
            phrases = [" ".join(phrase) for phrase in phrases]
            subtitle.text = "\n".join(phrases)


    def save(self, file_path):

        file_out = open(file_path, "w")

        for subtitle in self.subtitles:
            text = "\n".join([subtitle.id, subtitle.time, subtitle.text, "\n"])
            file_out.write(text)

        file_out.close()