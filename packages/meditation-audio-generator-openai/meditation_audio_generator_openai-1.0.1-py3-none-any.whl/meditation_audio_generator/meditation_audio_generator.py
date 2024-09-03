import json
import random
import shutil
import time
import textwrap
import platform
from pedalboard_native import LowShelfFilter
from typing import List
import os
from openai import OpenAI
from .mp3_mixer import MP3Mixer
from .mp3_merger import MP3Merger
from pedalboard import Pedalboard, Reverb, Gain, LowpassFilter
from pedalboard.io import AudioFile
from elevenlabs.client import ElevenLabs
from elevenlabs import play, save, VoiceSettings
import elevenlabs

YELLOW = (255, 255, 0, 255)  # used to build the image text. 100% opaque
BLUE = [0, 0, 255]  # used to build the image banner background. opacity filled in later.
WHITE = (255, 255, 255, 255)  # used to build the image banner text. 100% opaque
BLACK = [0, 0, 0]  # used to build the image banner text. 100% opaque
class MeditationAudioGenerator:
    def __init__(self, topic: str = "Mindfulness", length: float = 10, api_key: str = "",
                 base_on_text: bool = False,
                 text: str = "", num_sentences: int = 6,
                 bass_boost: bool = False,
                 balance_even: float = 0.0, balance_odd: float = 0.0,
                 two_voices: bool = False,
                 expand_on_section: bool = False,
                 sounds_dir: str = "ambient_files",
                 limit_parts: int = 0,
                 num_loops: int = 0,
                 in_spanish: bool = False,
                 affirmations_only: bool = False,
                 binaural: bool = False,
                 all_voices: bool = False,
                 binaural_fade_out_duration: float = 4,
                 binaural_fade_in_duration: float = 4,
                 start_beat_freq: float = 5,
                 end_beat_freq: float = 0.5,
                 base_freq: float = 110.0,
                 sample_rate: int = 44100,
                 num_samples_to_chop: int = 30000,
                 expansion_size: int = 4,
                 force_working_dir_overwrite: bool = False,
                 force_voice: str = "",
                 power_ratio = None,
                 elevenlabs_key: str = "",
                 elevenlabs_voice: str = "",
                 ):
        """
        Initializes the MeditationAudioGenerator with an OpenAI API key.
        :param topic: Topic of the meditation.
        :param length: Length of the meditation in minutes.
        :param base_on_text: If True, generate a meditation based on the text provided.
        :param text: Text to generate the meditation from.
        :param api_key: OpenAI API key for accessing the speech synthesizer.
        :param num_sentences: Number of sentences in each part of the meditation.
        :param bass_boost: If True, apply bass boost to the audio.
        :param balance_even: The balance for even segments (0.0 is centered, -1.0 is left, 1.0 is right).
        :param balance_odd: The balance for odd segments (0.0 is centered, -1.0 is left, 1.0 is right).
        :param two_voices: If True, use two different voices for odd and even segments.
        :param expand_on_section: If True, expand on each section of the meditation.
        :param sounds_dir: Directory containing ambient sounds.
        :param limit_parts: Limit the number of parts in the meditation using the prompt.
        :param num_loops: allows meditation parts to be looped multiple times.
        :param in_spanish: If True, generate the meditation in Spanish.
        :param affirmations_only: If True, generate affirmations only not meditations.
        :param binaural: If True, generate binaural beats.
        :param all_voices: If True, choose from all available voices.
        :param binaural_fade_out_duration: Duration in seconds of the fade-out at the end of the binaural beats.
        :param binaural_fade_in_duration: Duration in seconds of the fade-in at the beginning of the binaural beats.
        :param start_beat_freq: Initial frequency difference for the binaural effect.
        :param end_beat_freq: Final frequency difference for the binaural effect.
        :param base_freq: Base frequency for the binaural beats.
        :param sample_rate: Sample rate for mixer.
        :param num_samples_to_chop: Number of samples to chop off the beginning of the ambient sound files.
        :param fade_in_time: Duration in seconds of the fade-in at the beginning of the ambient sound overlay.
        :param fade_out_time: Duration in seconds of the fade-out at the end of the ambient sound overlay.
        :param expansion_size: Size of the expansion for the text, if expand_on_section is True.
        :param force_voice: Allows user to force selection of OpenAI voice, e.g. onyx
        :param power_ratio: Ratio (higher means louder voice) of the power of the binaural beats or ambient to the power of the voice audio.
        :param elevenlabs_key: Elevenlabs API key for accessing the speech synthesizer. If not an empty string, ElevenLabs speechsynth will be used intead of OpenAI.
        :param elevenlabs_voice: Elevenlabs voice to use for speech synthesis (if elevenlabs_key is not an empty string).
        """
        # setting any of these to false switches off that part of the pipeline
        self.pipeline: dict[str, bool] = {
            "texts": True,
            "audio_files": True,
            "combine_audio_files": True,
            "audio_fx": True,
            "background_audio": True
        }
        self.in_spanish = in_spanish
        self.limit_parts = limit_parts
        self.balance_odd = balance_odd
        self.balance_even = balance_even
        if not elevenlabs_key:
            self.voice_choices = ['onyx', 'shimmer'] #, 'echo']
        else:
            self.voice_choices = ['Charlotte', 'Charlotte']
        self.two_voices = two_voices
        self.num_loops = num_loops
        if two_voices:
            choices = self.voice_choices.copy()
            self.voice_odd = random.choice(choices)
            choices.remove(self.voice_odd)
            self.voice_even = random.choice(choices)
        self.expand_on_section = expand_on_section
        self.elevenlabs_key = elevenlabs_key
        self.elevenlabs_voice = elevenlabs_voice

        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
        if self.elevenlabs_key:
            print("Using ElevenLabs speechsynth.")
            self.client11 = ElevenLabs(api_key=self.elevenlabs_key)
        self.model = "gpt-4o"
        self.subsections = []
        self.subsection_audio_files = []
        self.length = length
        self.topic = topic
        self.topic_based_filename = self.topic.replace(" ", "_")[:20]  # in case topic too long
        # working directory for storing audio files etc
        self.working_directory = self.topic_based_filename
        # create the working directory if it doesnt exist
        if not os.path.exists(self.working_directory):
            os.makedirs(self.working_directory)
        # otherwise clear the directory of files
        elif not force_working_dir_overwrite:
            resp = input(
                f"The working directory '{self.working_directory}' already exists. Do you want to overwrite it? (y/n): ")
            if resp.lower() == "y" or resp.lower() == "yes":
                shutil.rmtree(self.working_directory)
                os.makedirs(self.working_directory)
        else:
            print("WARNING: Forced overwriting of working directory")
            shutil.rmtree(self.working_directory)
            os.makedirs(self.working_directory)
        self.mixer = MP3Mixer(mp3_file="TBD", binaural=binaural, working_dir=self.working_directory,
                              binaural_fade_out_duration=binaural_fade_out_duration,
                              binaural_fade_in_duration=binaural_fade_in_duration,
                              # duration in seconds of the fade-out at the end of the binaural beats
                              # how much binaural beats should be quieter than the input voice audio
                              start_beat_freq=start_beat_freq,  # initial frequency difference for the binaural effect
                              end_beat_freq=end_beat_freq,  # final frequency difference for the binaural effect
                              base_freq=base_freq,  # base frequency for the binaural beats
                              sample_rate=sample_rate,
                              power_ratio=power_ratio,  # how much ambient sound should be quieter than the input voice audio
                              )
        self.merger = MP3Merger(self.subsection_audio_files, duration=int(self.length * 60),
                                balance_odd=self.balance_odd,
                                balance_even=self.balance_even)
        self.bass_boost = bass_boost
        if not elevenlabs_key:
            self.voice_list = ['onyx', 'shimmer', 'echo', 'alloy', 'fable', 'nova']     # openai voices
        else:
            self.voice_list = ['Callum', 'Charlotte']   # elevenlabs voices
        if force_voice:
            self.voice = force_voice
        elif all_voices:
            self.voice = random.choice(self.voice_list)
        else:
            self.voice = random.choice(self.voice_list[:2])
        self.pedalboard_fx_list = []
        if self.bass_boost:
            # The below is ideal for 1st male voice, but not first female voice
            if self.voice != 'shimmer':
                self.pedalboard_fx_list += [
                    LowShelfFilter(cutoff_frequency_hz=150, gain_db=5.0, q=1)
                ]
            else:
                self.pedalboard_fx_list += [
                    LowShelfFilter(cutoff_frequency_hz=150, gain_db=3.0, q=1)
                ]
        self.pedalboard_fx_list += [
            LowpassFilter(10000),
            Reverb(room_size=0.04, wet_level=0.04)
        ]
        self.engine = "tts-1-hd"
        self.num_sentences = num_sentences
        self.technique = random.choice(["Watching the breath", "Body sensation", "Watching the thoughts",
                                        "Listening to sounds (but only mention sounds within the meditation track)."])
        if affirmations_only:
            output_type = "affirmation"
        else:
            output_type = "meditation"
        if base_on_text:
            self.prompt = f"""Generate a {output_type} based on the following text. 
            Do not use any contractions at all, for example isn't, there's or we're:\n{text}"""
        else:
            self.prompt = f"""Generate a {output_type} on the topic '{self.topic}'.
            Do not use any contractions at all, for example isn't, there's or we're."""
        self.prompt += f"The {output_type} should be {self.length} minutes long.\n"
        self.prompt += f"""
        Start with a welcome message part which has an introduction to the {output_type}.
        Finish with a closing message part which has a conclusion to the {output_type}.
        Break it down into multiple parts which will be read with pauses between them during {output_type}.
        Each part should only contain a thought by you on the topic and finish with a single action request, 
        but may contain multiple pieces of background information or motivations as well.
        The action request should be based on the meditation technique '{self.technique}'.
        THE ACTION SHOULD BE THE LAST SENTENCE OF THE PART! Do not relate the action to the topic, just to the technique.
        Some may only be reminders to continue the focus on what was instructed a previous part.
        Do NOT put two actions in one subsection. Do NOT ask the listener to both take an action and consider or think about something!
        """
        if self.limit_parts > 0:
            if self.limit_parts < 3:
                self.limit_parts = 3
                print("WARNING: limit_parts must be at least 3 to include introduction and conclusion parts. Setting to 3.")
            self.prompt += f"""
            The entire JSON {output_type} should contain NO MORE THAN {self.limit_parts} meditation_part  keys.\n"""
        if not self.expand_on_section:
            self.prompt += f"""
            Each meditation_part value should be no more than {self.num_sentences} sentences long.\n"""
        self.expansion_size = expansion_size
        if self.expand_on_section:
            self.prompt += f"""Start each part's text with a {self.expansion_size} sentence 
                                    details relating to that part. 
                                    Insure the details
                                   demonstrate your in-depth knowledge of the section (and topic) and help 
                                   the listener. Do not ask the listener to take actions or consider thoughts in this. \n """
        if not affirmations_only:
            self.prompt += f"""
            Whatever the topic of the meditation, embed it within the following meditation technique:\n
            {self.technique}. Do not talk about 'think about' or 'consider'.\n
            """
        json_subprompt = '''
        Return the responses in JSON format like:\n
        [
            {"meditation_part_1": "The first part of the meditation text."},
            {"meditation_part_2": "The second part of the meditation text."},
            {"meditation_part_3": "The third part of the meditation text."}
            etc.
        ]
        Add ellipsis '...' at the end of some sentences, to help humanise the speech.
        '''
        # repeat the below for emphasis
        if self.limit_parts > 0:
            self.prompt += f"""
            URGENT: The entire JSON {output_type} should contain NO MORE THAN {self.limit_parts} meditation_part JSON keys.\n""".upper()
        if not self.expand_on_section:
            self.prompt += f"""
            URGENT: Each meditation_part value should be no more than {self.num_sentences} sentences long.\n""".upper()
        if affirmations_only:
            json_subprompt = json_subprompt.replace("meditation", "affirmation")
        self.prompt += json_subprompt
        if self.in_spanish:
            self.prompt += "\n Responde en espanol."

    def send_prompt(self, prompt: str, use_json: bool = False) -> str:
        if prompt.strip() == "":
            raise ValueError("Error: send_prompt - Empty prompt.")
        content = {
            "type": "text",
            "text": prompt,
        }
        if use_json:
            content["response_format"] = "json"
            if "json" not in prompt and "JSON" not in prompt:
                raise ValueError("Error: send_prompt - JSON must be mentioned in a JSON prompt.")
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        content
                    ]
                }
            ]
        )
        return response.choices[0].message.content

    # first part of pipeline
    def generate_meditation_texts(self) -> List[str]:
        """
        Generates meditation text divided into subsections based on the given topic
        and stores in working directory.

        :return: List of text subsections for the meditation.
        """
        # check self. working_directory exists
        if not os.path.exists(self.working_directory):
            msg = f"Error: generate_meditations_texts - working_directory does not exist: {self.working_directory}"
            raise FileNotFoundError(msg)
        # check self.topic_based_filename exists
        if not self.topic_based_filename:
            raise ValueError("Error: topic_based_filename is not set.")
        # check prompt is set
        if not self.prompt:
            msg = "Error: generate_meditations_texts - Prompt is not set."
            raise ValueError(msg)
        # check is contains JSON or json
        if "json" not in self.prompt and "JSON" not in self.prompt:
            msg = "Error: generate_meditations_texts - JSON must be mentioned in a JSON prompt."
            raise ValueError(msg)
        # Generate the meditation text using OpenAI's LLM
        full_text = self.send_prompt(self.prompt, use_json=True)
        full_text = full_text.replace("```json", "").replace("```", "")
        try:
            full_json = json.loads(full_text)
            # Split the text into subsections
            self.subsections = [value for d in full_json for key, value in d.items()]
        except Exception as e:
            try:
                full_json = eval(full_text)
                self.subsections = [value for d in full_json for key, value in d.items()]
            except Exception as e:
                # write it to a file for debugging
                filename = os.path.join(self.working_directory,
                                        f"{self.topic_based_filename}_raw_meditation_text_debug.json")
                with open(filename, "w") as f:
                    f.write(full_text)
                msg = f"Error: generate_meditations_texts -  Could not parse the response from the API. Check the file {filename} for more information."
                raise ValueError(msg) from e

        # write to file
        filename = os.path.join(self.working_directory, f"{self.topic_based_filename}_meditation_text.json")
        with open(filename, "w") as f:
            json.dump(full_json, f, indent=4)
        return self.subsections

    # used by methods below
    def synthesize_speech(self, text: str, filename: str, voice: str = "") -> None:
        """
        Synthesizes speech from the given text and saves it as an MP3 file.

        :param text: Text to be converted to speech.
        :param filename: Name of the output MP3 file.
        :param voice: Voice to be used for the speech synthesis.
        """
        # check text not empty
        if text.strip() == "":
            raise ValueError("Error: synthesize_speech - Empty text.")
        # check filename not empty
        if filename.strip() == "":
            raise ValueError("Error: synthesize_speech - Empty filename.")
        # check filename ends with .mp3
        if not filename.endswith(".mp3"):
            raise ValueError("Error: synthesize_speech - Filename must end with .mp3.")
        if not voice:
            voice = self.voice

        if not self.elevenlabs_key:
            try:
                # https://stackoverflow.com/questions/77952454/method-in-python-stream-to-file-not-working
                with self.client.audio.speech.with_streaming_response.create(
                    model=self.engine,
                    voice=voice,
                    input=text
                ) as response:
                    response.stream_to_file(filename)
            except Exception as e:
                msg = f"Error: synthesize_speech - OpenAI API call failed for the text: {text}"
                raise RuntimeError(msg) from e
        else:
            elevenlabs_audio = self.client11.generate(
                text=text,
                voice=voice,
                model="eleven_multilingual_v2",
            )
            save(elevenlabs_audio, filename)  # save the audio to a file use elevenlabs API



    # second part of the pipeline
    def create_meditation_text_audio_files(self) -> List[str]:
        """
        Creates MP3 files for each subsection.

        :return: List of paths to the generated MP3 files.
        """
        self.subsection_audio_files = []
        # check self.subsections exists
        if not self.subsections:
            msg = "Error: create_meditation_text_audio_files - Subsections are not set."
            raise ValueError(msg)
        # check self.working_directory exists
        if not os.path.exists(self.working_directory):
            msg = f"Error: create_meditation_text_audio_files - working_directory does not exist: {self.working_directory}"
            raise FileNotFoundError(msg)
        for i, subsection in enumerate(self.subsections):
            filename = os.path.join(self.working_directory, f"meditation_part_{i + 1}.mp3")
            print(f"Generating audio for part {i + 1} of {len(self.subsections)}...")
            if self.two_voices:
                # check self.voice_even exists
                if not self.voice_even:
                    msg = "Error: create_meditation_text_audio_files - voice_even is not set."
                    raise ValueError(msg)
                # check self.voice_odd exists
                if not self.voice_odd:
                    msg = "Error: create_meditation_text_audio_files - voice_odd is not set."
                    raise ValueError(msg)
                if i % 2 == 0:
                    self.synthesize_speech(subsection, filename, voice=self.voice_even)
                else:
                    self.synthesize_speech(subsection, filename, voice=self.voice_odd)
            else:
                self.synthesize_speech(subsection, filename)
            self.subsection_audio_files.append(filename)
        if self.num_loops:
            subsection_audio_files_orig = self.subsection_audio_files.copy()
            # now copy the files num_loops times but update the filenames
            # so the index part fo the filename is unique and ordered
            # and update the self.subsection_audio_files
            base_index = len(subsection_audio_files_orig)
            for i in range(1, self.num_loops):  # num_loops 1 means no repeat
                for j, file in enumerate(subsection_audio_files_orig):
                    new_file = file.replace(f"meditation_part_{j + 1}", f"meditation_part_{base_index + j + 1}")
                    shutil.copy(file, new_file)
                    self.subsection_audio_files.append(new_file)
                base_index += len(subsection_audio_files_orig)
        return self.subsection_audio_files

    # third part of the pipeline
    def merge_meditation_audio(self) -> str:
        """
        merges them into a single MP3 file.

        :return: Path to the merged MP3 file.
        """
        # check self.working_directory exists
        if not os.path.exists(self.working_directory):
            msg = f"Error: merge_meditation_audio - working_directory does not exist: {self.working_directory}"
            raise FileNotFoundError(msg)
        if not self.subsection_audio_files:
            # get all files in working dir that start with meditation_part
            self.subsection_audio_files = [os.path.join(self.working_directory, f) for f in
                                           os.listdir(self.working_directory) if f.startswith("meditation_part")]
            # if empty list then return error
            if not self.subsection_audio_files:
                msg = "Error: merge_meditation_audio - No files in list and none found to merge."
                raise ValueError(msg)
            # ensure sorted in increasing order
            self.subsection_audio_files.sort(key=lambda x: int(x.split("_")[-1].split(".")[0]))
        self.merger.mp3_files = self.subsection_audio_files
        # merger.spread_out_all_files()  # puts extra silence between phrases
        merged_file = self.merger.merge()
        # check self.topic_based_filename not empty
        if self.topic_based_filename.strip() == "":
            msg = "Error: merge_meditation_audio - Empty topic_based_filename."
            raise ValueError(msg)
        # write to file
        filename = os.path.join(self.working_directory, f"{self.topic_based_filename}_meditation_text_merged.mp3")
        # rename merged file to filename
        shutil.move(merged_file, filename)
        return filename

    # fourth part of the pipeline
    # use pedalboard to add reverberation, echo, or other audio effects to the audio file
    def add_audio_fx(self) -> str:
        """
        Adds audio effects to the given audio file using Pedalboard.

        :return: Path to the output audio file with effects applied.
        """
        # check self.working_directory exists
        if not os.path.exists(self.working_directory):
            msg = f"Error: add_audio_fx - working_directory does not exist: {self.working_directory}"
            raise FileNotFoundError(msg)
        # check self.topic_based_filename not empty
        if self.topic_based_filename.strip() == "":
            msg = "Error: add_audio_fx - Empty topic_based_filename."
            raise ValueError(msg)
        # check a file ending _meditation_text_merged.mp3 exists in working dir
        if not os.path.exists(
                os.path.join(self.working_directory, f"{self.topic_based_filename}_meditation_text_merged.mp3")):
            msg = f"Error: add_audio_fx - File {self.topic_based_filename}_meditation_text_merged.mp3 does not exist in working directory."
            raise FileNotFoundError(msg)
        filename = os.path.join(self.working_directory,
                                f"{self.topic_based_filename}_meditation_text_merged.mp3")
        # Load the MP3 file
        with AudioFile(filename) as f:
            audio = f.read(f.frames)
            sample_rate = f.samplerate
        # Create a Pedalboard with desired effects
        board = Pedalboard(self.pedalboard_fx_list)
        # Apply the effects
        effected = board(audio, sample_rate)
        filename = os.path.join(self.working_directory,
                                f"{self.topic_based_filename}_meditation_text_merged_fx.mp3")
        # Write the effected audio to a new file
        with AudioFile(filename, 'w', sample_rate, effected.shape[0]) as f:
            f.write(effected)
        return filename

    # fifth part of the pipeline
    # generate binaural beats using MP3Mixer and merge with the merged_file
    def mix_meditation_audio(self) -> str:
        """
        Mixes the meditation audio with binaural beats.

        :param merged_file: Path to the merged MP3 file.
        :return: Path to the mixed MP3 file.
        """
        # check self.working_directory exists
        if not os.path.exists(self.working_directory):
            msg = f"Error: mix_meditation_audio - working_directory does not exist: {self.working_directory}"
            raise FileNotFoundError(msg)
        # check self.topic_based_filename not empty
        if self.topic_based_filename.strip() == "":
            msg = "Error: mix_meditation_audio - Empty topic_based_filename."
            raise ValueError(msg)
        # check a file ending _meditation_text_merged_fx.mp3 exists in working dir
        if not os.path.exists(
                os.path.join(self.working_directory, f"{self.topic_based_filename}_meditation_text_merged_fx.mp3")):
            msg = f"Error: add_audio_fx - File {self.topic_based_filename}_meditation_text_merged_fx.mp3 does not exist in working directory."
            raise FileNotFoundError(msg)
        merged_file = os.path.join(self.working_directory,
                                   f"{self.topic_based_filename}_meditation_text_merged_fx.mp3")
        self.mixer.mp3_file = merged_file
        mixed_file = self.mixer.mix_audio()
        base_filename = f"{self.topic_based_filename}_meditation_text_merged_fx_mixed.mp3"
        filename = os.path.join(self.working_directory, base_filename)
        # rename mixed file to filename
        os.rename(mixed_file, filename)
        # copy to base_filename as well
        # so that mp3 are in the top level directory in case user wants to upload
        # the mp3 to spotify or something.
        shutil.copy(filename, base_filename)
        return filename

    def run_meditation_pipeline(self, content: str = "") -> tuple[list[str], str]:
        """
        Generates a full meditation experience including text, audio.
        If content string is non-empty, it will be used as the meditation text
        instead of generating one.

        :param content: The meditation text to use. If empty one is generated.
        :return: list of the meditation subsection texts and the output filename
        """
        # note the below code is deliberately done in a repetitive way
        # to make it easier to understand
        # (It could have been implemented using a dictionary of functions and a loop)
        if content == "":
            print("Creating GENERATIVE MEDITATION")
            if self.pipeline.get("texts"):
                print("Generating meditation texts...")
                self.generate_meditation_texts()
            else:
                print("Skipping meditation texts...")
        else:
            print("Creating FREE TEXT MEDITATION")
            # content is a list of \n\n divided free text sections. Split into a list
            free_text = content.split("\n\n")
            # strip() all strings in the list
            free_text = [ft.strip() for ft in free_text]
            # remove any empty strings
            free_text = [ft for ft in free_text if ft]
            # check not empty
            if not free_text:
                msg = "Error: run_meditation_pipeline - Empty free_text list."
                raise ValueError(msg)
            self.subsections = free_text  # this is what would've been generated
        # generate the audio
        if self.pipeline.get("audio_files"):
            print("Generating meditation audio sub-files...")
            self.create_meditation_text_audio_files()
        else:
            print("Skipping generating meditation audio sub-files...")
        if self.pipeline.get("combine_audio_files"):
            # merge the audio
            print("Combining audio files with silences...")
            self.merge_meditation_audio()
        else:
            print("Skipping combining audio files...")
        if self.pipeline.get("audio_fx"):
            print("Adding audio effects...")
            self.add_audio_fx()
        else:
            print("Skipping audio effects...")
        if self.pipeline.get("background_audio"):
            # mix the audio
            print("Adding background sounds/music to spoken audio...")
            filename = self.mix_meditation_audio()
        else:
            print("Skipping adding background sounds/music to spoken audio...")
        return self.subsections, filename

    def translate_text(self, text: str, target_language: str = "Spanish") -> str:
        """
        Translate text to a target language.

        :param text: The text to translate.
        :param target_language: The target language to translate to.
        :return: The translated text.
        """
        # check text is a non-empty string
        if not isinstance(text, str) or text.strip() == "":
            msg = "Error: translate_text - text must be a non-empty string."
            raise ValueError(msg)
        # check target_language is a non-empty string
        if not isinstance(target_language, str) or target_language.strip() == "":
            msg = "Error: translate_text - target_language must be a non-empty string."
            raise ValueError(msg)
        # Translate the text to the target language
        translation_prompt = f"""
        Act as a professional translator who is an expert in translating text to different languages.
        You are tasked with translating the below TEXT to {target_language}:
        <TEXT>'{text}'</TEXT>
        Respond only with the translated text, with no prefix or suffix to your response.
        """
        print(f"Translating text to {target_language}...")
        translated_text = self.send_prompt(translation_prompt)
        return translated_text

    def delete_meditation_workspace(self):
        """
        Delete the meditation workspace - i.e. the directory and its contents.
        """
        if os.path.exists(self.working_directory):
            # remove files in dir first
            for file in os.listdir(self.working_directory):
                file_path = os.path.join(self.working_directory, file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Error deleting file: {e}")
            shutil.rmtree(self.working_directory)
            print(f"Deleted meditation workspace at '{self.working_directory}'.")
