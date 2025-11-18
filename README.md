# E-Commerce Scraping API

A FastAPI-based web scraping service for extracting product data from major Indonesian e-commerce platforms including Shopee, Tokopedia, and Blibli.

## Features

- **Multi-platform Support**: Scrape data from Shopee, Tokopedia, and Blibli
- **Caching**: Redis-based caching system for improved performance
- **Docker Support**: Containerized deployment with Docker Compose
- **RESTful API**: Clean and well-documented REST endpoints
- **Product Details**: Extract comprehensive product information
- **Shop Information**: Get seller and shop details
- **Category Browsing**: Browse products by categories
- **Search Functionality**: Search products by keywords

## Supported Platforms

### Shopee
- Product details extraction
- Product search by keyword
- Product listing by shop
- Shop details
- Category browsing (multi-level)
- Cookie management for enhanced scraping

### Tokopedia
- Product details extraction
- Product search by keyword
- Product listing by category
- Seller information
- Shop details
- Product listing by shop

### Blibli
- Product details extraction
- Product search by keyword
- Product listing by category
- Seller search
- Shop information
- Product listing by shop

## Installation

### Prerequisites
- Docker and Docker Compose
- Python 3.8+ (if running locally)

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/yourusername/e-commerce-scraping-api.git
cd e-commerce-scraping-api
```

2. Create a `.env` file in the root directory (if needed):
```
# Add any environment variables here
```

3. Run with Docker Compose:
```bash
docker-compose up -d
```

The API will be available at `http://localhost:8000`

### Local Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start Redis (required for caching):
```bash
redis-server
```

3. Run the application:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### Shopee Endpoints

#### Product Information
- `POST /shopee/detailProduct` - Get product details
- `POST /shopee/scrapByKeyword` - Search products by keyword
- `POST /shopee/scrapByCategory` - Get products by category
- `POST /shopee/scrapByShop` - Get products from specific shop

#### Shop Information
- `POST /shopee/shopDetailShop` - Get shop details
- `POST /shopee/addCookies` - Add cookies for enhanced scraping

#### Categories
- `GET /shopee/allCategory` - Get all categories
- `POST /shopee/allCategoryLevel3` - Get level 3 categories by level 2 ID

### Tokopedia Endpoints

#### Product Information
- `POST /tokopedia/getProductInfo` - Get product details
- `POST /tokopedia/getProductByKeyword` - Search products by keyword
- `POST /tokopedia/getProductByCat` - Get products by category
- `POST /tokopedia/getProductByShop` - Get products from specific shop

#### Shop Information
- `POST /tokopedia/getShopInfo` - Get shop details
- `POST /tokopedia/getSeller` - Get seller information

#### Categories
- `GET /tokopedia/getAllCategory` - Get all categories

### Blibli Endpoints

#### Product Information
- `POST /blibli/getDetailProduct` - Get product details
- `POST /blibli/getListProductByKeyword` - Search products by keyword
- `POST /blibli/getListProductByCat` - Get products by category
- `POST /blibli/getListProductByShop` - Get products from specific shop

#### Shop Information
- `POST /blibli/getInfoShop` - Get shop details
- `POST /blibli/getListSeller` - Get seller list

#### Categories
- `GET /blibli/getLevel1` - Get level 1 categories
- `POST /blibli/getLevel2` - Get level 2 categories by level 1 ID

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Example Usage

### Shopee - Get Product Details
```bash
curl -X POST "http://localhost:8000/shopee/detailProduct" \
     -H "Content-Type: application/json" \
     -d '{"URL": "https://shopee.co.id/product-url"}'
```

### Shopee - Search by Keyword
```bash
curl -X POST "http://localhost:8000/shopee/scrapByKeyword" \
     -H "Content-Type: application/json" \
     -d '{"keyword": "baju couple", "page": 1}'
```

### Tokopedia - Get Shop Info
```bash
curl -X POST "http://localhost:8000/tokopedia/getShopInfo" \
     -H "Content-Type: application/json" \
     -d '{"shop_domain": "shop-name"}'
```

### Blibli - Get Categories
```bash
curl -X GET "http://localhost:8000/blibli/getLevel1"
```

## Caching

The API uses Redis for caching responses to improve performance and reduce the load on target websites. Cached responses are automatically served for identical requests.

## Configuration

The application can be configured through:
- Environment variables (for Docker deployment)
- `.env` file in the root directory
- Code configuration in `app/core/config.py`

## Docker Services

The `docker-compose.yaml` file defines two services:
1. **app**: The FastAPI application
2. **redis**: Redis database for caching

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for educational and research purposes only. Users are responsible for ensuring compliance with the terms of service of the respective e-commerce platforms. Please respect robots.txt files and rate limits when using this API.