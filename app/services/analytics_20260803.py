from app.services.fake_data import ECommerceWorld
from collections import defaultdict
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models import Order, Customer, Order_item
import time

def order_count(db: Session, city: str = None) -> int:
    query = db.query(func.count(Order.id))

    if city is not None:
        # Customer 테이블과 JOIN하여 city 조건 추가
        query = query.join(Order.customer).filter(Customer.city == city)

    return query.scalar()


def order_count_python(data, city=None):
    if city is None:
        return len(data.orders)
    else:
        return len([o for o in data.orders if o.customer.city == city])


def customer_count(db, city=None):
    query = db.query(func.count(Customer.id))

    if city is not None:
        query = query.filter(Customer.city == city)

    return query.scalar()

def customer_count_python(data, city=None):
    if city is None:
        return len(data.customers)
    else:
        return len([c for c in data.customers if c.city == city])




def order_item_count(data):
    return(len(data.order_items))

def product_count(data):
    return(len(data.products))


def total_sales_python(data, city=None):
    if city is None:
        return sum(item.quantity * item.unit_price for item in data.order_items)
    else:
        return sum(item.quantity * item.unit_price for item in data.order_items if item.order.customer.city == city)

def total_sales(db, city=None):
    # 1. 수량 * 단가의 합계(SUM) 집계 식 정의
    stmt = select(
        func.coalesce(
            func.sum(Order_item.quantity * Order_item.unit_price),
            0
        )
    )

    # 2. city 인자가 주어졌을 경우 JOIN 및 Filter 추가
    if city is not None:
        stmt = (
            stmt
            .join(Order_item.order)  # OrderItem -> Order 관계 조인
            .join(Order.customer)  # Order -> Customer 관계 조인
            .filter(Customer.city == city)
        )

    # 3. 쿼리 실행 및 결과 반환
    return db.scalar(stmt)




def flatten(nested):
    for item in nested:
        # Check if the item is a list (but not a string, as strings are iterable)
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item

def city_sales(data):
    cities = [(v.city, v.orders) for v in data.customers]
    cities2C = {}
    for city, order in cities:
        cities2C.setdefault(city,[]).append(order)

    sales_city = {}
    for k, v in cities2C.items():
        sales = 0
        for order in list(flatten(v)): # this is important to flatten the "v". it is arbitrarily nested.
            for item in data.order_items:
                if order.id == item.order_id:
                    sales += item.quantity * item.unit_price
        sales_city[k] = sales

    return sales_city


def product_sales(data):
    products = [(item.product_id, item.quantity, item.unit_price) for item in data.order_items]
    products2C = {}
    for product in products:
        if product[0] not in products2C: products2C[product[0]] = []
        products2C[product[0]].append(product[1:])

    sales_product = {}
    for k, v in products2C.items():
        sales = 0
        for item in v:
            sales += item[0]*item[1]

        # product name 찾기
        for product in data.products:
            if product.id == k:
                sales_product[product.name] = sales
                break

    return sales_product


def yearly_sales(data):
    years = [(order.order_date[:4], order.id) for order in data.orders]
    years2C = {}
    for year, _id in years:
        if year not in years2C: years2C[year] = []
        years2C[year].append(_id)
    # print(years2C)

    sales_year = {}
    for year, _ids in years2C.items():
        sales = 0
        for item in data.order_items:
            if item.order_id in _ids:
                sales += item.quantity * item.unit_price
        sales_year[year] = sales

    return sales_year


def monthly_sales_mine(data):
    months = [(order.order_date[:7], order.id) for order in data.orders]
    months2C = {}
    for month, _id in months:
        if month not in months2C: months2C[month] = []
        months2C[month].append(_id)
    # print(months2C)

    sales_month = {}
    for month, _ids in months2C.items():
        sales = 0
        for item in data.order_items:
            if item.order_id in _ids:
                sales += item.quantity * item.unit_price
        sales_month[month] = sales

    return sales_month


def monthly_sales(world, city = None):
    sales = defaultdict(float)
    if city is None:
        for item in world.order_items:
            month = item.order.order_date[:7]

            sales[month] += item.quantity * float(item.unit_price)

        months = sorted(sales.keys())
    else:
        for item in world.order_items:
            month = item.order.order_date[:7]
            if item.order.customer.city == city:
                sales[month] += item.quantity * float(item.unit_price)

        months = sorted(sales.keys())

    return {
        "months": months,
        "sales": [sales[m] for m in months]
    }

def top_category(world, city=None):
    sales = defaultdict(float)

    if city is None:
        for item in world.order_items:
            category = item.product.category_id

            sales[category] += item.quantity * float(item.unit_price)
    else:
        for item in world.order_items:
            category = item.product.category_id
            if item.order.customer.city == city:
                sales[category] += item.quantity * float(item.unit_price)

    print('for category total sales: ', sum(sales.values()))

    topSales = max(sales.values())
    for k,v in sales.items():
        if v == topSales:
            for item in world.categories:
                if item.id == k:
                    return item.name


def piechart_categories(world, city=None):
    sales = defaultdict(float)

    if city is None:
        for item in world.order_items:
            category = item.product.category_id

            sales[category] += item.quantity * float(item.unit_price)
    else:
        for item in world.order_items:
            category = item.product.category_id
            if item.order.customer.city == city:
                sales[category] += item.quantity * float(item.unit_price)

    sales_new = {}
    for k,v in sales.items():
        for item in world.categories:
            if item.id == k:
                sales_new[item.name] = v

    return sales_new


def barchart_cities(data):
    return city_sales(data)


def dashboard_summary(db, city=None):
    return {
        "customers": customer_count(db, city),
        "orders": order_count(db, city),
        "sales": total_sales(db, city),
        "top_category": top_category(db, city)
    }


def confirmData(data: ECommerceWorld):
    with open("example.txt", "w", encoding="utf-8") as f:

        f.write('-'*10+'\ncategoryies:\n')
        for j, order in enumerate(data.categories):
            f.write(f"{j}: id={order.id}, name={order.name}\n")

        f.write('-'*10+'\nproducts:\n')
        for j, order in enumerate(data.products):
            f.write(f"{j}: id={order.id}, category_id={order.category_id}, name={order.name}, price={order.price}\n")

        f.write('-'*10+'\ncustomers:\n')
        for j, order in enumerate(data.customers):
            f.write(f"{j}: id={order.id}, name={order.name}, city=({order.city}), signup_date={order.signup_date}, customer_code={order.customer_code}\n")

        f.write('-'*10+'\norders:\n')
        for j, order in enumerate(data.orders):
            f.write(f"{j}: id={order.id}, customer_id={order.customer_id}, order_date=({order.order_date}), order_code={order.order_code}\n")

        f.write('-'*10+'\norder_items:\n')
        for j, order in enumerate(data.order_items):
            f.write(f"{j}: id={order.id}, order_id={order.order_id}, product_id=({order.product_id}), quantity={order.quantity}, price={order.unit_price}\n")


def analyse(data: ECommerceWorld):

    confirmData(data)
    totalSales = total_sales(data)
    sales_city = city_sales(data)
    totalSales_city = sum(sales_city.values())
    equality = totalSales_city == totalSales
    print('per city', totalSales_city, equality)
    if not equality:
        print('for total_sales: ', totalSales)

    # with open("sales_per_city.txt", "w", encoding="utf-8") as f:
    #     f.write('='*50+'\ncity\tsale\n')
    #     # for k,v in sales_city.items():
    #     for k in sorted(sales_city.keys()):
    #         v = sales_city[k]
    #         f.write(f"{k}\t{v}\n")
    #     f.write('-'*20+'\n')
    #     f.write(f'total\t{sum(v for v in sales_city.values())}')

    sales_product = product_sales(data)
    totalSales_product = sum(sales_product.values())
    equality2 = totalSales_product == totalSales
    print('per product', totalSales_product, equality2)
    if not equality2:
        print('for total_sales: ', totalSales)

    # with open("sales_per_product.txt", "w", encoding="utf-8") as f:
    #     f.write('='*50+'\nproduct\tsale\n')
    #     for v in sales_product.values():
    #         f.write(f"{v[0]}\t{v[1]}\n")
    #     f.write('-'*20+'\n')
    #     f.write(f'total\t{sum([v[1] for v in sales_product.values()])}')

    sales_year = yearly_sales(data)
    totalSales_year = sum(sales_year.values())
    equality3 = totalSales_year == totalSales
    print('per year', totalSales_year, equality3)
    if not equality3:
        print('for total_sales: ', totalSales)

    # with open("sales_per_year.txt", "w", encoding="utf-8") as f:
    #     f.write('='*50+'\nyear\tsale\n')
    #     # for k,v in sales_year.items():
    #     for k in sorted(sales_year.keys()):
    #         v = sales_year[k]
    #         f.write(f"{k}\t{v}\n")
    #     f.write('-'*20+'\n')
    #     f.write(f'total\t{sum([v for v in sales_year.values()])}')

    sales_month = monthly_sales_mine(data)
    totalSales_month = sum(sales_month.values())
    equality4 = totalSales_month == totalSales
    print('per month', totalSales_month, equality4)
    if not equality4:
        print('for total_sales: ', totalSales)

    sales_month_GPT = monthly_sales(data)
    totalSales_month_GPT = sum(sales_month_GPT['sales'])
    equality4_GPT = totalSales_month_GPT == totalSales
    print('per month', totalSales_month, equality4_GPT)
    if not equality4_GPT:
        print('for total_sales: ', totalSales)



def test_analyze(data, db, city=None):
    begin = time.time()
    ans = total_sales_python(data, city)
    print('testing.... with python: ', ans, 'with ', time.time() - begin)
    begin = time.time()
    ans2 = total_sales(db, city)
    print('testing.... with SQL query: ', ans2, ans2 == ans, 'with ', time.time() - begin)


