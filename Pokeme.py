import json
import urllib
import requests
import pykemon


nombre=int(input())

client = pykemon.V1Client()

p=client.get_Pokemon(uid=nombre)

print(p.name)