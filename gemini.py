# pip install -q -U google-generativeai
import google.generativeai as genai
import os, dotenv


dotenv.load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)

gemini_model = genai.GenerativeModel('gemini-pro')

def get_response(prompt):
    response = gemini_model.generate_content(prompt)
    return response.text


music_prompt = """I need assistance in producing AI-generated text
that I convert to music using MIDI files. Initially,
I'll provide a description of the format I need for
the textual representation of the music.
Since music is a time-based art form,
the notes follow each other in time, and
sometimes there are no notes, that is, silences.
The way I would like you to generate them is as
follows:
Each note is represented as a tuple of two
elements:
The pitch of the note (integer value).
Because I will use this text representation and
convert to MIDI the note should be a number
from 21 (that is note A0 - 27,50 Hz) to 96 (that is
C7 - 2093 hz) so use these numbers to represent
the note.
The duration of the note (float value)
represented as:
0.125 for an eighth note
0.25 for a quarter note
0.5 for a half note
1 for a whole note
2 for a double whole note
With this format i need you generate a text that
i will covert in music in this format:
melody_pitch_duration_data = [
(note, duration), (note, duration), (note,
duration),
etc,
]
And when there is a silence the note should be 0
and the duration is how long is that silence.
A melody is a linear sequence of notes that the
listener hears as a single entity. It is the
foreground to the backing elements and is a
combination of pitch and rhythm. Sequences of
notes that comprise melody are musically
satisfying and are often the most memorable
part of a song.
There are many ways to describe a melody. Here
are a few:
● Pitch: The pitch of a melody is the relative
highness or lowness of the notes. Melodies
can be high, low, or somewhere in between.
● Rhythm: The rhythm of a melody is the
pattern of long and short notes. Melodies can
have a slow, steady rhythm, a fast,
syncopated rhythm, or something in
between.
● Intervals: Intervals are the distance between
notes. Melodies can use a variety of
intervals, from small steps to large leaps.
● Contour: The contour of a melody is the
overall shape of the melody. Melodies can be
ascending, descending, or something in
between.
● Tonal center: The tonal center of a melody is
the note that the melody feels like it is
centered around. Melodies can have a strong
tonal center, a weak tonal center, or no tonal
center at all.
When describing a melody, it is important to
consider all of these factors. The pitch, rhythm,
intervals, contour, and tonal center all
contribute to the overall sound of the melody.
Here are some examples of how to describe
melodies:
● The melody of "Happy Birthday" is simple and
repetitive, with a clear tonal center.
● The melody of "Yesterday" by The Beatles is
more complex, with a variety of intervals and
a changing tonal center.
● The melody of "Bohemian Rhapsody" by
Queen is highly dramatic, with a wide range
of pitches and rhythms.
Quality melodies typically limit their range to
about an octave-and-a-half, feature repeating
elements like melodic intervals and rhythmic
patterns, and consist of stepwise motion with
occasional energetic leaps. Good melodies also
interact meaningfully with the bass line,
employing a mix of parallel, similar, oblique, or
contrary motions for a dynamic, counter melodic
effect. Finally, a standout melody tends to have
a climactic moment, often a high note with
significant harmonization and strong rhythmic
placement, which then descends to a restful
cadence.
No matter how it is described, a melody is one of
the most important elements of music. It is what
gives a song its identity and makes it memorable.
Please note that AI-generated music may not
sound pleasing as it is randomly generated so we
will use music theory but not random math so
don't randomize the generation process. take
into account musical concepts like scales,
modes, etc.
Now that you have a full understanding of the
text representation, generate a happy melogy.
"""

def get_music_response(mood):
    
    return get_response(music_prompt)

def get_caption_response(mood):
    pass

if __name__ == '__main__':
    print(get_music_response('happ'))