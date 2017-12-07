from captcha.audio import AudioCaptcha, create_noise, mix_wave, reduce, WAVE_SAMPLE_RATE, WAVE_HEADER, WAVE_HEADER_LENGTH, DATA_DIR, operator
import random


class CaptchaAuditivo(AudioCaptcha):
    def __init__(self, alfabeto):
        super().__init__(alfabeto)

    def create_background_noise(self, length, chars):
        noise = create_noise(length, 4)
        return noise

    def create_wave_body(self, chars):
        voices = []
        inters = []
        for key in chars:
            voices.append(self._twist_pick(key))
            v = random.randint(WAVE_SAMPLE_RATE, WAVE_SAMPLE_RATE * 3)
            inters.append(v)

        durations = map(lambda a: len(a), voices)
        length = max(durations) * len(chars) + reduce(operator.add, inters)
        bg = self.create_background_noise(length, chars)

        # begin
        pos = inters[0]
        for i, v in enumerate(voices):
            end = pos + len(v) + 1
            bg[pos:end] = mix_wave(v, bg[pos:end])
            pos = end + inters[i]

        return bg
