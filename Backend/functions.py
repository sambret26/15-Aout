from databases.repositories.settingsRepository import SettingsRepository
from databases.repositories.runnersRepository import RunnersRepository
from databases.base import engine, session
import xml.etree.ElementTree as ET
import zipfile
import shutil
import os

import messages
import config
import sender

settingsRepository = SettingsRepository(engine)
runnersRepository = RunnersRepository(engine)

async def updateResultMessage(bot):
    channel = bot.get_channel(config.RESULTS_CHANNEL_ID)
    await checkRewards(channel)
    async for message in channel.history(limit=100):
        if message.content.startswith("Nombre"):
            arrived = str(runnersRepository.count(session))
            total = str(settingsRepository.getRunnerNumber(session))
            newMessage = messages.RESULT.replace("ARRIVED", arrived).replace("TOTAL", total)
            newMessage += messages.REWARDS_LIST
            newMessage += createMessage() 
            newMessage += messages.TO_SEND_MAIL
            await message.edit(content=newMessage)
            
async def checkRewards(channel):
    rewardsNumbersInDB = settingsRepository.getRewardsNumber(session)
    rewards = getRewards()
    rewardsNumber = 0
    for reward in rewards:
        if reward[3] != None : rewardsNumber+= 1
    if rewardsNumber == rewardsNumbersInDB : return
    settingsRepository.setRewardsNumber(session, rewardsNumber)
    if rewardsNumber == config.REWARD_COUNTER:
        createWordFile()
        sender.sendMail()
        await channel.send(messages.ALL_REWARDS_KNOWN)
        
def createMessage():
    data = getRewards()
    headers = ("Catégorie", "Sexe", "Classement", "Nom", "Prénom", "Dossard", "Temps")
    colWidths = [len(header) for header in headers]
    for row in data:
        if row[3] == None : continue
        for i, item in enumerate(row):
            colWidths[i] = max(colWidths[i], len(str(item)))
    rowFormat = " | ".join(f"{{:<{width}}}" for width in colWidths)
    table = []
    table.append(rowFormat.format(*headers))
    table.append("-+-".join("-" * width for width in colWidths))
    for row in data:
        if row[3] == None : continue
        table.append(rowFormat.format(*row))
    return "```\n" + "\n".join(table) + "\n```\n"

def createWordFile():
    oldTextList = []
    newTextList = []
    rewards = getRewards()
    for reward in rewards:
        category = reward[0]
        sex = reward[1] if reward[1] != "M" else "H"
        oldTextList.append("R" + category + sex)
        newTextList.append(str(reward[2]))
        oldTextList.append("L" + category + sex)
        newTextList.append(reward[3])
        oldTextList.append("F" + category + sex)
        newTextList.append(reward[4])
        oldTextList.append("T" + category + sex)
        newTextList.append(reward[6])
    replaceTextInDocument(oldTextList, newTextList)
        
def replaceTextInDocument(oldTextList, newTextList):
    unzipDocx(config.EMPTY_WORD_FILENAME, config.TEMP)
    xmlFilePath = os.path.join(config.TEMP, 'word/document.xml')
    for oldText, newText in zip(oldTextList, newTextList):
        replaceFlagInXml(xmlFilePath, oldText, newText)
    zipDir(config.TEMP, config.FINAL_WORD_FILENAME)
    shutil.rmtree(config.TEMP)

def unzipDocx(docxPath, extractTo):
    with zipfile.ZipFile(docxPath, 'r') as zipRef:
        zipRef.extractall(extractTo)
        
def zipDir(directory, zipFile):
    with zipfile.ZipFile(zipFile, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory):
            for file in files:
                filePath = os.path.join(root, file)
                arcname = os.path.relpath(filePath, directory)
                zipf.write(filePath, arcname)
                
def replaceFlagInXml(filePath, flag, value):
    tree = ET.parse(filePath)
    root = tree.getroot()
    for elem in root.iter():
        if elem.text and flag in elem.text:
            elem.text = elem.text.replace(flag, value if value != None else "")
    tree.write(filePath)
    
def getRewards():
    rewards = []
    for i in range(1, 6):
        category = "S" + str(i)
        reward = runnersRepository.getRewardInScratch(session, i, "M")
        if reward != None : rewards.append((category, *reward))
        else: rewards.append((category, "M", None, None, None, None, None))
    for i in range(1, 4):
        category = "S" + str(i)
        reward = runnersRepository.getRewardInScratch(session, i, "F")
        if reward != None : rewards.append((category, *reward))
        else: rewards.append((category, "F", None, None, None, None, None))
    for category in config.CATEGORY_F:
        reward = runnersRepository.getRewardInCategoryF(session, category)
        if reward != None : rewards.append((category, *reward))
        else : rewards.append((category, "F", None, None, None, None, None))
    for category in config.CATEGORY_M:
        reward = runnersRepository.getRewardInCategoryM(session, category)
        if reward != None : rewards.append((category, *reward))
        else : rewards.append((category, "M", None, None, None, None, None))
    bibNumberRewarded = [reward[4] for reward in rewards if reward[4] is not None]
    reward = runnersRepository.getFirstOriolF(session, bibNumberRewarded)
    if reward != None : rewards.append(("O", *reward))
    else : rewards.append(("O", "F", None, None, None, None, None))
    reward = runnersRepository.getFirstOriolM(session, bibNumberRewarded)
    if reward != None : rewards.append(("O", *reward))
    else : rewards.append(("O", "M", None, None, None, None, None))
    return(rewards)