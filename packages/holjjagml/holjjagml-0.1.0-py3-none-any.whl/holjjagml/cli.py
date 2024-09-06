import random
from tqdm import tqdm
from time import sleep
from pyfiglet import Figlet

f = Figlet(font='slant')

def run():
    print(f.renderText('Nostradamus'))
    length = float(input("🤖 물고기의 길이를 입력하세요 (cm): "))
    weight = float(input("🤖 물고기의 무게를 입력하세요 (g): "))

    fish_list = ["🐟 빙어", "🐡 도미"]
    guess_fish = random.choice(fish_list)

    pbar = tqdm(["🐡 도미 🐳", "🐟 빙어 🐋"] * 5)
    for char in pbar:
        sleep(1)
        pbar.set_description(f"🤖 {char} ")


    print(f"🤖 이녀석은 바로 {guess_fish}!")
    
    user_answer = input("🤖 저의 예측이 맞쥬 ? (Y/n): ").upper() or 'Y'

    if user_answer == 'Y':
        print("🤖 역시 내가 바로 물고기 척척박사! 🐟")
    else:
        print("🤖 이럴수가...! 내가 틀렸다니...! 😱")

if __name__ == "__main__":
    run()
