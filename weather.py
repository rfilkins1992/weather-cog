import discord
from discord.ext import commands
import aiohttp
import asyncio
import json
import os
from .utils.dataIO import fileIO


class WeatherSearch:
	"""Search for weather in given location."""

	def __init__(self, bot):
		self.bot = bot
		self.settings = fileIO("data/weather/settings.json", "load")

	@commands.command(no_pm=True, pass_context=False)
	async def weather(self, location):
		url = "http://api.wunderground.com/api/" + self.settings['api_key'] + "/conditions/q/" + location + ".json"
		await self.bot.say(url)
		async with aiohttp.get(url) as r:
		    data = await r.json()
		if != ["error"] in data["response"]:
			currentobs = data["current_observation"]
			temperature = currentobs["temperature_string"]
			await self.bot.say(temperature)
		else:
			resp = data["error"]
			error = resp["description"]
			await self.bot.say(error +"\nPlease use your zip code for the format State/City (Country/City if outside of the US).")

def check_folders():
	if not os.path.exists("data/weather"):
		print("Creating data/weather folder...")
		os.makedirs("data/weather")

def check_files():
	f = "data/weather/settings.json"
	if not fileIO(f, "check"):
		print("Creating empty settings.json")
		fileIO(f, "save", {})

def setup(bot):
	check_folders()
	check_files()
	n = WeatherSearch(bot)
	bot.add_cog(n)