import random
from app.services.fake_data import ECommerceWorld
from app.models import Customer, Category, Product, Order, Order_item


def generate_fake_data(
        customer_count = 100,
        product_count = 20,
        order_count = 500
    ):

    products_dict = {'computing': [['laptop', 3000.00, 40], ['desktop', 3500.00, 1], ['tablet', 2000.00, 37],
                              ['monitor', 500.00, 42], ['printer', 550.00, 14]],
                'Home Theater': [['TV 4K', 2000.00, 35], ['TV 8K', 3000.00, 29], ['TV QLED 8K', 4000.00, 11],
                                 ['projector', 1500.00, 11], ['soundbar', 1299.00, 4]],
                'appliances': [['refrigerator', 2000.00, 26], ['washer', 1000.00, 20], ['dryerB', 800.00, 2],
                               ['dish washer', 850.00, 4], ['range', 500.00, 5]],
                'mobile': [['iPhone', 2009.00, 26], ['galaxy', 1929.00, 30], ['google phone', 1539.00, 82],
                           ['smart watch', 821.00, 60], ['headphone', 212.00, 46]]
                }

    products_list = []
    for k, product_dict in products_dict.items():
        products_list.extend([(k, v[0], v[1], v[2]) for v in product_dict])

    words = ['Adrianna', 'Foley', 'Mohammad', 'Roman', 'Astrid', 'Carey', 'Watson', 'Hull', 'Andi', 'Lowe',
             'Julius', 'Zuniga', 'Leslie', 'Summers', 'Darius', 'Aguirre', 'Ariah', 'Doyle', 'Kashton', 'Blevins',
             'Aila', 'Sanford', 'Truett', 'Hartman', 'Kennedi', 'Pineda', 'Gerardo','Greer', 'Reina','Romero',
             'Bryson', 'Esquivel', 'Jaylee', 'Cobb', 'Raphael', 'Kerr', 'Baylee', 'Gillespie', 'Forest', 'Beck',
             'Gia', 'Vega', 'Aidan', 'Juarez', 'Juliet', 'Stanley', 'Manuel', 'Stephens', 'Millie', 'Dalton',
             'Fletcher', 'Pratt', 'Ailani', 'Fuller', 'Andre', 'Valentine', 'August', 'Villegas', 'Clyde', 'Xiong',
             'Amayah', 'Moran', 'Tate', 'Barker', 'Remington', 'McConnell', 'London', 'Costa', 'Robin', 'McKenzie',
             'Scott', 'Bell', 'Melody', 'Parsons', 'Lewis', 'Greene', 'Selena', 'Valencia', 'Dax', 'Dillon',
             'Laurel', 'James', 'Jaxson','Wall', 'Jayda', 'Small', 'Rudy', 'Parkers', 'Aubrey', 'Ho',
             'Morgan', 'Bryant', 'Parker', 'Best', 'Harlem', 'Drake', 'Jayleen', 'Andrews', 'Lukas', 'Avila',
             'Amiyah', 'Stewart', 'Nolan', 'Castillo', 'Eva', 'Blankenship', 'Ernesto', 'Delgado', 'Alani', 'Washington',
             'Juan', 'Valenzuela', 'Henley', 'Bates', 'Ellis', 'Norton', 'Kylee', 'Randall', 'Trenton', 'Stafford',
             'Bridget', 'Thornton', 'Malik', 'Freeman', 'Norah', 'Lopez', 'Michael', 'Zimmerman', 'Ariyah', 'English']

    cities = [('Seoul', 9.29e6), ('Incheon', 3.06e6), ('Suwon', 1.2e6), ('Yongin', 1.11e6),
              ('Goyang', 1.08e6), ('Hwaseong', 1.07e6), ('Seongnam', 0.91e6), ('Bucheon', 0.78e6),
              ('Namyangju', 0.75e6), ('Ansan', 0.61e6), ('Pyengtaek', 0.61e6), ('Siheung', 0.6e6), ('Anyang', 0.55e6)]

    customer_names = []
    while len(customer_names) < customer_count:
        name = ' '.join(random.sample(words,2))
        if name not in customer_names:
            customer_names.append(name)

    print(customer_names)

    years = [f"{random.choice(range(2023, 2026))}" for _ in range(order_count)]
    month_days = [(random.choice(range(1, 13)), random.choice(range(1, 32))) for _ in range(order_count)]
    hour_mins = [(random.choice(range(10, 20)), random.choice(range(1, 60))) for _ in range(order_count)]
    for j, (m,d) in enumerate(month_days):
        if m in [4, 6, 9, 11] and d>30:
            month_days[j] = (m, d-1)
        elif m == 2 and d>28:
            month_days[j] = (m, 28)
    order_dates = [y+f"-{m:02d}-{d:02d} {h}::{minute:02d}" for y, (m, d), (h, minute) in zip(years, month_days, hour_mins)]

    orders_on_dates = []
    for date in order_dates:
        order_tmp = {'customer': random.choice(customer_names), 'order_date': date}
        products2order_tmp = random.choices(population=products_list, weights=[p for _,_,_,p in products_list], k=random.randint(3, 8))
        order_tmp['products'] = products2order_tmp

        orders_on_dates.append(order_tmp)

    customers = {}
    for order in orders_on_dates:
        if order['customer'] not in customers: customers[order['customer']] = []
        customers[order['customer']].append(order)

    print(customers)

    customers_id = {}
    for customer, purchases in customers.items():
        customers_id[customer] = sorted(purchase['order_date'] for purchase in purchases)[0].replace('::', '').replace(' ','-')

    print(len(order_dates), len(orders_on_dates), len(customers), len(customers_id))
    print(customers_id)


    # Customer <-> Order
    customer_map = {}
    customers = []
    order_map = {}
    orders = []

    for name, _id in customers_id.items():
        year, month, day, hNm = _id.split('-')
        tmp = Customer(name=name,
                       city=random.choices(population = [c for c,_ in cities], weights = [p for _,p in cities], k=1)[0],
                       signup_date = f"{year}-{month}-{day} {hNm[:2]}:{hNm[2:]}",
                       customer_code = _id)
        customers.append(tmp)
        customer_map[name] = tmp

    for order in orders_on_dates:
        tmp = Order(order_date=order['order_date'], customer=customer_map[order['customer']])
        orders.append(tmp)
        order_map[order['order_date']] = tmp


    # Category <-> Product
    category_map = {}
    categories = []
    product_map = {}
    products = []
    for k, v in products_dict.items():
        tmp = Category(name=k)
        category_map[k] = tmp
        categories.append(tmp)
        for name, price, popularity in v:
            tmp = Product(name=name,price=price,category=category_map[k])
            product_map[name] = tmp
            products.append(tmp)


    # Order, Product <-> Order_Item
    order_items = []
    order_item_map = {}
    for order in orders_on_dates:
        for product in order['products']:
            tmp = Order_item(
                order=order_map[order['order_date']],
                product=product_map[product[1]],
                quantity=5+random.choice(range(5)),
                unit_price=product[2]
            )
            order_items.append(tmp)
            order_item_map[order['order_date']] = tmp


    return ECommerceWorld(
        customers = customers,
        categories = categories,
        products = products,
        orders = orders,
        order_items = order_items,

        customer_map = customer_map,
        category_map = category_map,
        product_map = product_map,
        order_map = order_map,
        order_item_map = order_item_map
    )



'''generate_fake_data()는 단순히 "랜덤 데이터를 만드는 함수"가 아니라,
현실적인 전자상거래 데이터를 시뮬레이션하는 함수를 목표로 해 보면 좋겠습니다.

실제 쇼핑몰과 비슷한 데이터
이름은 중복될 수 있지만 고객 ID는 유일하게 생성하기
주문 날짜를 최근 3년 사이에 랜덤하게 분포시키기
상품별 인기도를 균등하게 하지 않고, 일부 인기 상품에 주문이 몰리도록 만들기
한 주문에는 평균 2~4개의 상품이 들어가도록 생성하기

예를 들어 앞으로는 이런 규칙들을 하나씩 추가할 수 있습니다.

고객은 서울보다 수도권에 더 많이 분포한다.
일부 상품은 베스트셀러라 주문이 훨씬 많이 발생한다.
주말에는 주문량이 평일보다 많다.
연말 시즌에는 주문량이 급증한다.
'''


# if __name__ == "__main__":
#     g = generate_fake_data(6, 20, 100)
#     print([c.city for c in g.customers])

    # data = range(10)
    # for _ in range(10):
    #     print(random.choices(population=data, weights=[1,1,1,3,1,1,1,10,3,1], k=4), random.sample(data,4))

    # purchase_customers = {}
    # for customer, purchases in customers.items():
    #     purchase_customers[customer] = sum(product[2] for purchase in purchases for product in purchase['products'])
    #
    # max_Purchase = max(purchase_customers.values())
    # for k,v in purchase_customers.items():
    #     if v == max_Purchase:
    #         max_Customer = k
    #         break
    # print(f'가장 많이 구매한 고객: {max_Customer}(id = {customers_id[max_Customer]}) purchased {max_Purchase}.')
    #
    # min_Purchase = min(purchase_customers.values())
    # for k,v in purchase_customers.items():
    #     if v == min_Purchase:
    #         min_Customer = k
    #         break
    # print(f'가장 적게 구매한 고객: {min_Customer}(id = {customers_id[min_Customer]}) purchased {min_Purchase}.')
    #
    # products_all = []
    # for order in orders:
    #     for item in order['products']:
    #         products_all.append(item)
    # print(f"판매된 총 물품수: {len(set(products_all))}") # 20
    #
    # # 품목별 판매 수:
    # counts = {}
    # for product in products:
    #     counts[product] = products_all.count(product)
    #
    # maxCount = max(counts.values())
    # mostFavored = None
    # for k,v in counts.items():
    #     if v == maxCount:
    #         mostFavored = k
    #         break
    # print(f'가장 많이 판매된 품목: {mostFavored} sold {maxCount} items.')
    #
    # minCount = min(counts.values())
    # leastFavored = None
    # for k,v in counts.items():
    #     if v == minCount:
    #         leastFavored = k
    #         break
    # print(f'가장 적게 판매된 품목: {leastFavored} sold {minCount} items.')


    # 나중에
    # @dataclass
    # class FakeData:
    #   customers: list[Customer]
    #   products: list[Product]
    #   orders: list[Order
    #   order_items: list[OrderItem]
    # 그러면
    # data.customers
    # data.products
    # data.orders    처럼 사용할 수 있다.
