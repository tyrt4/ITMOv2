from pathlib import Path
import json
from typing import List, Optional, Dict, Any
from datetime import datetime, time, date, timezone
import random
from fastapi import FastAPI, APIRouter, HTTPException, status, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field


def create_app() -> FastAPI:
    app = FastAPI(title="Coffee Backend", version="0.2.0")

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/ready")
    def ready():
        return {"ready": True}

    # Резервируем базовый путь /api и монтируем роутер /v1
    api_router = APIRouter(prefix="/api")
    v1_router = APIRouter(prefix="/v1")

    @v1_router.get("/")
    def v1_root():
        return {"service": "coffee-backend", "version": "v1"}

    api_router.include_router(v1_router)
    app.include_router(api_router)

    # Монтируем статический фронтенд по пути /ui
    frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
    if frontend_dir.exists():
        app.mount("/ui", StaticFiles(directory=str(frontend_dir), html=True), name="ui")

        @app.get("/")
        def root_redirect():
            # Редиректим корневой URL на UI
            return RedirectResponse(url="/ui/")

    return app


# --- Управление меню (in-memory) ---

class MenuItemIn(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(default="")
    category: str = Field(default="coffee")
    ingredients: List[str] = Field(default_factory=list)
    sizes: List[str] = Field(default_factory=list)
    priceCoffeeCoin: float = Field(gt=0)
    prices: Optional[Dict[str, float]] = None  # по размерам, если задано
    calories: float = Field(default=0, ge=0)
    popularity: int = Field(default=0, ge=0)


class MenuItem(MenuItemIn):
    id: int


class MenuRepo:
    def __init__(self) -> None:
        self._items: dict[int, MenuItem] = {}
        self._next_id: int = 1

    def list(self) -> List[MenuItem]:
        return list(self._items.values())

    def create(self, data: MenuItemIn) -> MenuItem:
        mid = self._next_id
        self._next_id += 1
        item = MenuItem(id=mid, **data.model_dump())
        self._items[mid] = item
        return item

    def get(self, mid: int) -> Optional[MenuItem]:
        return self._items.get(mid)

    def update(self, mid: int, data: MenuItemIn) -> MenuItem:
        if mid not in self._items:
            raise KeyError
        item = MenuItem(id=mid, **data.model_dump())
        self._items[mid] = item
        return item

    def delete(self, mid: int) -> None:
        if mid not in self._items:
            raise KeyError
        del self._items[mid]


repo = MenuRepo()


def mount_menu_api(app: FastAPI) -> None:
    menu = APIRouter(prefix="/api/v1/menu", tags=["menu"])

    @menu.get("/", response_model=List[MenuItem])
    def list_menu():
        return repo.list()

    @menu.post("/", status_code=status.HTTP_201_CREATED, response_model=MenuItem)
    def create_menu(item: MenuItemIn):
        return repo.create(item)

    @menu.get("/{mid}", response_model=MenuItem)
    def get_menu(mid: int):
        found = repo.get(mid)
        if not found:
            raise HTTPException(status_code=404, detail="Позиция меню не найдена")
        return found

    @menu.put("/{mid}", response_model=MenuItem)
    def update_menu(mid: int, item: MenuItemIn):
        try:
            return repo.update(mid, item)
        except KeyError:
            raise HTTPException(status_code=404, detail="Позиция меню не найдена")

    @menu.delete("/{mid}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_menu(mid: int):
        try:
            repo.delete(mid)
        except KeyError:
            raise HTTPException(status_code=404, detail="Позиция меню не найдена")

    @menu.get("/{mid}/details")
    def menu_details(mid: int):
        # Возвращаем состав/стоимость, включая калории
        found = repo.get(mid)
        if not found:
            raise HTTPException(status_code=404, detail="Позиция меню не найдена")
        return {
            "id": found.id,
            "name": found.name,
            "description": found.description,
            "category": found.category,
            "ingredients": found.ingredients,
            "calories": found.calories,
            "priceCoffeeCoin": found.priceCoffeeCoin,
            "prices": found.prices,
        }

    app.include_router(menu)


# --- Новости (in-memory) ---

class NewsItemIn(BaseModel):
    title: str = Field(min_length=1)
    body: str = Field(default="")


class NewsItem(NewsItemIn):
    id: int
    createdAt: datetime


class NewsRepo:
    def __init__(self) -> None:
        self._items: Dict[int, NewsItem] = {}
        self._next_id: int = 1

    def list(self) -> List[NewsItem]:
        return sorted(self._items.values(), key=lambda n: n.createdAt, reverse=True)

    def create(self, data: NewsItemIn) -> NewsItem:
        nid = self._next_id
        self._next_id += 1
        item = NewsItem(id=nid, createdAt=datetime.now(timezone.utc), **data.model_dump())
        self._items[nid] = item
        return item


news_repo = NewsRepo()


def mount_news_api(app: FastAPI) -> None:
    news = APIRouter(prefix="/api/v1/news", tags=["news"])

    @news.get("/", response_model=List[NewsItem])
    def list_news():
        return news_repo.list()

    @news.post("/", status_code=201, response_model=NewsItem)
    def create_news(item: NewsItemIn):
        return news_repo.create(item)

    app.include_router(news)

    # Публичные алиасы
    pub = APIRouter(prefix="/api/news", tags=["news"])

    @pub.get("/", response_model=List[NewsItem])
    def list_news_pub():
        return news_repo.list()

    @pub.get("/{nid}", response_model=NewsItem)
    def get_news_pub(nid: int):
        n = news_repo._items.get(nid)
        if not n:
            raise HTTPException(status_code=404, detail="Новость не найдена")
        return n

    app.include_router(pub)


# --- Часы работы и статус ---

class StoreHours(BaseModel):
    """График работы: одинаковое время открытия/закрытия для всех дней."""
    open: time
    close: time


DEFAULT_HOURS = StoreHours(open=time(hour=8, minute=0), close=time(hour=20, minute=0))


def is_open(now: Optional[datetime] = None, hours: StoreHours = DEFAULT_HOURS) -> bool:
    now = now or datetime.now()
    return hours.open <= now.time() <= hours.close


def parse_time_param(t: Optional[str]) -> Optional[time]:
    if not t:
        return None
    try:
        hh, mm = t.split(":", 1)
        return time(hour=int(hh), minute=int(mm))
    except Exception:
        return None


def mount_status_api(app: FastAPI) -> None:
    status_r = APIRouter(prefix="/api/v1/status", tags=["status"])

    @status_r.get("/open")
    def store_open(now: Optional[str] = Query(default=None, description="HH:MM override for tests")):
        t = parse_time_param(now)
        dt = datetime.combine(date.today(), t) if t else None
        return {"open": is_open(dt)}

    @status_r.get("/hours", response_model=StoreHours)
    def hours():
        return DEFAULT_HOURS

    app.include_router(status_r)

    # Публичный статус
    store = APIRouter(prefix="/api/store", tags=["status"])

    @store.get("/status")
    def store_status():
        now = datetime.now()
        opened = is_open(now)
        # Вычислим ближайшее изменение статуса
        today_open = datetime.combine(date.today(), DEFAULT_HOURS.open)
        today_close = datetime.combine(date.today(), DEFAULT_HOURS.close)
        if opened:
            nxt = today_close if now <= today_close else today_open.replace(day=now.day + 1)
        else:
            nxt = today_open if now <= today_open else today_close
        return {"open": opened, "next_change": nxt.isoformat()}

    app.include_router(store)


# --- Скидки ---

def discount_of_day(today: Optional[date] = None) -> Dict[str, Any]:
    d = today or date.today()
    rng = random.Random(d.toordinal())
    pct = rng.choice([0, 5, 10])
    return {"type": "daily", "percent": pct}


def mount_discounts_api(app: FastAPI) -> None:
    disc = APIRouter(prefix="/api/v1/discounts", tags=["discounts"])

    @disc.get("/current")
    def current_discount():
        return discount_of_day()

    app.include_router(disc)

    # Публичный список скидок (расширенный список для витрины)
    pubd = APIRouter(prefix="/api/discounts", tags=["discounts"])

    @pubd.get("/")
    def list_discounts():
        dd = discount_of_day()
        loyalty = {"type": "loyalty_after_3", "percent": 10, "rule": "после 3 заказов"}
        return [dd, {"type": "happy_hour", "percent": 10, "window": "14:00-16:00"}, loyalty]

    app.include_router(pubd)


# --- Заказы и оплата (mock) ---

class OrderItem(BaseModel):
    menuId: int
    quantity: int = Field(default=1, ge=1)


class OrderIn(BaseModel):
    items: List[OrderItem]
    customerId: Optional[str] = None
    now: Optional[str] = Field(default=None, description="HH:MM override for tests/discounts")


class Order(BaseModel):
    id: int
    items: List[OrderItem]
    totalCoffeeCoin: float
    discountPercent: int
    status: str  # создан, оплачен
    customerId: Optional[str] = None


class OrderRepo:
    def __init__(self) -> None:
        self._orders: Dict[int, Order] = {}
        self._next_id: int = 1

    def create(self, order: Order) -> Order:
        oid = self._next_id
        self._next_id += 1
        order.id = oid
        self._orders[oid] = order
        return order

    def get(self, oid: int) -> Optional[Order]:
        return self._orders.get(oid)

    def update(self, oid: int, order: Order) -> None:
        self._orders[oid] = order


orders_repo = OrderRepo()


def calc_order_total(items: List[OrderItem]) -> float:
    total = 0.0
    for it in items:
        mi = repo.get(it.menuId)
        if not mi:
            raise HTTPException(status_code=400, detail="Недопустимый menuId")
        total += mi.priceCoffeeCoin * it.quantity
    return round(total, 2)


def happy_hour_discount(now_time: time) -> int:
    # 14:00-16:00 -> 10%
    return 10 if time(14, 0) <= now_time <= time(16, 0) else 0


# Простейшее хранилище лояльности (баллы клиента)
class LoyaltyRepo:
    def __init__(self) -> None:
        self._points: Dict[str, int] = {}

    def add_points(self, cid: str, points: int) -> None:
        self._points[cid] = self._points.get(cid, 0) + points

    def get_points(self, cid: str) -> int:
        return self._points.get(cid, 0)


loyalty_repo = LoyaltyRepo()


def mount_orders_api(app: FastAPI) -> None:
    orders = APIRouter(prefix="/api/v1/orders", tags=["orders"])

    @orders.post("/", status_code=201, response_model=Order)
    def create_order(payload: OrderIn):
        # Считаем базовую сумму заказа
        total = calc_order_total(payload.items)
        # Определяем скидки
        now_param = parse_time_param(payload.now) if payload.now else None
        now_t = now_param or datetime.now().time()
        dd = discount_of_day()["percent"]
        hh = happy_hour_discount(now_t)
        # Берём максимум из скидок
        discount_pct = max(dd, hh)
        discounted_total = round(total * (1 - discount_pct / 100.0), 2)
        order = Order(
            id=0,
            items=payload.items,
            totalCoffeeCoin=discounted_total,
            discountPercent=discount_pct,
            status="created",
            customerId=payload.customerId,
        )
        created = orders_repo.create(order)
        # Лояльность: 1 балл за каждый целый CoffeeCoin
        if payload.customerId:
            loyalty_repo.add_points(payload.customerId, int(discounted_total))
        return created

    @orders.get("/{oid}", response_model=Order)
    def get_order(oid: int):
        o = orders_repo.get(oid)
        if not o:
            raise HTTPException(status_code=404, detail="Заказ не найден")
        return o

    @orders.post("/{oid}/pay", response_model=Order)
    def pay_order(oid: int):
        o = orders_repo.get(oid)
        if not o:
            raise HTTPException(status_code=404, detail="Заказ не найден")
        if o.status == "paid":
            return o
        o.status = "paid"
        orders_repo.update(oid, o)
        return o

    app.include_router(orders)

    # Публичные алиасы для совместимости со спецификацией раздела 4
    pub_orders = APIRouter(prefix="/api/orders", tags=["orders"])

    @pub_orders.post("/", status_code=201, response_model=Order)
    def pub_create_order(payload: OrderIn):
        # Переиспользуем ту же логику
        return create_order(payload)  # type: ignore[name-defined]

    @pub_orders.get("/{oid}", response_model=Order)
    def pub_get_order(oid: int):
        return get_order(oid)  # type: ignore[name-defined]

    @pub_orders.post("/{oid}/pay", response_model=Order)
    def pub_pay_order(oid: int):
        return pay_order(oid)  # type: ignore[name-defined]

    app.include_router(pub_orders)


# --- Лояльность API ---

def mount_loyalty_api(app: FastAPI) -> None:
    loy = APIRouter(prefix="/api/v1/loyalty", tags=["loyalty"])

    @loy.get("/{customerId}")
    def get_points(customerId: str):
        return {"customerId": customerId, "points": loyalty_repo.get_points(customerId)}

    app.include_router(loy)

    # Алиас
    pub = APIRouter(prefix="/api/loyalty", tags=["loyalty"])

    @pub.get("/{user_id}")
    def get_points_pub(user_id: str):
        return {"customerId": user_id, "points": loyalty_repo.get_points(user_id)}

    app.include_router(pub)


# --- Отзывы ---

class ReviewIn(BaseModel):
    menuId: int
    rating: int = Field(ge=1, le=5)
    comment: str = Field(default="")


class Review(ReviewIn):
    id: int
    createdAt: datetime


class ReviewRepo:
    def __init__(self) -> None:
        self._items: Dict[int, Review] = {}
        self._next: int = 1

    def add(self, r: Review) -> Review:
        rid = self._next
        self._next += 1
        r.id = rid
        self._items[rid] = r
        return r

    def list_for_menu(self, mid: Optional[int] = None) -> List[Review]:
        vals = list(self._items.values())
        return [r for r in vals if mid is None or r.menuId == mid]


reviews_repo = ReviewRepo()


def mount_reviews_api(app: FastAPI) -> None:
    rev = APIRouter(prefix="/api/v1/reviews", tags=["reviews"])

    @rev.get("/")
    def list_reviews(menuId: Optional[int] = None):
        return reviews_repo.list_for_menu(menuId)

    @rev.post("/", status_code=201)
    def create_review(payload: ReviewIn):
        if not repo.get(payload.menuId):
            raise HTTPException(status_code=400, detail="Недопустимый menuId")
        r = Review(createdAt=datetime.now(timezone.utc), **payload.model_dump(), id=0)
        return reviews_repo.add(r)

    app.include_router(rev)

    # Алиас
    pub = APIRouter(prefix="/api/reviews", tags=["reviews"])

    @pub.get("/")
    def list_reviews_pub(menuId: Optional[int] = None):
        return reviews_repo.list_for_menu(menuId)

    @pub.post("/", status_code=201)
    def create_review_pub(payload: ReviewIn):
        if not repo.get(payload.menuId):
            raise HTTPException(status_code=400, detail="Недопустимый menuId")
        r = Review(createdAt=datetime.now(timezone.utc), **payload.model_dump(), id=0)
        return reviews_repo.add(r)

    app.include_router(pub)


# --- Публичное меню с фильтрами ---

def price_for_sort(mi: MenuItem) -> float:
    if mi.prices:
        try:
            return min(mi.prices.values())
        except Exception:
            return mi.priceCoffeeCoin
    return mi.priceCoffeeCoin


def mount_public_menu_api(app: FastAPI) -> None:
    pm = APIRouter(prefix="/api/menu", tags=["menu"])

    @pm.get("/")
    def list_menu_public(category: Optional[str] = None, sort: Optional[str] = None, q: Optional[str] = None):
        items = repo.list()
        if category:
            items = [i for i in items if i.category == category]
        if q:
            ql = q.lower()
            items = [i for i in items if ql in i.name.lower() or ql in (i.description or "").lower()]
        if sort == "price":
            items = sorted(items, key=price_for_sort)
        elif sort == "popularity":
            items = sorted(items, key=lambda i: i.popularity, reverse=True)
        return items

    @pm.get("/{mid}")
    def get_menu_public(mid: int):
        found = repo.get(mid)
        if not found:
            raise HTTPException(status_code=404, detail="Позиция меню не найдена")
        return found

    # Админский алиас для добавления (POST /api/menu)
    @pm.post("/", status_code=status.HTTP_201_CREATED, response_model=MenuItem)
    def create_menu_public(item: MenuItemIn):
        # Зеркалим админский роут /api/v1
        return repo.create(item)

    app.include_router(pm)


# Создаём приложение и монтируем роутеры в правильном порядке
app = create_app()
mount_menu_api(app)
mount_public_menu_api(app)
mount_news_api(app)
mount_status_api(app)
mount_discounts_api(app)
mount_orders_api(app)
mount_loyalty_api(app)
mount_reviews_api(app)


# Пытаемся загрузить сид-данные из data/seed.json при старте (для демо)
@app.on_event("startup")
def _load_seed_on_startup() -> None:
    try:
        seed_path = Path(__file__).resolve().parent.parent / "data" / "seed.json"
        if not seed_path.exists():
            return
        # Если уже есть данные — пропускаем
        if repo.list():
            return
        data = json.loads(seed_path.read_text(encoding="utf-8"))
        # Заполняем меню
        for it in data.get("menu", []):
            try:
                repo.create(MenuItemIn(**it))
            except Exception:
                continue
        # Заполняем новости
        for n in data.get("news", []):
            try:
                news_repo.create(NewsItemIn(**{"title": n.get("title",""), "body": n.get("body","")}))
            except Exception:
                continue
        # Заполняем отзывы (опционально, по menuId)
        for r in data.get("reviews", []):
            try:
                payload = ReviewIn(**r)
                rev = Review(createdAt=datetime.now(timezone.utc), **payload.model_dump(), id=0)
                reviews_repo.add(rev)
            except Exception:
                continue
    except Exception:
        # Проглатываем ошибки, чтобы не блокировать запуск
        pass


# Хелпер для тестов: сброс in-memory состояния (чтобы тесты не мешали друг другу)
def _reset_state() -> None:
    global repo, news_repo, orders_repo, loyalty_repo, reviews_repo
    repo = MenuRepo()
    news_repo = NewsRepo()
    orders_repo = OrderRepo()
    loyalty_repo = LoyaltyRepo()
    reviews_repo = ReviewRepo()


# --- Dev seed endpoint (для наполнения демо-данными) ---
def _seed_demo():
    items = [
        {"name": "Латте", "description": "Мягкий молочный кофе", "category": "coffee", "ingredients": ["кофе","молоко"], "sizes": ["S","M","L"], "priceCoffeeCoin": 4.8, "prices": {"S":4.2, "M":4.8, "L":5.4}, "calories": 150, "popularity": 9},
        {"name": "Капучино", "description": "Классика", "category": "coffee", "ingredients": ["кофе","молоко"], "sizes": ["S","M","L"], "priceCoffeeCoin": 4.5, "prices": {"S":4.0, "M":4.5, "L":5.0}, "calories": 120, "popularity": 8},
        {"name": "Эспрессо", "description": "Крепкий шот", "category": "coffee", "ingredients": ["кофе"], "sizes": ["single"], "priceCoffeeCoin": 3.0, "calories": 5, "popularity": 7},
        {"name": "Флэт уайт", "description": "Микропена", "category": "coffee", "ingredients": ["кофе","молоко"], "sizes": ["S","M"], "priceCoffeeCoin": 4.9, "calories": 130, "popularity": 6},
        {"name": "Колд Брю", "description": "Холодное заваривание", "category": "coffee", "ingredients": ["кофе","вода"], "sizes": ["M"], "priceCoffeeCoin": 4.6, "calories": 10, "popularity": 5},
        {"name": "Матча Латте", "description": "Зелёный чай матча", "category": "tea", "ingredients": ["матча","молоко"], "sizes": ["M"], "priceCoffeeCoin": 5.0, "calories": 160, "popularity": 6},
        {"name": "Чай Масала", "description": "Пряный чай", "category": "tea", "ingredients": ["чай","специи","молоко"], "sizes": ["M"], "priceCoffeeCoin": 4.2, "calories": 110, "popularity": 5},
        {"name": "Круассан", "description": "Слоёное тесто", "category": "dessert", "ingredients": ["мука","масло"], "sizes": ["std"], "priceCoffeeCoin": 2.5, "calories": 250, "popularity": 7},
        {"name": "Маффин", "description": "Шоколадный", "category": "dessert", "ingredients": ["мука","шоколад"], "sizes": ["std"], "priceCoffeeCoin": 2.8, "calories": 300, "popularity": 6},
        {"name": "Чизкейк", "description": "Нью-Йорк", "category": "dessert", "ingredients": ["сыр","печенье"], "sizes": ["std"], "priceCoffeeCoin": 3.5, "calories": 320, "popularity": 8},
    ]
    for it in items:
        repo.create(MenuItemIn(**it))
    # новости
    titles = ["Новая смесь недели", "-20% в happy hour", "Осеннее меню"]
    bodies = ["Попробуйте свежую обжарку", "С 15 до 17 скидка", "Тыквенный латте вернулся"]
    for t, b in zip(titles, bodies):
        news_repo.create(NewsItemIn(title=t, body=b))


def mount_dev_seed(app: FastAPI) -> None:
    dev = APIRouter(prefix="/api/v1/dev", tags=["dev"])

    @dev.post("/seed")
    def seed():
        _reset_state()
        _seed_demo()
        return {"seeded": True}

    app.include_router(dev)

# Подключаем dev seed роутер после его определения
mount_dev_seed(app)
