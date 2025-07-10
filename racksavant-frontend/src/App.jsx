import React, { useRef, useState } from "react";
import "./index.css";

const eraList = [
  "1940s",
  "1950s",
  "1960s",
  "1970s",
  "1980s",
  "1990s",
];

const hollywoodStyles = {
  '1940s': {
    name: 'Film Noir Femme Fatale',
    description: 'Channel the mysterious allure of 1940s cinema with structured silhouettes, dramatic shoulders, and luxurious fabrics.',
    items: [
      { name: 'Silk Blouse', price: 89, type: 'user', icon: '👚' },
      { name: 'Wool Trench', price: 159, type: 'racksavant', icon: '🧥' },
      { name: 'Pearl Necklace', price: 79, type: 'racksavant', icon: '📿' },
      { name: 'Black Heels', price: 129, type: 'user', icon: '👠' }
    ]
  },
  '1950s': {
    name: 'Grace Kelly Elegance',
    description: 'Embody timeless sophistication with full skirts, cinched waists, and refined accessories.',
    items: [
      { name: 'Circle Skirt', price: 95, type: 'user', icon: '👗' },
      { name: 'Cashmere Cardigan', price: 145, type: 'racksavant', icon: '🧶' },
      { name: 'Silk Scarf', price: 65, type: 'racksavant', icon: '🧣' },
      { name: 'Pumps', price: 110, type: 'user', icon: '👠' }
    ]
  },
  '1960s': {
    name: 'Mod Revolution',
    description: 'Embrace the bold, geometric patterns and mini silhouettes that defined the swinging sixties.',
    items: [
      { name: 'Shift Dress', price: 75, type: 'user', icon: '👗' },
      { name: 'Go-Go Boots', price: 135, type: 'racksavant', icon: '👢' },
      { name: 'Oversized Sunglasses', price: 85, type: 'racksavant', icon: '🕶️' },
      { name: 'Mod Jacket', price: 125, type: 'user', icon: '🧥' }
    ]
  },
  '1970s': {
    name: 'Studio 54 Glamour',
    description: 'Capture the disco era with flowing fabrics, metallic accents, and bold statement pieces.',
    items: [
      { name: 'Wrap Dress', price: 105, type: 'user', icon: '👗' },
      { name: 'Platform Shoes', price: 149, type: 'racksavant', icon: '👠' },
      { name: 'Statement Necklace', price: 95, type: 'racksavant', icon: '💎' },
      { name: 'Flared Jeans', price: 89, type: 'user', icon: '👖' }
    ]
  },
  '1980s': {
    name: 'Power Dressing',
    description: 'Command attention with bold shoulders, structured blazers, and confident silhouettes.',
    items: [
      { name: 'Power Blazer', price: 165, type: 'racksavant', icon: '🏢' },
      { name: 'Pencil Skirt', price: 85, type: 'user', icon: '📐' },
      { name: 'Statement Earrings', price: 75, type: 'racksavant', icon: '💫' },
      { name: 'Leather Bag', price: 199, type: 'user', icon: '👜' }
    ]
  },
  '1990s': {
    name: 'Minimalist Chic',
    description: 'Embrace clean lines, neutral tones, and effortless sophistication.',
    items: [
      { name: 'Slip Dress', price: 95, type: 'user', icon: '👗' },
      { name: 'Minimal Blazer', price: 139, type: 'racksavant', icon: '🏷️' },
      { name: 'Strappy Sandals', price: 115, type: 'racksavant', icon: '👡' },
      { name: 'Denim Jacket', price: 79, type: 'user', icon: '🧥' }
    ]
  }
};

const BACKEND_URL = "http://localhost:8000";

function App() {
  const [currentEra, setCurrentEra] = useState("1940s");
  const [userWardrobe, setUserWardrobe] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const fileInputRef = useRef();

  // Handle era filter
  const filterEra = (era) => {
    setCurrentEra(era);
  };

  // Handle image upload
  const uploadWardrobe = async (e) => {
    if (e) e.preventDefault();
    fileInputRef.current.click();
  };

  // On file selected
  const onFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setIsLoading(true);
    // Upload to backend
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await fetch(`${BACKEND_URL}/upload`, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      // Add to wardrobe
      setUserWardrobe((prev) => [
        {
          ...data,
          imageUrl: `${BACKEND_URL}${data.image_url}`,
        },
        ...prev,
      ]);
      // Show era detection card
      setSuggestions((prev) => [
        {
          ...data,
          imageUrl: `${BACKEND_URL}${data.image_url}`,
        },
        ...prev,
      ]);
      setCurrentEra(data.era);
    } catch (err) {
      alert("Upload failed");
    }
    setIsLoading(false);
  };

  // Generate suggestions for current era
  const generateSuggestions = () => {
    setIsLoading(true);
    setTimeout(() => {
      setSuggestions([
        {
          type: "style",
          era: currentEra,
          ...hollywoodStyles[currentEra],
        },
      ]);
      setIsLoading(false);
    }, 1200);
  };

  // Purchase handler
  const purchaseItem = (name, price) => {
    alert(`Purchasing ${name} for $${price}!\n\nRedirecting to checkout...`);
  };

  // On mount, show example detection
  React.useEffect(() => {
    setTimeout(() => {
      const exampleItem = {
        name: "Vintage Silk Blouse",
        era: "1940s",
        confidence: 94,
        icon: "👚",
        description: "Classic button-down with structured shoulders and flowing silhouette",
        historicalContext: "Reminiscent of Lauren Bacall's sophisticated style in film noir classics",
        imageUrl: null,
      };
      setUserWardrobe([exampleItem]);
      setSuggestions([exampleItem]);
    }, 1000);
  }, []);

  return (
    <div className="container">
      <div className="header">
        <div className="logo">RackSavant</div>
        <div className="tagline">Hollywood Fashion, Your Closet</div>
      </div>

      <div className="upload-section">
        <button className="upload-btn" onClick={uploadWardrobe} disabled={isLoading}>
          {isLoading ? "🔍 Analyzing your piece..." : "📸 Upload Your Wardrobe"}
        </button>
        <input
          type="file"
          accept="image/*"
          style={{ display: "none" }}
          ref={fileInputRef}
          onChange={onFileChange}
        />
        <div className="wardrobe-count" id="wardrobeCount">
          {userWardrobe.length} items in your digital closet
        </div>
      </div>

      <div className="era-timeline">
        {eraList.map((era) => (
          <div
            key={era}
            className={`era-chip${currentEra === era ? " active" : ""}`}
            onClick={() => filterEra(era)}
          >
            {era}
          </div>
        ))}
      </div>

      <button className="style-button" onClick={generateSuggestions} disabled={isLoading}>
        ✨ Get Hollywood Styling
      </button>

      <div id="suggestions">
        {isLoading && (
          <div className="loading">
            <div>Creating your Hollywood look...</div>
          </div>
        )}
        {!isLoading && suggestions.map((item, idx) => (
          <div className="suggestion-card" key={idx}>
            {item.imageUrl && (
              <div style={{ textAlign: "center", marginBottom: 20 }}>
                <img
                  src={item.imageUrl}
                  alt={item.predicted_class || item.name}
                  style={{ maxWidth: 120, maxHeight: 120, borderRadius: 10, marginBottom: 10 }}
                />
              </div>
            )}
            {item.era && (
              <div className="era-badge">{item.era} Era Detected</div>
            )}
            {item.confidence && (
              <div style={{ color: "#90EE90", fontSize: "0.9em", marginTop: 5 }}>
                {item.confidence}% confidence match
              </div>
            )}
            <div className="style-title">{item.name || item.predicted_class}</div>
            {item.description && (
              <div className="style-description">{item.description}</div>
            )}
            {item.historicalContext && (
              <div style={{ background: "rgba(212, 175, 55, 0.1)", padding: 15, borderRadius: 10, margin: "15px 0", borderLeft: "3px solid #d4af37" }}>
                <div style={{ color: "#d4af37", fontWeight: "bold", marginBottom: 5 }}>✨ Hollywood Heritage</div>
                <div style={{ fontSize: "0.9em", color: "#ccc", fontStyle: "italic" }}>{item.historicalContext}</div>
              </div>
            )}
            {item.type === "style" && (
              <>
                <div className="inspiration-text">
                  "Fashion is architecture: it is a matter of proportions." - Coco Chanel
                </div>
                <div className="section-title">Your Complete Look</div>
                <div className="user-items">✓ Using {item.items.filter(i => i.type === 'user').length} items from your wardrobe</div>
                <div className="suggested-items">+ {item.items.filter(i => i.type === 'racksavant').length} RackSavant pieces to complete the look</div>
                <div className="items-grid">
                  {item.items.map((itm, i) => (
                    <div className={`item-card ${itm.type === 'racksavant' ? 'racksavant-item' : ''}`} key={i}>
                      <div className="item-image">{itm.icon}</div>
                      <div className="item-name">{itm.name}</div>
                      <div className="item-price">${itm.price}</div>
                      {itm.type === 'racksavant' ? (
                        <button className="buy-button" onClick={() => purchaseItem(itm.name, itm.price)}>
                          Add to Look
                        </button>
                      ) : (
                        <div style={{ color: '#90EE90', fontSize: '0.7em', marginTop: 5 }}>From Your Closet</div>
                      )}
                    </div>
                  ))}
                </div>
              </>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
