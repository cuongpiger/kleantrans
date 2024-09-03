import subprocess
import re


class TranslatedText:
    def __init__(self, raw_text: str, translated_text: str):
        self._raw_text = raw_text
        self._translated_text = translated_text

    @property
    def raw_text(self):
        return self._raw_text

    @property
    def translated_text(self):
        return self._translated_text


class Translator:
    def __init__(self):
        self.pattern = r"[^a-zA-Z0-9?!'()\.,+-=:;\s]"

    def translate(self, text: str, source: str, dest: str) -> str:
        text = self._clean_text(text.strip())
        print("The cleaned text is: ", text)
        trans_text = ""

        if text != "":
            try:
                cmd = """
                    trans -e google -s {} -t {} -show-original y -show-original-phonetics n -show-translation y -no-ansi -show-translation-phonetics n -show-prompt-message n -show-languages y -show-original-dictionary n -show-dictionary n -show-alternatives n "{}"
                    """.format(source, dest, text)

                subprocess_ = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                trans_text = subprocess_.stdout.read().decode('utf-8').split("\n\n")[1]
                trans_text = re.sub("(u200b)", "", trans_text)
            except (Exception,) as e:
                pass

        return trans_text

    def _clean_text(self, text):
        text = re.sub(r"\s+", " ", re.sub(self.pattern, " ", text)).strip()
        return text
