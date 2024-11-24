
import regex as re
# とりあえずひらがな一ないし二文字
kyuujitai_broken = re.compile(r'^\p{Hiragana}{1,2}$')
