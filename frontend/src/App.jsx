import { useEffect, useState } from "react";
import "./App.css";

const restaurantImages = {
  "Pizza Palace":
    "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=800&q=80",
  "Burger House":
    "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=800&q=80",
};

function App() {
  const [restaurants, setRestaurants] = useState([]);
  const [selectedRestaurant, setSelectedRestaurant] = useState(null);
  const [menuItems, setMenuItems] = useState([]);
  const [quantities, setQuantities] = useState({});
  const [cart, setCart] = useState([]);
  const [message, setMessage] = useState("");

  const [paymentData, setPaymentData] = useState({
    fullName: "",
    cardNumber: "",
    address: "",
    phone: "",
  });

  useEffect(() => {
    fetch("http://127.0.0.1:8000/restaurants")
      .then((res) => res.json())
      .then((data) => setRestaurants(data))
      .catch((err) => console.error("Restaurant fetch error:", err));
  }, []);

  const handleSelectRestaurant = (restaurant) => {
    setSelectedRestaurant(restaurant);
    setMessage("");

    fetch(`http://127.0.0.1:8000/restaurants/${restaurant.id}/menu`)
      .then((res) => res.json())
      .then((data) => setMenuItems(data))
      .catch((err) => console.error("Menu fetch error:", err));
  };

  const handleQuantityChange = (itemId, value) => {
    setQuantities((prev) => ({
      ...prev,
      [itemId]: Number(value),
    }));
  };

  const handleAddToCart = (item) => {
    const quantity = quantities[item.id] || 0;

    if (quantity <= 0) {
      setMessage("Lütfen önce adet seç.");
      return;
    }

    const restaurantName = selectedRestaurant ? selectedRestaurant.name : "";

    setCart((prevCart) => {
      const existingItem = prevCart.find(
        (cartItem) => cartItem.id === item.id
      );

      if (existingItem) {
        return prevCart.map((cartItem) =>
          cartItem.id === item.id
            ? {
                ...cartItem,
                quantity: cartItem.quantity + quantity,
              }
            : cartItem
        );
      }

      return [
        ...prevCart,
        {
          id: item.id,
          name: item.name,
          price: item.price,
          quantity: quantity,
          restaurantName: restaurantName,
        },
      ];
    });

    setQuantities((prev) => ({
      ...prev,
      [item.id]: 0,
    }));

    setMessage(`${item.name} sepete eklendi.`);
  };

  const handleRemoveFromCart = (itemId) => {
    setCart((prevCart) => prevCart.filter((item) => item.id !== itemId));
  };

  const handleClearCart = () => {
    setCart([]);
    setMessage("Sepet temizlendi.");
  };

  const totalPrice = cart.reduce(
    (total, item) => total + item.price * item.quantity,
    0
  );

  const handlePaymentChange = (e) => {
    const { name, value } = e.target;
    setPaymentData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleCheckout = () => {
    if (cart.length === 0) {
      setMessage("Önce sepete ürün eklemelisin.");
      return;
    }

    if (
      !paymentData.fullName ||
      !paymentData.cardNumber ||
      !paymentData.address ||
      !paymentData.phone
    ) {
      setMessage("Lütfen ödeme alanlarını doldur.");
      return;
    }

    const orderPayload = {
      user_id: 1,
      items: cart.map((item) => ({
        menu_item_id: item.id,
        quantity: item.quantity,
      })),
    };

    fetch("http://127.0.0.1:8000/orders", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(orderPayload),
    })
      .then((res) => res.json())
      .then((data) => {
        setMessage(
          `Ödeme başarılı! Sipariş oluşturuldu. Sipariş ID: ${data.id}, Toplam: $${data.total_price}`
        );
        setCart([]);
        setPaymentData({
          fullName: "",
          cardNumber: "",
          address: "",
          phone: "",
        });
      })
      .catch((err) => {
        console.error("Checkout error:", err);
        setMessage("Sipariş sırasında hata oluştu.");
      });
  };

  return (
    <div className="container">
      <h1>🍔 Food Ordering System</h1>
      <p className="subtitle">Restaurants, Cart, and Payment Demo</p>

      <div className="section">
        <h2>Restaurants</h2>
        <div className="restaurant-list">
          {restaurants.map((restaurant) => (
            <div key={restaurant.id} className="card restaurant-card">
              <img
                src={
                  restaurantImages[restaurant.name] ||
                  "https://via.placeholder.com/400x220"
                }
                alt={restaurant.name}
                className="restaurant-image"
              />
              <h3>{restaurant.name}</h3>
              <p>Cuisine: {restaurant.cuisine}</p>
              <button onClick={() => handleSelectRestaurant(restaurant)}>
                View Menu
              </button>
            </div>
          ))}
        </div>
      </div>

      {selectedRestaurant && (
        <div className="section">
          <h2>{selectedRestaurant.name} Menu</h2>
          <div className="menu-list">
            {menuItems.map((item) => (
              <div key={item.id} className="card">
                <h3>{item.name}</h3>
                <p>Price: ${item.price}</p>
                <label>Quantity: </label>
                <input
                  type="number"
                  min="0"
                  value={quantities[item.id] || 0}
                  onChange={(e) =>
                    handleQuantityChange(item.id, e.target.value)
                  }
                />
                <button
                  className="add-btn"
                  onClick={() => handleAddToCart(item)}
                >
                  Add to Cart
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="section">
        <h2>Cart</h2>
        {cart.length === 0 ? (
          <p>Your cart is empty.</p>
        ) : (
          <div className="cart-box">
            {cart.map((item) => (
              <div key={item.id} className="cart-item">
                <div>
                  <strong>{item.name}</strong>
                  <p>Restaurant: {item.restaurantName}</p>
                  <p>
                    {item.quantity} x ${item.price} = $
                    {(item.quantity * item.price).toFixed(2)}
                  </p>
                </div>
                <button
                  className="remove-btn"
                  onClick={() => handleRemoveFromCart(item.id)}
                >
                  Remove
                </button>
              </div>
            ))}
            <h3>Total: ${totalPrice.toFixed(2)}</h3>
            <button className="clear-btn" onClick={handleClearCart}>
              Clear Cart
            </button>
          </div>
        )}
      </div>

      <div className="section">
        <h2>Payment Information</h2>
        <div className="payment-form">
          <input
            type="text"
            name="fullName"
            placeholder="Full Name"
            value={paymentData.fullName}
            onChange={handlePaymentChange}
          />
          <input
            type="text"
            name="cardNumber"
            placeholder="Card Number"
            value={paymentData.cardNumber}
            onChange={handlePaymentChange}
          />
          <input
            type="text"
            name="address"
            placeholder="Delivery Address"
            value={paymentData.address}
            onChange={handlePaymentChange}
          />
          <input
            type="text"
            name="phone"
            placeholder="Phone Number"
            value={paymentData.phone}
            onChange={handlePaymentChange}
          />

          <button className="checkout-btn" onClick={handleCheckout}>
            Proceed to Payment
          </button>
        </div>
      </div>

      {message && <div className="message">{message}</div>}
    </div>
  );
}

export default App;