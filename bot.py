#!/bin/python3

import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import ssl
import requests
import sys
import traceback
import uuid

load_dotenv()

with open("DISCORD_TOKEN.conf", "r")as f:
    DISCORD_TOKEN=f.read()
    
bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def findname(ctx):
    if (len(ctx.message.attachments) > 0):
        try:
            jpgurl = ctx.message.attachments[0].url
            await ctx.send("Searching...")

            headers = {
                    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
                    }
            url = 'https://api.trace.moe/search?anilistInfo&url=' + jpgurl
            r = requests.get(url, headers = headers)
            seconds = int(r.json()['result'][0]['from'])
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            await ctx.send(jpgurl)
            await ctx.send(str(r.json()['result'][0]['anilist']['title']['native']) + '\n' + 
#                            str(r.json()['result'][0]['anilist']['title']['chinese']) + '\n' + 
                            str(r.json()['result'][0]['anilist']['title']['romaji']) + '\n' + 
                            str(r.json()['result'][0]['anilist']['title']['english']) + '\n' + 
                            'EP#' + str(r.json()['result'][0]['episode']).zfill(2) + ' ' + str(h).zfill(2) + ':' + str(m).zfill(2) + ':' + str(s).zfill(2) + '\n' + 
                            ('%.2f%%' % (float(r.json()['result'][0]['similarity']) * 100) + ' similarity'))

            videourl = r.json()['result'][0]['video']
#            videourl = 'https://media.trace.moe/video/' + str(r.json()['docs'][0]['anilist_id']) + '/' + r.json()['docs'][0]['filename'] + '?t=' + str(r.json()['docs'][0]['at']) + '&token=' + r.json()['docs'][0]['tokenthumb']

            #print(videourl)
            
            uuidd = uuid.uuid4()

            if videourl != None and videourl != "":
                req = requests.get(videourl, headers = headers)
                videoname = r.json()['result'][0]['filename'] + str(uuidd) + '.mp4'
                with open(videoname, "wb")as f:
                    f.write(req.content)
                    f.close()

                await ctx.send(file=discord.File(videoname))
                os.remove(videoname)

        except Exception as e:
            error_class = e.__class__.__name__ #取得錯誤類型
            detail = e.args[0] #取得詳細內容
            cl, exc, tb = sys.exc_info() #取得Call Stack
            lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
            fileName = lastCallStack[0] #取得發生的檔案名稱
            lineNum = lastCallStack[1] #取得發生的行號
            funcName = lastCallStack[2] #取得發生的函數名稱
            errMsg = "File \"{}\", line {}, in {}: [{}] \r\n\r\nerrMsg:{}".format(fileName, lineNum, funcName, error_class, detail)
            print(errMsg)
            #print(e)
            await ctx.send("error!")

    else:
        #print("dead")
        await ctx.send("bad args!")
    #lock.release()

@bot.command(pass_context=True)
async def upload_file(ctx):
    await ctx.send(type(ctx))
    #attachment_url = ctx.message.attachments[0].url
    #print(attachment_url)
    #file_request = requests.get(attachment_url)
    #print(file_request.content)

bot.run(DISCORD_TOKEN)
