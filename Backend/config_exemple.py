# -*- coding: utf-8 -*-

# DISCORD
DISCORD_TOKEN = "DISCORD_TOKEN" # TODO : Replace by discord_token
RESULTS_CHANNEL_ID = 123456789 # TODO : Replace by real channel ID

# MAIL
BODY = 'En piece jointe le tableau des recompenses'
FROM_ADRESS = "jean_dupont@orange.fr" # TODO : replace by real sender adress
TO_ADRESS = "jean_dupont@orange.fr" # TODO : replace by real sender adress
SUBJECT = "Recompenses Cross 2024"
MAIL_PASSWORD = "Password" # TODO : replace by real sender mail password
SMTP = "smtp.orange.fr" # TODO : Change if other SMTP than orange : https://serversmtp.com/fr/liste-serveur-smtp/
PORT = 465 # TODO : Change if other SMTP than orange : https://serversmtp.com/fr/liste-serveur-smtp/

# FILES
FINAL_WORD_FILENAME = "../Files/150824.docx"
EMPTY_WORD_FILENAME = "../Files/template.docx"
GMCAP_FILENAME = "../Files/150824.cap"
TEMP = '../Files/Temp'

# GMCAP
OFFSET_A = 42932 # a-1 pour un coureur en 00:00:01.000
OFFSET_B = 26301 # b   pour un coureur en 00:00:01.000
OFFSET_C = 576   # c   pour un coureur en 00:00:01.000
DEBUG = 0 # 1 to print debug info, 0 for real production utilisation

# OTHER
CATEGORY_M = ["J", "S", "35+", "45+", "55+", "65+"]
CATEGORY_F = ["J", "S", "35+", "45+", "55+"]
REWARD_COUNTER = 5 + 3 + len(CATEGORY_M) + len(CATEGORY_F) + 2 # 5&3 for scratch, 2 for locals
PC_NAME = "PC Affichage"