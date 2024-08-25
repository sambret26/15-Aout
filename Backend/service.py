from databases.repositories.settingsRepository import SettingsRepository
from databases.repositories.runnersRepository import RunnersRepository
from databases.base import engine, session

import functions
import messages
import config
import reader
import sender

settingsRepository = SettingsRepository(engine)
runnersRepository = RunnersRepository(engine)

async def importFile(bot, message):
    file = await message.attachments[0].to_file()
    if file.filename.endswith(".cap"): 
        await message.attachments[0].save(config.GMCAP_FILENAME)
        reader.handleFile(config.GMCAP_FILENAME)
        await message.channel.send(messages.FILE_TREATED)
        await functions.updateResultMessage(bot)
    else : await message.channel.send(messages.UNKNOWN_EXTENSION) 
        
async def mail(ctx):
    functions.createWordFile()
    sender.sendMail()
    await ctx.send(messages.MAIL_SEND)
    
async def init(ctx):
    runnersRepository.deleteAll(session)
    settingsRepository.setRunnerNumber(session, 0)
    settingsRepository.setRewardsNumber(session, 0)
    await ctx.send(messages.DB_INIT)
    
async def test(ctx):
    await ctx.send(messages.OK)
    
async def clear(ctx, nombre):
    await ctx.channel.purge(limit=nombre+1, check=lambda msg: not msg.pinned)

    
