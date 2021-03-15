class Pl:
    miliony = ["", "milion", "miliony", "milionów"]
    tysiace = ["", "tysiąc", "tysiące", "tysięcy"]
    setki = ["", "sto", "dwieście", "trzysta","czterysta", "pięćset", "sześćset", "siedemset", "osiemset", "dziewięćset"]
    dziesiatki = ["","dziesięć", "dwadzieścia","trzydzieści","czterdzieści", "pięćdziesiąt", "sześćdziesiąt", "siedemdziesiąt", "osiemdziesiąt", "dziewięćdziesiąt"]
    nastki = ["", "jedenaście", "dwanaście", "trzynaście", "czternaście", "piętnaście", "szesnaście", "siedemnaście", "osiemnaście", "dziewiętnaście"]
    jednosci = ["zero", "jeden", "dwa", "trzy", "cztery", "pięć", "sześć", "siedem", "osiem", "dziewięć"]

def number_to_text_pl(number):
    lang = Pl

    miliony = int(number / 1000000) % 1000
    tysiace = int(number / 1000) % 1000
    setki = int(number / 100) % 10
    dziesiatki = int(number / 10) % 10
    jednosci = int(number % 10)
    text = ""

    if number == 0:
        return lang.jednosci[0];

    if miliony == 1:
        text += lang.miliony[1] + " "
    if miliony % 10 > 1 and miliony % 10 < 5:
        text += number_to_text_pl(miliony) + " " + lang.miliony[2] + " "
    if miliony % 10 > 4:
        text += number_to_text_pl(miliony) + " " + lang.miliony[3] + " "

    if tysiace == 1:
        text += lang.tysiace[1] + " "
    if tysiace % 10 > 1 and tysiace % 10 < 5:
        text += number_to_text_pl(tysiace) + " " + lang.tysiace[2] + " "
    if tysiace % 10 > 4:
        text += number_to_text_pl(tysiace) + " " + lang.tysiace[3] + " "

    if setki > 0 and setki <10:
        text += lang.setki[setki] + " "

    if dziesiatki == 1:
        if jednosci == 0:
            text += lang.dziesiatki[1] + " "
        else:
            text += lang.nastki[jednosci] + " "
    if dziesiatki > 1:
        text += lang.dziesiatki[dziesiatki] + " "

    if dziesiatki != 1 and jednosci > 0:
        text += lang.jednosci[jednosci] + " "

    return text[:-1]
