import requests
import html_strings
from bs4 import BeautifulSoup
from html2image import Html2Image

#disable remote debugging


def generate():
  URL = 'https://modernalgos.com/dailymkt.aspx'
  r = requests.get(URL)

  soup = BeautifulSoup(r.text, 'html.parser')
  table = soup.find('table', {'id': 'GridViewsocimedia1'})

  market_dashboard = []
  for row in table.find_all('tr')[1:7]:
      symbol_obj = {}
      for i, cell in enumerate(row.find_all('td')):
          if i == 0:
              symbol_obj['symbol'] = cell.text
          elif i == 1:
              symbol_obj['close'] = cell.text
          elif i == 2:
              symbol_obj['change_pts'] = cell.text
          elif i == 3:
              symbol_obj['change_per'] = float(cell.text)
      market_dashboard.append(symbol_obj)
  final_string_market_dashboard = ''
  for symbol in market_dashboard:
      color_1 = ''
      color_2 = ''
      direction = ''
      if symbol['change_per'] > 0:
          color_1 = 'green-theme-1'
          color_2 = 'green-theme-2'
          direction = 'up'
      else:
          color_1 = 'red-theme-1'
          color_2 = 'red-theme-2'
          direction = 'down'

      final_string_market_dashboard += f'''<div class="w-84 rounded-4xl h-36 bg-{color_2}">
              <div
                class="flex flex-col items-center justify-center w-full h-full"
              >
                <p class="text-3.1xl text-blue-theme-4 pb-4 uppercase">
                  {symbol['symbol']}  <span class="font-bold">{symbol['close']}</span>
                </p>
                <p
                  class="text-3.1xl grid gap-4 grid-flow-col items-center justify-center text-{color_1}"
                >
                  <span class="font-bold">
                    <i class="fas fa-caret-{direction} text-4xl"></i>
                  </span>
                  {symbol['change_pts']} ({symbol['change_per']}%)
                </p>
              </div>
            </div>'''

  market_range = []
  for row in table.find_all('tr')[9:11]:
      rows_to_be_taken = [0, 4, 5, 6, 7, 8]
      symbol_obj = {}
      for i, cell in enumerate(row.find_all('td')):
          if i in rows_to_be_taken:
              if i == 0:
                  symbol_obj['symbol'] = cell.text
              elif i == 4:
                  symbol_obj['range'] = cell.text
              elif i == 5:
                  symbol_obj['support2'] = cell.text
              elif i == 6:
                  symbol_obj['support1'] = cell.text
              elif i == 7:
                  symbol_obj['resistance1'] = cell.text
              elif i == 8:
                  symbol_obj['resistance2'] = cell.text
      market_range.append(symbol_obj)
  print(market_range)

  final_string_market_range_1 = ''
  final_string_market_range_2 = ''
  for symbol in market_range:
      final_string_market_range_1 += f'''
          <div
              class = "flex flex-col text-blue-theme-4 items-center justify-center w-full h-full"
            >
              <p class="text-3.1xl">
                <span class="font-bold uppercase">{symbol['symbol']}</span>
              </p>
              <p class="text-3.1xl">Range {'('}{symbol['range']}{')'}</p>
          </div>
      '''

      final_string_market_range_2 += f'''
          <div
              class="grid grid-cols-2 grid-flow-row items-center justify-center gap-x-10 w-full pl-4">
              <div>Support 2</div>
              <div class="pl-10">{symbol['support2']}</div>
              <div>Support 1</div>
              <div class="pl-10">{symbol['support1']}</div>
              <div>Resistance 1</div>
              <div class="pl-10">{symbol['resistance1']}</div>
              <div>Resistance 2</div>
              <div class="pl-10">{symbol['resistance2']}</div>
          </div>
      '''


  gainersAndLosers = []
  for row in table.find_all('tr')[14:24]:
      data = {}
      for i, cell in enumerate(row.find_all('td')):
          if i == 0:
              data['symbol'] = cell.text
          elif i == 1:
              data['close'] = cell.text
          elif i == 2:
              data['change_pts'] = cell.text
          elif i == 3:
              data['change_per'] = float(cell.text)
      gainersAndLosers.append(data)

  # sort data by change_per
  gainersAndLosers.sort(key=lambda x: x['change_per'], reverse=True)

  # top 5 are gainers
  top_gainers = gainersAndLosers[:5]

  # last 5 are losers
  top_losers = gainersAndLosers[-5:]

  final_top_gainers = ''
  for symbol in top_gainers:
    final_top_gainers += f'''
    <div class="flex flex-row items-center justify-center">
                  <div
                  class="flex flex-col items-center justify-center w-full h-118 rounded-4xl bg-green-theme-2"
                >
                  <p class="text-xl text-blue-theme-4 uppercase">
                    {symbol['symbol']} <span class="font-bold">{symbol['close']}</span>
                  </p>

                  <p class="text-2.5xl pt-2 text-green-theme-1 uppercase">
                    <i class="fas fa-caret-up"></i>
                    {symbol['change_pts']} {'('}{symbol['change_per']}{')'}%
                  </p>
                </div>
                </div>
                '''
  final_top_losers = ''
  for symbol in top_losers:
    final_top_losers += f'''
    <div class="flex flex-row items-center justify-center">
                  <div
                  class="flex flex-col items-center justify-center w-full h-118 rounded-4xl bg-red-theme-2"
                >
                  <p class="text-xl text-blue-theme-4 uppercase">
                    {symbol['symbol']} <span class="font-bold">{symbol['close']}</span>
                  </p>

                  <p class="text-2.5xl pt-2 text-red-theme-1 uppercase">
                    <i class="fas fa-caret-down"></i>
                    {symbol['change_pts']} {'('}{symbol['change_per']}{')'}%
                  </p>
                </div>
                </div>
                '''


  block_deals = {}
  block_deals['symbol'] = table.find_all('tr')[27].find_all('td')[0].text
  block_deals['trade_price'] = table.find_all('tr')[27].find_all('td')[9].text
  block_deals['volume'] = table.find_all('tr')[27].find_all('td')[10].text
  block_deals['buysell'] = table.find_all('tr')[27].find_all('td')[11].text

  if block_deals['buysell'] == 'BUY':
    block_deals['color'] = 'green-theme-2'
  else:
    block_deals['color'] = 'red-theme-1'

  block_deals_string = f'''
  <div class="grid grid-cols-3 items-center justify-around pt-4">
            <div class="flex flex-col items-center justify-center">
              <p class="text-blue-theme-4 font-bold text-3xl">Symbol</p>
              <p class="text-blue-theme-4 pt-2 text-3xl">{block_deals["symbol"]}</p>
            </div>
            <div class="flex flex-col items-center justify-center">
              <p class="text-blue-theme-4 font-bold text-3xl">Price</p>
              <p class="text-blue-theme-4 pt-2 text-3xl">{block_deals["trade_price"]}</p>
            </div>
            <div class="flex flex-col items-center justify-center">
              <p class="text-blue-theme-4 font-bold text-3xl">Volume {'('}Buy/Sell{')'}</p>
              <p class="text-blue-theme-4 pt-2 text-3xl">{block_deals["volume"]} {'('}<span class="text-{block_deals['color']}">{block_deals['buysell']}</span>{')'}</p>
            </div>
          </div>
          '''

  institutional_activity_fii = {}
  institutional_activity_fii['buy_value'] = table.find_all(
      'tr')[31].find_all('td')[12].text
  institutional_activity_fii['sell_value'] = table.find_all(
      'tr')[31].find_all('td')[13].text
  institutional_activity_fii['net_value'] = table.find_all(
      'tr')[31].find_all('td')[14].text

  institutional_activity_dii = {}
  institutional_activity_dii['buy_value'] = table.find_all(
      'tr')[35].find_all('td')[12].text
  institutional_activity_dii['sell_value'] = table.find_all(
      'tr')[35].find_all('td')[13].text
  institutional_activity_dii['net_value'] = table.find_all(
      'tr')[35].find_all('td')[14].text

  institutional_activity = f'''
        <div class="grid grid-cols-2 items-center justify-around pt-4 px-24 w-full">
          <div class="flex flex-col items-center justify-center w-full">
            <p class="text-blue-theme-4 text-3xl font-bold">FII (Equity)</p>
            <div class="w-full">
              <div class="flex flex-row items-center justify-around w-full pt-4">
                <div class="text-blue-theme-4 text-3xl">
                  Buy Value (Rs. in Cr.)
                </div>
                <div class="text-blue-theme-4 text-3xl">{institutional_activity_fii['buy_value']}</div>
              </div>
              <div class="flex flex-row items-center justify-around w-full pt-4">
                <div class="text-blue-theme-4 text-3xl">
                  Sell Value (Rs. in Cr.)
                </div>
                <div class="text-blue-theme-4 text-3xl">{institutional_activity_fii['sell_value']}</div>
              </div>
              <div class="flex flex-row items-center justify-around w-full pt-4">
                <div class="text-blue-theme-4 text-3xl">
                  Net Value (Rs. in Cr.)
                </div>
                <div class="text-blue-theme-4 text-3xl">{institutional_activity_fii['net_value']}</div>
              </div>
            </div>
          </div>
          <div class="flex flex-col items-center justify-center">
            <p class="text-blue-theme-4 text-3xl font-bold">DII (Equity)</p>
            <div class="w-full">
              <div class="flex flex-row items-center justify-around w-full pt-4">
                <div class="text-blue-theme-4 text-3xl">
                  Buy Value (Rs. in Cr.)
                </div>
                <div class="text-blue-theme-4 text-3xl">{institutional_activity_dii['buy_value']}</div>
              </div>
              <div class="flex flex-row items-center justify-around w-full pt-4">
                <div class="text-blue-theme-4 text-3xl">
                  Sell Value (Rs. in Cr.)
                </div>
                <div class="text-blue-theme-4 text-3xl">{institutional_activity_dii['sell_value']}</div>
              </div>
              <div class="flex flex-row items-center justify-around w-full pt-4">
                <div class="text-blue-theme-4 text-3xl">
                  Net Value (Rs. in Cr.)
                </div>
                <div class="text-blue-theme-4 text-3xl">{institutional_activity_dii['net_value']}</div>
              </div>
            </div>
          </div>
        </div>
  '''

  html_string_1 = html_strings.template_1(final_string_market_dashboard, final_string_market_range_1, final_string_market_range_2)
  html_string_2 = html_strings.template_2(final_top_gainers, final_top_losers, block_deals_string, institutional_activity)

  with open('index1.html', 'w') as f:
      f.write(html_string_1)

  with open('index2.html', 'w') as f:
      f.write(html_string_2)
      
  hti = Html2Image()  
      
  try: 
      hti.screenshot(html_file='index1.html',
                    save_as='Image-1.jpg',
                    size=(1200, 1200)
                    )

      hti.screenshot(html_file='index2.html',
                      save_as='Image-2.jpg',
                      size=(1200, 1200)
    )
  except:
    print(e)
  
  return ['Image-1.jpg', 'Image-2.jpg']
