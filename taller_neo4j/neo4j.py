from neo4j import GraphDatabase

URL= 'bolt://localhost:7687'
USER= 'neo4j'
PASSWORD= '1234'

class Neo4j_app():
  def __init__(self, url, user, password):
    self.driver= GraphDatabase.driver(url, auth= (user, password))
  
  def close(self):
    self.driver.close()

  def create_client(self, name):
    with self.driver.session() as session:
      result= session.write_transaction(self._create_and_return_client, name)
      return result

  def _create_and_return_client(self, tx, name):
    query= (f'''
    CREATE (c:Person:Client {{name: '{name}'}})
    return c
    ''')
    result= tx.run(query, name= name)
    return [{'client': r['c']['name']} for r in result]

  def create_vendor(self, name):
    with self.driver.session() as session:
      result= session.write_transaction(self._create_and_return_vendor, name)
      return result

  def _create_and_return_vendor(self, tx, name):
    query= (f'''
    CREATE (v:Person:Vendor {{name: '{name}'}})
    return v
    ''')
    result= tx.run(query, name= name)
    return [{'vendor': r['v']['name']} for r in result]

  def create_product(self, product, category):
    with self.driver.session() as session:
      result= session.write_transaction(self._create_and_return_product, product,  category)
      return result

  def _create_and_return_product(self, tx, product, category):
    query= (f'''
    CREATE (p:Product {{product: '{product}', category: '{category}'}})
    return p
    ''')
    result= tx.run(query, category= category)
    return [{'product': r['p']['product'], 'category': r['p']['category']} for r in result]