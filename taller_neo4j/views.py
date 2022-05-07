import json
from django.http import JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from urllib3 import HTTPResponse

from taller_neo4j.neo4j import Neo4j_app, URL, USER, PASSWORD

# Create your views here.

neo4j_app= Neo4j_app(URL, USER, PASSWORD)

def index(request):
  pass

@csrf_exempt
def clients(request):
  if request.method == 'POST':
    #data= json.loads(request.body)
    data= request.POST
    c= neo4j_app.create_client(name= data['name'])
    if c:
      return JsonResponse(data= {k:c[k] for k in c.keys()}, status=201)
    else:
      return JsonResponse(data= {'msg': f'The client with name: {data["name"]} already exists'})
  return HttpResponseNotFound(content= 'No implemented')

@csrf_exempt
def vendors(request):
  if request.method == 'POST':
    #data= json.loads(request.body)
    data= request.POST
    v= neo4j_app.create_vendor(name= data['name'])
    if v:
      return JsonResponse(data= {k:v[k] for k in v.keys()}, status=201)
    else:
      return JsonResponse(data= {'msg': f'The vendor with name: {data["name"]} already exists'})
  return HttpResponseNotFound(content= 'No implemented')

@csrf_exempt
def products(request):
  if request.method == 'POST':
    #data= json.loads(request.body)
    data= request.POST
    p= neo4j_app.create_product(product= data['product'], category= data['category'], vendor_name= data['vendor'])
    if p:
      return JsonResponse(data= {k:p[k] for k in p.keys()}, status=201)
    else:
      return JsonResponse(data= {'msg': f'The product with name: {data["product"]} already exists'})
  return HttpResponseNotFound(content= 'No implemented')

@csrf_exempt
def buy_products(request):
  if request.method == 'POST':
    data= request.POST
    p= neo4j_app.buy_product(buyer= data['buyer'], product= data['product'])
    if p:
      return JsonResponse(data= {k:p[k] for k in p.keys()}, status= 201)
    else:
      return JsonResponse(data= {'msg': f'The product {data["product"]} could not be buy'})
  return HttpResponseNotFound(content= 'No implemented')

@csrf_exempt
def recomendations(request):
  if request.method == 'POST':
    data= request.POST
    try:
      cal= int(data['calification'])
    except ValueError:
        return JsonResponse(data= {'msg': f'The calification must be an integer not: {data["calification"]}'})
    if cal in range(0,6):
      p= neo4j_app.recomend_product(buyer= data['buyer'], product= data['product'], calification= cal)
      if p:
        return JsonResponse(data= {k:p[k] for k in p.keys()}, status= 201)
      else:
        return JsonResponse(data= {'msg': f'The product {data["product"]} could not be recomended'})
    else:
        return JsonResponse(data= {'msg': f'The calification must be between 0 and 5 not: {data["calification"]}'})
  return HttpResponseNotFound(content= 'No implemented')

def top_products(request):
  return HttpResponseNotFound(content= 'No implemented')