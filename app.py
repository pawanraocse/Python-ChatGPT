import openai
import requests
import streamlit as st

openai.api_key = "{API_KEY}"

def BasicGeneration(userPrompt):
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
          {"role": "user", "content": userPrompt}
      ]
    )
    return completion.choices[0].message.content

def GetBitCoinPrices():
  url = "https://coinranking1.p.rapidapi.com/coin/Qwsogvtv82FCd/history" 
  querystring = {"referenceCurrencyUuid":"yhjMzLPhuIDl","timePeriod":"7d"}

  headers = {
    	"content-type": "application/octet-stream",
    	"X-RapidAPI-Key": "{KEY}",
    	"X-RapidAPI-Host": "coinranking1.p.rapidapi.com"
    }
  response = requests.get(url, headers=headers, params=querystring)
  JSONResult = response.json()
  history = JSONResult["data"]["history"]
  prices = []
  for change in history:
     prices.append(change["price"])
  pricesList = ','.join(prices)
  return pricesList


st.title("Bition Analyzer")
st.header("Analyzing bitcion prices using ChatGPT")

if st.button('Start Analyzing'):
   with st.spinner('Getting Bitcoin Prices...'):
      bitcoinPrices = GetBitCoinPrices()
      st.success('Done!')
   with st.spinner('Analysing Bition Prices...'):
      prompt = f"""You are expert crypto trader with 10 years of experience,
             I will provide you the bitcion prices for last 7 days.Can you provide me with a technical analysis of bitcion
            based on these prices. here is what I want:
            Price Overview,
            Moving Averages
            Relative Strength Index (RSI),
            Do I buy or sell?
            please provide as much details as you can.
            Here is the price list: {bitcoinPrices}"""

      analysis = BasicGeneration(prompt)
      st.text_area('Analysis', analysis, height=500)
      st.success('Done!')
