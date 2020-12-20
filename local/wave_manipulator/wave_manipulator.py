from pydub import AudioSegment
from pydub.playback import play
from pydub.generators import WhiteNoise
from pydub.utils import mediainfo


audio_in_file = "in_sine.wav"
audio_out_file = "out_sine.wav"

class wave_manipulator:
    def __init__(self, input_wave_file):
        self.input_wave_file = input_wave_file
        self.audio = AudioSegment.from_wav(input_wave_file)
        self.audio_info = mediainfo(input_wave_file)




    def match_target_amplitude(self, sound, target_dBFS):
        change_in_dBFS = 2 * target_dBFS - sound.dBFS
        return sound.apply_gain(change_in_dBFS)

    def generate_white_noise(self, noise_duration, reduction = 10):
        noise = WhiteNoise().to_audio_segment(duration=noise_duration).set_frame_rate(int(self.audio_info['sample_rate']))
        return noise - 10

    def combine_noise_to_audio(self, noise):
        self.audio = self.audio.overlay(noise)

    def add_silence_beginning(self, silence_duration = 400, noisy = False):
        if(noisy == True):
            noise = self.generate_white_noise(silence_duration)
            noise = self.match_target_amplitude(noise, self.audio.dBFS)
            silence = AudioSegment.silent(duration = silence_duration)
            silence = silence.overlay(noise)
        else:
            silence = AudioSegment.silent(duration = silence_duration)
        
        self.audio = silence + self.audio
        return self.audio 

    def add_silence_end(self, silence_duration = 400, noisy = False):
        if(noisy == True):
            noise = self.generate_white_noise(silence_duration)
            noise = self.match_target_amplitude(noise, self.audio.dBFS)
            silence = AudioSegment.silent(duration = silence_duration)
            silence = silence.overlay(noise)
        else:
            silence = AudioSegment.silent(duration = silence_duration)
        
        self.audio = self.audio + silence
        return self.audio 

    def add_silence_beginning_and_end(self, beginning_silence_duration, end_silence_duration, noisy = False):
        self.audio = self.add_silence_beginning(silence_duration = beginning_silence_duration, noisy = True)
        self.audio = self.add_silence_end(silence_duration = end_silence_duration, noisy = True)
        return self.audio
    
    def export_file(self, path, export_format = "wav"):
        self.audio.export(path, format = export_format)

