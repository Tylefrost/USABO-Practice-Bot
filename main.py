import discord
import os
import requests
import json
import random
import PyPDF2

intent = discord.Intents.default()
intent.members = True
intent.message_content = True
client = discord.Client(intents=intent)

#asking random bio questions
def getrandquestion():
  prompt= []
  randnum = random.randint(1,49)
  beginning = str(randnum)
  end = str(randnum+1)
  #random USABO open test
  pdf = PyPDF2.PdfReader(open('2004_OpenExam_AnswerKey.pdf', 'rb')) 
  count = len(pdf.pages)
  text = ''
  #appends each page to the str(text) so we can choose questions from the entire document
  for i in range(count):
    page = pdf.pages[i]
    text += page.extract_text()
  #splits the text in two at the random question number and chooses the 2nd string from that split. Then splits that string in two at "Answer:" and chooses the 1st string from that 2nd second split. This prints the question between random question number and the "Answer:" 
  prompt.append(text.split(beginning + ". ")[1].split("Answer: ")[0]) 
  prompt.append(text.split(beginning + ". ")[1].split("Answer: ")[1].split(end + ". ")[0])
  return prompt

def getquote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$rand'): #if user wants a random question reply a random question then after response show answer
    text = getrandquestion()
    await message.channel.send(text[0])
    def check(m):
      return m.content == '$ans' and m.channel == message.channel

    await client.wait_for('message', check=check)
    await message.channel.send(text[1])

    
  
  if message.content.startswith('$hello'): #if user says hello reply hello
    await message.channel.send('Hello!')
    
  if message.content.startswith('$inspire'): #if user wants inspiration reply quote
    quote = getquote()
    await message.channel.send(quote)
    
client.run(os.environ['TOKEN'])  #runs bot