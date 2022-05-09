from neo4j import GraphDatabase

URL= 'bolt://localhost:7687'
USER= 'neo4j'
PASSWORD= '1234'

class Neo4j_app():
  def __init__(self, url, user, password):
    self.driver= GraphDatabase.driver(url, auth= (user, password))
    #self.create_constraints(f'''
    #CREATE CONSTRAINT ON (p:Person)
    #ASSERT p.name IS UNIQUE
    #''')
    #self.create_constraints(f'''
    #CREATE CONSTRAINT ON (p:Product)
    #ASSERT p.product IS UNIQUE
    #''')
  
  def close(self):
    self.driver.close()

  def _create_constraints(self, tx, query):
    return tx.run(query)
  
  def create_constraints(self, constraint):
    with self.driver.session() as session:
      return session.write_transaction(self._create_constraints, query= constraint)

  def get_client_by_name(self, name):
    with self.driver.session() as session:
      result= session.write_transaction(self._get_client_by_name, name)
      return result

  def _get_client_by_name(self, tx, name):
    query= (f'''
    MATCH (c:Client)
    WHERE c.name = '{name}'
    RETURN c
    ''')
    result= tx.run(query, name= name)
    return [{'client': r['c']['name']} for r in result]

  def get_vendor_by_name(self, name):
    with self.driver.session() as session:
      result= session.write_transaction(self._get_vendor_by_name, name)
      return result

  def _get_vendor_by_name(self, tx, name):
    query= (f'''
    MATCH (v:Vendor)
    WHERE v.name = '{name}'
    RETURN v
    ''')
    result= tx.run(query, name= name)
    return [{'vendor': r['v']['name']} for r in result]

  def get_product_by_name(self, name):
    with self.driver.session() as session:
      result= session.write_transaction(self._get_product_by_name, name)
      return result

  def _get_product_by_name(self, tx, name):
    query= (f'''
    MATCH (p:Product)
    WHERE p.product = '{name}'
    RETURN p
    ''')
    result= tx.run(query, name= name)
    return [{'product': r['p']['product']} for r in result]

  def create_client(self, name):
    with self.driver.session() as session:
      if self.get_client_by_name(name):
        return False
      result= session.write_transaction(self._create_and_return_client, name)
      return result

  def _create_and_return_client(self, tx, name):
    query= (f'''
    CREATE (c:Person:Client {{name: '{name}'}})
    return c
    ''')
    result= tx.run(query, name= name)
    return result.single()['c']
    #return [{'client': r['c']['name']} for r in result]

  def create_vendor(self, name):
    with self.driver.session() as session:
      if self.get_vendor_by_name(name):
        return False
      result= session.write_transaction(self._create_and_return_vendor, name)
      return result

  def _create_and_return_vendor(self, tx, name):
    query= (f'''
    CREATE (v:Person:Vendor {{name: '{name}'}})
    return v
    ''')
    result= tx.run(query, name= name)
    return result.single()['v']
    #return [{'vendor': r['v']['name']} for r in result]

  def create_product(self, product, category, vendor_name):
    with self.driver.session() as session:
      if self.get_product_by_name(product):
        return False
      result= session.write_transaction(self._create_and_return_product, product,  category, vendor_name)
      return result

  def _create_and_return_product(self, tx, product, category, vendor):
    query= (f'''
    MATCH (v:Vendor)
    WHERE v.name = '{vendor}'
    CREATE (p:Product {{product: '{product}', category: '{category}'}})
    CREATE (v)-[:Sell]->(p)
    return p
    ''')
    result= tx.run(query, product= product, category= category, vendor= vendor)
    try:
      return result.single()['p']
    except:
      return None
    #return [{'product': r['p']['product'], 'category': r['p']['category']} for r in result]

  def _buy_product(self, tx, buyer, product):
    query= (f'''
    MATCH (p:Product)
    WHERE p.product = '{product}'
    MATCH (c:Client)
    WHERE c.name= '{buyer}'
    CREATE (c)-[:Buy]->(p)
    return p
    ''')
    result= tx.run(query, buyer= buyer, product= product)
    try:
      return result.single()['p']
    except:
      return None
    #return [{'product': r['p']['product'], 'category': r['p']['category']} for r in result]

  def buy_product(self, buyer, product):
    with self.driver.session() as session:
      result= session.write_transaction(self._buy_product, buyer, product)
      return result
  
  def _recomend_product(self, tx, buyer, product, qualification):
    query= (f'''
    MATCH (p:Product)
    WHERE p.product = '{product}'
    MATCH (p)<-[b:Buy]-(c:Client)
    WHERE c.name= '{buyer}'
    CREATE (c)-[:Recommend {{qualification: {qualification}}}]->(p)
    return p
    ''')
    
    result= tx.run(query, buyer= buyer, product= product, qualification= qualification)
    try:
      return result.single()['p']
    except:
      return None
    #return [{'product': r['p']['product'], 'category': r['p']['category']} for r in result]

  def recomend_product(self, buyer, product, qualification):
    with self.driver.session() as session:
      result= session.write_transaction(self._recomend_product, buyer, product, qualification)
      return result

  def _top_sell_products(self, tx, n):
    query= (f'''
    MATCH (p:Product)<-[b:Buy]-(:Client)
    WITH p, count(b) AS qty
    MATCH (:Client)-[r:Recommend]->(p)
    RETURN p, qty, avg(r.qualification) AS average_qualification
    ORDER BY qty DESC
    LIMIT {n}
    ''')
    result= tx.run(query, n= n)
    try:
      return [{'product': r['p']['product'], 'category': r['p']['category'], 'qty': r['qty'], 'avg': r['average_qualification']} for r in result]
    except:
      return None

  def top_sell_products(self, n):
    with self.driver.session() as session:
      result= session.write_transaction(self._top_sell_products, n)
      return result